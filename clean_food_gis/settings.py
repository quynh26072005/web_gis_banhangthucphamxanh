"""
Django settings for clean_food_gis project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.gis',  # GIS support - disabled (Safe Mode)
    # 'leaflet',  # Leaflet maps - disabled (Safe Mode)
    
    # Custom apps
    'food_store',  # Main app for food store
    'gis_tools',   # GIS tools (Safe Mode enabled)
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'clean_food_gis.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'clean_food_gis.wsgi.application'

# GDAL Configuration (Optional/Ignored in Safe Mode)
import os
if os.name == 'nt':  # Windows
    GDAL_LIBRARY_PATH = r'C:\Users\Quynh\miniconda3\envs\clean_food_gis\Library\bin\gdal.dll'
    GEOS_LIBRARY_PATH = r'C:\Users\Quynh\miniconda3\envs\clean_food_gis\Library\bin\geos_c.dll'

# Database Configuration - PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'web_gis',
        'USER': 'postgres',
        'PASSWORD': '1',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'vi-vn'
TIME_ZONE = 'Asia/Ho_Chi_Minh'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Leaflet configuration
LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (10.8231, 106.6297),  # Ho Chi Minh City coordinates
    'DEFAULT_ZOOM': 10,
    'MIN_ZOOM': 3,
    'MAX_ZOOM': 18,
    'TILES': [
        ('OpenStreetMap', 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            'attribution': '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }),
    ],
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# Auth redirects
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'