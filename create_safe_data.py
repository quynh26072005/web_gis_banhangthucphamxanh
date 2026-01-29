"""
Safe Sample Data Creation for Demo
No GDAL dependency
"""
import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean_food_gis.settings')
django.setup()

from food_store.models import Farm, Category, Product, DeliveryZone, Customer, Order, OrderItem, User

def create_demo_data():
    print("🚀 Bắt đầu tạo dữ liệu demo (Safe Mode)...")
    
    # 1. Create Delivery Zones
    print("Creating zones...")
    zones = [
        {'name': 'TP. Hồ Chí Minh', 'fee': 30000, 'time': '1-2 ngày'},
        {'name': 'Hà Nội', 'fee': 35000, 'time': '3-4 ngày'},
        {'name': 'Đà Nẵng', 'fee': 25000, 'time': '2-3 ngày'}
    ]
    
    db_zones = []
    for z in zones:
        obj, created = DeliveryZone.objects.get_or_create(
            name=z['name'],
            defaults={
                'delivery_fee': z['fee'],
                'delivery_time': z['time'],
                'area_description': 'Demo Zone',
                'is_active': True
            }
        )
        db_zones.append(obj)

    # 2. Create Farms
    print("Creating farms...")
    farms_data = [
        {'name': 'Trang trại Xanh', 'lat': 10.97, 'lng': 106.49, 'organic': True},
        {'name': 'Nông trại Đà Lạt', 'lat': 11.94, 'lng': 108.43, 'organic': True},
        {'name': 'Vườn rau Củ Chi', 'lat': 11.00, 'lng': 106.50, 'organic': False},
        {'name': 'Trại gà Đồng Nai', 'lat': 10.95, 'lng': 106.82, 'organic': False}
    ]
    
    db_farms = []
    for f in farms_data:
        obj, created = Farm.objects.get_or_create(
            name=f['name'],
            defaults={
                'address': 'Địa chỉ mẫu, Việt Nam',
                'phone': '0909123456',
                'latitude': f['lat'],
                'longitude': f['lng'],
                'organic_certified': f['organic']
            }
        )
        db_farms.append(obj)
        
    # 3. Create Categories & Products
    print("Creating products...")
    cat, _ = Category.objects.get_or_create(name='Rau củ demo')
    
    products = []
    for i in range(5):
        p, _ = Product.objects.get_or_create(
            name=f'Sản phẩm demo {i+1}',
            category=cat,
            farm=random.choice(db_farms),
            defaults={
                'price': 50000 * (i+1),
                'description': 'Mô tả mẫu',
                'stock_quantity': 100
            }
        )
        products.append(p)
        
    # 4. Create Customer & Orders
    print("Creating orders...")
    user, _ = User.objects.get_or_create(username='demo_user', defaults={'email': 'demo@example.com'})
    customer, _ = Customer.objects.get_or_create(
        user=user, 
        defaults={
            'phone': '0123456789',
            'latitude': 10.762622,
            'longitude': 106.660172
        }
    )
    
    # Create 10 dummy orders
    for i in range(10):
        order = Order.objects.create(
            customer=customer,
            delivery_address='TP.HCM',
            delivery_latitude=10.762622,
            delivery_longitude=106.660172,
            delivery_zone=random.choice(db_zones),
            subtotal=0,
            delivery_fee=30000,
            total_amount=0,
            status=random.choice(['pending', 'processing', 'shipping', 'delivered'])
        )
        
        # Add items
        subtotal = 0
        for _ in range(random.randint(1, 3)):
            prod = random.choice(products)
            qty = random.randint(1, 5)
            price = prod.price
            OrderItem.objects.create(
                order=order,
                product=prod,
                quantity=qty,
                price=price
            )
            subtotal += price * qty
            
        order.subtotal = subtotal
        order.total_amount = subtotal + order.delivery_fee
        order.save()
        
    # Create superuser
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("✅ Created superuser: admin / admin123")
        
    print("✅ Done! Demo data created.")

if __name__ == '__main__':
    create_demo_data()
