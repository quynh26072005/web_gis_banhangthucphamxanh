"""
ASGI config for clean_food_gis project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean_food_gis.settings')

application = get_asgi_application()