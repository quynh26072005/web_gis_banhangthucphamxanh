"""
Views for GIS Tools
Modified for Non-GIS Environment (No GDAL)
"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import folium

from .gis_functions import (
    FarmLocationAnalyzer, 
    DeliveryZoneManager, 
    MapGenerator, 
    GeocodingService,
    OrderAnalytics
)
from food_store.models import Farm, Order, DeliveryZone

def gis_tools_home(request):
    """Trang chủ GIS Tools"""
    context = {
        'title': 'Công cụ GIS - Thực phẩm Sạch',
        'total_farms': Farm.objects.count(),
        'total_zones': DeliveryZone.objects.filter(is_active=True).count(),
        'total_orders': Order.objects.count(),
    }
    return render(request, 'gis_tools/home.html', context)

def farms_map_view(request):
    """Hiển thị bản đồ trang trại"""
    farms_map = MapGenerator.create_farms_map()
    
    context = {
        'title': 'Bản đồ Trang trại',
        'map_html': farms_map._repr_html_(),
        'farms_count': Farm.objects.count()
    }
    return render(request, 'gis_tools/farms_map.html', context)

def delivery_zones_map_view(request):
    """Hiển thị bản đồ khu vực giao hàng"""
    zones_map = MapGenerator.create_delivery_zones_map()
    
    context = {
        'title': 'Bản đồ Khu vực Giao hàng',
        'map_html': zones_map._repr_html_(),
        'zones_count': DeliveryZone.objects.filter(is_active=True).count()
    }
    return render(request, 'gis_tools/delivery_zones_map.html', context)

def order_tracking_view(request, order_id):
    """Theo dõi đơn hàng trên bản đồ"""
    order = get_object_or_404(Order, pk=order_id)
    tracking_map = MapGenerator.create_order_tracking_map(order_id)
    
    if not tracking_map:
        context = {
            'title': 'Theo dõi Đơn hàng',
            'order': order,
            'error': 'Không thể tạo bản đồ (thiếu tọa độ)'
        }
        return render(request, 'gis_tools/order_tracking.html', context)
    
    context = {
        'title': f'Theo dõi Đơn hàng #{order_id}',
        'order': order,
        'map_html': tracking_map._repr_html_()
    }
    return render(request, 'gis_tools/order_tracking.html', context)

def analytics_dashboard_view(request):
    """Dashboard phân tích dữ liệu GIS"""
    orders_by_zone = OrderAnalytics.get_orders_by_zone()
    popular_farms = OrderAnalytics.get_popular_farms()[:10]
    
    # Tạo bản đồ nhiệt
    heatmap = MapGenerator.create_heatmap_map()
    
    context = {
        'title': 'Dashboard Phân tích GIS',
        'orders_by_zone': orders_by_zone,
        'popular_farms': popular_farms,
        'total_farms': Farm.objects.count(),
        'total_zones': DeliveryZone.objects.filter(is_active=True).count(),
        'total_orders': Order.objects.count(),
        'map_html': heatmap._repr_html_() if heatmap else None,
    }
    return render(request, 'gis_tools/analytics_dashboard.html', context)


def store_locator_view(request):
    """Tìm trang trại gần bạn"""
    context = {
        'title': 'Tìm trang trại gần bạn',
    }
    return render(request, 'gis_tools/store_locator.html', context)

def farm_analysis_view(request, farm_id):
    """Phân tích chi tiết một trang trại"""
    farm = get_object_or_404(Farm, pk=farm_id)
    products = farm.product_set.all()
    
    from django.db.models import Count, Sum
    order_stats = farm.product_set.aggregate(
        total_orders=Count('orderitem__order', distinct=True),
        total_products_sold=Sum('orderitem__quantity'),
        total_revenue=Sum('orderitem__price')
    )
    
    # Create mini map for this farm
    if farm.latitude and farm.longitude:
        m = folium.Map(location=[farm.latitude, farm.longitude], zoom_start=14)
        folium.Marker(
            location=[farm.latitude, farm.longitude],
            popup=farm.name,
            icon=folium.Icon(color='green', icon='leaf', prefix='fa')
        ).add_to(m)
        map_html = m._repr_html_()
    else:
        map_html = None
        
    context = {
        'title': f'Phân tích Trang trại: {farm.name}',
        'farm': farm,
        'products': products,
        'order_stats': order_stats,
        'map_html': map_html
    }
    return render(request, 'gis_tools/farm_analysis.html', context)

# --- API Endpoints ---

@csrf_exempt
@require_http_methods(["GET", "POST"])
def find_nearest_farms_api(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            lat = float(data.get('latitude'))
            lng = float(data.get('longitude'))
            max_dist = int(data.get('max_distance', 50))
        else:
            lat = float(request.GET.get('lat', request.GET.get('latitude')))
            lng = float(request.GET.get('lon', request.GET.get('longitude')))
            max_dist = int(request.GET.get('max_distance', 50))
        
        nearest = FarmLocationAnalyzer.find_nearest_farms(lat, lng, max_dist)
        
        results = []
        for farm in nearest:
            results.append({
                'id': farm.id,
                'name': farm.name,
                'address': farm.address,
                'distance_km': getattr(farm, 'distance_km', 0),
                'latitude': farm.latitude,
                'longitude': farm.longitude
            })
            
        return JsonResponse({'success': True, 'farms': results})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def check_delivery_availability_api(request):
    try:
        data = json.loads(request.body)
        lat = float(data.get('latitude'))
        lng = float(data.get('longitude'))
        
        result = DeliveryZoneManager.check_delivery_availability(lat, lng)
        return JsonResponse({'success': True, 'delivery_info': result})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def geocode_address_api(request):
    # Mock geocode
    return JsonResponse({
        'success': True, 
        'coordinates': {'latitude': 10.762622, 'longitude': 106.660172}
    })

def delivery_zones_geojson_api(request):
    data = DeliveryZoneManager.get_all_delivery_zones_geojson()
    return JsonResponse(data)