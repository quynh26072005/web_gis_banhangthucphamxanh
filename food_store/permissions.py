"""
Permission helpers for Store Admin system
"""
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.template.loader import render_to_string
from functools import wraps


def is_super_admin(user):
    """Kiểm tra user có phải super admin không"""
    return user.is_authenticated and (user.is_superuser or user.is_staff)


def is_store_admin(user):
    """Kiểm tra user có phải store admin không"""
    if not user.is_authenticated:
        return False
    
    try:
        from food_store.models import StoreAdmin
        return StoreAdmin.objects.filter(user=user, is_active=True).exists()
    except:
        return False


def is_admin_user(user):
    """Kiểm tra user có phải admin (super hoặc store) không"""
    return is_super_admin(user) or is_store_admin(user)


def get_user_role(user):
    """Lấy role của user"""
    if not user.is_authenticated:
        return 'guest'
    
    if is_super_admin(user):
        return 'super_admin'
    
    if is_store_admin(user):
        return 'store_admin'
    
    # Check shipper
    try:
        from food_store.models import Shipper
        if Shipper.objects.filter(user=user).exists():
            return 'shipper'
    except:
        pass
    
    # Check customer
    try:
        from food_store.models import Customer
        if Customer.objects.filter(user=user).exists():
            return 'customer'
    except:
        pass
    
    return 'user'


def get_managed_farm(user):
    """Lấy farm mà user quản lý (nếu là store admin)"""
    if not is_store_admin(user):
        return None
    
    try:
        from food_store.models import StoreAdmin
        store_admin = StoreAdmin.objects.select_related('farm').get(
            user=user,
            is_active=True
        )
        return store_admin.farm
    except:
        return None


def require_super_admin(view_func):
    """Decorator yêu cầu super admin - Redirect đến 403 nếu không có quyền"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Vui lòng đăng nhập để tiếp tục!')
            return redirect('food_store:custom_login')
        
        if not is_super_admin(request.user):
            # Render 403 page
            html = render_to_string('errors/403.html', request=request)
            return HttpResponseForbidden(html)
        
        return view_func(request, *args, **kwargs)
    return wrapper


def require_store_admin(view_func):
    """Decorator yêu cầu store admin - Redirect đến 403 nếu không có quyền"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Vui lòng đăng nhập để tiếp tục!')
            return redirect('food_store:custom_login')
        
        if not is_store_admin(request.user):
            # Render 403 page
            html = render_to_string('errors/403.html', request=request)
            return HttpResponseForbidden(html)
        
        return view_func(request, *args, **kwargs)
    return wrapper


def require_admin(view_func):
    """Decorator yêu cầu admin (super hoặc store) - Redirect đến 403 nếu không có quyền"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Vui lòng đăng nhập để tiếp tục!')
            return redirect('food_store:custom_login')
        
        if not is_admin_user(request.user):
            # Render 403 page
            html = render_to_string('errors/403.html', request=request)
            return HttpResponseForbidden(html)
        
        return view_func(request, *args, **kwargs)
    return wrapper


def check_permission(user, permission_name):
    """
    Kiểm tra quyền cụ thể của store admin
    
    Permissions:
    - can_manage_products
    - can_manage_orders
    - can_manage_inventory
    - can_manage_shippers
    - can_view_reports
    """
    # Super admin có tất cả quyền
    if is_super_admin(user):
        return True
    
    # Kiểm tra quyền của store admin
    if is_store_admin(user):
        try:
            from food_store.models import StoreAdmin
            store_admin = StoreAdmin.objects.get(user=user, is_active=True)
            return getattr(store_admin, permission_name, False)
        except:
            return False
    
    return False


def require_permission(permission_name):
    """Decorator yêu cầu quyền cụ thể - Redirect đến 403 nếu không có quyền"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not check_permission(request.user, permission_name):
                # Render 403 page
                html = render_to_string('errors/403.html', request=request)
                return HttpResponseForbidden(html)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator


def filter_queryset_by_farm(queryset, user, farm_field='farm'):
    """
    Filter queryset theo farm của store admin
    
    Args:
        queryset: QuerySet cần filter
        user: User object
        farm_field: Tên field liên kết với Farm (mặc định: 'farm')
    
    Returns:
        Filtered queryset
    """
    # Super admin thấy tất cả
    if is_super_admin(user):
        return queryset
    
    # Store admin chỉ thấy data của farm mình quản lý
    if is_store_admin(user):
        managed_farm = get_managed_farm(user)
        if managed_farm:
            filter_kwargs = {farm_field: managed_farm}
            return queryset.filter(**filter_kwargs)
    
    # Không có quyền -> trả về empty queryset
    return queryset.none()


def can_access_farm(user, farm):
    """Kiểm tra user có quyền truy cập farm không"""
    # Super admin có quyền truy cập tất cả
    if is_super_admin(user):
        return True
    
    # Store admin chỉ truy cập farm mình quản lý
    if is_store_admin(user):
        managed_farm = get_managed_farm(user)
        return managed_farm and managed_farm.id == farm.id
    
    return False


def can_access_order(user, order):
    """Kiểm tra user có quyền truy cập order không"""
    # Super admin có quyền truy cập tất cả
    if is_super_admin(user):
        return True
    
    # Store admin chỉ truy cập order của farm mình quản lý
    if is_store_admin(user):
        managed_farm = get_managed_farm(user)
        return managed_farm and order.assigned_farm and order.assigned_farm.id == managed_farm.id
    
    return False


def can_access_product(user, product):
    """Kiểm tra user có quyền truy cập product không"""
    # Super admin có quyền truy cập tất cả
    if is_super_admin(user):
        return True
    
    # Store admin chỉ truy cập product của farm mình quản lý
    if is_store_admin(user):
        managed_farm = get_managed_farm(user)
        return managed_farm and product.farm and product.farm.id == managed_farm.id
    
    return False
