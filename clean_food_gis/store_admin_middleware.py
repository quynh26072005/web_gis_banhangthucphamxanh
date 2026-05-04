"""
Store Admin Middleware
Middleware để xử lý phân quyền và filter data theo chi nhánh
"""
from django.utils.deprecation import MiddlewareMixin


class StoreAdminMiddleware(MiddlewareMixin):
    """
    Middleware để gắn thông tin store admin vào request
    """
    
    def process_request(self, request):
        """
        Kiểm tra user có phải store admin không và gắn thông tin vào request
        """
        if request.user.is_authenticated:
            # Kiểm tra xem user có phải super admin không
            request.is_super_admin = request.user.is_superuser or request.user.is_staff
            
            # Kiểm tra xem user có phải store admin không
            try:
                from food_store.models import StoreAdmin
                store_admin = StoreAdmin.objects.select_related('farm').get(
                    user=request.user,
                    is_active=True
                )
                request.is_store_admin = True
                request.store_admin = store_admin
                request.managed_farm = store_admin.farm
            except StoreAdmin.DoesNotExist:
                request.is_store_admin = False
                request.store_admin = None
                request.managed_farm = None
        else:
            request.is_super_admin = False
            request.is_store_admin = False
            request.store_admin = None
            request.managed_farm = None
        
        return None
