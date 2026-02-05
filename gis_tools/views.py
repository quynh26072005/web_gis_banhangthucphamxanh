"""
Views for GIS Tools
Modified for Non-GIS Environment (No GDAL)
"""
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test
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


def is_superuser(user):
    """Kiểm tra user có phải superuser không"""
    return user.is_authenticated and user.is_superuser


def gis_tools_home(request):
    """Trang chủ GIS Tools"""
    context = {
        'title': 'Công cụ GIS - Thực phẩm Sạch',
        'total_farms': Farm.objects.count(),
        'total_zones': DeliveryZone.objects.filter(is_active=True).count(),
        'total_orders': Order.objects.count(),
    }
    return render(request, 'gis/home.html', context)

def farms_map_view(request):
    """Hiển thị bản đồ cửa hàng"""
    farms_map = MapGenerator.create_farms_map()
    
    context = {
        'title': 'Bản đồ Cửa hàng',
        'map_html': farms_map._repr_html_(),
        'stores_count': Farm.objects.count()
    }
    return render(request, 'gis/farms_map.html', context)

def delivery_zones_map_view(request):
    """Hiển thị bản đồ khu vực giao hàng"""
    zones_map = MapGenerator.create_delivery_zones_map()
    
    context = {
        'title': 'Bản đồ Khu vực Giao hàng',
        'map_html': zones_map._repr_html_(),
        'zones_count': DeliveryZone.objects.filter(is_active=True).count()
    }
    return render(request, 'gis/delivery_zones_map.html', context)

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
        return render(request, 'gis/order_tracking.html', context)
    
    context = {
        'title': f'Theo dõi Đơn hàng #{order_id}',
        'order': order,
        'map_html': tracking_map._repr_html_()
    }
    return render(request, 'gis/order_tracking.html', context)

@user_passes_test(is_superuser)
def analytics_dashboard_view(request):
    """Dashboard phân tích dữ liệu GIS - Chỉ dành cho Admin"""
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
    return render(request, 'gis/analytics_dashboard.html', context)


def store_locator_view(request):
    """Tìm trang trại gần bạn"""
    context = {
        'title': 'Tìm trang trại gần bạn',
    }
    return render(request, 'gis/store_locator.html', context)

def route_planner_view(request):
    """Lập kế hoạch tuyến đường giao hàng"""
    context = {
        'title': 'Lập kế hoạch tuyến đường',
    }
    return render(request, 'gis/route_planner.html', context)

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
    return render(request, 'gis/farm_analysis.html', context)

# --- API Endpoints ---

@csrf_exempt
@require_http_methods(["GET", "POST"])
def find_nearest_farms_api(request):
    try:
        if request.method == "POST":
            data = json.loads(request.body)
            lat = float(data.get('latitude'))
            lng = float(data.get('longitude'))
            max_dist = int(data.get('max_distance', 99999))
            include_route = data.get('include_route', False)
            vehicle_type = data.get('vehicle_type', 'driving')
        else:
            lat = float(request.GET.get('lat', request.GET.get('latitude')))
            lng = float(request.GET.get('lon', request.GET.get('longitude')))
            max_dist = int(request.GET.get('max_distance', 99999))
            include_route = request.GET.get('include_route', 'false').lower() == 'true'
            vehicle_type = request.GET.get('vehicle_type', 'driving')
        
        # Tăng limit nếu không giới hạn khoảng cách
        limit = 50 if max_dist >= 99999 else 20
        
        # Tìm farms gần nhất theo đường bộ thực tế với vehicle type
        nearest = FarmLocationAnalyzer.find_nearest_farms_by_road(
            lat, lng, max_dist, limit, vehicle_type
        )
        
        results = []
        for farm in nearest:
            farm_data = {
                'id': farm.id,
                'name': farm.name,
                'address': farm.address,
                'phone': farm.phone,
                'distance_km': getattr(farm, 'distance_km', 0),
                'duration_min': getattr(farm, 'duration_min', 0),
                'latitude': farm.latitude,
                'longitude': farm.longitude,
                'organic_certified': farm.organic_certified,
                'product_count': farm.product_set.count(),
                'vehicle_type': getattr(farm, 'vehicle_type', vehicle_type)
            }
            
            # Chỉ thêm route geometry nếu yêu cầu, không tính phí ship
            if include_route and hasattr(farm, 'route_geometry'):
                farm_data['route_geometry'] = farm.route_geometry
            
            results.append(farm_data)
            
        return JsonResponse({
            'success': True, 
            'farms': results,
            'total_found': len(results),
            'search_radius_km': max_dist if max_dist < 99999 else 'unlimited',
            'vehicle_type': vehicle_type
        })
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

@csrf_exempt
@require_http_methods(["POST"])
def get_route_to_farm_api(request):
    """API lấy thông tin đường đi chi tiết đến một farm cụ thể"""
    try:
        data = json.loads(request.body)
        
        farm_id = int(data.get('farm_id'))
        customer_lat = float(data.get('customer_lat'))
        customer_lng = float(data.get('customer_lng'))
        vehicle_type = data.get('vehicle_type', 'driving')
        
        # Lấy thông tin farm
        try:
            farm = Farm.objects.get(id=farm_id)
        except Farm.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Farm không tồn tại'}, status=404)
        
        if not farm.latitude or not farm.longitude:
            return JsonResponse({'success': False, 'error': 'Farm chưa có tọa độ'}, status=400)
        
        # Tính toán route với vehicle type (không tính phí ship)
        from .routing import get_road_route
        
        # Lấy route với vehicle type
        route_info = get_road_route(
            farm.latitude, farm.longitude,
            customer_lat, customer_lng,
            vehicle_type=vehicle_type
        )
        
        if not route_info:
            return JsonResponse({'success': False, 'error': 'Không thể tính toán đường đi'}, status=400)
        
        # Lấy thông tin sản phẩm của farm
        products = farm.product_set.filter(is_available=True)[:5]  # Top 5 products
        product_list = []
        for product in products:
            product_list.append({
                'id': product.id,
                'name': product.name,
                'price': float(product.price),
                'unit': product.unit,
                'image_url': product.image.url if product.image else None
            })
        
        # Tên phương tiện tiếng Việt
        vehicle_names = {
            'driving': 'Ô tô',
            'car': 'Ô tô',
            'motorcycle': 'Xe máy',
            'motorbike': 'Xe máy',
            'bicycle': 'Xe đạp',
            'bike': 'Xe đạp',
            'foot': 'Đi bộ',
            'walking': 'Đi bộ'
        }
        
        result = {
            'success': True,
            'farm': {
                'id': farm.id,
                'name': farm.name,
                'address': farm.address,
                'phone': farm.phone,
                'latitude': farm.latitude,
                'longitude': farm.longitude,
                'organic_certified': farm.organic_certified,
                'certification_number': farm.certification_number
            },
            'route': {
                'distance_km': route_info['distance_km'],
                'duration_min': route_info['duration_min'],
                'geometry': route_info.get('geometry'),
                'vehicle_type': vehicle_type,
                'vehicle_name': vehicle_names.get(vehicle_type, vehicle_type),
                'waypoints': route_info.get('waypoints', [])
            },
            'products': product_list
        }
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

