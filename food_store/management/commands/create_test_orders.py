"""
Management command to create test orders for demo
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from food_store.models import Customer, Product, Order, OrderItem, DeliveryZone
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Create test orders for demo purposes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=20,
            help='Number of test orders to create',
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Get or create test users
        test_users = []
        for i in range(5):
            username = f'customer{i+1}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@test.com',
                    'first_name': f'Khách hàng',
                    'last_name': f'{i+1}',
                }
            )
            
            customer, created = Customer.objects.get_or_create(
                user=user,
                defaults={
                    'phone': f'090123456{i}',
                    'address': f'Địa chỉ test {i+1}, TP.HCM',
                    'latitude': 10.8 + (i * 0.01),
                    'longitude': 106.6 + (i * 0.01),
                }
            )
            test_users.append(customer)
        
        # Get products and delivery zones
        products = list(Product.objects.filter(is_available=True))
        zones = list(DeliveryZone.objects.filter(is_active=True))
        
        if not products:
            self.stdout.write(
                self.style.ERROR('No products available. Please create some products first.')
            )
            return
        
        if not zones:
            self.stdout.write(
                self.style.ERROR('No delivery zones available. Please create some delivery zones first.')
            )
            return
        
        # Create test orders
        statuses = ['pending', 'confirmed', 'preparing', 'shipping', 'delivered']
        
        for i in range(count):
            customer = random.choice(test_users)
            zone = random.choice(zones)
            status = random.choice(statuses)
            
            # Create order
            order = Order.objects.create(
                customer=customer,
                status=status,
                delivery_address=f"Địa chỉ giao hàng test {i+1}",
                delivery_latitude=customer.latitude,
                delivery_longitude=customer.longitude,
                delivery_zone=zone,
                subtotal=Decimal('0'),
                delivery_fee=zone.delivery_fee,
                total_amount=Decimal('0'),
                notes=f"Đơn hàng test số {i+1}"
            )
            
            # Add random products to order
            num_items = random.randint(1, 4)
            selected_products = random.sample(products, min(num_items, len(products)))
            
            subtotal = Decimal('0')
            for product in selected_products:
                quantity = random.randint(1, 3)
                price = product.price
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=price
                )
                
                subtotal += price * quantity
            
            # Update order totals
            order.subtotal = subtotal
            order.total_amount = subtotal + order.delivery_fee
            order.save()
            
            self.stdout.write(f'Created order #{order.id} for {customer.user.username}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {count} test orders!')
        )