#!/usr/bin/env python
"""
Script tạo dữ liệu mẫu và superuser
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean_food_gis.settings')
django.setup()

from django.contrib.auth.models import User
from food_store.models import Farm, Category, Product, Customer

def create_superuser():
    """Tạo superuser"""
    print("🔐 Tạo superuser...")
    
    if User.objects.filter(username='admin').exists():
        print("⚠️  Superuser 'admin' đã tồn tại")
        return User.objects.get(username='admin')
    
    user = User.objects.create_superuser(
        username='admin',
        email='admin@cleanfood.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    print("✅ Đã tạo superuser: admin / admin123")
    return user

def create_sample_data():
    """Tạo dữ liệu mẫu"""
    print("📊 Tạo dữ liệu mẫu...")
    
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
    
    # Tạo trang trại
    farms_data = [
        {
            'name': 'Trang trại Xanh Đà Lạt',
            'address': 'Đà Lạt, Lâm Đồng',
            'phone': '0123456789',
            'email': 'dalat@farm.com',
            'description': 'Trang trại rau sạch tại Đà Lạt với khí hậu mát mẻ',
            'latitude': 11.9404,
            'longitude': 108.4583,
            'organic_certified': True,
            'certification_number': 'ORG001'
        },
        {
            'name': 'Trang trại Hữu cơ Cần Thơ',
            'address': 'Cần Thơ, Đồng bằng sông Cửu Long',
            'phone': '0987654321',
            'email': 'cantho@farm.com',
            'description': 'Trang trại trái cây nhiệt đới hữu cơ',
            'latitude': 10.0452,
            'longitude': 105.7469,
            'organic_certified': True,
            'certification_number': 'ORG002'
        },
        {
            'name': 'Trang trại Sạch Đồng Nai',
            'address': 'Đồng Nai',
            'phone': '0369852147',
            'email': 'dongnai@farm.com',
            'description': 'Trang trại chăn nuôi và trồng trọt sạch',
            'latitude': 10.9804,
            'longitude': 106.8468,
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
            print(f"✅ Tạo trang trại: {farm.name}")
    
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
            'name': 'Cà rót Đà Lạt',
            'category': 'Rau củ quả',
            'farm': 'Trang trại Xanh Đà Lạt',
            'description': 'Cà rót tím tươi ngon, không thuốc trừ sâu',
            'price': 45000,
            'unit': 'kg',
            'stock_quantity': 30,
            'nutritional_info': 'Chứa anthocyanin, chống oxy hóa'
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
            'name': 'Bưởi da xanh Cần Thơ',
            'category': 'Trái cây',
            'farm': 'Trang trại Hữu cơ Cần Thơ',
            'description': 'Bưởi da xanh ngọt mát, múi to',
            'price': 60000,
            'unit': 'kg',
            'stock_quantity': 40,
            'nutritional_info': 'Ít đường, nhiều vitamin C'
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

def main():
    """Chạy tất cả"""
    print("🚀 Bắt đầu tạo dữ liệu mẫu...\n")
    
    try:
        # Tạo superuser
        admin_user = create_superuser()
        
        # Tạo dữ liệu mẫu
        create_sample_data()
        
        # Tạo customer profile cho admin
        customer, created = Customer.objects.get_or_create(
            user=admin_user,
            defaults={
                'phone': '0123456789',
                'address': 'TP. Hồ Chí Minh',
                'latitude': 10.8231,
                'longitude': 106.6297
            }
        )
        if created:
            print("✅ Tạo customer profile cho admin")
        
        print("\n🎉 Hoàn tất tạo dữ liệu mẫu!")
        print("\n📝 Thông tin đăng nhập:")
        print("👤 Username: admin")
        print("🔑 Password: admin123")
        print("\n🚀 Bây giờ chạy: python manage.py runserver")
        print("🌐 Truy cập: http://localhost:8000/")
        print("⚙️  Admin: http://localhost:8000/admin/")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()