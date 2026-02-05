#!/usr/bin/env python
'''
Create sample data for Clean Food GIS
'''
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean_food_gis.settings')
django.setup()

from food_store.models import Farm, Category, Product, DeliveryZone

def create_sample_data():
    print("Creating sample data...")
    # Implementation here
    pass

if __name__ == '__main__':
    create_sample_data()
