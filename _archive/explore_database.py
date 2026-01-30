#!/usr/bin/env python
"""
Script khám phá database qua Django ORM
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean_food_gis.settings')
django.setup()

from food_store.models import Farm, Category, Product, DeliveryZone, Customer
from django.contrib.auth.models import User

def explore_database():
    """Khám phá dữ liệu trong database"""
    print("🗄️  Khám phá Database Django GIS\n")
    
    # Users
    print("👥 USERS:")
    for user in User.objects.all():
        print(f"  - {user.username} ({user.email}) - Staff: {user.is_staff}")
    
    print(f"\n📂 CATEGORIES ({Category.objects.count()}):")
    for cat in Category.objects.all():
        print(f"  - {cat.name}: {cat.description}")
    
    print(f"\n🏡 FARMS ({Farm.objects.count()}):")
    for farm in Farm.objects.all():
        location_info = f"({farm.location.y:.4f}, {farm.location.x:.4f})" if farm.location else "No location"
        organic = "🌿 Hữu cơ" if farm.organic_certified else "🏠 Thông thường"
        print(f"  - {farm.name} {organic}")
        print(f"    📍 {farm.address} - {location_info}")
        print(f"    📞 {farm.phone}")
    
    print(f"\n🛒 PRODUCTS ({Product.objects.count()}):")
    for product in Product.objects.all():
        print(f"  - {product.name}")
        print(f"    💰 {product.price:,.0f}đ/{product.unit}")
        print(f"    🏡 {product.farm.name}")
        print(f"    📦 Kho: {product.stock_quantity}")
    
    print(f"\n🚚 DELIVERY ZONES ({DeliveryZone.objects.count()}):")
    for zone in DeliveryZone.objects.all():
        print(f"  - {zone.name}")
        print(f"    💰 Phí: {zone.delivery_fee:,.0f}đ")
        print(f"    ⏰ Thời gian: {zone.delivery_time}")
        print(f"    📍 Polygon: {zone.area.num_points} điểm")
    
    print(f"\n👤 CUSTOMERS ({Customer.objects.count()}):")
    for customer in Customer.objects.all():
        location_info = f"({customer.location.y:.4f}, {customer.location.x:.4f})" if customer.location else "No location"
        print(f"  - {customer.user.get_full_name() or customer.user.username}")
        print(f"    📞 {customer.phone}")
        print(f"    📍 {customer.address} - {location_info}")

def show_gis_info():
    """Hiển thị thông tin GIS"""
    print("\n🗺️  GIS INFORMATION:")
    
    # Trang trại có tọa độ
    farms_with_location = Farm.objects.filter(location__isnull=False)
    print(f"Trang trại có tọa độ: {farms_with_location.count()}/{Farm.objects.count()}")
    
    # Khu vực giao hàng
    zones_with_area = DeliveryZone.objects.filter(area__isnull=False)
    print(f"Khu vực có polygon: {zones_with_area.count()}/{DeliveryZone.objects.count()}")
    
    # Khách hàng có tọa độ
    customers_with_location = Customer.objects.filter(location__isnull=False)
    print(f"Khách hàng có tọa độ: {customers_with_location.count()}/{Customer.objects.count()}")

def show_database_stats():
    """Hiển thị thống kê database"""
    print("\n📊 DATABASE STATISTICS:")
    print(f"Total Users: {User.objects.count()}")
    print(f"Total Categories: {Category.objects.count()}")
    print(f"Total Farms: {Farm.objects.count()}")
    print(f"Total Products: {Product.objects.count()}")
    print(f"Total Delivery Zones: {DeliveryZone.objects.count()}")
    print(f"Total Customers: {Customer.objects.count()}")
    
    # Sản phẩm theo danh mục
    print("\nProducts by Category:")
    for cat in Category.objects.all():
        count = Product.objects.filter(category=cat).count()
        print(f"  - {cat.name}: {count} products")
    
    # Sản phẩm theo trang trại
    print("\nProducts by Farm:")
    for farm in Farm.objects.all():
        count = Product.objects.filter(farm=farm).count()
        print(f"  - {farm.name}: {count} products")

def main():
    """Chạy khám phá database"""
    try:
        explore_database()
        show_gis_info()
        show_database_stats()
        
        print("\n" + "="*50)
        print("🎯 Để xem chi tiết hơn:")
        print("1. Django Admin: http://localhost:8000/admin/")
        print("2. pgAdmin 4: Mở từ Start Menu")
        print("3. Django Shell: python manage.py shell")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()