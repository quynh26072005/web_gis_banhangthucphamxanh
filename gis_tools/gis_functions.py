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
    Công cụ phân tích vị trí cửa hàng
    Tính toán khoảng cách, tìm cửa hàng gần nhất
    """
    
    @staticmethod
    def find_nearest_farms(latitude, longitude, max_distance_km=99999, limit=50):
        """
        Tìm các cửa hàng gần nhất từ vị trí khách hàng
        Args:
            latitude: Vĩ độ khách hàng
            longitude: Kinh độ khách hàng
            max_distance_km: Khoảng cách tối đa (km) - mặc định không giới hạn
            limit: Số lượng cửa hàng tối đa trả về
        """
        all_farms = Farm.objects.all()
        nearest_farms = []
        
        for farm in all_farms:
            if farm.latitude is not None and farm.longitude is not None:
                dist = calculate_distance(latitude, longitude, farm.latitude, farm.longitude)
                
                # Nếu max_distance_km >= 99999, coi như không giới hạn
                if max_distance_km >= 99999 or dist <= max_distance_km:
                    # Attach distance to farm object temporarily
                    farm.distance_km = dist 
                    nearest_farms.append(farm)
        
        # Sort by distance
        nearest_farms.sort(key=lambda x: x.distance_km)
        
        return nearest_farms[:limit]
    
    @staticmethod
    def find_nearest_farms_by_road(latitude, longitude, max_distance_km=99999, limit=50, vehicle_type='driving'):
        """
        Tìm cửa hàng gần nhất theo ĐƯỜNG ĐI THỰC TẾ (road routing)
        
        Args:
            latitude: Vĩ độ khách hàng
            longitude: Kinh độ khách hàng
            max_distance_km: Khoảng cách tối đa (km) - mặc định không giới hạn
            limit: Số lượng cửa hàng tối đa trả về
            vehicle_type: Loại phương tiện ('driving', 'motorcycle', 'bicycle', 'foot')
        
        Returns:
            List of Store objects với attributes:
                - distance_km: Khoảng cách đường bộ (km)
                - duration_min: Thời gian di chuyển (phút)
                - route_geometry: GeoJSON LineString
                - vehicle_type: Loại phương tiện
        """
        from .routing import get_road_route
        
        all_farms = Farm.objects.all()
        farms_with_route = []
        
        for farm in all_farms:
            if farm.latitude and farm.longitude:
                # Call routing API để lấy route thực tế với vehicle type
                route_info = get_road_route(
                    farm.latitude, farm.longitude,  # FROM farm
                    latitude, longitude,             # TO customer
                    vehicle_type=vehicle_type
                )
                
                # Nếu max_distance_km >= 99999, coi như không giới hạn
                distance_check = max_distance_km >= 99999 or (route_info and route_info['distance_km'] <= max_distance_km)
                
                if route_info and distance_check:
                    # Attach route info to farm object (không tính phí ship)
                    farm.distance_km = route_info['distance_km']
                    farm.duration_min = route_info['duration_min']
                    farm.route_geometry = route_info['geometry']
                    farm.vehicle_type = route_info['vehicle_type']
                    farms_with_route.append(farm)
        
        # Sort by road distance
        farms_with_route.sort(key=lambda x: x.distance_km)
        
        return farms_with_route[:limit]
    
    @staticmethod
    def calculate_farm_distance(farm_location, customer_location):
        """
        Tính khoảng cách giữa cửa hàng và khách hàng
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
        Tạo GeoJSON cho delivery zones miền Nam Việt Nam
        """
        zones = DeliveryZone.objects.filter(is_active=True)
        features = []
        
        # Định nghĩa polygon cho các tỉnh/thành miền Nam (tọa độ thực tế)
        south_vietnam_polygons = {
            'TP. Hồ Chí Minh': [[
                [106.4, 10.5], [106.9, 10.5], [106.9, 11.0], [106.4, 11.0], [106.4, 10.5]
            ]],
            'Bình Dương': [[
                [106.5, 11.0], [107.0, 11.0], [107.0, 11.4], [106.5, 11.4], [106.5, 11.0]
            ]],
            'Đồng Nai': [[
                [106.8, 10.8], [107.6, 10.8], [107.6, 11.5], [106.8, 11.5], [106.8, 10.8]
            ]],
            'Bà Rịa - Vũng Tàu': [[
                [106.8, 10.1], [107.4, 10.1], [107.4, 10.7], [106.8, 10.7], [106.8, 10.1]
            ]],
            'Long An': [[
                [105.9, 10.4], [106.6, 10.4], [106.6, 11.0], [105.9, 11.0], [105.9, 10.4]
            ]],
            'Tây Ninh': [[
                [105.8, 11.0], [106.5, 11.0], [106.5, 11.7], [105.8, 11.7], [105.8, 11.0]
            ]],
            'Tiền Giang': [[
                [105.9, 10.1], [106.6, 10.1], [106.6, 10.6], [105.9, 10.6], [105.9, 10.1]
            ]],
            'Bến Tre': [[
                [106.0, 9.9], [106.7, 9.9], [106.7, 10.4], [106.0, 10.4], [106.0, 9.9]
            ]],
            'Vĩnh Long': [[
                [105.6, 9.9], [106.2, 9.9], [106.2, 10.4], [105.6, 10.4], [105.6, 9.9]
            ]],
            'Trà Vinh': [[
                [106.0, 9.6], [106.6, 9.6], [106.6, 10.2], [106.0, 10.2], [106.0, 9.6]
            ]],
            'Đồng Tháp': [[
                [105.3, 10.2], [105.9, 10.2], [105.9, 10.8], [105.3, 10.8], [105.3, 10.2]
            ]],
            'An Giang': [[
                [104.9, 10.1], [105.7, 10.1], [105.7, 10.8], [104.9, 10.8], [104.9, 10.1]
            ]],
            'Kiên Giang': [[
                [104.5, 9.5], [105.4, 9.5], [105.4, 10.5], [104.5, 10.5], [104.5, 9.5]
            ]],
            'Cần Thơ': [[
                [105.5, 9.8], [106.0, 9.8], [106.0, 10.3], [105.5, 10.3], [105.5, 9.8]
            ]],
            'Hậu Giang': [[
                [105.4, 9.5], [105.9, 9.5], [105.9, 10.0], [105.4, 10.0], [105.4, 9.5]
            ]],
            'Sóc Trăng': [[
                [105.7, 9.3], [106.3, 9.3], [106.3, 9.9], [105.7, 9.9], [105.7, 9.3]
            ]],
            'Bạc Liêu': [[
                [105.4, 9.0], [105.9, 9.0], [105.9, 9.5], [105.4, 9.5], [105.4, 9.0]
            ]],
            'Cà Mau': [[
                [104.8, 8.6], [105.5, 8.6], [105.5, 9.4], [104.8, 9.4], [104.8, 8.6]
            ]],
            'Bình Phước': [[
                [106.4, 11.4], [107.2, 11.4], [107.2, 12.2], [106.4, 12.2], [106.4, 11.4]
            ]],
            'Bình Thuận': [[
                [107.4, 10.5], [108.5, 10.5], [108.5, 11.6], [107.4, 11.6], [107.4, 10.5]
            ]],
            'Ninh Thuận': [[
                [108.2, 11.2], [109.2, 11.2], [109.2, 12.0], [108.2, 12.0], [108.2, 11.2]
            ]],
            'Lâm Đồng': [[
                [107.2, 11.0], [108.8, 11.0], [108.8, 12.3], [107.2, 12.3], [107.2, 11.0]
            ]]
        }
        
        for zone in zones:
            coordinates = south_vietnam_polygons.get(zone.name, [])
            if not coordinates:
                # Default fallback polygon
                coordinates = [[
                    [106.0, 10.0], [107.0, 10.0], 
                    [107.0, 11.0], [106.0, 11.0], [106.0, 10.0]
                ]]
                
            feature = {
                'type': 'Feature',
                'properties': {
                    'name': zone.name,
                    'delivery_fee': float(zone.delivery_fee),
                    'delivery_time': zone.delivery_time,
                    'area_description': zone.area_description
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


class RouteOptimizer:
    """Tối ưu hóa tuyến đường giao hàng"""
    
    @staticmethod
    def optimize_delivery_route(user_lat, user_lng, delivery_points):
        """
        Tối ưu tuyến đường sử dụng thuật toán Nearest Neighbor (Greedy)
        
        Args:
            user_lat: vĩ độ điểm bắt đầu
            user_lng: kinh độ điểm bắt đầu
            delivery_points: danh sách dict {'id', 'lat', 'lng', 'address'}
        
        Returns:
            dict với 'route' (danh sách điểm theo thứ tự), 'total_distance' (km)
        """
        if not delivery_points:
            return {'route': [], 'total_distance': 0}
        
        # Khởi tạo
        current_lat, current_lng = user_lat, user_lng
        unvisited = delivery_points.copy()
        route = []
        total_distance = 0
        
        # Nearest Neighbor algorithm
        while unvisited:
            # Tìm điểm gần nhất
            nearest = min(unvisited, key=lambda p: calculate_distance(
                current_lat, current_lng, p['lat'], p['lng']
            ))
            
            # Tính khoảng cách
            distance = calculate_distance(current_lat, current_lng, nearest['lat'], nearest['lng'])
            total_distance += distance
            
            # Cập nhật
            route.append({
                **nearest,
                'distance_from_previous': distance,
                'cumulative_distance': total_distance
            })
            
            # Di chuyển đến điểm tiếp theo
            current_lat, current_lng = nearest['lat'], nearest['lng']
            unvisited.remove(nearest)
        
        return {
            'route': route,
            'total_distance': round(total_distance, 2),
            'num_stops': len(route)
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
        
        # Tạo MarkerCluster để group markers
        from folium.plugins import MarkerCluster
        marker_cluster = MarkerCluster(
            name='Cửa hàng',
            overlay=True,
            control=True,
            icon_create_function="""
                function(cluster) {
                    var count = cluster.getChildCount();
                    var size = count < 10 ? 'small' : count < 50 ? 'medium' : 'large';
                    return L.divIcon({
                        html: '<div><span>' + count + '</span></div>',
                        className: 'marker-cluster marker-cluster-' + size,
                        iconSize: new L.Point(40, 40)
                    });
                }
            """
        ).add_to(m)
        
        # Thêm các cửa hàng lên bản đồ
        farms = Farm.objects.all()
        for farm in farms:
            if farm.latitude and farm.longitude:
                # Icon khác nhau cho cửa hàng có chứng nhận hữu cơ
                icon_color = 'green' if farm.organic_certified else 'blue'
                icon = 'leaf' if farm.organic_certified else 'home'
                
                popup_html = f"""
                <div style="width: 200px;">
                    <h4>{farm.name}</h4>
                    <p><strong>Địa chỉ:</strong> {farm.address}</p>
                    <p><strong>Loại:</strong> {'Hữu cơ' if farm.organic_certified else 'Sạch'}</p>
                    {f'<p><strong>Mô tả:</strong> {farm.description[:100]}...</p>' if farm.description else ''}
                </div>
                """
                
                folium.Marker(
                    location=[farm.latitude, farm.longitude],
                    popup=folium.Popup(popup_html, max_width=250),
                    tooltip=farm.name,
                    icon=folium.Icon(color=icon_color, icon=icon, prefix='fa')
                ).add_to(marker_cluster)  # Add to cluster instead of map directly
        
        folium.LayerControl().add_to(m)
        return m
    
    @staticmethod
    def create_delivery_zones_map(center_lat=10.5, center_lng=106.5, zoom=7):
        """Tạo bản đồ khu vực giao hàng miền Nam Việt Nam"""
        m = folium.Map(
            location=[center_lat, center_lng],
            zoom_start=zoom,
            tiles='OpenStreetMap'
        )
        
        zones_data = DeliveryZoneManager.get_all_delivery_zones_geojson()
        
        # Màu sắc cho các khu vực (gradient từ gần đến xa)
        colors = [
            '#FF6B6B',  # Đỏ - gần nhất (TP.HCM)
            '#4ECDC4',  # Xanh ngọc - gần
            '#45B7D1',  # Xanh dương - trung bình
            '#96CEB4',  # Xanh lá nhạt - xa
            '#FFEAA7',  # Vàng - xa hơn
            '#DDA0DD',  # Tím nhạt - rất xa
            '#F0E68C',  # Vàng khaki
            '#FFB6C1',  # Hồng nhạt
            '#98FB98',  # Xanh lá nhạt
            '#87CEEB',  # Xanh da trời
            '#DEB887',  # Nâu nhạt
            '#F5DEB3',  # Wheat
            '#FFE4E1',  # Misty rose
            '#E0FFFF',  # Light cyan
            '#FAFAD2',  # Light goldenrod
            '#D3D3D3',  # Light gray
            '#FFF8DC',  # Cornsilk
            '#F0F8FF',  # Alice blue
            '#FDF5E6',  # Old lace
            '#F5F5DC',  # Beige
            '#FFFACD',  # Lemon chiffon
            '#E6E6FA'   # Lavender
        ]
        
        for i, feature in enumerate(zones_data['features']):
            coords = feature['geometry']['coordinates'][0]
            # Folium cần Lat, Lng - GeoJSON là Lng, Lat
            folium_coords = [[c[1], c[0]] for c in coords]
            props = feature['properties']
            
            color = colors[i % len(colors)]
            
            # Popup HTML với thông tin chi tiết
            popup_html = f"""
            <div style="font-family: 'Inter', Arial, sans-serif; width: 280px;">
                <div style="background: linear-gradient(135deg, {color}, {color}88); padding: 15px; margin: -10px -10px 10px -10px; border-radius: 8px 8px 0 0;">
                    <h3 style="margin: 0; color: white; text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
                        <i class="fas fa-map-marker-alt"></i> {props['name']}
                    </h3>
                </div>
                
                <div style="padding: 5px 0;">
                    <p style="margin: 8px 0; font-size: 13px; line-height: 1.4;">
                        <strong><i class="fas fa-info-circle" style="color: #007bff;"></i> Khu vực:</strong><br>
                        <span style="color: #666;">{props['area_description']}</span>
                    </p>
                    
                    <div style="display: flex; justify-content: space-between; margin: 12px 0;">
                        <div style="text-align: center; flex: 1;">
                            <div style="background: #e8f5e8; padding: 8px; border-radius: 6px;">
                                <i class="fas fa-truck" style="color: #28a745; font-size: 16px;"></i><br>
                                <strong style="color: #28a745;">{props['delivery_fee']:,.0f} VNĐ</strong><br>
                                <small style="color: #666;">Phí giao hàng</small>
                            </div>
                        </div>
                        <div style="width: 10px;"></div>
                        <div style="text-align: center; flex: 1;">
                            <div style="background: #fff3cd; padding: 8px; border-radius: 6px;">
                                <i class="fas fa-clock" style="color: #856404; font-size: 16px;"></i><br>
                                <strong style="color: #856404;">{props['delivery_time']}</strong><br>
                                <small style="color: #666;">Thời gian</small>
                            </div>
                        </div>
                    </div>
                    
                    <div style="text-align: center; margin-top: 10px;">
                        <span style="background: #d4edda; color: #155724; padding: 4px 8px; border-radius: 12px; font-size: 12px;">
                            <i class="fas fa-check-circle"></i> Đang hoạt động
                        </span>
                    </div>
                </div>
            </div>
            """
            
            # Vẽ polygon cho khu vực
            folium.Polygon(
                locations=folium_coords,
                popup=folium.Popup(popup_html, max_width=320),
                tooltip=f"{props['name']} - {props['delivery_time']} - {props['delivery_fee']:,.0f} VNĐ",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.3,
                weight=2,
                opacity=0.8
            ).add_to(m)
            
            # Tính center của polygon để đặt marker
            center_lat = sum([c[0] for c in folium_coords]) / len(folium_coords)
            center_lng = sum([c[1] for c in folium_coords]) / len(folium_coords)
            
            # Icon khác nhau dựa trên phí giao hàng
            if props['delivery_fee'] <= 30000:
                icon_color = 'green'
                icon = 'home'
            elif props['delivery_fee'] <= 60000:
                icon_color = 'blue'
                icon = 'truck'
            else:
                icon_color = 'orange'
                icon = 'plane'
            
            # Thêm marker cho center của khu vực
            folium.Marker(
                location=[center_lat, center_lng],
                popup=popup_html,
                tooltip=f"{props['name']} - {props['delivery_fee']:,.0f} VNĐ",
                icon=folium.Icon(color=icon_color, icon=icon, prefix='fa')
            ).add_to(m)
        
        # Thêm legend
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; right: 50px; width: 200px; height: auto; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px; border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <h4 style="margin-top: 0;"><i class="fas fa-info-circle"></i> Chú thích</h4>
            <p style="margin: 5px 0;"><i class="fas fa-home" style="color: green;"></i> Gần (≤30k VNĐ)</p>
            <p style="margin: 5px 0;"><i class="fas fa-truck" style="color: blue;"></i> Trung bình (30-60k VNĐ)</p>
            <p style="margin: 5px 0;"><i class="fas fa-plane" style="color: orange;"></i> Xa (>60k VNĐ)</p>
            <hr style="margin: 8px 0;">
            <p style="margin: 5px 0; font-size: 12px; color: #666;">
                <strong>Phạm vi:</strong> Toàn miền Nam<br>
                <strong>Tổng:</strong> 22 tỉnh/thành
            </p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
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
            icon=folium.Icon(color='red', icon='store', prefix='fa')
        ).add_to(m)
        
        # Assigned Farm (if exists)
        if order.assigned_farm and order.assigned_farm.latitude and order.assigned_farm.longitude:
            farm = order.assigned_farm
            
            folium.Marker(
                location=[farm.latitude, farm.longitude],
                popup=f"<b>{farm.name}</b><br>Farm được gán cho đơn hàng",
                icon=folium.Icon(color='green', icon='leaf', prefix='fa')
            ).add_to(m)
            
            # Lấy route thực tế từ routing API
            from .routing import get_route_with_fee
# Shipping calculator imports removed for minimal version
# from .shipping_calculator import ShippingCalculator
            
            route_info = get_route_with_fee(
                farm.latitude, farm.longitude,
                order.delivery_latitude, order.delivery_longitude
            )
            
            if route_info:
                # Tính phí ship để hiển thị
                shipping_fee = order.delivery_fee if order.delivery_fee else 0
                
                # Hiển thị route THỰC TẾ theo đường phố
                folium.GeoJson(
                    route_info['geometry'],
                    style_function=lambda x: {
                        'color': '#4285F4',
                        'weight': 5,
                        'opacity': 0.8
                    },
                    tooltip=f"📍 {route_info['distance_km']:.1f} km | ⏱ {route_info['duration_min']:.0f} phút | 💰 {shipping_fee:,.0f} VNĐ"
                ).add_to(m)
            else:
                # Fallback: nếu routing API lỗi, dùng đường thẳng
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
        """Tạo bản đồ cho một cửa hàng duy nhất"""
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
    Thống kê theo khu vực, cửa hàng
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
        Thống kê cửa hàng phổ biến nhất
        Returns: List các cửa hàng được đặt hàng nhiều nhất
        """
        from django.db.models import Count, Sum
        
        farms_stats = Farm.objects.annotate(
            total_orders=Count('product__orderitem__order', distinct=True),
            total_products_sold=Sum('product__orderitem__quantity')
        ).filter(total_orders__gt=0).order_by('-total_orders')
        
        return farms_stats