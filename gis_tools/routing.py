"""
Road Routing Module using OSRM (OpenStreetMap Routing Machine)
Tính toán đường đi thực tế trên bản đồ thay vì đường chim bay
"""
import requests
import logging

logger = logging.getLogger(__name__)


def get_road_route(start_lat, start_lng, end_lat, end_lng, timeout=5):
    """
    Lấy thông tin đường đi thực tế từ OSRM API
    
    Args:
        start_lat (float): Vĩ độ điểm bắt đầu
        start_lng (float): Kinh độ điểm bắt đầu
        end_lat (float): Vĩ độ điểm kết thúc
        end_lng (float): Kinh độ điểm kết thúc
        timeout (int): Timeout cho API call (seconds)
    
    Returns:
        dict: {
            'distance_km': float,     # Khoảng cách (km)
            'duration_min': float,    # Thời gian (phút)
            'geometry': dict          # GeoJSON LineString
        }
        None nếu không tìm được route
    """
    try:
        # OSRM API endpoint (public server)
        # Format: lon,lat (NOT lat,lon!)
        url = f"http://router.project-osrm.org/route/v1/driving/{start_lng},{start_lat};{end_lng},{end_lat}"
        
        params = {
            'overview': 'full',        # Get full route geometry
            'geometries': 'geojson'    # Return as GeoJSON
        }
        
        response = requests.get(url, params=params, timeout=timeout)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get('code') == 'Ok' and data.get('routes'):
            route = data['routes'][0]
            
            return {
                'distance_km': route['distance'] / 1000,      # meters → km
                'duration_min': route['duration'] / 60,       # seconds → minutes
                'geometry': route['geometry']                  # GeoJSON LineString
            }
        else:
            logger.warning(f"OSRM returned non-Ok status: {data.get('code')}")
            return None
            
    except requests.Timeout:
        logger.error(f"OSRM API timeout after {timeout}s")
        return None
    except requests.RequestException as e:
        logger.error(f"OSRM API error: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in get_road_route: {e}")
        return None


def calculate_shipping_fee(distance_km, base_fee=15000, per_km_fee=5000):
    """
    Tính phí giao hàng dựa trên khoảng cách
    
    Args:
        distance_km (float): Khoảng cách (km)
        base_fee (int): Phí cơ bản (VNĐ)
        per_km_fee (int): Phí mỗi km (VNĐ/km)
    
    Returns:
        int: Tổng phí giao hàng (VNĐ)
    
    Example:
        >>> calculate_shipping_fee(10)  # 10km
        65000  # 15,000 + (10 * 5,000)
    """
    return int(base_fee + (distance_km * per_km_fee))


def get_route_with_fee(start_lat, start_lng, end_lat, end_lng):
    """
    Kết hợp: lấy route + tính phí ship
    
    Returns:
        dict: {
            'distance_km': float,
            'duration_min': float,
            'geometry': dict,
            'shipping_fee': int
        }
        None nếu không tìm được route
    """
    route_info = get_road_route(start_lat, start_lng, end_lat, end_lng)
    
    if route_info:
        route_info['shipping_fee'] = calculate_shipping_fee(route_info['distance_km'])
        return route_info
    
    return None
