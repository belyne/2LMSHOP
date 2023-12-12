from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class Categories(models.Model):
#     name = models.CharField(max_length=250)
#
#     def __str__(self):
#         return self.name


DRESS_SIZES = [
    ('S', 'Small'),
    ('M', 'Medium'),
    ('L', 'Large'),
    ('XL', 'Xtra Large'),
    ('XXL', 'Xtra Xtra Large')
]


class Items(models.Model):
    name = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # size = models.CharField(choices=DRESS_SIZES, null=True)
    # category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=True)
    category = models.CharField(max_length=10, null=True)
    rating = models.IntegerField(default=0)
    quantity_in_stock = models.PositiveIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.quantity_in_stock < 0:
            raise ValueError('Quantity in stock cannot be negative.')


class Images(models.Model):
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    image = models.FileField(upload_to='pics', null=True)


class Order(models.Model):
    items = models.ManyToManyField(Items, through='OrderItem')
    users = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in Order #{self.order.id}"

    def getTotalPrice(self):
        return self.quantity * self.item.price
