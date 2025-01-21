from itertools import product
from urllib.request import ProxyDigestAuthHandler

from django.core.exceptions import ValidationError
from django.db import models


def validatePrice(value):
    if value <= 0:
        raise ValidationError('Price must be a positive number')

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    price = models.DecimalField(decimal_places=2, max_digits=10, validators=[validatePrice])
    available = models.BooleanField()

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False, blank=False)
    address = models.CharField(max_length=50, null=False, blank=False)

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    date = models.DateField()

    class Status(models.TextChoices):
        New = 'New', 'new'
        InProcess = 'In Process', 'in process'
        Sent = 'Sent', 'sent'
        Completed = 'Completed', 'completed'

    status = models.CharField(max_length=50, choices=Status.choices, default=Status.New)

    def calculateTotal(self):
        return sum(product.price for product in self.products.all())

    def checkAvailability(self):
        unavailable_products = [product.name for product in self.products.all() if not product.available]

        if unavailable_products:
            list = ', '.join(unavailable_products)
            raise ValidationError(f'{list} are not available')

        return True
