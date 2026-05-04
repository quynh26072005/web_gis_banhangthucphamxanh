"""
URL configuration for clean_food_gis project.
KHÔNG SỬ DỤNG DJANGO ADMIN - Chỉ dùng Custom Admin Dashboard
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

# User Site URLs
urlpatterns = [
    # Other authentication URLs
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Main User Website (bao gồm Custom Admin Dashboard)
    path('', include('food_store.urls')),
    
    # GIS Tools
    path('gis/', include('gis_tools.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'clean_food_gis.views.custom_404_view'
handler403 = 'clean_food_gis.views.custom_403_view'
handler500 = 'clean_food_gis.views.custom_500_view'