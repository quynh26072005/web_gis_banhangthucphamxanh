"""
Management command to create sample shipper account
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from food_store.models import Shipper


class Command(BaseCommand):
    help = 'Tạo tài khoản shipper mẫu'

    def handle(self, *args, **options):
        # Create shipper user
        username = 'shipper'
        password = 'shipper123'
        
        # Check if user exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User {username} đã tồn tại!'))
            user = User.objects.get(username=username)
        else:
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name='Nguyễn',
                last_name='Văn A',
                email='shipper@cleanfood.com'
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Đã tạo user: {username}'))
        
        # Create or update shipper profile
        shipper, created = Shipper.objects.get_or_create(
            user=user,
            defaults={
                'phone': '0901234567',
                'vehicle_number': '59-A1 12345',
                'status': 'offline',
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Đã tạo profile shipper'))
        else:
            self.stdout.write(self.style.WARNING('Profile shipper đã tồn tại'))
        
        self.stdout.write(self.style.SUCCESS('\n' + '='*50))
        self.stdout.write(self.style.SUCCESS('✓ Hoàn thành!'))
        self.stdout.write(self.style.SUCCESS('\nThông tin đăng nhập:'))
        self.stdout.write(self.style.SUCCESS(f'  Username: {username}'))
        self.stdout.write(self.style.SUCCESS(f'  Password: {password}'))
        self.stdout.write(self.style.SUCCESS(f'\nTruy cập: http://127.0.0.1:8000/shipper/'))
        self.stdout.write(self.style.SUCCESS('='*50))
