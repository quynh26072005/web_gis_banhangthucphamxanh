"""
Custom Admin Dashboard Views
Trang admin riêng biệt với user site
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import timedelta
from food_store.models import (
    Order, Product, Farm, Customer, 
    StockTransaction, StockAlert, Supplier, Shipper
)


def is_staff_user(user):
    """Kiểm tra user có phải staff không"""
    return user.is_staff


def check_login_status(request):
    """Trang kiểm tra trạng thái đăng nhập"""
    return render(request, 'check_login_status.html')


@login_required(login_url='/admin-panel/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_dashboard(request):
    """Trang dashboard admin chính"""
    
    # Thống kê tổng quan
    total_orders = Order.objects.count()
    total_products = Product.objects.count()
    total_customers = Customer.objects.count()
    total_farms = Farm.objects.count()
    
    # Doanh thu
    total_revenue = Order.objects.filter(
        status='delivered'
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Đơn hàng hôm nay
    today = timezone.now().date()
    orders_today = Order.objects.filter(created_at__date=today).count()
    
    # Đơn hàng chờ xử lý
    pending_orders = Order.objects.filter(status='pending').count()
    
    # Cảnh báo tồn kho
    stock_alerts = StockAlert.objects.filter(is_resolved=False).count()
    
    # Đơn hàng gần nhất
    recent_orders = Order.objects.select_related(
        'customer', 'assigned_farm'
    ).order_by('-created_at')[:10]
    
    # Sản phẩm sắp hết
    low_stock_products = Product.objects.filter(
        stock_quantity__lt=20
    ).order_by('stock_quantity')[:10]
    
    # Doanh thu 7 ngày gần nhất
    last_7_days = []
    revenue_7_days = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        revenue = Order.objects.filter(
            created_at__date=date,
            status='delivered'
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        last_7_days.append(date.strftime('%d/%m'))
        revenue_7_days.append(float(revenue))
    
    # Top sản phẩm bán chạy
    top_products = Product.objects.annotate(
        total_sold=Count('orderitem')
    ).order_by('-total_sold')[:5]
    
    context = {
        'total_orders': total_orders,
        'total_products': total_products,
        'total_customers': total_customers,
        'total_farms': total_farms,
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
    
    return render(request, 'admin_dashboard/dashboard.html', context)


@login_required(login_url='/admin-panel/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_orders(request):
    """Quản lý đơn hàng"""
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    
    orders = Order.objects.select_related(
        'customer', 'assigned_farm'
    ).order_by('-created_at')
    
    # Filter theo status
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    # Phân trang - 20 đơn hàng mỗi trang
    paginator = Paginator(orders, 20)
    page = request.GET.get('page', 1)
    
    try:
        orders_page = paginator.page(page)
    except PageNotAnInteger:
        orders_page = paginator.page(1)
    except EmptyPage:
        orders_page = paginator.page(paginator.num_pages)
    
    context = {
        'orders': orders_page,
        'current_status': status,
        'paginator': paginator,
    }
    
    return render(request, 'admin_dashboard/orders.html', context)


@login_required(login_url='/admin-panel/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_products(request):
    """Quản lý sản phẩm"""
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    
    products = Product.objects.select_related(
        'farm', 'category'
    ).order_by('-created_at')
    
    # Phân trang - 20 sản phẩm mỗi trang
    paginator = Paginator(products, 20)
    page = request.GET.get('page', 1)
    
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)
    
    context = {
        'products': products_page,
        'paginator': paginator,
    }
    
    return render(request, 'admin_dashboard/products.html', context)


@login_required(login_url='/admin-panel/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_inventory(request):
    """Quản lý kho"""
    from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
    
    transactions = StockTransaction.objects.select_related(
        'product', 'farm', 'supplier'
    ).order_by('-created_at')
    
    # Phân trang - 30 giao dịch mỗi trang
    paginator = Paginator(transactions, 30)
    page = request.GET.get('page', 1)
    
    try:
        transactions_page = paginator.page(page)
    except PageNotAnInteger:
        transactions_page = paginator.page(1)
    except EmptyPage:
        transactions_page = paginator.page(paginator.num_pages)
    
    alerts = StockAlert.objects.filter(
        is_resolved=False
    ).select_related('product', 'farm')
    
    suppliers = Supplier.objects.filter(is_active=True)
    
    context = {
        'transactions': transactions_page,
        'alerts': alerts,
        'paginator': paginator,
        'suppliers': suppliers,
    }
    
    return render(request, 'admin_dashboard/inventory.html', context)


# ============= QUẢN LÝ KHÁCH HÀNG =============
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_customers(request):
    """Quản lý khách hàng"""
    customers = Customer.objects.select_related('user').order_by('-created_at')
    
    # Tìm kiếm
    search = request.GET.get('search', '')
    if search:
        customers = customers.filter(
            Q(user__username__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(phone__icontains=search)
        )
    
    context = {
        'customers': customers,
        'search': search,
    }
    return render(request, 'admin_dashboard/customers.html', context)


# ============= QUẢN LÝ CỬA HÀNG/NÔNG TRẠI =============
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_farms(request):
    """Quản lý cửa hàng/nông trại"""
    farms = Farm.objects.annotate(
        product_count=Count('product')
    ).order_by('-created_at')
    
    context = {
        'farms': farms,
    }
    return render(request, 'admin_dashboard/farms.html', context)


# ============= QUẢN LÝ DANH MỤC =============
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_categories(request):
    """Quản lý danh mục sản phẩm"""
    from food_store.models import Category
    
    categories = Category.objects.annotate(
        product_count=Count('product')
    ).order_by('name')
    
    context = {
        'categories': categories,
    }
    return render(request, 'admin_dashboard/categories.html', context)


# ============= QUẢN LÝ KHU VỰC GIAO HÀNG =============
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_delivery_zones(request):
    """Quản lý khu vực giao hàng"""
    from food_store.models import DeliveryZone
    
    zones = DeliveryZone.objects.annotate(
        order_count=Count('order')
    ).order_by('name')
    
    context = {
        'zones': zones,
    }
    return render(request, 'admin_dashboard/delivery_zones.html', context)


# ============= QUẢN LÝ NHÀ CUNG CẤP =============
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_suppliers(request):
    """Quản lý nhà cung cấp"""
    suppliers = Supplier.objects.annotate(
        transaction_count=Count('stocktransaction')
    ).order_by('name')
    
    context = {
        'suppliers': suppliers,
    }
    return render(request, 'admin_dashboard/suppliers.html', context)


# ============= BÁO CÁO THỐNG KÊ =============
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_reports(request):
    """Báo cáo thống kê chi tiết"""
    from food_store.models import InventoryReport
    from django.db.models.functions import TruncDate
    
    # Thống kê theo ngày (7 ngày gần nhất)
    seven_days_ago = timezone.now() - timedelta(days=7)
    daily_orders = Order.objects.filter(
        created_at__gte=seven_days_ago
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        count=Count('id'),
        revenue=Sum('total_amount')
    ).order_by('date')
    
    # Thống kê theo trạng thái đơn hàng
    order_status_stats = Order.objects.values('status').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Top sản phẩm bán chạy
    from food_store.models import OrderItem
    top_products = OrderItem.objects.values(
        'product__name', 'product__farm__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('price')
    ).order_by('-total_quantity')[:10]
    
    # Báo cáo kiểm kê
    inventory_reports = InventoryReport.objects.select_related(
        'created_by'
    ).order_by('-report_date')[:10]
    
    context = {
        'daily_orders': daily_orders,
        'order_status_stats': order_status_stats,
        'top_products': top_products,
        'inventory_reports': inventory_reports,
    }
    return render(request, 'admin_dashboard/reports.html', context)


# ============= CRUD KHÁCH HÀNG =============
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_customer_create(request):
    """Thêm khách hàng mới"""
    from django.contrib.auth.models import User
    from django.contrib import messages
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        try:
            # Tạo user
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            
            # Tạo customer
            Customer.objects.create(
                user=user,
                phone=phone,
                address=address
            )
            
            messages.success(request, 'Thêm khách hàng thành công!')
            return redirect('food_store:admin_customers')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    return render(request, 'admin_dashboard/customer_form.html', {'action': 'create'})


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_customer_edit(request, pk):
    """Sửa thông tin khách hàng"""
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        customer.user.email = request.POST.get('email')
        customer.user.first_name = request.POST.get('first_name')
        customer.user.last_name = request.POST.get('last_name')
        customer.phone = request.POST.get('phone')
        customer.address = request.POST.get('address')
        
        customer.user.save()
        customer.save()
        
        messages.success(request, 'Cập nhật thành công!')
        return redirect('food_store:admin_customers')
    
    return render(request, 'admin_dashboard/customer_form.html', {
        'action': 'edit',
        'customer': customer
    })


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_customer_delete(request, pk):
    """Xóa khách hàng"""
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    
    customer = get_object_or_404(Customer, pk=pk)
    
    if request.method == 'POST':
        customer.user.delete()  # Cascade delete customer
        messages.success(request, 'Xóa khách hàng thành công!')
        return redirect('food_store:admin_customers')
    
    return render(request, 'admin_dashboard/customer_confirm_delete.html', {
        'customer': customer
    })


# ============= CRUD CỬA HÀNG =============
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_farm_create(request):
    """Thêm cửa hàng mới"""
    from django.contrib import messages
    
    if request.method == 'POST':
        try:
            # Xử lý latitude/longitude an toàn
            lat_str = request.POST.get('latitude', '').strip()
            lng_str = request.POST.get('longitude', '').strip()
            
            Farm.objects.create(
                name=request.POST.get('name'),
                address=request.POST.get('address'),
                phone=request.POST.get('phone'),
                description=request.POST.get('description'),
                latitude=float(lat_str) if lat_str else 0,
                longitude=float(lng_str) if lng_str else 0,
                organic_certified=request.POST.get('organic_certified') == 'on'
            )
            messages.success(request, 'Thêm cửa hàng thành công!')
            return redirect('food_store:admin_farms')
        except ValueError as e:
            messages.error(request, f'Lỗi: Tọa độ không hợp lệ. Vui lòng chọn vị trí trên bản đồ.')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    return render(request, 'admin_dashboard/farm_form.html', {'action': 'create'})


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_farm_edit(request, pk):
    """Sửa thông tin cửa hàng"""
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    
    farm = get_object_or_404(Farm, pk=pk)
    
    if request.method == 'POST':
        try:
            farm.name = request.POST.get('name')
            farm.address = request.POST.get('address')
            farm.phone = request.POST.get('phone')
            farm.description = request.POST.get('description')
            
            # Xử lý latitude/longitude an toàn
            lat_str = request.POST.get('latitude', '').strip()
            lng_str = request.POST.get('longitude', '').strip()
            farm.latitude = float(lat_str) if lat_str else 0
            farm.longitude = float(lng_str) if lng_str else 0
            
            farm.organic_certified = request.POST.get('organic_certified') == 'on'
            farm.save()
            
            messages.success(request, 'Cập nhật thành công!')
            return redirect('food_store:admin_farms')
        except ValueError as e:
            messages.error(request, f'Lỗi: Tọa độ không hợp lệ. Vui lòng chọn vị trí trên bản đồ.')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    return render(request, 'admin_dashboard/farm_form.html', {
        'action': 'edit',
        'farm': farm
    })


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_farm_delete(request, pk):
    """Xóa cửa hàng"""
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    
    farm = get_object_or_404(Farm, pk=pk)
    
    if request.method == 'POST':
        farm.delete()
        messages.success(request, 'Xóa cửa hàng thành công!')
        return redirect('food_store:admin_farms')
    
    return render(request, 'admin_dashboard/farm_confirm_delete.html', {
        'farm': farm
    })


# ============= CRUD DANH MỤC =============
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_category_create(request):
    """Thêm danh mục mới"""
    from django.contrib import messages
    from food_store.models import Category
    
    if request.method == 'POST':
        try:
            Category.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description')
            )
            messages.success(request, 'Thêm danh mục thành công!')
            return redirect('food_store:admin_categories')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    return render(request, 'admin_dashboard/category_form.html', {'action': 'create'})


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_category_edit(request, pk):
    """Sửa danh mục"""
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    from food_store.models import Category
    
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        category.save()
        
        messages.success(request, 'Cập nhật thành công!')
        return redirect('food_store:admin_categories')
    
    return render(request, 'admin_dashboard/category_form.html', {
        'action': 'edit',
        'category': category
    })


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_category_delete(request, pk):
    """Xóa danh mục"""
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    from food_store.models import Category
    
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Xóa danh mục thành công!')
        return redirect('food_store:admin_categories')
    
    return render(request, 'admin_dashboard/category_confirm_delete.html', {
        'category': category
    })


# ============= CRUD KHU VỰC GIAO HÀNG =============
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_zone_create(request):
    """Thêm khu vực giao hàng mới"""
    from django.contrib import messages
    from food_store.models import DeliveryZone
    
    if request.method == 'POST':
        try:
            DeliveryZone.objects.create(
                name=request.POST.get('name'),
                area_description=request.POST.get('area_description'),
                delivery_fee=float(request.POST.get('delivery_fee', 0)),
                delivery_time=request.POST.get('delivery_time'),
                is_active=request.POST.get('is_active') == 'on'
            )
            messages.success(request, 'Thêm khu vực thành công!')
            return redirect('food_store:admin_delivery_zones')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    return render(request, 'admin_dashboard/zone_form.html', {'action': 'create'})


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_zone_edit(request, pk):
    """Sửa khu vực giao hàng"""
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    from food_store.models import DeliveryZone
    
    zone = get_object_or_404(DeliveryZone, pk=pk)
    
    if request.method == 'POST':
        zone.name = request.POST.get('name')
        zone.area_description = request.POST.get('area_description')
        zone.delivery_fee = float(request.POST.get('delivery_fee', 0))
        zone.delivery_time = request.POST.get('delivery_time')
        zone.is_active = request.POST.get('is_active') == 'on'
        zone.save()
        
        messages.success(request, 'Cập nhật thành công!')
        return redirect('food_store:admin_delivery_zones')
    
    return render(request, 'admin_dashboard/zone_form.html', {
        'action': 'edit',
        'zone': zone
    })


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_zone_delete(request, pk):
    """Xóa khu vực giao hàng"""
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    from food_store.models import DeliveryZone
    
    zone = get_object_or_404(DeliveryZone, pk=pk)
    
    if request.method == 'POST':
        zone.delete()
        messages.success(request, 'Xóa khu vực thành công!')
        return redirect('food_store:admin_delivery_zones')
    
    return render(request, 'admin_dashboard/zone_confirm_delete.html', {
        'zone': zone
    })


# ============= CRUD NHÀ CUNG CẤP =============
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_supplier_create(request):
    """Thêm nhà cung cấp mới"""
    from django.contrib import messages
    
    if request.method == 'POST':
        try:
            Supplier.objects.create(
                name=request.POST.get('name'),
                contact_person=request.POST.get('contact_person'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address')
            )
            messages.success(request, 'Thêm nhà cung cấp thành công!')
            return redirect('food_store:admin_suppliers')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    return render(request, 'admin_dashboard/supplier_form.html', {'action': 'create'})


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_supplier_edit(request, pk):
    """Sửa nhà cung cấp"""
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        supplier.name = request.POST.get('name')
        supplier.contact_person = request.POST.get('contact_person')
        supplier.email = request.POST.get('email')
        supplier.phone = request.POST.get('phone')
        supplier.address = request.POST.get('address')
        supplier.save()
        
        messages.success(request, 'Cập nhật thành công!')
        return redirect('food_store:admin_suppliers')
    
    return render(request, 'admin_dashboard/supplier_form.html', {
        'action': 'edit',
        'supplier': supplier
    })


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_supplier_delete(request, pk):
    """Xóa nhà cung cấp"""
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        supplier.delete()
        messages.success(request, 'Xóa nhà cung cấp thành công!')
        return redirect('food_store:admin_suppliers')
    
    return render(request, 'admin_dashboard/supplier_confirm_delete.html', {
        'supplier': supplier
    })


# ============= CRUD SẢN PHẨM =============
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_product_create(request):
    """Thêm sản phẩm mới"""
    from django.contrib import messages
    from food_store.models import Category
    
    categories = Category.objects.all()
    farms = Farm.objects.all()
    
    if request.method == 'POST':
        try:
            # Xử lý upload hình ảnh
            image = request.FILES.get('image')
            
            product = Product.objects.create(
                name=request.POST.get('name'),
                category_id=request.POST.get('category'),
                farm_id=request.POST.get('farm'),
                description=request.POST.get('description'),
                price=float(request.POST.get('price', 0)),
                unit=request.POST.get('unit'),
                stock_quantity=int(request.POST.get('stock_quantity', 0)),
                is_available=request.POST.get('is_available') == 'on',
                nutritional_info=request.POST.get('nutritional_info', ''),
                image=image
            )
            
            messages.success(request, 'Thêm sản phẩm thành công!')
            return redirect('food_store:admin_products')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    return render(request, 'admin_dashboard/product_form.html', {
        'action': 'create',
        'categories': categories,
        'farms': farms
    })


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_product_edit(request, pk):
    """Sửa sản phẩm"""
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    from food_store.models import Category
    
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()
    farms = Farm.objects.all()
    
    if request.method == 'POST':
        try:
            product.name = request.POST.get('name')
            product.category_id = request.POST.get('category')
            product.farm_id = request.POST.get('farm')
            product.description = request.POST.get('description')
            product.price = float(request.POST.get('price', 0))
            product.unit = request.POST.get('unit')
            product.stock_quantity = int(request.POST.get('stock_quantity', 0))
            product.is_available = request.POST.get('is_available') == 'on'
            product.nutritional_info = request.POST.get('nutritional_info', '')
            
            # Xử lý upload hình ảnh mới (nếu có)
            if request.FILES.get('image'):
                product.image = request.FILES.get('image')
            
            product.save()
            
            messages.success(request, 'Cập nhật thành công!')
            return redirect('food_store:admin_products')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    return render(request, 'admin_dashboard/product_form.html', {
        'action': 'edit',
        'product': product,
        'categories': categories,
        'farms': farms
    })


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_product_delete(request, pk):
    """Xóa sản phẩm"""
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Xóa sản phẩm thành công!')
        return redirect('food_store:admin_products')
    
    return render(request, 'admin_dashboard/product_confirm_delete.html', {
        'product': product
    })


# ============= QUẢN LÝ KHO - NHẬP HÀNG =============
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_stock_import(request):
    """Nhập hàng vào kho"""
    from django.contrib import messages
    
    products = Product.objects.select_related('farm', 'category').all()
    suppliers = Supplier.objects.filter(is_active=True)
    farms = Farm.objects.all()
    
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product')
            farm_id = request.POST.get('farm')
            quantity = int(request.POST.get('quantity', 0))
            unit_price = float(request.POST.get('unit_price', 0))
            supplier_id = request.POST.get('supplier')
            reference_number = request.POST.get('reference_number', '')
            notes = request.POST.get('notes', '')
            
            # Validation
            if quantity <= 0:
                messages.error(request, 'Số lượng phải lớn hơn 0!')
                return redirect('food_store:admin_stock_import')
            
            if unit_price < 0:
                messages.error(request, 'Đơn giá không được âm!')
                return redirect('food_store:admin_stock_import')
            
            product = Product.objects.get(id=product_id)
            
            # Tạo giao dịch nhập kho
            # Model StockTransaction.save() sẽ TỰ ĐỘNG cập nhật tồn kho
            transaction = StockTransaction.objects.create(
                product_id=product_id,
                farm_id=farm_id,
                transaction_type='import',  # ✅ SỬA: 'in' → 'import'
                quantity=quantity,
                unit_price=unit_price,
                supplier_id=supplier_id if supplier_id else None,
                reference_number=reference_number,
                notes=notes,
                created_by=request.user
            )
            
            # ✅ XÓA: Không cần cập nhật tồn kho thủ công
            # Model đã tự động cập nhật trong save()
            
            messages.success(request, f'Nhập hàng thành công! Đã thêm {quantity} {product.unit} vào kho. Tồn kho mới: {transaction.stock_after}')
            return redirect('food_store:admin_inventory')
        except Product.DoesNotExist:
            messages.error(request, 'Sản phẩm không tồn tại!')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    return render(request, 'admin_dashboard/stock_import_form.html', {
        'products': products,
        'suppliers': suppliers,
        'farms': farms
    })


# ============= QUẢN LÝ KHO - XUẤT HÀNG =============
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_stock_export(request):
    """Xuất hàng ra khỏi kho"""
    from django.contrib import messages
    
    products = Product.objects.filter(stock_quantity__gt=0).select_related('farm', 'category')
    farms = Farm.objects.all()
    
    if request.method == 'POST':
        try:
            product_id = request.POST.get('product')
            farm_id = request.POST.get('farm')
            quantity = int(request.POST.get('quantity', 0))
            unit_price = float(request.POST.get('unit_price', 0))
            reference_number = request.POST.get('reference_number', '')
            notes = request.POST.get('notes', '')
            
            # Validation
            if quantity <= 0:
                messages.error(request, 'Số lượng phải lớn hơn 0!')
                return redirect('food_store:admin_stock_export')
            
            if unit_price < 0:
                messages.error(request, 'Đơn giá không được âm!')
                return redirect('food_store:admin_stock_export')
            
            product = Product.objects.get(id=product_id)
            
            # Kiểm tra tồn kho
            if product.stock_quantity < quantity:
                messages.error(request, f'Không đủ hàng trong kho! Tồn kho hiện tại: {product.stock_quantity} {product.unit}')
                return redirect('food_store:admin_stock_export')
            
            # Tạo giao dịch xuất kho
            # Model StockTransaction.save() sẽ TỰ ĐỘNG cập nhật tồn kho
            transaction = StockTransaction.objects.create(
                product_id=product_id,
                farm_id=farm_id,
                transaction_type='export',  # ✅ SỬA: 'out' → 'export'
                quantity=quantity,
                unit_price=unit_price,
                reference_number=reference_number,
                notes=notes,
                created_by=request.user
            )
            
            # ✅ XÓA: Không cần cập nhật tồn kho thủ công
            # Model đã tự động cập nhật trong save()
            
            messages.success(request, f'Xuất hàng thành công! Đã xuất {quantity} {product.unit} ra khỏi kho. Tồn kho còn: {transaction.stock_after}')
            return redirect('food_store:admin_inventory')
        except Product.DoesNotExist:
            messages.error(request, 'Sản phẩm không tồn tại!')
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    return render(request, 'admin_dashboard/stock_export_form.html', {
        'products': products,
        'farms': farms
    })


# ============= XÓA GIAO DỊCH KHO =============
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_transaction_delete(request, pk):
    """Xóa giao dịch kho (không khuyến khích)"""
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    
    transaction = get_object_or_404(StockTransaction, pk=pk)
    
    if request.method == 'POST':
        # Hoàn tác thay đổi tồn kho
        product = transaction.product
        if transaction.transaction_type == 'in':
            product.stock_quantity -= transaction.quantity
        else:
            product.stock_quantity += transaction.quantity
        product.save()
        
        transaction.delete()
        messages.warning(request, 'Đã xóa giao dịch và hoàn tác thay đổi tồn kho!')
        return redirect('food_store:admin_inventory')
    
    return render(request, 'admin_dashboard/transaction_confirm_delete.html', {
        'transaction': transaction
    })


# ============= CẬP NHẬT TRẠNG THÁI ĐƠN HÀNG =============
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_order_update_status(request, pk):
    """Cập nhật trạng thái đơn hàng"""
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    from django.http import JsonResponse
    from django.utils import timezone
    
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        
        # Validate status
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status not in valid_statuses:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Trạng thái không hợp lệ'})
            messages.error(request, 'Trạng thái không hợp lệ!')
            return redirect('food_store:admin_orders')
        
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
        
        messages.success(request, f'Đã cập nhật trạng thái đơn hàng #{order.id} thành "{order.get_status_display()}"')
        return redirect('food_store:admin_orders')
    
    # GET request - hiển thị form
    context = {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'admin_dashboard/order_update_status.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_order_detail(request, pk):
    """Xem chi tiết đơn hàng"""
    from django.shortcuts import get_object_or_404
    
    order = get_object_or_404(
        Order.objects.select_related(
            'customer__user',
            'assigned_farm',
            'delivery_zone'
        ).prefetch_related('items__product'),
        pk=pk
    )
    
    context = {
        'order': order,
        'order_items': order.items.all(),
        'status_choices': Order.STATUS_CHOICES,
    }
    
    return render(request, 'admin_dashboard/order_detail.html', context)


# ============= QUẢN LÝ SHIPPER =============
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_shippers(request):
    """Quản lý shipper"""
    from food_store.models import Shipper
    from django.contrib.auth.models import User
    
    shippers = Shipper.objects.select_related('user').order_by('-created_at')
    
    # Lấy danh sách user chưa có shipper profile
    users_without_shipper = User.objects.exclude(
        id__in=shippers.values_list('user_id', flat=True)
    ).order_by('username')
    
    # Tìm kiếm
    search = request.GET.get('search', '')
    if search:
        shippers = shippers.filter(
            Q(user__username__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(phone__icontains=search) |
            Q(vehicle_number__icontains=search)
        )
    
    context = {
        'shippers': shippers,
        'users_without_shipper': users_without_shipper,
        'search': search,
    }
    return render(request, 'admin_dashboard/shippers.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_shipper_create(request):
    """Tạo shipper mới hoặc phân quyền cho user hiện có"""
    from django.contrib import messages
    from django.contrib.auth.models import User
    from food_store.models import Shipper
    
    # Lấy danh sách user chưa có shipper profile
    available_users = User.objects.exclude(
        id__in=Shipper.objects.values_list('user_id', flat=True)
    ).order_by('username')
    
    if request.method == 'POST':
        try:
            action_type = request.POST.get('action_type')  # 'existing' hoặc 'new'
            
            if action_type == 'existing':
                # Phân quyền cho user hiện có
                user_id = request.POST.get('user_id')
                user = User.objects.get(id=user_id)
                
                Shipper.objects.create(
                    user=user,
                    phone=request.POST.get('phone'),
                    vehicle_number=request.POST.get('vehicle_number'),
                    status='offline'
                )
                
                messages.success(request, f'Đã phân quyền shipper cho {user.get_full_name() or user.username}!')
                
            else:
                # Tạo user mới và shipper
                username = request.POST.get('username')
                password = request.POST.get('password')
                email = request.POST.get('email')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                phone = request.POST.get('phone')
                vehicle_number = request.POST.get('vehicle_number')
                
                # Tạo user
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Tạo shipper profile
                Shipper.objects.create(
                    user=user,
                    phone=phone,
                    vehicle_number=vehicle_number,
                    status='offline'
                )
                
                messages.success(request, f'Đã tạo tài khoản shipper mới: {username}!')
            
            return redirect('food_store:admin_shippers')
            
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    context = {
        'action': 'create',
        'available_users': available_users,
    }
    return render(request, 'admin_dashboard/shipper_form.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_shipper_edit(request, pk):
    """Sửa thông tin shipper"""
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    from food_store.models import Shipper
    
    shipper = get_object_or_404(Shipper, pk=pk)
    
    if request.method == 'POST':
        try:
            # Cập nhật thông tin user
            shipper.user.email = request.POST.get('email')
            shipper.user.first_name = request.POST.get('first_name')
            shipper.user.last_name = request.POST.get('last_name')
            shipper.user.save()
            
            # Cập nhật thông tin shipper
            shipper.phone = request.POST.get('phone')
            shipper.vehicle_number = request.POST.get('vehicle_number')
            shipper.status = request.POST.get('status')
            shipper.save()
            
            messages.success(request, 'Cập nhật thông tin shipper thành công!')
            return redirect('food_store:admin_shippers')
            
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    context = {
        'action': 'edit',
        'shipper': shipper,
    }
    return render(request, 'admin_dashboard/shipper_form.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_shipper_delete(request, pk):
    """Xóa shipper (chỉ xóa profile, không xóa user)"""
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    from food_store.models import Shipper
    
    shipper = get_object_or_404(Shipper, pk=pk)
    
    if request.method == 'POST':
        user_name = shipper.user.get_full_name() or shipper.user.username
        shipper.delete()
        messages.success(request, f'Đã xóa quyền shipper của {user_name}!')
        return redirect('food_store:admin_shippers')
    
    context = {
        'shipper': shipper,
    }
    return render(request, 'admin_dashboard/shipper_confirm_delete.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_shipper_detail(request, pk):
    """Xem chi tiết shipper và thống kê"""
    from django.shortcuts import get_object_or_404
    from food_store.models import Shipper
    from datetime import datetime, timedelta
    
    shipper = get_object_or_404(Shipper, pk=pk)
    
    # Đơn hàng đang xử lý
    active_orders = Order.objects.filter(
        assigned_shipper=shipper,
        status__in=['confirmed', 'shipping']
    ).select_related('customer__user', 'assigned_farm')
    
    # Đơn hàng hoàn thành hôm nay
    today = timezone.now().date()
    today_orders = Order.objects.filter(
        assigned_shipper=shipper,
        status='delivered',
        delivered_at__date=today
    ).select_related('customer__user', 'assigned_farm')
    
    # Lịch sử 7 ngày gần nhất
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_orders = Order.objects.filter(
        assigned_shipper=shipper,
        created_at__gte=seven_days_ago
    ).select_related('customer__user', 'assigned_farm').order_by('-created_at')
    
    # Thống kê
    total_completed = Order.objects.filter(
        assigned_shipper=shipper,
        status='delivered'
    ).count()
    
    total_earnings = Order.objects.filter(
        assigned_shipper=shipper,
        status='delivered'
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    context = {
        'shipper': shipper,
        'active_orders': active_orders,
        'today_orders': today_orders,
        'recent_orders': recent_orders,
        'total_completed': total_completed,
        'total_earnings': total_earnings,
    }
    return render(request, 'admin_dashboard/shipper_detail.html', context)



# ============= QUẢN LÝ STORE ADMIN (CHỈ SUPER ADMIN) =============
@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_store_admins(request):
    """Quản lý Store Admin (chỉ Super Admin)"""
    from food_store.models import StoreAdmin
    from django.contrib.auth.models import User
    
    store_admins = StoreAdmin.objects.select_related('user', 'farm').order_by('-created_at')
    
    # Lấy danh sách user chưa có store admin profile
    users_without_store_admin = User.objects.exclude(
        id__in=store_admins.values_list('user_id', flat=True)
    ).exclude(
        is_superuser=True
    ).order_by('username')
    
    # Tìm kiếm
    search = request.GET.get('search', '')
    if search:
        store_admins = store_admins.filter(
            Q(user__username__icontains=search) |
            Q(user__first_name__icontains=search) |
            Q(user__last_name__icontains=search) |
            Q(farm__name__icontains=search)
        )
    
    context = {
        'store_admins': store_admins,
        'users_without_store_admin': users_without_store_admin,
        'search': search,
    }
    return render(request, 'admin_dashboard/store_admins.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_store_admin_create(request):
    """Tạo Store Admin mới hoặc phân quyền cho user hiện có"""
    from django.contrib import messages
    from django.contrib.auth.models import User
    from food_store.models import StoreAdmin
    
    # Lấy danh sách user chưa có store admin profile
    available_users = User.objects.exclude(
        id__in=StoreAdmin.objects.values_list('user_id', flat=True)
    ).exclude(
        is_superuser=True
    ).order_by('username')
    
    farms = Farm.objects.all()
    
    if request.method == 'POST':
        try:
            action_type = request.POST.get('action_type')  # 'existing' hoặc 'new'
            
            if action_type == 'existing':
                # Phân quyền cho user hiện có
                user_id = request.POST.get('user_id')
                user = User.objects.get(id=user_id)
                farm_id = request.POST.get('farm_id')
                farm = Farm.objects.get(id=farm_id)
                
                StoreAdmin.objects.create(
                    user=user,
                    farm=farm,
                    phone=request.POST.get('phone'),
                    can_manage_products=request.POST.get('can_manage_products') == 'on',
                    can_manage_orders=request.POST.get('can_manage_orders') == 'on',
                    can_manage_inventory=request.POST.get('can_manage_inventory') == 'on',
                    can_manage_shippers=request.POST.get('can_manage_shippers') == 'on',
                    can_view_reports=request.POST.get('can_view_reports') == 'on',
                )
                
                messages.success(request, f'Đã phân quyền quản lý chi nhánh {farm.name} cho {user.get_full_name() or user.username}!')
                
            else:
                # Tạo user mới và store admin
                username = request.POST.get('username')
                password = request.POST.get('password')
                email = request.POST.get('email')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                phone = request.POST.get('phone')
                farm_id = request.POST.get('farm_id')
                farm = Farm.objects.get(id=farm_id)
                
                # Tạo user
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Tạo store admin profile
                StoreAdmin.objects.create(
                    user=user,
                    farm=farm,
                    phone=phone,
                    can_manage_products=request.POST.get('can_manage_products') == 'on',
                    can_manage_orders=request.POST.get('can_manage_orders') == 'on',
                    can_manage_inventory=request.POST.get('can_manage_inventory') == 'on',
                    can_manage_shippers=request.POST.get('can_manage_shippers') == 'on',
                    can_view_reports=request.POST.get('can_view_reports') == 'on',
                )
                
                messages.success(request, f'Đã tạo tài khoản quản lý chi nhánh mới: {username}!')
            
            return redirect('food_store:admin_store_admins')
            
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    context = {
        'action': 'create',
        'available_users': available_users,
        'farms': farms,
    }
    return render(request, 'admin_dashboard/store_admin_form.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_store_admin_edit(request, pk):
    """Sửa thông tin Store Admin"""
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    from food_store.models import StoreAdmin
    
    store_admin = get_object_or_404(StoreAdmin, pk=pk)
    farms = Farm.objects.all()
    
    if request.method == 'POST':
        try:
            # Cập nhật thông tin user
            store_admin.user.email = request.POST.get('email')
            store_admin.user.first_name = request.POST.get('first_name')
            store_admin.user.last_name = request.POST.get('last_name')
            store_admin.user.save()
            
            # Cập nhật thông tin store admin
            store_admin.phone = request.POST.get('phone')
            store_admin.farm_id = request.POST.get('farm_id')
            store_admin.can_manage_products = request.POST.get('can_manage_products') == 'on'
            store_admin.can_manage_orders = request.POST.get('can_manage_orders') == 'on'
            store_admin.can_manage_inventory = request.POST.get('can_manage_inventory') == 'on'
            store_admin.can_manage_shippers = request.POST.get('can_manage_shippers') == 'on'
            store_admin.can_view_reports = request.POST.get('can_view_reports') == 'on'
            store_admin.is_active = request.POST.get('is_active') == 'on'
            store_admin.save()
            
            messages.success(request, 'Cập nhật thông tin Store Admin thành công!')
            return redirect('food_store:admin_store_admins')
            
        except Exception as e:
            messages.error(request, f'Lỗi: {str(e)}')
    
    context = {
        'action': 'edit',
        'store_admin': store_admin,
        'farms': farms,
    }
    return render(request, 'admin_dashboard/store_admin_form.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_store_admin_delete(request, pk):
    """Xóa Store Admin (chỉ xóa profile, không xóa user)"""
    from django.contrib import messages
    from django.shortcuts import get_object_or_404
    from food_store.models import StoreAdmin
    
    store_admin = get_object_or_404(StoreAdmin, pk=pk)
    
    if request.method == 'POST':
        user_name = store_admin.user.get_full_name() or store_admin.user.username
        farm_name = store_admin.farm.name
        store_admin.delete()
        messages.success(request, f'Đã xóa quyền quản lý chi nhánh {farm_name} của {user_name}!')
        return redirect('food_store:admin_store_admins')
    
    context = {
        'store_admin': store_admin,
    }
    return render(request, 'admin_dashboard/store_admin_confirm_delete.html', context)


@login_required(login_url='/accounts/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_store_admin_detail(request, pk):
    """Xem chi tiết Store Admin và thống kê"""
    from django.shortcuts import get_object_or_404
    from food_store.models import StoreAdmin
    from datetime import datetime, timedelta
    
    store_admin = get_object_or_404(StoreAdmin, pk=pk)
    farm = store_admin.farm
    
    # Thống kê chi nhánh
    total_products = Product.objects.filter(farm=farm).count()
    total_orders = Order.objects.filter(assigned_farm=farm).count()
    total_shippers = Shipper.objects.filter(assigned_farm=farm).count()
    
    # Doanh thu
    total_revenue = Order.objects.filter(
        assigned_farm=farm,
        status='delivered'
    ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # Đơn hàng hôm nay
    today = timezone.now().date()
    orders_today = Order.objects.filter(
        assigned_farm=farm,
        created_at__date=today
    ).count()
    
    # Đơn hàng gần nhất
    recent_orders = Order.objects.filter(
        assigned_farm=farm
    ).select_related('customer__user').order_by('-created_at')[:10]
    
    context = {
        'store_admin': store_admin,
        'farm': farm,
        'total_products': total_products,
        'total_orders': total_orders,
        'total_shippers': total_shippers,
        'total_revenue': total_revenue,
        'orders_today': orders_today,
        'recent_orders': recent_orders,
    }
    return render(request, 'admin_dashboard/store_admin_detail.html', context)


# ==================== EXPORT FUNCTIONS FOR ADMIN ====================

@login_required(login_url='/admin-panel/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_export_transactions_pdf(request):
    """Xuất danh sách giao dịch kho ra PDF (Admin)"""
    from food_store.export_utils import export_stock_transactions_pdf
    from datetime import datetime
    from django.http import HttpResponse
    
    transactions = StockTransaction.objects.select_related(
        'product', 'farm', 'supplier'
    ).order_by('-created_at')
    
    pdf_data = export_stock_transactions_pdf(transactions, "Tất cả cửa hàng")
    
    response = HttpResponse(pdf_data, content_type='application/pdf')
    filename = f"XuatNhapKho_TatCa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@login_required(login_url='/admin-panel/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_export_transactions_excel(request):
    """Xuất danh sách giao dịch kho ra Excel (Admin)"""
    from food_store.export_utils import export_stock_transactions_excel
    from datetime import datetime
    from django.http import HttpResponse
    
    transactions = StockTransaction.objects.select_related(
        'product', 'farm', 'supplier'
    ).order_by('-created_at')
    
    excel_data = export_stock_transactions_excel(transactions, "Tất cả cửa hàng")
    
    response = HttpResponse(
        excel_data,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"XuatNhapKho_TatCa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@login_required(login_url='/admin-panel/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_export_inventory_pdf(request):
    """Xuất báo cáo tồn kho ra PDF (Admin)"""
    from food_store.export_utils import export_inventory_report_pdf
    from datetime import datetime
    from django.http import HttpResponse
    
    products = Product.objects.select_related('category', 'farm').order_by('farm__name', 'name')
    
    pdf_data = export_inventory_report_pdf(products, "Tất cả cửa hàng")
    
    response = HttpResponse(pdf_data, content_type='application/pdf')
    filename = f"BaoCaoTonKho_TatCa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response


@login_required(login_url='/admin-panel/login/')
@user_passes_test(is_staff_user, login_url='/')
def admin_export_inventory_excel(request):
    """Xuất báo cáo tồn kho ra Excel (Admin)"""
    from food_store.export_utils import export_inventory_report_excel
    from datetime import datetime
    from django.http import HttpResponse
    
    products = Product.objects.select_related('category', 'farm').order_by('farm__name', 'name')
    
    excel_data = export_inventory_report_excel(products, "Tất cả cửa hàng")
    
    response = HttpResponse(
        excel_data,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    filename = f"BaoCaoTonKho_TatCa_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response
