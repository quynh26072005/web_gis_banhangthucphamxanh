"""
Create Enhanced Sample Data for Clean Food GIS
Tạo dữ liệu mẫu phong phú cho demo
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean_food_gis.settings')
django.setup()

from django.contrib.gis.geos import Point, Polygon
from food_store.models import Farm, Category, Product, DeliveryZone, Customer, Order, OrderItem
from django.contrib.auth.models import User
from decimal import Decimal
import random

def create_sample_data():
    print("🌱 Bắt đầu tạo dữ liệu mẫu...")
    
    # Clear existing data (optional)
    print("🗑️  Xóa dữ liệu cũ...")
    OrderItem.objects.all().delete()
    Order.objects.all().delete()
    Product.objects.all().delete()
    Farm.objects.all().delete()
    Category.objects.all().delete()
    DeliveryZone.objects.all().delete()
    
    # Create Categories
    print("📦 Tạo danh mục sản phẩm...")
    categories = [
        {
            'name': 'Rau củ quả',
            'description': 'Rau củ quả tươi ngon, không hóa chất'
        },
        {
            'name': 'Trái cây',
            'description': 'Trái cây sạch, ngọt tự nhiên'
        },
        {
            'name': 'Thịt sạch',
            'description': 'Thịt hươu, gà, heo sạch, nuôi tự nhiên'
        },
        {
            'name': 'Trứng',
            'description': 'Trứng gà, vịt hữu cơ'
        },
        {
            'name': 'Sữa & Sản phẩm sữa',
            'description': 'Sữa tươi và các sản phẩm từ sữa'
        }
    ]
    
    category_objects = {}
    for cat_data in categories:
        cat = Category.objects.create(**cat_data)
        category_objects[cat.name] = cat
        print(f"  ✓ {cat.name}")
    
    # Create Delivery Zones (Vietnam cities)
    print("\n🗺️  Tạo khu vực giao hàng...")
    zones_data = [
        {
            'name': 'TP. Hồ Chí Minh',
            'coords': [
                (106.55, 10.65),
                (106.85, 10.65),
                (106.85, 10.95),
                (106.55, 10.95),
                (106.55, 10.65)
            ],
            'delivery_fee': 30000,
            'delivery_time': '1-2 ngày'
        },
        {
            'name': 'Hà Nội',
            'coords': [
                (105.75, 20.95),
                (105.95, 20.95),
                (105.95, 21.15),
                (105.75, 21.15),
                (105.75, 20.95)
            ],
            'delivery_fee': 35000,
            'delivery_time': '2-3 ngày'
        },
        {
            'name': 'Đà Nẵng',
            'coords': [
                (108.15, 16.00),
                (108.25, 16.00),
                (108.25, 16.10),
                (108.15, 16.10),
                (108.15, 16.00)
            ],
            'delivery_fee': 25000,
            'delivery_time': '1-2 ngày'
        },
        {
            'name': 'Cần Thơ',
            'coords': [
                (105.70, 10.00),
                (105.85, 10.00),
                (105.85, 10.10),
                (105.70, 10.10),
                (105.70, 10.00)
            ],
            'delivery_fee': 28000,
            'delivery_time': '1-2 ngày'
        }
    ]
    
    for zone_data in zones_data:
        coords = zone_data.pop('coords')
        polygon = Polygon(coords)
        zone = DeliveryZone.objects.create(
            area=polygon,
            is_active=True,
            **zone_data
        )
        print(f"  ✓ {zone.name}")
    
    # Create Farms with realistic locations
    print("\n🏡 Tạo trang trại...")
    farms_data = [
        {
            'name': 'Trang trại Xanh Organic',
            'address': 'Củ Chi, TP. Hồ Chí Minh',
            'location': Point(106.49, 10.97),
            'phone': '0909123456',
            'email': 'xanhorganic@gmail.com',
            'description': 'Chuyên cung cấp rau củ hữu cơ chất lượng cao',
            'organic_certified': True,
            'certification_number': 'ORG-VN-001'
        },
        {
            'name': 'Nông trại Đồng Nai',
            'address': 'Long Thành, Đồng Nai',
            'location': Point(106.98, 10.75),
            'phone': '0909234567',
            'email': 'dongnai@farm.vn',
            'description': 'Rau sạch và trái cây tươi ngon',
            'organic_certified': True,
            'certification_number': 'ORG-VN-002'
        },
        {
            'name': 'Trang trại Hoa Sen',
            'address': 'Bình Dương',
            'location': Point(106.71, 11.12),
            'phone': '0909345678',
            'email': 'hoasen@farm.vn',
            'description': 'Chuyên sản xuất rau sạch công nghệ cao',
            'organic_certified': False,
            'certification_number': ''
        },
        {
            'name': 'Green Valley Farm',
            'address': 'Tây Ninh',
            'location': Point(106.11, 11.31),
            'phone': '0909456789',
            'email': 'greenvalley@gmail.com',
            'description': 'Trang trại nuôi gà hữu cơ và trồng rau sạch',
            'organic_certified': True,
            'certification_number': 'ORG-VN-003'
        },
        {
            'name': 'Trang trại Phước An',
            'address': 'Long An',
            'location': Point(106.24, 10.53),
            'phone': '0909567890',
            'email': 'phuocan@farm.vn',
            'description': 'Chuyên cung cấp thịt heo và gà sạch',
            'organic_certified': False,
            'certification_number': ''
        }
    ]
    
    farm_objects = []
    for farm_data in farms_data:
        farm = Farm.objects.create(**farm_data)
        farm_objects.append(farm)
        print(f"  ✓ {farm.name} - {farm.address}")
    
    # Create Products
    print("\n🛒 Tạo sản phẩm...")
    products_data = [
        # Rau củ
        {'name': 'Cải xanh', 'category': 'Rau củ quả', 'price': 25000, 'unit': 'kg', 'stock': 100},
        {'name': 'Cà chua', 'category': 'Rau củ quả', 'price': 35000, 'unit': 'kg', 'stock': 80},
        {'name': 'Dưa chuột', 'category': 'Rau củ quả', 'price': 20000, 'unit': 'kg', 'stock': 90},
        {'name': 'Xà lách', 'category': 'Rau củ quả', 'price': 30000, 'unit': 'kg', 'stock': 70},
        {'name': 'Rau muống', 'category': 'Rau củ quả', 'price': 15000, 'unit': 'kg', 'stock': 120},
        
        # Trái cây
        {'name': 'Cam sành', 'category': 'Trái cây', 'price': 45000, 'unit': 'kg', 'stock': 60},
        {'name': 'Táo Mỹ', 'category': 'Trái cây', 'price': 85000, 'unit': 'kg', 'stock': 40},
        {'name': 'Chuối già', 'category': 'Trái cây', 'price': 25000, 'unit': 'kg', 'stock': 100},
        {'name': 'Dưa hấu', 'category': 'Trái cây', 'price': 20000, 'unit': 'kg', 'stock': 80},
        {'name': 'Nho xanh', 'category': 'Trái cây', 'price': 120000, 'unit': 'kg', 'stock': 30},
        
        # Thịt sạch
        {'name': 'Thịt gà ta', 'category': 'Thịt sạch', 'price': 150000, 'unit': 'kg', 'stock': 50},
        {'name': 'Thịt heo sạch', 'category': 'Thịt sạch', 'price': 130000, 'unit': 'kg', 'stock': 60},
        {'name': 'Thịt bò úc', 'category': 'Thịt sạch', 'price': 250000, 'unit': 'kg', 'stock': 40},
        
        # Trứng
        {'name': 'Trứng gà công nghiệp', 'category': 'Trứng', 'price': 3500, 'unit': 'quả', 'stock': 500},
        {'name': 'Trứng gà ta', 'category': 'Trứng', 'price': 5000, 'unit': 'quả', 'stock': 300},
        {'name': 'Trứng vịt', 'category': 'Trứng', 'price': 4000, 'unit': 'quả', 'stock': 200},
        
        # Sữa
        {'name': 'Sữa tươi nguyên chất', 'category': 'Sữa & Sản phẩm sữa', 'price': 35000, 'unit': 'lít', 'stock': 100},
        {'name': 'Phô mai tươi', 'category': 'Sữa & Sản phẩm sữa', 'price': 80000, 'unit': 'hộp', 'stock': 50},
    ]
    
    for i, prod_data in enumerate(products_data):
        category = category_objects[prod_data.pop('category')]
        farm = farm_objects[i % len(farm_objects)]  # Distribute products across farms
        stock = prod_data.pop('stock')
        
        product = Product.objects.create(
            farm=farm,
            category=category,
            description=f"{prod_data['name']} tươi ngon, sạch sẽ",
            stock_quantity=stock,
            is_available=True,
            **prod_data
        )
        print(f"  ✓ {product.name} - {product.price}₫/{product.unit} ({farm.name})")
    
    print("\n✅ Hoàn thành tạo dữ liệu mẫu!")
    print(f"   📊 Thống kê:")
    print(f"      - Danh mục: {Category.objects.count()}")
    print(f"      - Trang trại: {Farm.objects.count()}")
    print(f"      - Sản phẩm: {Product.objects.count()}")
    print(f"      - Khu vực giao hàng: {DeliveryZone.objects.count()}")
    print(f"\n🎉 Bạn có thể truy cập website để xem dữ liệu!")

if __name__ == '__main__':
    create_sample_data()
