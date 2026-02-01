#!/usr/bin/env python
"""
Script tạo dữ liệu GIS mẫu
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean_food_gis.settings')
django.setup()

from django.contrib.gis.geos import Point, Polygon
from django.contrib.auth.models import User
from food_store.models import Farm, Category, Product, DeliveryZone, Customer

def create_gis_sample_data():
    """Tạo dữ liệu GIS mẫu"""
    print("🗺️  Tạo dữ liệu GIS mẫu...")
    
    # Tạo danh mục
    categories_data = [
        {'name': 'Rau củ quả', 'description': 'Rau củ quả tươi sạch từ trang trại'},
        {'name': 'Trái cây', 'description': 'Trái cây tươi ngon, không thuốc trừ sâu'},
        {'name': 'Thịt sạch', 'description': 'Thịt từ trang trại chăn nuôi sạch'},
        {'name': 'Sữa & Trứng', 'description': 'Sữa tươi và trứng từ trang trại'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"✅ Tạo danh mục: {category.name}")
    
    # Tạo trang trại với GIS location
    farms_data = [
        {
            'name': 'Trang trại Xanh Đà Lạt',
            'address': 'Đà Lạt, Lâm Đồng',
            'phone': '0123456789',
            'email': 'dalat@farm.com',
            'description': 'Trang trại rau sạch tại Đà Lạt với khí hậu mát mẻ',
            'location': Point(108.4583, 11.9404),  # Đà Lạt coordinates
            'organic_certified': True,
            'certification_number': 'ORG001'
        },
        {
            'name': 'Trang trại Hữu cơ Cần Thơ',
            'address': 'Cần Thơ, Đồng bằng sông Cửu Long',
            'phone': '0987654321',
            'email': 'cantho@farm.com',
            'description': 'Trang trại trái cây nhiệt đới hữu cơ',
            'location': Point(105.7469, 10.0452),  # Cần Thơ coordinates
            'organic_certified': True,
            'certification_number': 'ORG002'
        },
        {
            'name': 'Trang trại Sạch Đồng Nai',
            'address': 'Đồng Nai',
            'phone': '0369852147',
            'email': 'dongnai@farm.com',
            'description': 'Trang trại chăn nuôi và trồng trọt sạch',
            'location': Point(106.8468, 10.9804),  # Đồng Nai coordinates
            'organic_certified': False,
            'certification_number': ''
        }
    ]
    
    for farm_data in farms_data:
        farm, created = Farm.objects.get_or_create(
            name=farm_data['name'],
            defaults=farm_data
        )
        if created:
            print(f"✅ Tạo trang trại GIS: {farm.name}")
        else:
            print(f"🔄 Cập nhật trang trại: {farm.name}")
    
    # Tạo sản phẩm
    products_data = [
        {
            'name': 'Rau cải xanh Đà Lạt',
            'category': 'Rau củ quả',
            'farm': 'Trang trại Xanh Đà Lạt',
            'description': 'Rau cải xanh tươi ngon từ Đà Lạt, giàu vitamin',
            'price': 35000,
            'unit': 'kg',
            'stock_quantity': 50,
            'nutritional_info': 'Giàu vitamin A, C, K và chất xơ'
        },
        {
            'name': 'Xoài cát Cần Thơ',
            'category': 'Trái cây',
            'farm': 'Trang trại Hữu cơ Cần Thơ',
            'description': 'Xoài cát ngọt thơm, hữu cơ 100%',
            'price': 80000,
            'unit': 'kg',
            'stock_quantity': 25,
            'nutritional_info': 'Giàu vitamin C, beta-carotene'
        },
        {
            'name': 'Thịt heo sạch',
            'category': 'Thịt sạch',
            'farm': 'Trang trại Sạch Đồng Nai',
            'description': 'Thịt heo từ trang trại chăn nuôi sạch',
            'price': 180000,
            'unit': 'kg',
            'stock_quantity': 15,
            'nutritional_info': 'Protein cao, ít mỡ'
        }
    ]
    
    for prod_data in products_data:
        try:
            category = Category.objects.get(name=prod_data['category'])
            farm = Farm.objects.get(name=prod_data['farm'])
            
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    'category': category,
                    'farm': farm,
                    'description': prod_data['description'],
                    'price': prod_data['price'],
                    'unit': prod_data['unit'],
                    'stock_quantity': prod_data['stock_quantity'],
                    'nutritional_info': prod_data['nutritional_info'],
                    'is_available': True
                }
            )
            if created:
                print(f"✅ Tạo sản phẩm: {product.name}")
        except Exception as e:
            print(f"❌ Lỗi tạo sản phẩm {prod_data['name']}: {e}")
    
    # Tạo khu vực giao hàng với polygon
    delivery_zones = [
        {
            'name': 'TP. Hồ Chí Minh',
            'coords': [
                (106.6, 10.7),
                (106.8, 10.7),
                (106.8, 10.9),
                (106.6, 10.9),
                (106.6, 10.7)
            ],
            'delivery_fee': 30000,
            'delivery_time': '1-2 ngày'
        },
        {
            'name': 'Hà Nội',
            'coords': [
                (105.8, 21.0),
                (105.9, 21.0),
                (105.9, 21.1),
                (105.8, 21.1),
                (105.8, 21.0)
            ],
            'delivery_fee': 35000,
            'delivery_time': '2-3 ngày'
        }
    ]
    
    for zone_data in delivery_zones:
        polygon = Polygon(zone_data['coords'])
        
        zone, created = DeliveryZone.objects.get_or_create(
            name=zone_data['name'],
            defaults={
                'area': polygon,
                'delivery_fee': zone_data['delivery_fee'],
                'delivery_time': zone_data['delivery_time'],
                'is_active': True
            }
        )
        if created:
            print(f"✅ Tạo khu vực giao hàng: {zone.name}")
    
    # Tạo customer với location
    try:
        admin_user = User.objects.get(username='admin')
        customer, created = Customer.objects.get_or_create(
            user=admin_user,
            defaults={
                'phone': '0123456789',
                'address': 'TP. Hồ Chí Minh',
                'location': Point(106.6297, 10.8231)  # TP.HCM center
            }
        )
        if created:
            print("✅ Tạo customer GIS profile cho admin")
    except User.DoesNotExist:
        print("⚠️  Admin user không tồn tại")

def main():
    """Chạy tạo dữ liệu GIS"""
    print("🚀 Tạo dữ liệu GIS mẫu cho Django project\n")
    
    try:
        create_gis_sample_data()
        
        print("\n🎉 Tạo dữ liệu GIS hoàn tất!")
        print("\n📊 Dữ liệu đã tạo:")
        print(f"- Danh mục: {Category.objects.count()}")
        print(f"- Trang trại: {Farm.objects.count()}")
        print(f"- Sản phẩm: {Product.objects.count()}")
        print(f"- Khu vực giao hàng: {DeliveryZone.objects.count()}")
        print(f"- Khách hàng: {Customer.objects.count()}")
        
        print("\n🌐 Bây giờ có thể:")
        print("1. Chạy server: python manage.py runserver")
        print("2. Truy cập: http://localhost:8000/")
        print("3. GIS Tools: http://localhost:8000/gis-tools/")
        print("4. Admin: http://localhost:8000/admin/ (admin/admin123)")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()