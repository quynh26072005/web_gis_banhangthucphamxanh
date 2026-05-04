"""
Custom middleware for Clean Food GIS
"""
from django.utils import translation


class VietnameseLanguageMiddleware:
    """
    Middleware to force Vietnamese language
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        translation.activate('vi')
        request.LANGUAGE_CODE = 'vi'
        response = self.get_response(request)
        return response
