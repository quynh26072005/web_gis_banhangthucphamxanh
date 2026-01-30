"""
GIS Tools and Functions for Clean Food Store
Các công cụ xử lý GIS cho website bán thực phẩm sạch
Modified for Non-GIS Environment (No GDAL required)
"""

import math
from food_store.models import Farm, DeliveryZone, Order
import folium
from folium import plugins
import json

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two points using Haversine formula
    Returns distance in km
    """
    R = 6371  # Earth radius in km
    
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    
    a = math.sin(dLat/2) * math.sin(dLat/2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dLon/2) * math.sin(dLon/2)
        
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    
    return round(d, 2)


class FarmLocationAnalyzer:
    """
    Công cụ phân tích vị trí trang trại
    Tính toán khoảng cách, tìm trang trại gần nhất
    """
    
    @staticmethod
    def find_nearest_farms(latitude, longitude, max_distance_km=50, limit=10):
        """
        Tìm các trang trại gần nhất từ vị trí khách hàng
        Args:
            latitude: Vĩ độ khách hàng
            longitude: Kinh độ khách hàng
            max_distance_km: Khoảng cách tối đa (km)
            limit: Số lượng trang trại tối đa trả về
        """
        all_farms = Farm.objects.all()
        nearest_farms = []
        
        for farm in all_farms:
            if farm.latitude is not None and farm.longitude is not None:
                dist = calculate_distance(latitude, longitude, farm.latitude, farm.longitude)
                if dist <= max_distance_km:
                    # Attach distance to farm object temporarily
                    farm.distance_km = dist 
                    nearest_farms.append(farm)
        
        # Sort by distance
        nearest_farms.sort(key=lambda x: x.distance_km)
        
        return nearest_farms[:limit]
    
    @staticmethod
    def calculate_farm_distance(farm_location, customer_location):
        """
        Tính khoảng cách giữa trang trại và khách hàng
        Args:
            farm_location: Tuple (lat, lng) hoặc object có .y, .x
            customer_location: Tuple (lat, lng) hoặc object có .y, .x
        """
        # Handle tuple inputs
        lat1, lon1 = farm_location if isinstance(farm_location, (tuple, list)) else (getattr(farm_location, 'latitude', 0), getattr(farm_location, 'longitude', 0))
        lat2, lon2 = customer_location if isinstance(customer_location, (tuple, list)) else (getattr(customer_location, 'latitude', 0), getattr(customer_location, 'longitude', 0))
        
        return calculate_distance(lat1, lon1, lat2, lon2)


class DeliveryZoneManager:
    """
    Quản lý khu vực giao hàng
    """
    
    @staticmethod
    def check_delivery_availability(latitude, longitude):
        """
        Kiểm tra khả năng giao hàng (Simple approximation)
        """
        # Giả lập: TP.HCM center
        hcm_lat, hcm_lng = 10.762622, 106.660172
        dist = calculate_distance(latitude, longitude, hcm_lat, hcm_lng)
        
        if dist < 20:  # 20km radius from HCM center
            return {
                'can_deliver': True,
                'zone_name': 'TP. Hồ Chí Minh',
                'delivery_fee': 30000,
                'delivery_time': '1-2 ngày'
            }
        
        return {
            'can_deliver': False,
            'zone_name': None,
            'delivery_fee': 0,
            'delivery_time': 'Không giao hàng đến khu vực này'
        }
    
    @staticmethod
    def get_all_delivery_zones_geojson():
        """
        Tạo GeoJSON giả lập cho delivery zones vì không có PolygonField
        """
        zones = DeliveryZone.objects.filter(is_active=True)
        features = []
        
        # Define some static polygons for demo
        demo_polygons = {
            'TP. Hồ Chí Minh': [[
                [106.55, 10.65], [106.85, 10.65], 
                [106.85, 10.95], [106.55, 10.95], [106.55, 10.65]
            ]],
            'Hà Nội': [[
                [105.75, 20.95], [105.95, 20.95], 
                [105.95, 21.15], [105.75, 21.15], [105.75, 20.95]
            ]]
        }
        
        for zone in zones:
            coordinates = demo_polygons.get(zone.name, [])
            if not coordinates:
                # Default box
                coordinates = [[
                    [106.0, 10.0], [107.0, 10.0], 
                    [107.0, 11.0], [106.0, 11.0], [106.0, 10.0]
                ]]
                
            feature = {
                'type': 'Feature',
                'properties': {
                    'name': zone.name,
                    'delivery_fee': float(zone.delivery_fee),
                    'delivery_time': zone.delivery_time
                },
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': coordinates
                }
            }
            features.append(feature)
        
        return {
            'type': 'FeatureCollection',
            'features': features
        }


class MapGenerator:
    """Tạo bản đồ tương tác với Folium"""
    
    @staticmethod
    def create_farms_map(center_lat=10.8231, center_lng=106.6297, zoom=10):
        # Tạo bản đồ cơ bản
        m = folium.Map(
            location=[center_lat, center_lng],
            zoom_start=zoom,
            tiles='OpenStreetMap'
        )
        
        # Thêm các trang trại lên bản đồ
        farms = Farm.objects.all()
        for farm in farms:
            if farm.latitude and farm.longitude:
                # Icon khác nhau cho trang trại có chứng nhận hữu cơ
                icon_color = 'green' if farm.organic_certified else 'blue'
                icon = 'leaf' if farm.organic_certified else 'home'
                
                popup_html = f"""
                <div style="width: 200px;">
                    <h4>{farm.name}</h4>
                    <p><strong>Địa chỉ:</strong> {farm.address}</p>
                    <p><strong>Điện thoại:</strong> {farm.phone}</p>
                    <p><strong>Chứng nhận hữu cơ:</strong> {'Có' if farm.organic_certified else 'Không'}</p>
                    <p>{farm.description[:100]}...</p>
                </div>
                """
                
                folium.Marker(
                    location=[farm.latitude, farm.longitude],
                    popup=folium.Popup(popup_html, max_width=250),
                    tooltip=farm.name,
                    icon=folium.Icon(color=icon_color, icon=icon, prefix='fa')
                ).add_to(m)
        
        return m
    
    @staticmethod
    def create_delivery_zones_map(center_lat=10.8231, center_lng=106.6297, zoom=10):
        m = folium.Map(
            location=[center_lat, center_lng],
            zoom_start=zoom,
            tiles='OpenStreetMap'
        )
        
        zones_data = DeliveryZoneManager.get_all_delivery_zones_geojson()
        colors = ['red', 'blue', 'green', 'purple', 'orange']
        
        for i, feature in enumerate(zones_data['features']):
            coords = feature['geometry']['coordinates'][0]
            # Folium needs Lat, Lng - GeoJSON is Lng, Lat
            folium_coords = [[c[1], c[0]] for c in coords]
            props = feature['properties']
            
            color = colors[i % len(colors)]
            
            popup_html = f"""
            <div>
                <h4>{props['name']}</h4>
                <p><strong>Phí:</strong> {props['delivery_fee']:,.0f} VNĐ</p>
                <p><strong>Thời gian:</strong> {props['delivery_time']}</p>
            </div>
            """
            
            folium.Polygon(
                locations=folium_coords,
                popup=folium.Popup(popup_html, max_width=200),
                tooltip=props['name'],
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.3
            ).add_to(m)
        
        return m
    
    @staticmethod
    def create_heatmap_map():
        """Tạo bản đồ nhiệt mật độ đơn hàng"""
        farms = Farm.objects.all()
        center_lat = 10.8231
        center_lng = 106.6297
        
        if farms.exists():
            center_lat = sum(f.latitude for f in farms) / farms.count()
            center_lng = sum(f.longitude for f in farms) / farms.count()
            
        m = folium.Map(location=[center_lat, center_lng], zoom_start=11)
        
        # Lấy dữ liệu đơn hàng
        orders = Order.objects.filter(delivery_latitude__isnull=False, delivery_longitude__isnull=False)
        heat_data = [[o.delivery_latitude, o.delivery_longitude, 1] for o in orders]
        
        if heat_data:
            plugins.HeatMap(heat_data).add_to(m)
            
        return m
    
    @staticmethod
    def create_order_tracking_map(order_id):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return None
        
        if not (order.delivery_latitude and order.delivery_longitude):
            return None
            
        m = folium.Map(
            location=[order.delivery_latitude, order.delivery_longitude],
            zoom_start=12
        )
        
        # Customer Location
        folium.Marker(
            location=[order.delivery_latitude, order.delivery_longitude],
            popup=order.delivery_address,
            icon=folium.Icon(color='red', icon='home', prefix='fa')
        ).add_to(m)
        
        # Farm Locations
        for item in order.items.all():
            farm = item.product.farm
            if farm.latitude and farm.longitude:
                folium.Marker(
                    location=[farm.latitude, farm.longitude],
                    popup=farm.name,
                    icon=folium.Icon(color='green', icon='leaf', prefix='fa')
                ).add_to(m)
                
                # AntPath - Đường đi động
                plugins.AntPath(
                    locations=[
                        [farm.latitude, farm.longitude],
                        [order.delivery_latitude, order.delivery_longitude]
                    ],
                    dash_array=[10, 20],
                    delay=1000,
                    color='blue',
                    pulse_color='white',
                    weight=5,
                    opacity=0.8
                ).add_to(m)
        
        return m

    @staticmethod
    def create_single_farm_map(farm):
        """Tạo bản đồ cho một trang trại duy nhất"""
        if not farm or not farm.latitude or not farm.longitude:
            return None
            
        m = folium.Map(
            location=[farm.latitude, farm.longitude],
            zoom_start=15,
            tiles='OpenStreetMap'
        )
        
        icon_color = 'green' if farm.organic_certified else 'blue'
        icon = 'leaf' if farm.organic_certified else 'home'
        
        folium.Marker(
            location=[farm.latitude, farm.longitude],
            tooltip=farm.name,
            icon=folium.Icon(color=icon_color, icon=icon, prefix='fa')
        ).add_to(m)
        
        return m


class GeocodingService:
    """Mock geocoding service using OpenStreetMap via Geopy if available, else requests"""
    def address_to_coordinates(self, address):
        # Mock implementation for demo
        if "HCM" in address or "Hồ Chí Minh" in address:
            return 10.762622, 106.660172
        return 21.028511, 105.854164 # Hanoi default

class OrderAnalytics:
    """
    Phân tích đơn hàng theo địa lý
    Thống kê theo khu vực, trang trại
    """
    
    @staticmethod
    def get_orders_by_zone():
        """
        Thống kê đơn hàng theo khu vực giao hàng
        Returns: Dict với thống kê theo zone
        """
        zones_stats = {}
        zones = DeliveryZone.objects.filter(is_active=True)
        
        for zone in zones:
            orders = Order.objects.filter(delivery_zone=zone)
            total_orders = orders.count()
            total_revenue = sum(order.total_amount for order in orders)
            
            zones_stats[zone.name] = {
                'total_orders': total_orders,
                'total_revenue': float(total_revenue),
                'average_order_value': float(total_revenue / total_orders) if total_orders > 0 else 0
            }
        
        return zones_stats
    
    @staticmethod
    def get_popular_farms():
        """
        Thống kê trang trại phổ biến nhất
        Returns: List các trang trại được đặt hàng nhiều nhất
        """
        from django.db.models import Count, Sum
        
        farms_stats = Farm.objects.annotate(
            total_orders=Count('product__orderitem__order', distinct=True),
            total_products_sold=Sum('product__orderitem__quantity')
        ).filter(total_orders__gt=0).order_by('-total_orders')
        
        return farms_stats