"""
WSGI config for clean_food_gis project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean_food_gis.settings')

application = get_wsgi_application()