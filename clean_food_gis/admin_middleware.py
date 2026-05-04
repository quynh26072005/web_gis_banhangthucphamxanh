"""
Middleware to separate Admin and User access with independent sessions
"""
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import BACKEND_SESSION_KEY, HASH_SESSION_KEY, SESSION_KEY
from django.contrib.auth import get_user_model


class AdminAccessMiddleware:
    """
    Middleware to restrict admin panel access to staff users only
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Check if accessing admin panel
        if request.path.startswith('/admin-panel/'):
            # Allow access to login page
            if request.path.startswith('/admin-panel/login/'):
                return self.get_response(request)
            
            # Check if user is authenticated and is staff
            if not request.user.is_authenticated:
                messages.warning(request, 'Vui lòng đăng nhập để truy cập Admin Panel.')
                return redirect(f'/admin-panel/login/?next={request.path}')
            
            if not request.user.is_staff:
                messages.error(request, 'Bạn không có quyền truy cập Admin Panel.')
                return redirect('/')
        
        response = self.get_response(request)
        return response


class UserSiteMiddleware:
    """
    Middleware to add context for user site
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Add flag to distinguish admin vs user site
        request.is_admin_site = request.path.startswith('/admin-panel/')
        
        response = self.get_response(request)
        return response


class DualSessionMiddleware:
    """
    Middleware để tách biệt session giữa Admin và User site
    
    Cách hoạt động:
    - Admin site dùng session keys: admin_user_id, admin_backend, admin_hash
    - User site dùng session keys: user_user_id, user_backend, user_hash
    - Django's default session keys được swap tùy theo site đang truy cập
    
    QUAN TRỌNG: Middleware này PHẢI chạy TRƯỚC AuthenticationMiddleware
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        is_admin = request.path.startswith('/admin-panel/')
        
        # Swap session keys TRƯỚC khi AuthenticationMiddleware chạy
        if is_admin:
            # Đang ở admin site - load admin session
            self._load_admin_session(request)
        else:
            # Đang ở user site - load user session  
            self._load_user_session(request)
        
        response = self.get_response(request)
        
        # Save session keys SAU khi request xử lý xong
        if is_admin:
            self._save_admin_session(request)
        else:
            self._save_user_session(request)
        
        return response
    
    def _load_admin_session(self, request):
        """Load admin session vào Django session keys"""
        # Lưu user session hiện tại (nếu có)
        if SESSION_KEY in request.session:
            request.session['user_user_id'] = request.session[SESSION_KEY]
            request.session['user_backend'] = request.session.get(BACKEND_SESSION_KEY, '')
            request.session['user_hash'] = request.session.get(HASH_SESSION_KEY, '')
        
        # Load admin session
        if 'admin_user_id' in request.session:
            request.session[SESSION_KEY] = request.session['admin_user_id']
            if 'admin_backend' in request.session:
                request.session[BACKEND_SESSION_KEY] = request.session['admin_backend']
            if 'admin_hash' in request.session:
                request.session[HASH_SESSION_KEY] = request.session['admin_hash']
        else:
            # Chưa có admin session - xóa session keys
            request.session.pop(SESSION_KEY, None)
            request.session.pop(BACKEND_SESSION_KEY, None)
            request.session.pop(HASH_SESSION_KEY, None)
    
    def _load_user_session(self, request):
        """Load user session vào Django session keys"""
        # Lưu admin session hiện tại (nếu có)
        if SESSION_KEY in request.session:
            request.session['admin_user_id'] = request.session[SESSION_KEY]
            request.session['admin_backend'] = request.session.get(BACKEND_SESSION_KEY, '')
            request.session['admin_hash'] = request.session.get(HASH_SESSION_KEY, '')
        
        # Load user session
        if 'user_user_id' in request.session:
            request.session[SESSION_KEY] = request.session['user_user_id']
            if 'user_backend' in request.session:
                request.session[BACKEND_SESSION_KEY] = request.session['user_backend']
            if 'user_hash' in request.session:
                request.session[HASH_SESSION_KEY] = request.session['user_hash']
        else:
            # Chưa có user session - xóa session keys
            request.session.pop(SESSION_KEY, None)
            request.session.pop(BACKEND_SESSION_KEY, None)
            request.session.pop(HASH_SESSION_KEY, None)
    
    def _save_admin_session(self, request):
        """Lưu admin session từ Django session keys"""
        if SESSION_KEY in request.session:
            request.session['admin_user_id'] = request.session[SESSION_KEY]
            request.session['admin_backend'] = request.session.get(BACKEND_SESSION_KEY, '')
            request.session['admin_hash'] = request.session.get(HASH_SESSION_KEY, '')
    
    def _save_user_session(self, request):
        """Lưu user session từ Django session keys"""
        if SESSION_KEY in request.session:
            request.session['user_user_id'] = request.session[SESSION_KEY]
            request.session['user_backend'] = request.session.get(BACKEND_SESSION_KEY, '')
            request.session['user_hash'] = request.session.get(HASH_SESSION_KEY, '')
