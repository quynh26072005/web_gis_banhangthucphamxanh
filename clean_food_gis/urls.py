"""
URL configuration for clean_food_gis project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Auth URLs (login, logout, password reset)
    path('', include('food_store.urls')),  # Main website URLs
    path('gis/', include('gis_tools.urls')),  # GIS tools URLs - Safe Mode enabled
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)