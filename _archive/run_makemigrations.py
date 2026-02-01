#!/usr/bin/env python
"""
Script chạy makemigrations
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean_food_gis.settings')

def main():
    print("🔄 Tạo migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        print("✅ Makemigrations hoàn tất!")
    except Exception as e:
        print(f"❌ Lỗi makemigrations: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()