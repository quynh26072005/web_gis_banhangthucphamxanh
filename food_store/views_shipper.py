"""
Shipper Views - Mobile-First Design
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Sum, Q
from datetime import datetime, timedelta
from .models import Shipper, Order
import json


@login_required
def shipper_dashboard(request):
    """Dashboard chính - Mobile First"""
    try:
        shipper = request.user.shipper
    except Shipper.DoesNotExist:
        messages.error(request, 'Bạn không có quyền truy cập.')
        return redirect('food_store:home')
    
    # Thống kê hôm nay
    today = timezone.now().date()
    today_orders = Order.objects.filter(
        assigned_shipper=shipper,
        created_at__date=today
    )
    
    context = {
        'shipper': shipper,
        'today_deliveries': shipper.today_deliveries,
        'cod_holding': shipper.cod_holding,
        'today_earnings': shipper.today_earnings,
    }
    
    return render(request, 'shipper/dashboard.html', context)


@login_required
@require_POST
def toggle_status(request):
    """Bật/tắt trạng thái làm việc"""
    try:
        shipper = request.user.shipper
        data = json.loads(request.body)
        new_status = data.get('status')
        
        if new_status in ['available', 'offline']:
            shipper.status = new_status
            shipper.save()
            
            return JsonResponse({
                'success': True,
                'status': shipper.status,
                'message': 'Đã cập nhật trạng thái'
            })
        
        return JsonResponse({'success': False, 'message': 'Trạng thái không hợp lệ'})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
def order_list(request):
    """Danh sách đơn hàng theo tab"""
    try:
        shipper = request.user.shipper
    except Shipper.DoesNotExist:
        return redirect('food_store:home')
    
    tab = request.GET.get('tab', 'new')
    
    # Đơn mới (chưa có shipper)
    new_orders = Order.objects.filter(
        status='confirmed',
        assigned_shipper__isnull=True
    ).select_related('customer__user', 'assigned_farm').order_by('-created_at')[:20]
    
    # Đang lấy hàng (đã nhận nhưng chưa lấy)
    picking_orders = Order.objects.filter(
        assigned_shipper=shipper,
        status='confirmed',
        shipper_picked_at__isnull=True
    ).select_related('customer__user', 'assigned_farm')
    
    # Đang giao (đã lấy hàng)
    delivering_orders = Order.objects.filter(
        assigned_shipper=shipper,
        status='shipping'
    ).select_related('customer__user', 'assigned_farm')
    
    # Hoàn thành hôm nay
    today = timezone.now().date()
    completed_orders = Order.objects.filter(
        assigned_shipper=shipper,
        status='delivered',
        delivered_at__date=today
    ).select_related('customer__user', 'assigned_farm')
    
    context = {
        'shipper': shipper,
        'tab': tab,
        'new_orders': new_orders,
        'picking_orders': picking_orders,
        'delivering_orders': delivering_orders,
        'completed_orders': completed_orders,
    }
    
    return render(request, 'shipper/order_list.html', context)


@login_required
def order_detail(request, order_id):
    """Chi tiết đơn hàng"""
    try:
        shipper = request.user.shipper
    except Shipper.DoesNotExist:
        return redirect('food_store:home')
    
    order = get_object_or_404(Order, id=order_id)
    
    # Kiểm tra quyền xem
    if order.assigned_shipper and order.assigned_shipper != shipper:
        messages.error(request, 'Bạn không có quyền xem đơn hàng này.')
        return redirect('food_store:shipper_orders')
    
    # Tính subtotal (tổng tiền hàng không bao gồm phí ship)
    from decimal import Decimal
    subtotal = order.total_amount - Decimal(str(order.delivery_fee))
    
    context = {
        'shipper': shipper,
        'order': order,
        'subtotal': subtotal,
    }
    
    return render(request, 'shipper/order_detail.html', context)


@login_required
@require_POST
def accept_order(request, order_id):
    """Nhận đơn hàng"""
    try:
        shipper = request.user.shipper
        order = get_object_or_404(Order, id=order_id)
        
        # Kiểm tra đơn còn available không
        if order.assigned_shipper is not None:
            return JsonResponse({
                'success': False,
                'message': 'Đơn hàng đã được shipper khác nhận'
            })
        
        if order.status != 'confirmed':
            return JsonResponse({
                'success': False,
                'message': 'Đơn hàng không ở trạng thái có thể nhận'
            })
        
        # Gán shipper
        order.assigned_shipper = shipper
        order.shipper_accepted_at = timezone.now()
        order.save()
        
        # Cập nhật trạng thái shipper
        shipper.status = 'busy'
        shipper.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Đã nhận đơn hàng thành công!',
            'order_id': order.id
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_POST
def mark_picked(request, order_id):
    """Đánh dấu đã lấy hàng"""
    try:
        shipper = request.user.shipper
        order = get_object_or_404(Order, id=order_id, assigned_shipper=shipper)
        
        order.shipper_picked_at = timezone.now()
        order.status = 'shipping'
        order.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Đã xác nhận lấy hàng!'
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
@require_POST
def complete_order(request, order_id):
    """Hoàn thành đơn hàng"""
    try:
        from decimal import Decimal
        
        shipper = request.user.shipper
        order = get_object_or_404(Order, id=order_id, assigned_shipper=shipper)
        
        # Xử lý ảnh chứng minh (nếu có)
        if 'proof_image' in request.FILES:
            order.proof_image = request.FILES['proof_image']
        
        # Ghi chú
        shipper_notes = request.POST.get('shipper_notes', '')
        if shipper_notes:
            order.shipper_notes = shipper_notes
        
        # Hoàn thành
        order.status = 'delivered'
        order.delivered_at = timezone.now()
        order.save()
        
        # Cập nhật thống kê shipper
        shipper.total_deliveries += 1
        shipper.today_deliveries += 1
        
        # Nếu COD, cộng vào tiền đang giữ
        if order.payment_method == 'cod':
            shipper.cod_holding += order.total_amount
        
        # Tính thu nhập (giả sử 10% giá trị đơn)
        shipper.today_earnings += order.total_amount * Decimal('0.1')
        
        # Kiểm tra còn đơn nào đang giao không
        has_active_orders = Order.objects.filter(
            assigned_shipper=shipper,
            status__in=['confirmed', 'shipping']
        ).exists()
        
        if not has_active_orders:
            shipper.status = 'available'
        
        shipper.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Đã hoàn thành giao hàng!'
        })
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@login_required
def order_map(request, order_id):
    """Bản đồ điều hướng"""
    try:
        shipper = request.user.shipper
    except Shipper.DoesNotExist:
        return redirect('food_store:home')
    
    order = get_object_or_404(Order, id=order_id)
    
    context = {
        'shipper': shipper,
        'order': order,
    }
    
    return render(request, 'shipper/order_map.html', context)
