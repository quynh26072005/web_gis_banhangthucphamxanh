"""
Order Tracking Views - Real-time tracking for customers
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.contrib import messages
from .models import Order, Customer, Shipper
from decimal import Decimal


@login_required
@require_GET
def order_tracking_view(request, order_id):
    """
    Trang theo dõi đơn hàng realtime với Google Maps
    """
    from django.conf import settings
    
    try:
        customer = request.user.customer
        order = get_object_or_404(Order, id=order_id, customer=customer)
        
        # Kiểm tra đơn hàng có shipper chưa
        has_shipper = order.assigned_shipper is not None
        
        # Tính subtotal
        subtotal = order.total_amount - Decimal(str(order.delivery_fee))
        
        context = {
            'order': order,
            'has_shipper': has_shipper,
            'subtotal': subtotal,
            'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        }
        
        return render(request, 'pages/orders/order_tracking_google.html', context)
        
    except Customer.DoesNotExist:
        messages.error(request, 'Không tìm thấy thông tin khách hàng')
        return redirect('food_store:home')


@login_required
@require_GET
def order_tracking_api(request, order_id):
    """
    API trả về thông tin tracking realtime
    Frontend sẽ gọi API này mỗi 5-10 giây để cập nhật vị trí
    """
    try:
        customer = request.user.customer
        order = get_object_or_404(Order, id=order_id, customer=customer)
        
        # Thông tin cơ bản
        data = {
            'success': True,
            'order_id': order.id,
            'status': order.status,
            'status_display': order.get_status_display(),
            'has_shipper': order.assigned_shipper is not None,
        }
        
        # Thông tin cửa hàng (điểm lấy hàng)
        if order.assigned_farm:
            data['store'] = {
                'name': order.assigned_farm.name,
                'address': order.assigned_farm.address,
                'lat': float(order.assigned_farm.latitude) if order.assigned_farm.latitude else None,
                'lng': float(order.assigned_farm.longitude) if order.assigned_farm.longitude else None,
            }
        
        # Thông tin địa chỉ giao hàng (điểm đến)
        data['destination'] = {
            'address': order.delivery_address,
            'lat': float(order.delivery_latitude) if order.delivery_latitude else None,
            'lng': float(order.delivery_longitude) if order.delivery_longitude else None,
        }
        
        # Thông tin shipper (nếu có)
        if order.assigned_shipper:
            shipper = order.assigned_shipper
            data['shipper'] = {
                'name': shipper.user.get_full_name() or shipper.user.username,
                'phone': shipper.phone,
                'vehicle': shipper.vehicle_number,
                'status': shipper.status,
                'status_display': shipper.get_status_display(),
                # TODO: Thêm vị trí realtime của shipper khi có GPS tracking
                # Hiện tại dùng vị trí cửa hàng hoặc địa chỉ giao hàng tùy trạng thái
                'current_lat': _get_shipper_estimated_location(order)['lat'],
                'current_lng': _get_shipper_estimated_location(order)['lng'],
            }
            
            # Thời gian
            if order.shipper_accepted_at:
                data['shipper']['accepted_at'] = order.shipper_accepted_at.strftime('%H:%M %d/%m/%Y')
            if order.shipper_picked_at:
                data['shipper']['picked_at'] = order.shipper_picked_at.strftime('%H:%M %d/%m/%Y')
        
        # Thông tin giao hàng
        if order.delivered_at:
            data['delivered_at'] = order.delivered_at.strftime('%H:%M %d/%m/%Y')
        
        # Route info
        if order.delivery_distance_km:
            data['distance_km'] = float(order.delivery_distance_km)
        if order.estimated_delivery_time:
            data['estimated_time'] = order.estimated_delivery_time
        
        return JsonResponse(data)
        
    except Customer.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Không tìm thấy khách hàng'}, status=403)
    except Order.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Không tìm thấy đơn hàng'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def _get_shipper_estimated_location(order):
    """
    Ước tính vị trí shipper dựa trên trạng thái đơn hàng
    TODO: Thay bằng GPS tracking thực tế
    """
    # Nếu chưa lấy hàng -> shipper ở cửa hàng
    if not order.shipper_picked_at and order.assigned_farm:
        return {
            'lat': float(order.assigned_farm.latitude) if order.assigned_farm.latitude else 10.8231,
            'lng': float(order.assigned_farm.longitude) if order.assigned_farm.longitude else 106.6297,
        }
    
    # Nếu đã lấy hàng nhưng chưa giao -> shipper đang trên đường (giữa cửa hàng và địa chỉ)
    if order.shipper_picked_at and not order.delivered_at:
        if order.assigned_farm and order.delivery_latitude and order.delivery_longitude:
            # Tính điểm giữa (midpoint)
            store_lat = float(order.assigned_farm.latitude) if order.assigned_farm.latitude else 10.8231
            store_lng = float(order.assigned_farm.longitude) if order.assigned_farm.longitude else 106.6297
            dest_lat = float(order.delivery_latitude)
            dest_lng = float(order.delivery_longitude)
            
            return {
                'lat': (store_lat + dest_lat) / 2,
                'lng': (store_lng + dest_lng) / 2,
            }
    
    # Nếu đã giao -> shipper ở địa chỉ giao hàng
    if order.delivered_at and order.delivery_latitude and order.delivery_longitude:
        return {
            'lat': float(order.delivery_latitude),
            'lng': float(order.delivery_longitude),
        }
    
    # Default: Trung tâm TP.HCM
    return {'lat': 10.8231, 'lng': 106.6297}


@login_required
@require_GET
def order_status_timeline_api(request, order_id):
    """
    API trả về timeline trạng thái đơn hàng
    """
    try:
        customer = request.user.customer
        order = get_object_or_404(Order, id=order_id, customer=customer)
        
        timeline = []
        
        # Đơn hàng được tạo
        timeline.append({
            'status': 'created',
            'title': 'Đơn hàng đã được tạo',
            'time': order.created_at.strftime('%H:%M %d/%m/%Y'),
            'completed': True,
        })
        
        # Đơn hàng được xác nhận
        if order.status in ['confirmed', 'shipping', 'delivered']:
            timeline.append({
                'status': 'confirmed',
                'title': 'Đơn hàng đã được xác nhận',
                'time': order.created_at.strftime('%H:%M %d/%m/%Y'),  # TODO: Thêm confirmed_at field
                'completed': True,
            })
        
        # Shipper nhận đơn
        if order.assigned_shipper and order.shipper_accepted_at:
            timeline.append({
                'status': 'accepted',
                'title': f'Shipper {order.assigned_shipper.user.get_full_name()} đã nhận đơn',
                'time': order.shipper_accepted_at.strftime('%H:%M %d/%m/%Y'),
                'completed': True,
            })
        
        # Shipper lấy hàng
        if order.shipper_picked_at:
            timeline.append({
                'status': 'picked',
                'title': 'Shipper đã lấy hàng',
                'time': order.shipper_picked_at.strftime('%H:%M %d/%m/%Y'),
                'completed': True,
            })
        
        # Đang giao hàng
        if order.status == 'shipping':
            timeline.append({
                'status': 'shipping',
                'title': 'Đang giao hàng đến bạn',
                'time': 'Đang thực hiện',
                'completed': False,
                'active': True,
            })
        
        # Đã giao hàng
        if order.status == 'delivered' and order.delivered_at:
            timeline.append({
                'status': 'delivered',
                'title': 'Đã giao hàng thành công',
                'time': order.delivered_at.strftime('%H:%M %d/%m/%Y'),
                'completed': True,
            })
        
        # Đã hủy
        if order.status == 'cancelled':
            timeline.append({
                'status': 'cancelled',
                'title': 'Đơn hàng đã bị hủy',
                'time': order.updated_at.strftime('%H:%M %d/%m/%Y'),
                'completed': True,
                'cancelled': True,
            })
        
        return JsonResponse({
            'success': True,
            'timeline': timeline,
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
