#!/usr/bin/env python
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
