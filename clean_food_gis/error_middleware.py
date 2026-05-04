"""
Middleware để hiển thị custom error pages ngay cả khi DEBUG=True
"""
from django.http import Http404
from django.shortcuts import render


class CustomErrorMiddleware:
    """
    Middleware bắt lỗi 404 và hiển thị trang custom
    Hoạt động ngay cả khi DEBUG=True
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Bắt lỗi 404 và hiển thị trang custom
        if response.status_code == 404:
            return render(request, 'errors/404.html', status=404)
        
        # Bắt lỗi 403 và hiển thị trang custom
        if response.status_code == 403:
            return render(request, 'errors/403.html', status=403)
        
        # Bắt lỗi 500 và hiển thị trang custom
        if response.status_code == 500:
            return render(request, 'errors/500.html', status=500)
        
        return response
    
    def process_exception(self, request, exception):
        """
        Xử lý exception và hiển thị trang lỗi phù hợp
        """
        if isinstance(exception, Http404):
            return render(request, 'errors/404.html', status=404)
        
        # Các exception khác -> 500
        return render(request, 'errors/500.html', status=500)
