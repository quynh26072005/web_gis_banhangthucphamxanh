"""
URL configuration for GIS Tools
"""
from django.urls import path
from . import views

app_name = 'gis_tools'

urlpatterns = [
    # Main GIS tools pages
    path('', views.gis_tools_home, name='home'),
    path('farms-map/', views.farms_map_view, name='farms_map'),
    path('delivery-zones-map/', views.delivery_zones_map_view, name='delivery_zones_map'),
    path('order-tracking/<int:order_id>/', views.order_tracking_view, name='order_tracking'),
    path('analytics/', views.analytics_dashboard_view, name='analytics_dashboard'),
    path('farm-analysis/<int:farm_id>/', views.farm_analysis_view, name='farm_analysis'),
    path('store-locator/', views.store_locator_view, name='store_locator'),
    
    # API endpoints
    path('api/find-nearest-farms/', views.find_nearest_farms_api, name='find_nearest_farms_api'),
    path('api/check-delivery/', views.check_delivery_availability_api, name='check_delivery_api'),
    path('api/geocode/', views.geocode_address_api, name='geocode_api'),
    path('api/delivery-zones-geojson/', views.delivery_zones_geojson_api, name='delivery_zones_geojson'),
]