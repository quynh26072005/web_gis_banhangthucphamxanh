#!/usr/bin/env python
"""
Script cài đặt GDAL với Conda
"""
import subprocess
import sys
import os

def run_command(command, description):
    """Chạy command và hiển thị kết quả"""
    print(f"🔄 {description}...")
    print(f"Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} thành công!")
            if result.stdout:
                print(f"Output: {result.stdout.strip()}")
        else:
            print(f"❌ {description} thất bại!")
            if result.stderr:
                print(f"Error: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Lỗi khi chạy command: {e}")
        return False

def check_conda():
    """Kiểm tra Conda có sẵn không"""
    print("🔍 Kiểm tra Conda...")
    return run_command("conda --version", "Kiểm tra Conda")

def create_conda_env():
    """Tạo conda environment cho dự án"""
    env_name = "clean_food_gis"
    print(f"🏗️  Tạo conda environment: {env_name}")
    
    # Kiểm tra environment đã tồn tại chưa
    result = subprocess.run(f"conda env list | findstr {env_name}", shell=True, capture_output=True, text=True)
    if env_name in result.stdout:
        print(f"⚠️  Environment {env_name} đã tồn tại")
        return True
    
    # Tạo environment mới
    return run_command(
        f"conda create -n {env_name} python=3.9 -y",
        f"Tạo environment {env_name}"
    )

def install_gdal_packages():
    """Cài đặt GDAL và các packages liên quan"""
    env_name = "clean_food_gis"
    
    packages = [
        "gdal",
        "geos", 
        "proj",
        "fiona",
        "shapely",
        "pyproj",
        "rasterio"
    ]
    
    print("📦 Cài đặt GDAL packages...")
    
    for package in packages:
        success = run_command(
            f"conda install -n {env_name} -c conda-forge {package} -y",
            f"Cài đặt {package}"
        )
        if not success:
            print(f"⚠️  Không thể cài {package}, tiếp tục...")

def install_django_packages():
    """Cài đặt Django và packages Python"""
    env_name = "clean_food_gis"
    
    packages = [
        "django=4.2.7",
        "psycopg2",
        "pillow",
        "folium",
        "geopy",
        "requests"
    ]
    
    print("🐍 Cài đặt Django packages...")
    
    # Activate environment và cài packages
    activate_cmd = f"conda activate {env_name} && "
    
    for package in packages:
        run_command(
            f"{activate_cmd}conda install {package} -y",
            f"Cài đặt {package}"
        )
    
    # Cài django-leaflet qua pip
    run_command(
        f"{activate_cmd}pip install django-leaflet",
        "Cài đặt django-leaflet"
    )

def test_installation():
    """Test GDAL installation"""
    env_name = "clean_food_gis"
    activate_cmd = f"conda activate {env_name} && "
    
    print("🧪 Test GDAL installation...")
    
    test_commands = [
        ("gdalinfo --version", "GDAL command line"),
        ("python -c \"from osgeo import gdal; print('GDAL version:', gdal.VersionInfo())\"", "Python GDAL"),
        ("python -c \"from django.contrib.gis.geos import Point; print('GEOS OK')\"", "Django GIS")
    ]
    
    for cmd, desc in test_commands:
        run_command(f"{activate_cmd}{cmd}", f"Test {desc}")

def create_activation_script():
    """Tạo script để activate environment"""
    script_content = f"""@echo off
echo Activating clean_food_gis conda environment...
call conda activate clean_food_gis
echo.
echo Environment activated! You can now run:
echo   python manage.py runserver
echo   python check_gdal.py
echo   python enable_gis_features.py
echo.
cmd /k
"""
    
    with open("activate_env.bat", "w") as f:
        f.write(script_content)
    
    print("✅ Đã tạo activate_env.bat")

def main():
    """Chạy tất cả bước cài đặt"""
    print("🚀 Cài đặt GDAL với Conda cho Django GIS\n")
    
    # Kiểm tra Conda
    if not check_conda():
        print("❌ Conda không có sẵn. Vui lòng cài đặt Anaconda/Miniconda trước.")
        return
    
    # Tạo environment
    if not create_conda_env():
        print("❌ Không thể tạo conda environment")
        return
    
    # Cài đặt GDAL packages
    install_gdal_packages()
    
    # Cài đặt Django packages
    install_django_packages()
    
    # Test installation
    test_installation()
    
    # Tạo activation script
    create_activation_script()
    
    print("\n🎉 Cài đặt hoàn tất!")
    print("\n📝 Các bước tiếp theo:")
    print("1. Chạy: activate_env.bat")
    print("2. Test: python check_gdal.py")
    print("3. Kích hoạt GIS: python enable_gis_features.py")
    print("4. Chạy server: python manage.py runserver")
    
    print("\n💡 Lưu ý:")
    print("- Luôn activate environment trước khi làm việc")
    print("- Environment name: clean_food_gis")
    print("- Để activate: conda activate clean_food_gis")

if __name__ == "__main__":
    main()