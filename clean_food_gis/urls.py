"""
URL configuration for clean_food_gis project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Admin analytics imports removed for minimal version
# from food_store.admin_analytics import admin_analytics_dashboard, admin_reports_view, admin_export_data

urlpatterns = [
    path('admin/', admin.site.urls),
    # Admin analytics URLs removed for minimal version
    # path('admin/analytics/', admin_analytics_dashboard, name='admin_analytics'),
    # path('admin/reports/', admin_reports_view, name='admin_reports'),
    # path('admin/export/', admin_export_data, name='admin_export'),
    path('accounts/', include('django.contrib.auth.urls')),  # Auth URLs (login, logout, password reset)
    path('', include('food_store.urls')),  # Main website URLs
    path('gis/', include('gis_tools.urls')),  # GIS tools URLs - Safe Mode enabled
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)