#!/usr/bin/env python
"""
Create sample data for testing cart system
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean_food_gis.settings')
django.setup()

from food_store.models import Farm, Category, Product, DeliveryZone
from django.contrib.auth.models import User

def create_sample_data():
    print("🌱 Tạo dữ liệu mẫu cho hệ thống giỏ hàng...")
    
    # Create categories
    categories_data = [
        {'name': 'Rau củ quả', 'description': 'Rau củ quả tươi sạch'},
        {'name': 'Trái cây', 'description': 'Trái cây tươi ngon'},
        {'name': 'Thịt sạch', 'description': 'Thịt heo, gà, bò sạch'},
        {'name': 'Hải sản', 'description': 'Hải sản tươi sống'},
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        categories.append(category)
        if created:
            print(f"✅ Tạo danh mục: {category.name}")
    
    # Create farms
    farms_data = [
        {
            'name': 'Trang trại Xanh',
            'address': 'Củ Chi, TP.HCM',
            'phone': '0901234567',
            'email': 'xanh@farm.com',
            'description': 'Trang trại rau sạch hữu cơ',
            'organic_certified': True,
            'latitude': 10.9,
            'longitude': 106.5
        },
        {
            'name': 'Trang trại Sạch',
            'address': 'Hóc Môn, TP.HCM',
            'phone': '0901234568',
            'email': 'sach@farm.com',
            'description': 'Trang trại thịt sạch',
            'organic_certified': False,
            'latitude': 10.8,
            'longitude': 106.6
        },
        {
            'name': 'Trang trại Biển',
            'address': 'Cần Giờ, TP.HCM',
            'phone': '0901234569',
            'email': 'bien@farm.com',
            'description': 'Trang trại hải sản tươi sống',
            'organic_certified': True,
            'latitude': 10.4,
            'longitude': 106.8
        }
    ]
    
    farms = []
    for farm_data in farms_data:
        farm, created = Farm.objects.get_or_create(
            name=farm_data['name'],
            defaults=farm_data
        )
        farms.append(farm)
        if created:
            print(f"🏡 Tạo trang trại: {farm.name}")
    
    # Create products
    products_data = [
        # Rau củ quả
        {
            'name': 'Rau muống hữu cơ',
            'category': categories[0],
            'farm': farms[0],
            'description': 'Rau muống tươi, trồng theo phương pháp hữu cơ',
            'price': 15000,
            'unit': 'bó',
            'stock_quantity': 50,
            'nutritional_info': 'Giàu vitamin A, C và sắt'
        },
        {
            'name': 'Cà chua bi',
            'category': categories[0],
            'farm': farms[0],
            'description': 'Cà chua bi ngọt, không thuốc trừ sâu',
            'price': 25000,
            'unit': 'kg',
            'stock_quantity': 30,
            'nutritional_info': 'Chứa lycopene, vitamin C'
        },
        # Trái cây
        {
            'name': 'Xoài cát Hòa Lộc',
            'category': categories[1],
            'farm': farms[0],
            'description': 'Xoài cát Hòa Lộc thơm ngon, ngọt tự nhiên',
            'price': 80000,
            'unit': 'kg',
            'stock_quantity': 20,
            'nutritional_info': 'Giàu vitamin A, C và chất xơ'
        },
        {
            'name': 'Cam sành',
            'category': categories[1],
            'farm': farms[0],
            'description': 'Cam sành tươi, vỏ mỏng, nhiều nước',
            'price': 35000,
            'unit': 'kg',
            'stock_quantity': 40,
            'nutritional_info': 'Vitamin C cao, tăng cường miễn dịch'
        },
        # Thịt sạch
        {
            'name': 'Thịt heo sạch',
            'category': categories[2],
            'farm': farms[1],
            'description': 'Thịt heo nuôi tự nhiên, không hormone',
            'price': 120000,
            'unit': 'kg',
            'stock_quantity': 15,
            'nutritional_info': 'Protein cao, ít mỡ'
        },
        {
            'name': 'Gà ta thả vườn',
            'category': categories[2],
            'farm': farms[1],
            'description': 'Gà ta thả vườn, thịt chắc, ngọt tự nhiên',
            'price': 150000,
            'unit': 'con',
            'stock_quantity': 10,
            'nutritional_info': 'Protein cao, ít cholesterol'
        },
        # Hải sản
        {
            'name': 'Tôm sú tươi',
            'category': categories[3],
            'farm': farms[2],
            'description': 'Tôm sú tươi sống, nuôi trong môi trường sạch',
            'price': 200000,
            'unit': 'kg',
            'stock_quantity': 8,
            'nutritional_info': 'Protein cao, omega-3'
        },
        {
            'name': 'Cá basa fillet',
            'category': categories[3],
            'farm': farms[2],
            'description': 'Cá basa fillet tươi, không xương',
            'price': 85000,
            'unit': 'kg',
            'stock_quantity': 12,
            'nutritional_info': 'Protein cao, ít mỡ, omega-3'
        }
    ]
    
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
        if created:
            print(f"🥬 Tạo sản phẩm: {product.name} - {product.price:,}đ/{product.unit}")
    
    # Create delivery zones
    zones_data = [
        {
            'name': 'TP. Hồ Chí Minh',
            'area_description': 'Các quận nội thành TP.HCM',
            'delivery_fee': 30000,
            'delivery_time': '1-2 ngày',
            'is_active': True
        },
        {
            'name': 'Huyện ngoại thành',
            'area_description': 'Các huyện ngoại thành TP.HCM',
            'delivery_fee': 50000,
            'delivery_time': '2-3 ngày',
            'is_active': True
        }
    ]
    
    for zone_data in zones_data:
        zone, created = DeliveryZone.objects.get_or_create(
            name=zone_data['name'],
            defaults=zone_data
        )
        if created:
            print(f"🚚 Tạo khu vực giao hàng: {zone.name} - {zone.delivery_fee:,}đ")
    
    print("\n✅ Hoàn thành tạo dữ liệu mẫu!")
    print(f"📊 Thống kê:")
    print(f"   - Danh mục: {Category.objects.count()}")
    print(f"   - Trang trại: {Farm.objects.count()}")
    print(f"   - Sản phẩm: {Product.objects.count()}")
    print(f"   - Khu vực giao hàng: {DeliveryZone.objects.count()}")

if __name__ == '__main__':
    create_sample_data()