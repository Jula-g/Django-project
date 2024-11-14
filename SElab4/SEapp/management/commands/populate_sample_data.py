from django.core.management.base import BaseCommand
from SEapp.models import Product, Customer, Order

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        product1 = Product.objects.create(
            name='Hair Brush',
            price=19.99,
            available=True
        )
        product2 = Product.objects.create(
            name='Shampoo',
            price=10.49,
            available=True
        )
        product3 = Product.objects.create(
            name='Conditioner',
            price=8.99,
            available=False
        )

        # Create Customer entries
        customer1 = Customer.objects.create(
            name='Jane Doe',
            address='123 Main St, Springfield'
        )
        customer2 = Customer.objects.create(
            name='John Smith',
            address='456 Oak St, Shelbyville'
        )
        customer3 = Customer.objects.create(
            name='Alice Johnson',
            address='789 Maple Ave, Capital City'
        )

        # Create Order entries and associate products
        order1 = Order.objects.create(
            customer=customer1,
            status='New'
        )
        order1.products.add(product1, product2)  # Add multiple products to the order

        order2 = Order.objects.create(
            customer=customer2,
            status='In Process'
        )
        order2.products.add(product2, product3)

        order3 = Order.objects.create(
            customer=customer3,
            status='Sent'
        )
        order3.products.add(product1, product3)

        self.stdout.write("Data created successfully.")