"""
Store Admin Dashboard Views
Dashboard riêng cho quản lý chi nhánh
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.http import HttpResponse
from datetime import timedelta, datetime

from food_store.models import (
    Order, Product, Farm, Customer, StoreAdmin,
    StockTransaction, StockAlert, Supplier, Shipper
)
from food_store.permissions import (
    require_store_admin, require_permission,
    filter_queryset_by_farm, get_managed_farm,
    check_permission, is_super_admin
)


@login_required(login_url='/accounts/login/')
@require_store_admin
def store_admin_dashboard(request):
    """Dashboard cho Store Admin"""
    managed_farm = get_managed_farm(request.user)
    
    if not managed_farm:
        messages.error(request, 'Không tìm thấy chi nhánh bạn quản lý!')
        return redirect('food_store:home')
    
    # Thống kê tổng quan CHỈ CỦA CHI NHÁNH NÀY
    total_orders = Order.objects.filter(assigned_farm=managed_farm).count()
    total_products = Product.objects.filter(farm=managed_farm).count()
    total_shippers = Shipper.objects.filter(assigned_farm=managed_farm).count()
    
    # Doanh thu CHI NHÁNH
    total_revenue = Order.objects.filter(
        assigned_farm=managed_farm,
        status='delivered'
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Đơn hàng hôm nay
    today = timezone.now().date()
    orders_today = Order.objects.filter(
        assigned_farm=managed_farm,
        created_at__date=today
    ).count()
    
    # Đơn hàng chờ xử lý
    pending_orders = Order.objects.filter(
        assigned_farm=managed_farm,
        status='pending'
    ).count()
    
    # Cảnh báo tồn kho
    stock_alerts = StockAlert.objects.filter(
        farm=managed_farm,
        is_resolved=False
    ).count()
    
    # Đơn hàng gần nhất
    recent_orders = Order.objects.filter(
        assigned_farm=managed_farm
    ).select_related(
        'customer', 'assigned_shipper'
    ).order_by('-created_at')[:10]
    
    # Sản phẩm sắp hết
    low_stock_products = Product.objects.filter(
        farm=managed_farm,
        stock_quantity__lt=20
    ).order_by('stock_quantity')[:10]
    
    # Doanh thu 7 ngày gần nhất
    last_7_days = []
    revenue_7_days = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        revenue = Order.objects.filter(
            assigned_farm=managed_farm,
            created_at__date=date,
            status='delivered'
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        last_7_days.append(date.strftime('%d/%m'))
        revenue_7_days.append(float(revenue))
    
    # Top sản phẩm bán chạy CỦA CHI NHÁNH
    from food_store.models import OrderItem
    top_products = OrderItem.objects.filter(
        product__farm=managed_farm
    ).values(
        'product__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('price')
    ).order_by('-total_quantity')[:5]
    
    # Shipper đang hoạt động
    active_shippers = Shipper.objects.filter(
        assigned_farm=managed_farm,
        status__in=['available', 'busy']
    ).count()
    
    context = {
        'managed_farm': managed_farm,
        'total_orders': total_orders,
        'total_products': total_products,
        'total_shippers': total_shippers,
        'active_shippers': active_shippers,
        'total_revenue': total_revenue,
        'orders_today': orders_today,
        'pending_orders': pending_orders,
        'stock_alerts': stock_alerts,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'last_7_days': last_7_days,
        'revenue_7_days': revenue_7_days,
        'top_products': top_products,
    }
    
    return render(request, 'store_admin_dashboard/dashboard.html', context)


@login_required(login_url='/accounts/login/')
@require_store_admin
@require_permission('can_manage_orders')
def store_admin_orders(request):
    """Quản lý đơn hàng của chi nhánh"""
    managed_farm = get_managed_farm(request.user)
    
    orders = Order.objects.filter(
        assigned_farm=managed_farm
    ).select_related(
        'customer', 'assigned_shipper'
    ).order_by('-created_at')
    
    # Filter theo status
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    context = {
        'managed_farm': managed_farm,
        'orders': orders,
        'current_status': status,
    }
    
    return render(request, 'store_admin_dashboard/orders.html', context)


@login_required(login_url='/accounts/login/')
@require_store_admin
@require_permission('can_manage_products')
def store_admin_products(request):
    """Quản lý sản phẩm của chi nhánh"""
    managed_farm = get_managed_farm(request.user)
    
    products = Product.objects.filter(
        farm=managed_farm
    ).select_related('category').order_by('-created_at')
    
    context = {
        'managed_farm': managed_farm,
        'products': products,
    }
    
    return render(request, 'store_admin_dashboard/products.html', context)


@login_required(login_url='/accounts/login/')
@require_store_admin
@require_permission('can_manage_products')
def store_admin_product_create(request):
    """Tạo sản phẩm mới"""
    managed_farm = get_managed_farm(request.user)
    
    if request.method == 'POST':
        from food_store.models import Category
        
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        unit = request.POST.get('unit')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        is_available = request.POST.get('is_available') == 'on'
        
        try:
            category = Category.objects.get(id=category_id)
            
            product = Product.objects.create(
                farm=managed_farm,
                category=category,
                name=name,
                price=price,
                stock_quantity=stock_quantity,
                unit=unit,
                description=description,
                image=image,
                is_available=is_available
            )
            
            messages.success(request, f'Đã tạo sản phẩm "{product.name}" thành công!')
            return redirect('food_store:store_admin_products')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    from food_store.models import Category
    categories = Category.objects.all()
    
    context = {
        'managed_farm': managed_farm,
        'categories': categories,
    }
    
    return render(request, 'store_admin_dashboard/product_form.html', context)


@login_required(login_url='/accounts/login/')
@require_store_admin
@require_permission('can_manage_products')
def store_admin_product_edit(request, pk):
    """Sửa sản phẩm"""
    managed_farm = get_managed_farm(request.user)
    
    product = get_object_or_404(
        Product.objects.filter(farm=managed_farm),
        pk=pk
    )
    
    if request.method == 'POST':
        from food_store.models import Category
        
        product.name = request.POST.get('name')
        product.category = Category.objects.get(id=request.POST.get('category'))
        product.price = request.POST.get('price')
        product.stock_quantity = request.POST.get('stock_quantity')
        product.unit = request.POST.get('unit')
        product.description = request.POST.get('description')
        
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        
        product.is_available = request.POST.get('is_available') == 'on'
        
        try:
            product.save()
            messages.success(request, f'Đã cập nhật sản phẩm "{product.name}" thành công!')
            return redirect('food_store:store_admin_products')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    from food_store.models import Category
    categories = Category.objects.all()
    
    context = {
        'managed_farm': managed_farm,
        'product': product,
        'categories': categories,
    }
    
    return render(request, 'store_admin_dashboard/product_form.html', context)


@login_required(login_url='/accounts/login/')
@require_store_admin
@require_permission('can_manage_products')
def store_admin_product_delete(request, pk):
    """Xóa sản phẩm"""
    managed_farm = get_managed_farm(request.user)
    
    product = get_object_or_404(
        Product.objects.filter(farm=managed_farm),
        pk=pk
    )
    
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Đã xóa sản phẩm "{product_name}" thành công!')
        return redirect('food_store:store_admin_products')
    
    context = {
        'managed_farm': managed_farm,
        'product': product,
    }
    
    return render(request, 'store_admin_dashboard/product_confirm_delete.html', context)


@login_required(login_url='/accounts/login/')
@require_store_admin
@require_permission('can_manage_inventory')
def store_admin_inventory(request):
    """Quản lý kho của chi nhánh"""
    managed_farm = get_managed_farm(request.user)
    
    transactions = StockTransaction.objects.filter(
        farm=managed_farm
    ).select_related(
        'product', 'supplier'
    ).order_by('-created_at')[:50]
    
    alerts = StockAlert.objects.filter(
        farm=managed_farm,
        is_resolved=False
    ).select_related('product')
    
    suppliers = Supplier.objects.filter(is_active=True)
    
    context = {
        'managed_farm': managed_farm,
        'transactions': transactions,
        'alerts': alerts,
        'suppliers': suppliers,
    }
    
    return render(request, 'store_admin_dashboard/inventory.html', context)


@login_required(login_url='/accounts/login/')
@require_store_admin
@require_permission('can_manage_inventory')
def store_admin_stock_import(request):
    """Nhập hàng vào kho chi nhánh"""
    from django.contrib import messages
    
    managed_farm = get_managed_farm(request.user)
    
    # Chỉ lấy sản phẩm của chi nhánh này
    products = Product.objects.filter(farm=managed_farm).select_related('category')
    suppliers = Supplier.objects.filter(is_active=True)
    
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product')
            quantity = int(request.POST.get('quantity', 0))
            unit_price = float(request.POST.get('unit_price', 0))
            supplier_id = request.POST.get('supplier')
            reference_number = request.POST.get('reference_number', '')
            notes = request.POST.get('notes', '')
            
            # Validation
            if quantity <= 0:
                messages.error(request, 'Số lượng phải lớn hơn 0!')
                return redirect('food_store:store_admin_stock_import')
            
            if unit_price < 0:
                messages.error(request, 'Đơn giá không được âm!')
                return redirect('food_store:store_admin_stock_import')
            
            product = Product.objects.get(id=product_id, farm=managed_farm)
            
            # Tạo giao dịch nhập kho
            # Model StockTransaction.save() sẽ TỰ ĐỘNG cập nhật tồn kho
            transaction = StockTransaction.objects.create(
                product=product,
                farm=managed_farm,
                transaction_type='import',
                quantity=quantity,
                unit_price=unit_price,
                supplier_id=supplier_id if supplier_id else None,
                reference_number=reference_number,
                notes=notes,
                created_by=request.user
            )
            
            messages.success(request, f'Nhập hàng thành công! Đã thêm {quantity} {product.unit} vào kho. Tồn kho mới: {transaction.stock_after}')
            return redirect('food_store:store_admin_inventory')
        except Product.DoesNotExist:
            messages.error(request, 'Sản phẩm không tồn tại hoặc không thuộc chi nhánh của bạn!')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    context = {
        'managed_farm': managed_farm,
        'products': products,
        'suppliers': suppliers,
    }
    
    return render(request, 'store_admin_dashboard/stock_import_form.html', context)


@login_required(login_url='/accounts/login/')
@require_store_admin
@require_permission('can_manage_inventory')
def store_admin_stock_export(request):
    """Xuất hàng ra khỏi kho chi nhánh"""
    from django.contrib import messages
    
    managed_farm = get_managed_farm(request.user)
    
    # Chỉ lấy sản phẩm của chi nhánh này và còn hàng
    products = Product.objects.filter(
        farm=managed_farm,
        stock_quantity__gt=0
    ).select_related('category')
    
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product')
            quantity = int(request.POST.get('quantity', 0))
            unit_price = float(request.POST.get('unit_price', 0))
            reference_number = request.POST.get('reference_number', '')
            notes = request.POST.get('notes', '')
            
            # Validation
            if quantity <= 0:
                messages.error(request, 'Số lượng phải lớn hơn 0!')
                return redirect('food_store:store_admin_stock_export')
            
            if unit_price < 0:
                messages.error(request, 'Đơn giá không được âm!')
                return redirect('food_store:store_admin_stock_export')
            
            product = Product.objects.get(id=product_id, farm=managed_farm)
            
            # Kiểm tra tồn kho
            if product.stock_quantity < quantity:
                messages.error(request, f'Không đủ hàng trong kho! Tồn kho hiện tại: {product.stock_quantity} {product.unit}')
                return redirect('food_store:store_admin_stock_export')
            
            # Tạo giao dịch xuất kho
            # Model StockTransaction.save() sẽ TỰ ĐỘNG cập nhật tồn kho
            transaction = StockTransaction.objects.create(
                product=product,
                farm=managed_farm,
                transaction_type='export',
                quantity=quantity,
                unit_price=unit_price,
                reference_number=reference_number,
                notes=notes,
                created_by=request.user
            )
            
            messages.success(request, f'Xuất hàng thành công! Đã xuất {quantity} {product.unit} ra khỏi kho. Tồn kho còn: {transaction.stock_after}')
            return redirect('food_store:store_admin_inventory')
        except Product.DoesNotExist:
            messages.error(request, 'Sản phẩm không tồn tại hoặc không thuộc chi nhánh của bạn!')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    context = {
        'managed_farm': managed_farm,
        'products': products,
    }
    
    return render(request, 'store_admin_dashboard/stock_export_form.html', context)


@login_required(login_url='/accounts/login/')
@require_store_admin
@require_permission('can_manage_shippers')
def store_admin_shippers(request):
    """Quản lý shipper của chi nhánh"""
    managed_farm = get_managed_farm(request.user)
    
    shippers = Shipper.objects.filter(
        assigned_farm=managed_farm
    ).select_related('user').order_by('-created_at')
    
    # Tìm kiếm
    search = request.GET.get('search', '')
    if search:
        shippers = shippers.filter(
            Q(user__username__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(phone__icontains=search)
        )
    
    context = {
        'managed_farm': managed_farm,
        'shippers': shippers,
        'search': search,
    }
    
    return render(request, 'store_admin_dashboard/shippers.html', context)


@login_required(login_url='/accounts/login/')
@require_store_admin
@require_permission('can_manage_shippers')
def store_admin_shipper_create(request):
    """Tạo shipper mới"""
    managed_farm = get_managed_farm(request.user)
    
    if request.method == 'POST':
        from django.contrib.auth.models import User
        
        # Lấy dữ liệu từ form
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        vehicle_number = request.POST.get('vehicle_number')
        
        try:
            # Kiểm tra username đã tồn tại chưa
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username "{username}" đã tồn tại!')
                return render(request, 'store_admin_dashboard/shipper_form.html', {
                    'managed_farm': managed_farm,
                })
            
            # Tạo user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            
            # Tạo shipper
            shipper = Shipper.objects.create(
                user=user,
                phone=phone,
                vehicle_number=vehicle_number,
                assigned_farm=managed_farm,
                status='offline'
            )
            
            messages.success(request, f'Đã tạo shipper "{user.get_full_name()}" thành công!')
            return redirect('food_store:store_admin_shippers')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    context = {
        'managed_farm': managed_farm,
    }
    
    return render(request, 'store_admin_dashboard/shipper_form.html', context)


@login_required(login_url='/accounts/login/')
@require_store_admin
@require_permission('can_manage_shippers')
def store_admin_shipper_edit(request, pk):
    """Sửa thông tin shipper"""
    managed_farm = get_managed_farm(request.user)
    
    shipper = get_object_or_404(
        Shipper.objects.filter(assigned_farm=managed_farm).select_related('user'),
        pk=pk
    )
    
    if request.method == 'POST':
        # Cập nhật thông tin user
        shipper.user.first_name = request.POST.get('first_name')
        shipper.user.last_name = request.POST.get('last_name')
        shipper.user.email = request.POST.get('email')
        
        # Đổi password nếu có
        new_password = request.POST.get('password')
        if new_password:
            shipper.user.set_password(new_password)
        
        shipper.user.save()
        
        # Cập nhật thông tin shipper
        shipper.phone = request.POST.get('phone')
        shipper.vehicle_number = request.POST.get('vehicle_number')
        shipper.status = request.POST.get('status')
        
        try:
            shipper.save()
            messages.success(request, f'Đã cập nhật shipper "{shipper.user.get_full_name()}" thành công!')
            return redirect('food_store:store_admin_shippers')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    context = {
        'managed_farm': managed_farm,
        'shipper': shipper,
    }
    
    return render(request, 'store_admin_dashboard/shipper_form.html', context)


@login_required(login_url='/accounts/login/')
@require_store_admin
@require_permission('can_manage_shippers')
def store_admin_shipper_delete(request, pk):
    """Xóa shipper"""
    managed_farm = get_managed_farm(request.user)
    
    shipper = get_object_or_404(
        Shipper.objects.filter(assigned_farm=managed_farm).select_related('user'),
        pk=pk
    )
    
    if request.method == 'POST':
        shipper_name = shipper.user.get_full_name() or shipper.user.username
        user = shipper.user
        shipper.delete()
        user.delete()  # Xóa cả user
        messages.success(request, f'Đã xóa shipper "{shipper_name}" thành công!')
        return redirect('food_store:store_admin_shippers')
    
    context = {
        'managed_farm': managed_farm,
        'shipper': shipper,
    }
    
    return render(request, 'store_admin_dashboard/shipper_confirm_delete.html', context)


@login_required(login_url='/accounts/login/')
@require_store_admin
@require_permission('can_view_reports')
def store_admin_reports(request):
    """Báo cáo thống kê chi nhánh"""
    managed_farm = get_managed_farm(request.user)
    
    from django.db.models.functions import TruncDate
    from food_store.models import OrderItem, InventoryReport
    
    # Thống kê theo ngày (7 ngày gần nhất)
    seven_days_ago = timezone.now() - timedelta(days=7)
    daily_orders = Order.objects.filter(
        assigned_farm=managed_farm,
        created_at__gte=seven_days_ago
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        count=Count('id'),
        revenue=Sum('total_amount')
    ).order_by('date')
    
    # Thống kê theo trạng thái đơn hàng
    order_status_stats = Order.objects.filter(
        assigned_farm=managed_farm
    ).values('status').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Top sản phẩm bán chạy
    top_products = OrderItem.objects.filter(
        product__farm=managed_farm
    ).values(
        'product__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('price')
    ).order_by('-total_quantity')[:10]
    
    # Báo cáo kiểm kê
    inventory_reports = InventoryReport.objects.filter(
        farm=managed_farm
    ).select_related('created_by').order_by('-report_date')[:10]
    
    context = {
        'managed_farm': managed_farm,
        'daily_orders': daily_orders,
        'order_status_stats': order_status_stats,
        'top_products': top_products,
        'inventory_reports': inventory_reports,
    }
    
    return render(request, 'store_admin_dashboard/reports.html', context)


@login_required(login_url='/accounts/login/')
@require_store_admin
def store_admin_order_detail(request, pk):
    """Xem chi tiết đơn hàng"""
    managed_farm = get_managed_farm(request.user)
    
    order = get_object_or_404(
        Order.objects.filter(assigned_farm=managed_farm).select_related(
            'customer__user',
            'assigned_farm',
            'assigned_shipper',
            'delivery_zone'
        ).prefetch_related('items__product'),
        pk=pk
    )
    
    context = {
        'managed_farm': managed_farm,
        'order': order,
        'order_items': order.items.all(),
        'status_choices': Order.STATUS_CHOICES,
    }
    
    return render(request, 'store_admin_dashboard/order_detail.html', context)


@login_required(login_url='/accounts/login/')
@require_store_admin
@require_permission('can_manage_orders')
def store_admin_order_update_status(request, pk):
    """Cập nhật trạng thái đơn hàng"""
    managed_farm = get_managed_farm(request.user)
    
    order = get_object_or_404(
        Order.objects.filter(assigned_farm=managed_farm),
        pk=pk
    )
    
    if request.method == 'POST':
        from django.http import JsonResponse
        
        new_status = request.POST.get('status')
        
        # Validate status
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status not in valid_statuses:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Trạng thái không hợp lệ'})
            messages.error(request, 'Trạng thái không hợp lệ!')
            return redirect('food_store:store_admin_orders')
        
        # Cập nhật trạng thái
        old_status = order.status
        order.status = new_status
        
        # Tự động cập nhật delivered_at khi chuyển sang delivered
        if new_status == 'delivered' and old_status != 'delivered':
            order.delivered_at = timezone.now()
            # Nếu COD, tự động cập nhật payment
            if order.payment_method == 'cod':
                order.payment_status = 'completed'
                order.payment_amount = order.total_amount
                order.payment_date = timezone.now()
        
        order.save()
        
        # Response cho AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'Đã cập nhật trạng thái đơn hàng #{order.id}',
                'new_status': order.get_status_display()
            })
        
        messages.success(request, f'Đã cập nhật trạng thái đơn hàng #{order.id}')
        return redirect('food_store:store_admin_orders')
    
    context = {
        'managed_farm': managed_farm,
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'store_admin_dashboard/order_update_status.html', context)


# ==================== EXPORT FUNCTIONS ====================

@login_required(login_url='/accounts/login/')
@require_store_admin
@require_permission('can_manage_inventory')
def export_transactions_pdf(request):
    """Xuất danh sách giao dịch kho ra PDF"""
    from food_store.export_utils import export_stock_transactions_pdf
    
    managed_farm = get_managed_farm(request.user)
    transactions = StockTransaction.objects.filter(
        farm=managed_farm
    ).select_related('product', 'supplier').order_by('-created_at')
    
    pdf_data = export_stock_transactions_pdf(transactions, managed_farm.name)
    
    response = HttpResponse(pdf_data, content_type='application/pdf')
    filename = f"XuatNhapKho_{managed_farm.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@login_required(login_url='/accounts/login/')
@require_store_admin
@require_permission('can_manage_inventory')
def export_transactions_excel(request):
    """Xuất danh sách giao dịch kho ra Excel"""
    from food_store.export_utils import export_stock_transactions_excel
    
    managed_farm = get_managed_farm(request.user)
    transactions = StockTransaction.objects.filter(
        farm=managed_farm
    ).select_related('product', 'supplier').order_by('-created_at')
    
    excel_data = export_stock_transactions_excel(transactions, managed_farm.name)
    
    response = HttpResponse(
        excel_data,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"XuatNhapKho_{managed_farm.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@login_required(login_url='/accounts/login/')
@require_store_admin
@require_permission('can_manage_inventory')
def export_inventory_pdf(request):
    """Xuất báo cáo tồn kho ra PDF"""
    from food_store.export_utils import export_inventory_report_pdf
    
    managed_farm = get_managed_farm(request.user)
    products = Product.objects.filter(
        farm=managed_farm
    ).select_related('category').order_by('name')
    
    pdf_data = export_inventory_report_pdf(products, managed_farm.name)
    
    response = HttpResponse(pdf_data, content_type='application/pdf')
    filename = f"BaoCaoTonKho_{managed_farm.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@login_required(login_url='/accounts/login/')
@require_store_admin
@require_permission('can_manage_inventory')
def export_inventory_excel(request):
    """Xuất báo cáo tồn kho ra Excel"""
    from food_store.export_utils import export_inventory_report_excel
    
    managed_farm = get_managed_farm(request.user)
    products = Product.objects.filter(
        farm=managed_farm
    ).select_related('category').order_by('name')
    
    excel_data = export_inventory_report_excel(products, managed_farm.name)
    
    response = HttpResponse(
        excel_data,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"BaoCaoTonKho_{managed_farm.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response
