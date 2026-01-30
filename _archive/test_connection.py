#!/usr/bin/env python
"""
Test PostgreSQL + PostGIS connection
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean_food_gis.settings')
django.setup()

def test_connection():
    print("🔍 Testing PostgreSQL + PostGIS connection...")
    
    try:
        from django.db import connection
        cursor = connection.cursor()
        
        # Test basic connection
        cursor.execute("SELECT version()")
        pg_version = cursor.fetchone()[0]
        print(f"✅ PostgreSQL connected: {pg_version}")
        
        # Test PostGIS
        cursor.execute("SELECT PostGIS_Version()")
        postgis_version = cursor.fetchone()[0]
        print(f"✅ PostGIS available: {postgis_version}")
        
        # Test GIS functionality
        from django.contrib.gis.geos import Point
        test_point = Point(106.6297, 10.8231)  # Ho Chi Minh City
        print(f"✅ GIS Point created: {test_point}")
        
        print("\n🎉 All tests passed! Ready to run the project.")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check PostgreSQL is running")
        print("2. Verify password in settings.py")
        print("3. Ensure PostGIS extension is installed")
        return False

if __name__ == "__main__":
    test_connection()