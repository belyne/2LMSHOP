from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.http import Http404
from django.core.mail import send_mail
from django.core.files.storage import default_storage
from django.views.generic.edit import CreateView
from app.models import *
from django.conf import settings

from app.forms import ItemForm
from app.models import Items, Images


# Create your views here.
class ProductDetailView(APIView):
    def get(self, request, pk):
        try:
            item = get_object_or_404(Items, id=pk)
            print(item)
            item_images = Images.objects.filter(item=item)
            return Response({
                'name': item.name,
                'price': item.price,
                'category': item.category,
                'quantity_in_stock': item.quantity_in_stock,
                'image_urls': [default_storage.url(image.image) for image in item_images]
            })
        except Http404:
            return Response({'error': 'Product Not Found'})


class ProductListView(APIView):
    def get(self, request):
        products = Items.objects.all()
        list_of_products = dict()
        for item in products:
            item_images = Images.objects.filter(item=item)
            image_urls = [default_storage.url(image.image) for image in item_images]
            list_of_products[item.id] = {
                "name": item.name,
                "price": item.price,
                "rating": item.rating,
                "category": item.category,
                "image-urls": image_urls
            }
        return Response(list_of_products)

    # def post(self, request):
    #     name = request.data.get('name')
    #     price = request.data.get('price')
    #     category=  request.data.get('category')
    #     quantity_in_stock = request.data.get('quantity_in_stock')
    #     Items.objects.create(
    #         name=name,
    #         price=price,
    #         quantity_in_stock=quantity_in_stock
    #     )
    #     if Items.objects.get(name=name):
    #         return Response({'success': 'Product {} added w/o issue'.format(name)})
    #     return Response({'error': "Couldn't add Product {}".format(name)})

    def put(self, request):
        name = request.data.get('name')
        item = get_object_or_404(Items, name=name)
        price = request.data.get('price', item.price)
        quantity_in_stock = request.data.get('quantityInStock', item.quantity_in_stock)
        item.price = price
        item.quantity_in_stock = quantity_in_stock
        item.save()
        return Response({'success': "The price of product {} has been updated.".format(name)})

    def delete(self, request):
        name = request.data.get('name')
        price = request.data.get('price')
        item = get_object_or_404(Items, name=name)
        item.delete()
        return Response("Product {} has been deleted successfully".format(name))


class OrderView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(users=request.user)
        list_of_orders = dict()
        list_of_orders[0] = "Title: List Of Orders"
        i = 1
        for order in orders:
            list_of_orders[i] = {
                "items": [f"{OrderItem.objects.get(order=order, item=item).quantity} {item.name}" for item in
                          order.items.all()],
                "Date ordered": order.date_ordered,
                "Completed": order.ordered
            }
            i += 1
        return Response(list_of_orders)


class AddToCartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        item_id = request.data.get('item_id')
        quantity = int(request.data.get('quantity'))

        # Retrieve the product object from the database
        try:
            item = Items.objects.get(id=item_id)
        except Items.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Making sure there are enough in stock
        if quantity > item.quantity_in_stock or item.quantity_in_stock == 0:
            return Response({'Sorry': "There aren't enough of this product in stock."})

        order, created = Order.objects.get_or_create(users=request.user, ordered=False)
        OrderItem.objects.create(order=order, item=item, quantity=quantity)
        return Response({'Success': 'Product {} was added to cart.'.format(item.name), 'statusCode': status.HTTP_200_OK})


class CartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        order = Order.objects.get(users=request.user, ordered=False)
        item_id = request.data.get('item_id')
        order_item = get_object_or_404(OrderItem, order=order, item__id=item_id)
        quantity = request.data.get('quantity', order_item.quantity)
        # data = json.loads(request.body)
        # quantity = data.get('quantity', order_item.quantity)
        if quantity < 0:
            return Response({'error': 'Quantity cannot be negative.'}, status=status.HTTP_400_BAD_REQUEST)
        order_item.quantity = quantity
        order_item.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

    def delete(self, request):
        order = Order.objects.get(users=request.user, ordered=False)
        item_id = request.data.get('item_id')
        order_item = get_object_or_404(OrderItem, order=order, item__id=item_id)
        order_item.delete()


class CheckoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            order = Order.objects.get(users=request.user, ordered=False)
        except Order.DoesNotExist:
            return Response({'message': 'No order found for the current user.'}, status=status.HTTP_404_NOT_FOUND)

        # Updating the quantities of the items in Stock.
        for item in order.items.all():
            i = OrderItem.objects.get(order=order, item=item)
            item.quantityInStock -= i.quantity
            item.save()
        totalPrice = sum([order_item.getTotalPrice() for order_item in OrderItem.objects.filter(order=order)])
        # Charging the user for the order
        # (The payment processing code)
        if totalPrice > 0:
            order.ordered = True
            order.save()
            # Payment successful

            # Sending an email with the purchase information
            message = f"Thank you for your purchase! Your order will be shipped to:\n{order.users.email}\n\nItems:\n"
            for order_item in OrderItem.objects.filter(order=order):
                message += f"{order_item.quantity} x {order_item.item.name} - {order_item.getTotalPrice()}frs\n"
            message += f"Total Price: {totalPrice}frs"
            send_mail(
                subject=f"Purchase Confirmation - Order #{order.id} for {order.users.username}",
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[order.users.email],
                fail_silently=False
            )
            return Response({"Price": totalPrice, 'message': 'Payment successful!'}, status=status.HTTP_200_OK)
        else:
            # Payment failed
            return Response({'message': 'Payment failed.'}, status=status.HTTP_400_BAD_REQUEST)


class ItemView(CreateView):
    model = Items
    form_class = ItemForm
    template_name = 'app/forms.html'
