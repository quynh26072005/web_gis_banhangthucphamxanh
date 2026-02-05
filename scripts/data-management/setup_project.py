#!/usr/bin/env python
"""
Setup script for minimal clean food GIS project
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean_food_gis.settings')
django.setup()

from django.contrib.auth.models import User
from food_store.models import Farm, Category, Product, DeliveryZone, Customer
from django.core.management import call_command

def create_superuser():
    """Create superuser if not exists"""
    print("👤 CREATING SUPERUSER")
    print("=" * 50)
    
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@cleanfood.com',
            password='admin123'
        )
        print("✅ Created superuser: admin/admin123")
    else:
        print("✅ Superuser already exists")

def create_sample_data():
    """Create minimal sample data"""
    print("\n📊 CREATING SAMPLE DATA")
    print("=" * 50)
    
    # Create categories
    categories_data = [
        {'name': 'Rau củ', 'description': 'Rau củ tươi sạch'},
        {'name': 'Trái cây', 'description': 'Trái cây tươi ngon'},
        {'name': 'Thịt sạch', 'description': 'Thịt sạch chất lượng cao'},
        {'name': 'Hải sản', 'description': 'Hải sản tươi sống'},
        {'name': 'Sữa & Trứng', 'description': 'Sữa và trứng tươi'}
    ]
    
    created_categories = 0
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        if created:
            created_categories += 1
    
    print(f"✅ Created {created_categories} categories")
    
    # Create farms
    farms_data = [
        {
            'name': 'Trang trại Xanh',
            'address': '123 Đường ABC, Quận 1, TP.HCM',
            'phone': '0901234567',
            'latitude': 10.762622,
            'longitude': 106.660172,
            'organic_certified': True
        },
        {
            'name': 'Cửa hàng Sạch',
            'address': '456 Đường DEF, Quận 3, TP.HCM',
            'phone': '0907654321',
            'latitude': 10.768431,
            'longitude': 106.681602,
            'organic_certified': False
        },
        {
            'name': 'Farm Hữu cơ',
            'address': '789 Đường GHI, Quận 7, TP.HCM',
            'phone': '0909876543',
            'latitude': 10.732776,
            'longitude': 106.719017,
            'organic_certified': True
        }
    ]
    
    created_farms = 0
    for farm_data in farms_data:
        farm, created = Farm.objects.get_or_create(
            name=farm_data['name'],
            defaults=farm_data
        )
        if created:
            created_farms += 1
    
    print(f"✅ Created {created_farms} farms")
    
    # Create products
    if Category.objects.exists() and Farm.objects.exists():
        rau_cu = Category.objects.get(name='Rau củ')
        trai_cay = Category.objects.get(name='Trái cây')
        farm1 = Farm.objects.first()
        farm2 = Farm.objects.last()
        
        products_data = [
            {
                'name': 'Cà chua cherry',
                'category': rau_cu,
                'farm': farm1,
                'description': 'Cà chua cherry tươi ngon',
                'price': 45000,
                'unit': 'kg',
                'stock_quantity': 100,
                'is_available': True
            },
            {
                'name': 'Xoài cát Hòa Lộc',
                'category': trai_cay,
                'farm': farm2,
                'description': 'Xoài cát Hòa Lộc thơm ngon',
                'price': 80000,
                'unit': 'kg',
                'stock_quantity': 50,
                'is_available': True
            },
            {
                'name': 'Rau muống',
                'category': rau_cu,
                'farm': farm1,
                'description': 'Rau muống tươi xanh',
                'price': 25000,
                'unit': 'kg',
                'stock_quantity': 200,
                'is_available': True
            }
        ]
        
        created_products = 0
        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                farm=prod_data['farm'],
                defaults=prod_data
            )
            if created:
                created_products += 1
        
        print(f"✅ Created {created_products} products")

def create_delivery_zones():
    """Create essential delivery zones"""
    print("\n🚚 CREATING DELIVERY ZONES")
    print("=" * 50)
    
    zones_data = [
        {
            'name': 'TP. Hồ Chí Minh - Nội thành',
            'area_description': 'Quận 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12',
            'delivery_fee': 25000,
            'delivery_time': '30-60 phút',
            'is_active': True
        },
        {
            'name': 'TP. Hồ Chí Minh - Ngoại thành',
            'area_description': 'Thủ Đức, Bình Tân, Hóc Môn, Củ Chi',
            'delivery_fee': 35000,
            'delivery_time': '45-90 phút',
            'is_active': True
        },
        {
            'name': 'Bình Dương',
            'area_description': 'Thủ Dầu Một, Dĩ An, Thuận An',
            'delivery_fee': 30000,
            'delivery_time': '45-90 phút',
            'is_active': True
        }
    ]
    
    created_zones = 0
    for zone_data in zones_data:
        zone, created = DeliveryZone.objects.get_or_create(
            name=zone_data['name'],
            defaults=zone_data
        )
        if created:
            created_zones += 1
    
    print(f"✅ Created {created_zones} delivery zones")

def run_migrations():
    """Run migrations to ensure database is up to date"""
    print("\n🔄 RUNNING MIGRATIONS")
    print("=" * 50)
    
    try:
        call_command('migrate', verbosity=0)
        print("✅ Migrations completed")
    except Exception as e:
        print(f"❌ Migration failed: {e}")

def collect_static():
    """Collect static files"""
    print("\n📁 COLLECTING STATIC FILES")
    print("=" * 50)
    
    try:
        call_command('collectstatic', '--noinput', verbosity=0)
        print("✅ Static files collected")
    except Exception as e:
        print(f"❌ Static collection failed: {e}")

def check_project_status():
    """Check project status"""
    print("\n📊 PROJECT STATUS")
    print("=" * 50)
    
    try:
        print(f"🏪 Farms: {Farm.objects.count()}")
        print(f"📦 Products: {Product.objects.count()}")
        print(f"🚚 Delivery Zones: {DeliveryZone.objects.count()}")
        print(f"👥 Users: {User.objects.count()}")
        print(f"🔑 Superusers: {User.objects.filter(is_superuser=True).count()}")
        
        if Farm.objects.exists() and Product.objects.exists():
            print("✅ Project is ready to use")
        else:
            print("⚠️ Project needs more data")
            
    except Exception as e:
        print(f"❌ Status check failed: {e}")

def main():
    print("🚀 MINIMAL PROJECT SETUP")
    print("=" * 70)
    print("Setting up Clean Food GIS minimal version...")
    print("=" * 70)
    
    run_migrations()
    create_superuser()
    create_sample_data()
    create_delivery_zones()
    collect_static()
    check_project_status()
    
    print("\n🎉 SETUP COMPLETED!")
    print("=" * 70)
    print("🌐 Access your project:")
    print("   Website: http://127.0.0.1:8000/")
    print("   Admin: http://127.0.0.1:8000/admin/")
    print("   GIS Tools: http://127.0.0.1:8000/gis/")
    print("\n🔑 Admin credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n✨ Your minimal Clean Food GIS project is ready!")

if __name__ == '__main__':
    main()