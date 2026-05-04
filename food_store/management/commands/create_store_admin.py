"""
Management command to create Store Admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from food_store.models import StoreAdmin, Farm


class Command(BaseCommand):
    help = 'Create a Store Admin for testing'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username')
        parser.add_argument('--password', type=str, default='123456', help='Password (default: 123456)')
        parser.add_argument('--farm-id', type=int, help='Farm ID')
        parser.add_argument('--phone', type=str, default='0901234567', help='Phone number')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        phone = options['phone']
        farm_id = options.get('farm_id')
        
        # Check if user exists
        try:
            user = User.objects.get(username=username)
            self.stdout.write(self.style.WARNING(f'User {username} already exists'))
        except User.DoesNotExist:
            # Create user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name='Store',
                last_name='Admin'
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Created user: {username}'))
        
        # Check if already has StoreAdmin profile
        if StoreAdmin.objects.filter(user=user).exists():
            self.stdout.write(self.style.ERROR(f'✗ User {username} already has StoreAdmin profile'))
            return
        
        # Get farm
        if farm_id:
            try:
                farm = Farm.objects.get(id=farm_id)
            except Farm.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'✗ Farm with ID {farm_id} not found'))
                return
        else:
            # Get first farm
            farm = Farm.objects.first()
            if not farm:
                self.stdout.write(self.style.ERROR('✗ No farms found. Please create a farm first.'))
                return
        
        # Create StoreAdmin
        store_admin = StoreAdmin.objects.create(
            user=user,
            farm=farm,
            phone=phone,
            can_manage_products=True,
            can_manage_orders=True,
            can_manage_inventory=True,
            can_manage_shippers=True,
            can_view_reports=True,
            is_active=True
        )
        
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('✓ Store Admin created successfully!'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(f'Username: {username}')
        self.stdout.write(f'Password: {password}')
        self.stdout.write(f'Farm: {farm.name}')
        self.stdout.write(f'Phone: {phone}')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.WARNING('Now you can login with:'))
        self.stdout.write(f'  URL: http://127.0.0.1:8000/accounts/login/')
        self.stdout.write(f'  Username: {username}')
        self.stdout.write(f'  Password: {password}')
        self.stdout.write(self.style.SUCCESS('=' * 60))
