from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from SEapp.models import Product, Customer, Order


class ProductModelTest(TestCase):
    def test_create_product_with_valid_data(self):
        product = Product.objects.create(name="Valid Product", price=1.99, available=True)
        self.assertEqual(product.name, "Valid Product")
        self.assertEqual(product.price, 1.99)
        self.assertTrue(product.available)

    def test_create_product_with_negative_price(self):
        product = Product(name='Invalid product', price=-1.99, available=True)
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_create_product_with_missing_fields(self):
        with self.assertRaises(IntegrityError):
            Product.objects.create(name=None, price=10.99, available=True)

    def test_create_product_with_blank_name(self):
        product = Product(name="", price=10.99, available=True)
        with self.assertRaises(ValidationError):
            product.full_clean()

    def test_create_product_with_edge_name_length(self):
        max_length_name = "A" * 255
        product = Product.objects.create(name=max_length_name, price=10.99, available=True)
        self.assertEqual(product.name, max_length_name)

    def test_create_product_with_edge_price_values(self):
        product = Product.objects.create(name="Edge Price Values", price=0.01, available=True)
        self.assertEqual(product.price, 0.01)

        product = Product.objects.create(name="Edge Price Values", price=999999.99, available=True)
        self.assertEqual(product.price, 999999.99)

    def test_create_product_with_invalid_price_format(self):
        product = Product(name='Invalid product', price='abc', available=True)
        with self.assertRaises(ValidationError):
            product.full_clean()


class CustomerModelTest(TestCase):
    def test_create_customer_with_valid_data(self):
        customer = Customer.objects.create(name="Valid Customer", address="123 Main St")
        self.assertEqual(customer.name, "Valid Customer")
        self.assertEqual(customer.address, "123 Main St")

    def test_create_customer_with_missing_name(self):
        with self.assertRaises(IntegrityError):
            Customer.objects.create(name=None, address="123 Main St")

    def test_create_customer_with_missing_address(self):
        with self.assertRaises(IntegrityError):
            Customer.objects.create(name="Valid Customer", address=None)


    def test_create_customer_with_blank_name(self):
        with self.assertRaises(ValidationError):
            customer = Customer.objects.create(name="", address="123 Main St")
            customer.full_clean()

    def test_create_customer_with_blank_address(self):
        with self.assertRaises(ValidationError):
            customer = Customer.objects.create(name="Valid Customer", address="")
            customer.full_clean()

    def test_create_customer_with_edge_name_length(self):
        max_length_name = "A" * 100
        customer = Customer.objects.create(name=max_length_name, address="123 Main St")
        self.assertEqual(customer.name, max_length_name)


class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Valid Customer", address="123 Main St")
        self.product1 = Product.objects.create(name="Product 1", price=1.99, available=True)
        self.product2 = Product.objects.create(name="Product 2", price=2.99, available=True)
        self.product3 = Product.objects.create(name="Product 3", price=3.99, available=True)

    def test_create_order_with_valid_data(self):
        order = Order.objects.create(customer=self.customer, status='New')
        order.products.add(self.product1)
        order.products.add(self.product2)
        order.products.add(self.product3)
        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.status, 'New')
        self.assertEqual(order.products.count(), 3)

    def test_create_order_with_missing_customer(self):
        with self.assertRaises(IntegrityError):
            Order.objects.create(customer=None, status='New')

    def test_create_order_with_missing_status(self):
        with self.assertRaises(IntegrityError):
            Order.objects.create(customer=self.customer, status=None)

    def test_create_order_with_invalid_status(self):
        order = Order(customer=self.customer, status='Invalid')
        with self.assertRaises(ValidationError):
            order.full_clean()


    def test_total_order_price(self):
        order = Order.objects.create(customer=self.customer, status='New')
        order.products.add(self.product1)
        order.products.add(self.product2)
        order.products.add(self.product3)
        self.assertEqual(order.total_order_price(), 1.99 + 2.99 + 3.99)

    def test_total_order_price_no_products(self):
        order = Order.objects.create(customer=self.customer, status='New')
        self.assertEqual(order.total_order_price(), 0)

    def test_is_order_fulfilled(self):
        order = Order.objects.create(customer=self.customer, status='New')
        order.products.add(self.product1)
        order.products.add(self.product2)
        order.products.add(self.product3)
        self.assertTrue(order.is_order_fulfilled())
