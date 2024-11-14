from django.core.exceptions import ValidationError
from django.db import models


def validate_price(value):
    if value <= 0:
        raise ValidationError('Price must be positive.')

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(validators=[validate_price])
    available = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.price = round(self.price, 2)
        super().save(*args, **kwargs)


class Customer(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()


class Order(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Process', 'In Process'),
        ('Sent', 'Sent'),
        ('Completed', 'Completed')
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, related_name="orders")
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def total_order_price(self):
        return sum(product.price for product in self.products.all())

    def is_order_fulfilled(self):
        unavailable_products = [product for product in self.products.all() if not product.available]
        return len(unavailable_products) == 0

