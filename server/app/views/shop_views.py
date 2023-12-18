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
from app.models import Items, Images, Order, OrderItem


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

        # Making sure the object doesn't exist before adding to Cart
        try:
            order_item = OrderItem.objects.get(order=order, item=item)
            order_item.quantity = quantity
            order_item.save()
        except OrderItem.DoesNotExist:
            order_item = OrderItem.objects.create(order=order, item=item, quantity=quantity)
        return Response({
            'Success': 'Product {} was added to cart.'.format(order_item.item.name),
            'statusCode': status.HTTP_200_OK
        })


class CartView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        order = Order.objects.get(users=request.user, ordered=False)
        cart_products = OrderItem.objects.filter(order=order)
        list_of_cart_products = dict()
        for order_item in cart_products:
            item_images = Images.objects.filter(item=order_item.item)
            image_urls = [default_storage.url(image.image) for image in item_images]
            list_of_cart_products[order_item.id] = {
                "name": order_item.item.name,
                "price": order_item.item.price,
                "quantity": order_item.quantity,
                "category": order_item.item.category,
                "quantity-in-stock": order_item.item.quantity_in_stock,
                "image-urls": image_urls
            }
        return Response(list_of_cart_products)
    def put(self, request):
        order = Order.objects.get(users=request.user, ordered=False)
        order_item_id = request.data.get('item_id')
        order_item = OrderItem.objects.get(id=order_item_id)
        # order_item = get_object_or_404(OrderItem, order=order, item__id=item_id)
        quantity = int(request.data.get('quantity', order_item.quantity))
        if quantity < 0:
            return Response({'error': 'Quantity cannot be negative.'}, status=status.HTTP_400_BAD_REQUEST)
        order_item.quantity = quantity
        order_item.save()
        return Response({'status': 'success'}, status=status.HTTP_200_OK)

    def delete(self, request):
        order = Order.objects.get(users=request.user, ordered=False)
        order_item_id = request.data.get('item_id')
        # order_item = get_object_or_404(OrderItem, order=order, item__id=item_id)
        order_item = OrderItem.objects.get(id=order_item_id)
        order_item.delete()
        return Response({'success': f"OrderItem '{order_item.item.name}' was successfully deleted"})


class CheckoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        full_name = request.data.get('fullname')
        email = request.data.get('email')
        address = request.data.get('address')
        try:
            order = Order.objects.get(users=request.user, ordered=False)
        except Order.DoesNotExist:
            return Response({'message': 'No order found for the current user.'}, status=status.HTTP_404_NOT_FOUND)

        # Updating the quantities of the items in Stock.
        for item in order.items.all():
            i = OrderItem.objects.get(order=order, item=item)
            item.quantity_in_stock -= i.quantity
            item.save()
        total_price = sum([order_item.getTotalPrice() for order_item in OrderItem.objects.filter(order=order)])
        # Charging the user for the order
        # (The payment processing code)
        if total_price > 0:
            order.ordered = True
            order.save()
            # Payment successful

            # Sending an email with the purchase information
            message = f"Thank you for your purchase! Your order will be shipped to:\n{address}\n\nItems:\n"
            for order_item in OrderItem.objects.filter(order=order):
                message += f"{order_item.quantity} x {order_item.item.name} - {order_item.getTotalPrice()}frs\n"
            message += f"Total Price: {total_price}frs"
            send_mail(
                subject=f"Purchase Confirmation - Order #{order.id} for {full_name}",
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[order.users.email, email],
                fail_silently=False
            )
            return Response({"Price": total_price, 'message': 'Payment successful!', 'body': message, 'statusCode': 200})
        else:
            # Payment failed
            return Response({'message': 'Payment failed.', 'statusCode': 400})


class ItemView(CreateView):
    model = Items
    form_class = ItemForm
    template_name = 'app/forms.html'
