"""
Custom error views for Clean Food GIS
"""
from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token


@requires_csrf_token
def custom_404_view(request, exception=None):
    """
    Custom 404 error page
    Hiển thị khi URL không tồn tại
    """
    return render(request, 'errors/404.html', status=404)


@requires_csrf_token
def custom_403_view(request, exception=None):
    """
    Custom 403 error page
    Hiển thị khi user không có quyền truy cập
    """
    return render(request, 'errors/403.html', status=403)


@requires_csrf_token
def custom_500_view(request):
    """
    Custom 500 error page
    Hiển thị khi có lỗi server
    """
    return render(request, 'errors/500.html', status=500)

