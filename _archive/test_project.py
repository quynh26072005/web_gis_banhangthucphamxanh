#!/usr/bin/env python
"""
Script để test các chức năng cơ bản của project
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean_food_gis.settings')
django.setup()

from django.contrib.gis.geos import Point, Polygon
from food_store.models import Farm, Category, Product, DeliveryZone, Customer
from gis_tools.gis_functions import FarmLocationAnalyzer, DeliveryZoneManager, MapGenerator
from django.contrib.auth.models import User

def test_models():
    """Test tạo dữ liệu mẫu"""
    print("=== Testing Models ===")
    
    # Tạo danh mục
    category, created = Category.objects.get_or_create(
        name="Rau củ quả",
        defaults={
            'description': "Rau củ quả tươi sạch từ trang trại"
        }
    )
    print(f"Category: {category.name} ({'created' if created else 'exists'})")
    
    # Tạo trang trại
    farm, created = Farm.objects.get_or_create(
        name="Trang trại Xanh Đà Lạt",
        defaults={
            'address': "Đà Lạt, Lâm Đồng",
            'phone': "0123456789",
            'email': "dalat@farm.com",
            'description': "Trang trại rau sạch tại Đà Lạt",
            'location': Point(108.4583, 11.9404),  # Đà Lạt coordinates
            'organic_certified': True,
            'certification_number': "ORG001"
        }
    )
    print(f"Farm: {farm.name} ({'created' if created else 'exists'})")
    
    # Tạo sản phẩm
    product, created = Product.objects.get_or_create(
        name="Rau cải xanh Đà Lạt",
        defaults={
            'category': category,
            'farm': farm,
            'description': "Rau cải xanh tươi ngon từ Đà Lạt",
            'price': 35000,
            'unit': "kg",
            'stock_quantity': 50,
            'is_available': True
        }
    )
    print(f"Product: {product.name} ({'created' if created else 'exists'})")
    
    # Tạo khu vực giao hàng (TP.HCM)
    coords = [
        (106.6, 10.7),
        (106.8, 10.7),
        (106.8, 10.9),
        (106.6, 10.9),
        (106.6, 10.7)
    ]
    polygon = Polygon(coords)
    
    zone, created = DeliveryZone.objects.get_or_create(
        name="TP. Hồ Chí Minh",
        defaults={
            'area': polygon,
            'delivery_fee': 30000,
            'delivery_time': "1-2 ngày",
            'is_active': True
        }
    )
    print(f"Delivery Zone: {zone.name} ({'created' if created else 'exists'})")
    
    print("✅ Models test completed!\n")

def test_gis_functions():
    """Test các chức năng GIS"""
    print("=== Testing GIS Functions ===")
    
    # Test tìm trang trại gần nhất
    customer_location = Point(106.7, 10.8)  # TP.HCM
    farms = FarmLocationAnalyzer.find_nearest_farms(customer_location, max_distance_km=500)
    print(f"Found {farms.count()} farms near customer location")
    
    for farm in farms:
        distance = FarmLocationAnalyzer.calculate_farm_distance(
            farm.location, customer_location
        )
        print(f"  - {farm.name}: {distance} km")
    
    # Test kiểm tra giao hàng
    delivery_point = Point(106.7, 10.8)
    delivery_info = DeliveryZoneManager.check_delivery_availability(delivery_point)
    print(f"Delivery availability: {delivery_info}")
    
    # Test tạo bản đồ
    try:
        farms_map = MapGenerator.create_farms_map()
        print("✅ Farms map created successfully")
    except Exception as e:
        print(f"❌ Error creating farms map: {e}")
    
    try:
        zones_map = MapGenerator.create_delivery_zones_map()
        print("✅ Delivery zones map created successfully")
    except Exception as e:
        print(f"❌ Error creating delivery zones map: {e}")
    
    print("✅ GIS Functions test completed!\n")

def test_database_connection():
    """Test kết nối database"""
    print("=== Testing Database Connection ===")
    
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print("✅ Database connection successful")
        
        # Test GIS capabilities
        cursor.execute("SELECT PostGIS_Version()")
        postgis_version = cursor.fetchone()
        if postgis_version:
            print(f"✅ PostGIS version: {postgis_version[0]}")
        else:
            print("⚠️  PostGIS not available (using SpatiaLite?)")
            
    except Exception as e:
        print(f"❌ Database connection error: {e}")
    
    print("✅ Database test completed!\n")

def show_statistics():
    """Hiển thị thống kê dữ liệu"""
    print("=== Project Statistics ===")
    print(f"Categories: {Category.objects.count()}")
    print(f"Farms: {Farm.objects.count()}")
    print(f"Products: {Product.objects.count()}")
    print(f"Delivery Zones: {DeliveryZone.objects.count()}")
    print(f"Users: {User.objects.count()}")
    print(f"Customers: {Customer.objects.count()}")
    print()

def main():
    """Chạy tất cả tests"""
    print("🚀 Starting Clean Food GIS Project Tests\n")
    
    try:
        test_database_connection()
        test_models()
        test_gis_functions()
        show_statistics()
        
        print("🎉 All tests completed successfully!")
        print("\n📝 Next steps:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: http://localhost:8000/")
        print("3. Admin: http://localhost:8000/admin/")
        print("4. GIS Tools: http://localhost:8000/gis-tools/")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()