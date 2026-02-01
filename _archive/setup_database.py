#!/usr/bin/env python
"""
Script để setup PostgreSQL database cho dự án
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

def create_database():
    """Tạo database và kích hoạt PostGIS"""
    
    # Thông tin kết nối (sử dụng database mặc định 'postgres')
    print("🔍 Đang kết nối PostgreSQL...")
    
    # Bạn cần nhập password PostgreSQL của mình ở đây
    PASSWORD = input("Nhập password PostgreSQL của bạn: ")
    
    try:
        # Kết nối đến PostgreSQL server
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            user="postgres",
            password=PASSWORD,
            database="postgres"  # Kết nối đến database mặc định
        )
        
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print("✅ Kết nối PostgreSQL thành công!")
        
        # Kiểm tra database đã tồn tại chưa
        cursor.execute("SELECT 1 FROM pg_database WHERE datname='clean_food_gis_db'")
        exists = cursor.fetchone()
        
        if exists:
            print("⚠️  Database 'clean_food_gis_db' đã tồn tại")
        else:
            # Tạo database mới
            cursor.execute("CREATE DATABASE clean_food_gis_db")
            print("✅ Đã tạo database 'clean_food_gis_db'")
        
        cursor.close()
        conn.close()
        
        # Kết nối đến database mới để kích hoạt PostGIS
        print("🔧 Đang kích hoạt PostGIS extension...")
        
        conn = psycopg2.connect(
            host="localhost",
            port="5432", 
            user="postgres",
            password=PASSWORD,
            database="clean_food_gis_db"
        )
        
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Kích hoạt PostGIS extension
        try:
            cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis")
            print("✅ PostGIS extension đã được kích hoạt")
        except Exception as e:
            print(f"⚠️  Lỗi khi kích hoạt PostGIS: {e}")
        
        # Kiểm tra PostGIS version
        try:
            cursor.execute("SELECT PostGIS_Version()")
            version = cursor.fetchone()[0]
            print(f"✅ PostGIS version: {version}")
        except Exception as e:
            print(f"❌ PostGIS không hoạt động: {e}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Database setup hoàn tất!")
        print("📝 Bây giờ hãy cập nhật password trong clean_food_gis/settings.py")
        print(f"   Thay 'your_password_here' bằng '{PASSWORD}'")
        
        return PASSWORD
        
    except psycopg2.Error as e:
        print(f"❌ Lỗi PostgreSQL: {e}")
        print("\n🔧 Kiểm tra:")
        print("1. PostgreSQL service đang chạy")
        print("2. Password đúng")
        print("3. User 'postgres' tồn tại")
        return None
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        return None

if __name__ == "__main__":
    password = create_database()
    
    if password:
        print(f"\n🚀 Tiếp theo, chạy:")
        print("1. Cập nhật password trong settings.py")
        print("2. pip install -r requirements.txt")
        print("3. python manage.py makemigrations")
        print("4. python manage.py migrate")
        print("5. python manage.py createsuperuser")
        print("6. python manage.py runserver")