from django.core.management.base import BaseCommand
from myapp.models import Product, Customer, Order

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        product1 = Product.objects.create(
            name='Water',
            price=1.99,
            available=True
        )

        product2 = Product.objects.create(
            name='Soda',
            price=2.49,
            available=True
        )

        product3 = Product.objects.create(
            name='Juice',
            price=3.29,
            available=False
        )

        product4 = Product.objects.create(
            name='Milk',
            price=2.79,
            available=True
        )

        product5 = Product.objects.create(
            name='Coffee',
            price=5.99,
            available=False
        )

        product6 = Product.objects.create(
            name='Tea',
            price=4.49,
            available=True
        )

        product7 = Product.objects.create(
            name='Bread',
            price=1.29,
            available=True
        )

        product8 = Product.objects.create(
            name='Butter',
            price=3.99,
            available=True
        )

        product9 = Product.objects.create(
            name='Cheese',
            price=4.50,
            available=False
        )

        product10 = Product.objects.create(
            name='Eggs',
            price=2.99,
            available=True
        )

        customer1 = Customer.objects.create(
            name='Anabele',
            address='Address1'
        )
        customer2 = Customer.objects.create(
            name='John',
            address='Address2'
        )
        customer3 = Customer.objects.create(
            name='Alex',
            address='Address2'
        )

        order1 = Order.objects.create(
            customer=customer1,
            status='In Progress',
            date='2024-11-28'
        )
        order2 = Order.objects.create(
            customer=customer1,
            status='New',
            date='2024-11-29'
        )
        order3 = Order.objects.create(
            customer=customer1,
            status='Completed',
            date='2024-11-15'
        )

        order1.products.add(product1, product5, product2, product8)
        order1.customer = customer1

        order2.products.add(product1, product2, product6, product3, product8)
        order2.customer = customer2

        order3.products.add(product1, product2, product4, product10, product7, product9)
        order3.customer = customer3

        self.stdout.write("Data created successfully.")