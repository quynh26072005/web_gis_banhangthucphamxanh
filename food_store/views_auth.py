"""
Custom Authentication Views
Xử lý login và redirect theo role
"""
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from food_store.permissions import get_user_role


def custom_login_view(request):
    """
    Custom login view - redirect theo role
    """
    # Nếu đã đăng nhập, redirect theo role
    if request.user.is_authenticated:
        return redirect_by_role(request.user)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next_url = request.GET.get('next', '')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            
            # Nếu có next URL, redirect đến đó
            if next_url:
                return redirect(next_url)
            
            # Ngược lại, redirect theo role
            return redirect_by_role(user)
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng!')
    
    return render(request, 'auth/login.html')


def redirect_by_role(user):
    """
    Redirect user theo role của họ
    """
    role = get_user_role(user)
    
    if role == 'super_admin':
        # Super Admin → Dashboard tổng
        return redirect('food_store:admin_dashboard')
    
    elif role == 'store_admin':
        # Store Admin → Dashboard chi nhánh
        return redirect('food_store:store_admin_dashboard')
    
    elif role == 'shipper':
        # Shipper → Dashboard shipper
        return redirect('food_store:shipper_dashboard')
    
    elif role == 'customer':
        # Customer → Trang chủ
        return redirect('food_store:home')
    
    else:
        # User thường → Trang chủ
        return redirect('food_store:home')


@login_required
def custom_logout_view(request):
    """Custom logout view"""
    auth_logout(request)
    messages.success(request, 'Đã đăng xuất thành công!')
    return redirect('food_store:home')


def role_dashboard_view(request):
    """
    Trang dashboard tự động redirect theo role
    Dùng cho các link chung như /dashboard/
    """
    if not request.user.is_authenticated:
        return redirect('food_store:custom_login')
    
    return redirect_by_role(request.user)
