from django.db import IntegrityError
from django.test import TestCase

from myapp.models import Product, Customer, Order
from django.core.exceptions import ValidationError

class ProductModelTest(TestCase):
    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(name='Temporary product',
            price=1.99, available=True)
        self.assertEqual(temp_product.name, 'Temporary product')
        self.assertEqual(temp_product.price, 2.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Invalid product',
                price = -1.99, available = True)
            temp_product.full_clean()

    def test_create_product_name_missing(self):
        temp_product = Product(price=2.00, available=True)
        with self.assertRaises(ValidationError):
            temp_product.full_clean()

    def test_create_product_name_blank(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name = '', price = 2.00, available = True)
            temp_product.full_clean()

    def test_create_product_price_missing(self):
        with self.assertRaises(IntegrityError):
            temp_product = Product.objects.create(name='Missing field product', available = True)

    def test_create_product_available_missing(self):
        with self.assertRaises(IntegrityError):
            temp_product = Product.objects.create(name='Missing field product', price = 2.00)

    def test_create_product_with_min_length_name(self):
        min_length_name = 'A' * 3
        temp_product = Product.objects.create(name=min_length_name, price=1.99, available=True)
        self.assertEqual(temp_product.name, min_length_name)
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_max_length_name(self):
        max_length_name = 'A' * 255
        temp_product = Product.objects.create(name=max_length_name, price=1.99, available=True)
        self.assertEqual(temp_product.name, max_length_name)
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)


    def test_create_product_with_minimum_price(self):
        temp_product = Product.objects.create(name='Product with minimum price', price=0.1, available=True)
        self.assertEqual(temp_product.name, 'Product with minimum price')
        self.assertEqual(temp_product.price, 0.1)
        self.assertTrue(temp_product.available)

    def test_create_product_with_maximum_price(self):
        max_price = 99999999.99
        temp_product = Product.objects.create(name='Product with maximum price', price=max_price, available=True)
        self.assertEqual(temp_product.name, 'Product with maximum price')
        self.assertEqual(temp_product.price, max_price)
        self.assertTrue(temp_product.available)

    def test_create_product_with_invalid_price_format(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name='Invalid price format', price=1.9999, available=True)
            temp_product.full_clean()


class CustomerModelTest(TestCase):
    def test_create_customer_with_valid_data(self):
        temp_customer = Customer.objects.create(name='Temporary customer', address='Address')
        self.assertEqual(temp_customer.name, 'Temporary customer')
        self.assertEqual(temp_customer.address, 'Address')

    def test_create_customer_name_missing(self):
        temp_customer = Customer.objects.create(address='Address')
        with self.assertRaises(ValidationError):
            temp_customer.full_clean()

    def test_create_customer_name_blank(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer.objects.create(name='', address='Address')
            temp_customer.full_clean()

    def test_create_customer_address_missing(self):
        temp_customer = Customer.objects.create(name='Temporary customer')
        with self.assertRaises(ValidationError):
            temp_customer.full_clean()


    def test_create_customer_with_min_length_name(self):
        min_length_name = 'A' * 3
        temp_customer = Customer.objects.create(name=min_length_name, address='Address')
        self.assertEqual(temp_customer.name, min_length_name)
        self.assertEqual(temp_customer.address, 'Address')

    def test_create_customer_with_max_length_name(self):
        max_length_name = 'A' * 100
        temp_customer = Customer.objects.create(name=max_length_name, address='Address')
        self.assertEqual(temp_customer.name, max_length_name)
        self.assertEqual(temp_customer.address, 'Address')

class OrderModelTest(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name='Temporary customer', address='Address')
        self.product1 = Product.objects.create(name='Product 1', price=2.00, available=True)
        self.product2 = Product.objects.create(name='Product 2', price=4.50, available=True)
        self.product3 = Product.objects.create(name='Product 3', price=7.50, available=False)

    def test_create_order_with_valid_data(self):
        temp_order = Order.objects.create(customer=self.customer, date='2025-04-02')
        temp_order.products.add(self.product1)
        temp_order.products.add(self.product2)
        self.assertEqual(temp_order.date, '2025-04-02')
        self.assertEqual(temp_order.customer.name, 'Temporary customer')
        products = temp_order.products.all()
        self.assertIn(self.product1, products)
        self.assertIn(self.product2, products)

    def test_create_order_with_customer_missing(self):
        temp_order = Order(date='2025-04-02', status="new")
        Order.products.through(order=temp_order, product=self.product1)
        Order.products.through(order=temp_order, product=self.product2)
        with self.assertRaises(ValidationError):
            temp_order.full_clean()

    def test_create_order_with_status_missing(self):
        temp_order = Order(customer=self.customer, date='2025-04-02')
        Order.products.through(order=temp_order, product=self.product1)
        Order.products.through(order=temp_order, product=self.product2)
        self.assertEqual(temp_order.status, Order.Status.New)

    def test_create_order_with_date_missing(self):
        temp_order = Order(customer=self.customer)
        Order.products.through(order=temp_order, product=self.product1)
        with self.assertRaises(ValidationError):
            temp_order.full_clean()

    def test_total_price_calc_valid(self):
        temp_order = Order.objects.create(customer=self.customer, date='2025-04-02')
        temp_order.products.add(self.product1)
        temp_order.products.add(self.product2)
        total_price = temp_order.calculateTotal()
        self.assertEqual(total_price, 6.50)

    def test_total_price_calc_invalid(self):
        temp_order = Order.objects.create(customer=self.customer, date='2025-04-02')
        total_price = temp_order.calculateTotal()
        self.assertEqual(total_price, 0)

    def test_order_with_all_products_available(self):
        order = Order.objects.create(customer=self.customer, date='2025-04-02')
        order.products.add(self.product1, self.product2)

        try:
            order.checkAvailability()
        except ValidationError:
            self.fail("checkAvailability raised ValidationError unexpectedly!")

    def test_order_with_some_products_unavailable(self):
        order = Order.objects.create(customer=self.customer, date='2025-04-02')
        order.products.add(self.product1, self.product2, self.product3)

        with self.assertRaises(ValidationError) as context:
            order.checkAvailability()

        self.assertIn('Product 3', str(context.exception))

    def test_order_with_all_products_unavailable(self):
        order = Order.objects.create(customer=self.customer, date='2025-04-02')
        order.products.add(self.product3)

        with self.assertRaises(ValidationError) as context:
            order.checkAvailability()

        self.assertIn('Product 3', str(context.exception))
