#!/usr/bin/env python
"""
Script tự động kích hoạt tính năng GIS
"""
import os
import shutil
import sys

def backup_current_files():
    """Backup các file hiện tại"""
    print("📦 Backup các file hiện tại...")
    
    # Backup models
    if os.path.exists('food_store/models.py'):
        shutil.copy('food_store/models.py', 'food_store/models_simple_backup.py')
        print("✅ Backup models.py")
    
    # Backup admin
    if os.path.exists('food_store/admin.py'):
        shutil.copy('food_store/admin.py', 'food_store/admin_simple_backup.py')
        print("✅ Backup admin.py")

def restore_gis_files():
    """Khôi phục các file GIS"""
    print("🔄 Khôi phục các file GIS...")
    
    # Restore GIS models
    if os.path.exists('food_store/models_gis_backup.py'):
        shutil.copy('food_store/models_gis_backup.py', 'food_store/models.py')
        print("✅ Khôi phục GIS models")
    
    # Restore GIS admin
    if os.path.exists('food_store/admin_gis_backup.py'):
        shutil.copy('food_store/admin_gis_backup.py', 'food_store/admin.py')
        print("✅ Khôi phục GIS admin")

def update_settings():
    """Cập nhật settings.py"""
    print("⚙️  Cập nhật settings.py...")
    
    settings_path = 'clean_food_gis/settings.py'
    
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Enable GIS apps
    content = content.replace(
        "# 'django.contrib.gis',  # Tạm thời bỏ GIS",
        "'django.contrib.gis',  # GIS support"
    )
    content = content.replace(
        "# 'leaflet',  # Tạm thời bỏ leaflet",
        "'leaflet',  # Leaflet maps"
    )
    
    # Enable PostGIS database
    content = content.replace(
        "# Database with SQLite (simple version without GIS)",
        "# Database with PostGIS support"
    )
    content = content.replace(
        "'ENGINE': 'django.db.backends.sqlite3',",
        "'ENGINE': 'django.contrib.gis.db.backends.postgis',"
    )
    content = content.replace(
        "'NAME': BASE_DIR / 'db.sqlite3',",
        """'NAME': 'clean_food_gis_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password_here',  # Cập nhật password PostgreSQL
        'HOST': 'localhost',
        'PORT': '5432',"""
    )
    
    with open(settings_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Đã cập nhật settings.py")

def update_urls():
    """Kích hoạt GIS tools URLs"""
    print("🔗 Kích hoạt GIS tools URLs...")
    
    urls_path = 'clean_food_gis/urls.py'
    
    with open(urls_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace(
        "# path('gis-tools/', include('gis_tools.urls')),  # Tạm thời bỏ GIS tools",
        "path('gis-tools/', include('gis_tools.urls')),  # GIS tools URLs"
    )
    
    with open(urls_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Đã kích hoạt GIS tools URLs")

def update_templates():
    """Kích hoạt GIS links trong templates"""
    print("🎨 Kích hoạt GIS links trong templates...")
    
    # Update base.html
    base_template = 'templates/base.html'
    with open(base_template, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Enable GIS dropdown menu
    content = content.replace(
        "<!-- GIS Tools tạm thời bị tắt -->",
        ""
    )
    content = content.replace(
        "<!-- <li class=\"nav-item dropdown\">",
        "<li class=\"nav-item dropdown\">"
    )
    content = content.replace(
        "</li> -->",
        "</li>"
    )
    
    with open(base_template, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Đã cập nhật base template")

def create_migration_script():
    """Tạo script migration cho GIS"""
    print("📝 Tạo script migration...")
    
    migration_script = """#!/usr/bin/env python
# Migration script for GIS features

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean_food_gis.settings')
django.setup()

from django.core.management import execute_from_command_line

print("🔄 Tạo migrations mới...")
execute_from_command_line(['manage.py', 'makemigrations'])

print("🔄 Chạy migrations...")
execute_from_command_line(['manage.py', 'migrate'])

print("✅ Migration hoàn tất!")
"""
    
    with open('migrate_to_gis.py', 'w', encoding='utf-8') as f:
        f.write(migration_script)
    
    print("✅ Đã tạo migrate_to_gis.py")

def main():
    """Chạy tất cả bước kích hoạt GIS"""
    print("🚀 Bắt đầu kích hoạt tính năng GIS...\n")
    
    try:
        backup_current_files()
        restore_gis_files()
        update_settings()
        update_urls()
        update_templates()
        create_migration_script()
        
        print("\n🎉 Đã kích hoạt tính năng GIS!")
        print("\n📝 Các bước tiếp theo:")
        print("1. Cập nhật password PostgreSQL trong clean_food_gis/settings.py")
        print("2. Chạy: python migrate_to_gis.py")
        print("3. Chạy: python manage.py runserver")
        print("4. Truy cập: http://localhost:8000/gis-tools/")
        
        print("\n⚠️  Lưu ý:")
        print("- Đảm bảo PostgreSQL đang chạy")
        print("- Đảm bảo database 'clean_food_gis_db' đã được tạo")
        print("- Đảm bảo PostGIS extension đã được kích hoạt")
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()