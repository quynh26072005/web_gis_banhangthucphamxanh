#!/usr/bin/env python
"""
Script setup PostgreSQL database với PostGIS
"""
import subprocess
import sys
import os

def run_psql_command(command, description, password="postgres"):
    """Chạy lệnh psql"""
    print(f"🔄 {description}...")
    
    # Tìm đường dẫn psql
    psql_paths = [
        r"C:\Program Files\PostgreSQL\18\bin\psql.exe",
        r"C:\Program Files\PostgreSQL\17\bin\psql.exe",
        r"C:\Program Files\PostgreSQL\16\bin\psql.exe",
        r"C:\Program Files\PostgreSQL\15\bin\psql.exe",
    ]
    
    psql_path = None
    for path in psql_paths:
        if os.path.exists(path):
            psql_path = path
            break
    
    if not psql_path:
        print("❌ Không tìm thấy psql.exe")
        return False
    
    try:
        # Set PGPASSWORD environment variable
        env = os.environ.copy()
        env['PGPASSWORD'] = password
        
        result = subprocess.run(
            [psql_path, "-U", "postgres", "-h", "localhost", "-c", command],
            capture_output=True,
            text=True,
            env=env
        )
        
        if result.returncode == 0:
            print(f"✅ {description} thành công!")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} thất bại!")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ Lỗi khi chạy psql: {e}")
        return False

def get_postgres_password():
    """Lấy password PostgreSQL từ user"""
    print("🔐 Cần password PostgreSQL để tạo database")
    print("Nếu bạn không nhớ password, thử các password phổ biến:")
    print("- postgres")
    print("- admin") 
    print("- 123456")
    print("- (để trống nếu không có password)")
    
    password = input("Nhập password PostgreSQL: ").strip()
    if not password:
        password = "postgres"  # Default
    
    return password

def create_database_and_postgis(password):
    """Tạo database và kích hoạt PostGIS"""
    
    # Kiểm tra database đã tồn tại chưa
    check_db = "SELECT 1 FROM pg_database WHERE datname='clean_food_gis_db'"
    
    # Tạo database
    create_db = "CREATE DATABASE clean_food_gis_db"
    
    # Kích hoạt PostGIS
    enable_postgis = "CREATE EXTENSION IF NOT EXISTS postgis"
    
    print("🗄️ Tạo database PostgreSQL...")
    
    # Kiểm tra kết nối
    if not run_psql_command("SELECT version()", "Kiểm tra kết nối PostgreSQL", password):
        return False
    
    # Tạo database (có thể thất bại nếu đã tồn tại)
    run_psql_command(create_db, "Tạo database clean_food_gis_db", password)
    
    # Kích hoạt PostGIS trên database mới
    psql_paths = [
        r"C:\Program Files\PostgreSQL\18\bin\psql.exe",
        r"C:\Program Files\PostgreSQL\17\bin\psql.exe",
        r"C:\Program Files\PostgreSQL\16\bin\psql.exe",
        r"C:\Program Files\PostgreSQL\15\bin\psql.exe",
    ]
    
    psql_path = None
    for path in psql_paths:
        if os.path.exists(path):
            psql_path = path
            break
    
    if psql_path:
        try:
            env = os.environ.copy()
            env['PGPASSWORD'] = password
            
            result = subprocess.run(
                [psql_path, "-U", "postgres", "-h", "localhost", "-d", "clean_food_gis_db", "-c", enable_postgis],
                capture_output=True,
                text=True,
                env=env
            )
            
            if result.returncode == 0:
                print("✅ PostGIS extension đã được kích hoạt!")
            else:
                print(f"⚠️  PostGIS có thể đã được kích hoạt: {result.stderr}")
                
        except Exception as e:
            print(f"⚠️  Lỗi khi kích hoạt PostGIS: {e}")
    
    return True

def update_django_settings(password):
    """Cập nhật password trong Django settings"""
    print("⚙️  Cập nhật Django settings...")
    
    settings_path = 'clean_food_gis/settings.py'
    
    try:
        with open(settings_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Thay thế password
        content = content.replace(
            "'PASSWORD': 'your_password_here',  # Cập nhật password PostgreSQL",
            f"'PASSWORD': '{password}',  # Password PostgreSQL"
        )
        
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Đã cập nhật password trong settings.py")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi cập nhật settings: {e}")
        return False

def main():
    """Chạy setup PostgreSQL"""
    print("🚀 Setup PostgreSQL Database cho Django GIS\n")
    
    # Lấy password
    password = get_postgres_password()
    
    # Tạo database và PostGIS
    if not create_database_and_postgis(password):
        print("❌ Không thể tạo database")
        return
    
    # Cập nhật Django settings
    if not update_django_settings(password):
        print("❌ Không thể cập nhật settings")
        return
    
    print("\n🎉 Setup PostgreSQL hoàn tất!")
    print("\n📝 Các bước tiếp theo:")
    print("1. Chạy: run_with_conda.bat")
    print("2. Test: python check_gdal.py")
    print("3. Migration: python migrate_to_gis.py")
    print("4. Chạy server: python manage.py runserver")
    
    print("\n💡 Thông tin database:")
    print(f"- Database: clean_food_gis_db")
    print(f"- User: postgres")
    print(f"- Password: {password}")
    print(f"- Host: localhost")
    print(f"- Port: 5432")

if __name__ == "__main__":
    main()