#!/usr/bin/env python
"""
Kiểm tra GDAL đã được cài đặt chưa
"""

def check_gdal():
    """Kiểm tra GDAL"""
    print("🔍 Kiểm tra GDAL...")
    
    try:
        from osgeo import gdal
        print(f"✅ GDAL version: {gdal.VersionInfo()}")
        return True
    except ImportError:
        print("❌ GDAL chưa được cài đặt")
        return False

def check_geos():
    """Kiểm tra GEOS"""
    print("🔍 Kiểm tra GEOS...")
    
    try:
        from django.contrib.gis.geos import Point
        test_point = Point(106.6297, 10.8231)
        print(f"✅ GEOS hoạt động: {test_point}")
        return True
    except Exception as e:
        print(f"❌ GEOS lỗi: {e}")
        return False

def check_django_gis():
    """Kiểm tra Django GIS"""
    print("🔍 Kiểm tra Django GIS...")
    
    try:
        import django
        django.setup()
        from django.contrib.gis.db import models
        print("✅ Django GIS sẵn sàng")
        return True
    except Exception as e:
        print(f"❌ Django GIS lỗi: {e}")
        return False

def main():
    print("🚀 Kiểm tra các thành phần GIS...\n")
    
    gdal_ok = check_gdal()
    geos_ok = check_geos()
    django_gis_ok = check_django_gis()
    
    print("\n📊 Kết quả:")
    print(f"GDAL: {'✅' if gdal_ok else '❌'}")
    print(f"GEOS: {'✅' if geos_ok else '❌'}")
    print(f"Django GIS: {'✅' if django_gis_ok else '❌'}")
    
    if all([gdal_ok, geos_ok, django_gis_ok]):
        print("\n🎉 Tất cả thành phần GIS đã sẵn sàng!")
        print("Có thể chạy: python enable_gis_features.py")
    else:
        print("\n⚠️  Cần cài đặt thêm:")
        if not gdal_ok:
            print("- Cài đặt GDAL từ OSGeo4W")
        if not geos_ok:
            print("- Kiểm tra GEOS installation")
        if not django_gis_ok:
            print("- Kiểm tra Django GIS setup")

if __name__ == "__main__":
    main()