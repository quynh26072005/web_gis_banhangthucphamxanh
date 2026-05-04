"""
URL configuration for food_store app
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from django.shortcuts import render
from . import views
from . import views_admin
from . import views_auth
from . import views_verification

app_name = 'food_store'

urlpatterns = [
    # Authentication
    path('accounts/login/', views_auth.custom_login_view, name='custom_login'),
    path('accounts/logout/', views_auth.custom_logout_view, name='custom_logout'),
    path('dashboard/', views_auth.role_dashboard_view, name='role_dashboard'),
    
    # Email verification & Password reset
    path('register/', views_verification.register_step1, name='register_step1'),
    path('register/verify/<int:verification_id>/', views_verification.register_step2, name='register_step2'),
    path('register/resend/<int:verification_id>/', views_verification.resend_otp, name='resend_otp'),
    path('forgot-password/', views_verification.forgot_password_step1, name='forgot_password_step1'),
    path('forgot-password/verify/<int:reset_id>/', views_verification.forgot_password_step2, name='forgot_password_step2'),
    path('forgot-password/resend/<int:reset_id>/', views_verification.resend_reset_otp, name='resend_reset_otp'),
    
    # Main pages
    path('', views.home_view, name='home'),
    path('products/', views.product_list_view, name='product_list'),
    path('products/search/', views.product_list_view, name='product_search'),
    path('product/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('categories/', views.category_list_view, name='category_list'),
    path('farms/', views.farm_list_view, name='farm_list'),
    path('farm/<int:pk>/', views.farm_detail_view, name='farm_detail'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    
    # User authentication
    path('register/', views.register_view, name='register'),
    
    # User profile and orders
    path('profile/', views.profile_view, name='profile'),
    path('orders/', views.order_history_view, name='order_history'),
    path('order/<int:pk>/', views.order_detail_view, name='order_detail'),
    
    # Shopping cart
    path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-success/<int:order_id>/', views.order_success_view, name='order_success'),
    
    # Cart APIs
    path('api/add-to-cart/', views.add_to_cart_api, name='add_to_cart_api'),
    path('api/update-cart-item/', views.update_cart_item_api, name='update_cart_item_api'),
    path('api/remove-from-cart/', views.remove_from_cart_api, name='remove_from_cart_api'),
    path('api/create-order/', views.create_order_api, name='create_order_api'),
    path('api/get-stores/', views.get_stores_api, name='get_stores_api'),
    path('api/cart-count/', views.cart_count_api, name='cart_count_api'),
    
    # Custom Admin Dashboard (KHÔNG DÙNG DJANGO ADMIN)
    path('quan-tri/', views_admin.admin_dashboard, name='admin_dashboard'),
    path('quan-tri/don-hang/', views_admin.admin_orders, name='admin_orders'),
    path('quan-tri/don-hang/<int:pk>/', views_admin.admin_order_detail, name='admin_order_detail'),
    path('quan-tri/don-hang/<int:pk>/cap-nhat/', views_admin.admin_order_update_status, name='admin_order_update_status'),
    
    # Quản lý Sản phẩm
    path('quan-tri/san-pham/', views_admin.admin_products, name='admin_products'),
    path('quan-tri/san-pham/them/', views_admin.admin_product_create, name='admin_product_create'),
    path('quan-tri/san-pham/<int:pk>/sua/', views_admin.admin_product_edit, name='admin_product_edit'),
    path('quan-tri/san-pham/<int:pk>/xoa/', views_admin.admin_product_delete, name='admin_product_delete'),
    
    # Quản lý Kho
    path('quan-tri/kho/', views_admin.admin_inventory, name='admin_inventory'),
    path('quan-tri/kho/nhap-hang/', views_admin.admin_stock_import, name='admin_stock_import'),
    path('quan-tri/kho/xuat-hang/', views_admin.admin_stock_export, name='admin_stock_export'),
    path('quan-tri/kho/giao-dich/<int:pk>/xoa/', views_admin.admin_transaction_delete, name='admin_transaction_delete'),
    
    # Export Admin Inventory
    path('quan-tri/kho/xuat-pdf/', views_admin.admin_export_transactions_pdf, name='admin_export_transactions_pdf'),
    path('quan-tri/kho/xuat-excel/', views_admin.admin_export_transactions_excel, name='admin_export_transactions_excel'),
    path('quan-tri/kho/ton-kho-pdf/', views_admin.admin_export_inventory_pdf, name='admin_export_inventory_pdf'),
    path('quan-tri/kho/ton-kho-excel/', views_admin.admin_export_inventory_excel, name='admin_export_inventory_excel'),
    
    # Quản lý Khách hàng
    path('quan-tri/khach-hang/', views_admin.admin_customers, name='admin_customers'),
    path('quan-tri/khach-hang/them/', views_admin.admin_customer_create, name='admin_customer_create'),
    path('quan-tri/khach-hang/<int:pk>/sua/', views_admin.admin_customer_edit, name='admin_customer_edit'),
    path('quan-tri/khach-hang/<int:pk>/xoa/', views_admin.admin_customer_delete, name='admin_customer_delete'),
    
    # Quản lý Cửa hàng
    path('quan-tri/cua-hang/', views_admin.admin_farms, name='admin_farms'),
    path('quan-tri/cua-hang/them/', views_admin.admin_farm_create, name='admin_farm_create'),
    path('quan-tri/cua-hang/<int:pk>/sua/', views_admin.admin_farm_edit, name='admin_farm_edit'),
    path('quan-tri/cua-hang/<int:pk>/xoa/', views_admin.admin_farm_delete, name='admin_farm_delete'),
    
    # Quản lý Danh mục
    path('quan-tri/danh-muc/', views_admin.admin_categories, name='admin_categories'),
    path('quan-tri/danh-muc/them/', views_admin.admin_category_create, name='admin_category_create'),
    path('quan-tri/danh-muc/<int:pk>/sua/', views_admin.admin_category_edit, name='admin_category_edit'),
    path('quan-tri/danh-muc/<int:pk>/xoa/', views_admin.admin_category_delete, name='admin_category_delete'),
    
    # Quản lý Khu vực giao hàng
    path('quan-tri/khu-vuc/', views_admin.admin_delivery_zones, name='admin_delivery_zones'),
    path('quan-tri/khu-vuc/them/', views_admin.admin_zone_create, name='admin_zone_create'),
    path('quan-tri/khu-vuc/<int:pk>/sua/', views_admin.admin_zone_edit, name='admin_zone_edit'),
    path('quan-tri/khu-vuc/<int:pk>/xoa/', views_admin.admin_zone_delete, name='admin_zone_delete'),
    
    # Quản lý Nhà cung cấp
    path('quan-tri/nha-cung-cap/', views_admin.admin_suppliers, name='admin_suppliers'),
    path('quan-tri/nha-cung-cap/them/', views_admin.admin_supplier_create, name='admin_supplier_create'),
    path('quan-tri/nha-cung-cap/<int:pk>/sua/', views_admin.admin_supplier_edit, name='admin_supplier_edit'),
    path('quan-tri/nha-cung-cap/<int:pk>/xoa/', views_admin.admin_supplier_delete, name='admin_supplier_delete'),
    
    # Báo cáo
    path('quan-tri/bao-cao/', views_admin.admin_reports, name='admin_reports'),
    
    # Quản lý Shipper
    path('quan-tri/shipper/', views_admin.admin_shippers, name='admin_shippers'),
    path('quan-tri/shipper/them/', views_admin.admin_shipper_create, name='admin_shipper_create'),
    path('quan-tri/shipper/<int:pk>/', views_admin.admin_shipper_detail, name='admin_shipper_detail'),
    path('quan-tri/shipper/<int:pk>/sua/', views_admin.admin_shipper_edit, name='admin_shipper_edit'),
    path('quan-tri/shipper/<int:pk>/xoa/', views_admin.admin_shipper_delete, name='admin_shipper_delete'),
    
    # Quản lý Store Admin (chỉ Super Admin)
    path('quan-tri/quan-ly-chi-nhanh/', views_admin.admin_store_admins, name='admin_store_admins'),
    path('quan-tri/quan-ly-chi-nhanh/them/', views_admin.admin_store_admin_create, name='admin_store_admin_create'),
    path('quan-tri/quan-ly-chi-nhanh/<int:pk>/', views_admin.admin_store_admin_detail, name='admin_store_admin_detail'),
    path('quan-tri/quan-ly-chi-nhanh/<int:pk>/sua/', views_admin.admin_store_admin_edit, name='admin_store_admin_edit'),
    path('quan-tri/quan-ly-chi-nhanh/<int:pk>/xoa/', views_admin.admin_store_admin_delete, name='admin_store_admin_delete'),
    
    # Check login status
    path('check-login/', views_admin.check_login_status, name='check_login_status'),
    
    # Test scrollbar
    path('test-scrollbar/', lambda request: render(request, 'test_scrollbar.html'), name='test_scrollbar'),
    
    # Test export
    path('test-export/', lambda request: render(request, 'test_export.html'), name='test_export'),
]

# Order Tracking URLs (Customer)
from . import views_tracking

tracking_patterns = [
    path('order/<int:order_id>/tracking/', views_tracking.order_tracking_view, name='order_tracking'),
    path('api/order/<int:order_id>/tracking/', views_tracking.order_tracking_api, name='order_tracking_api'),
    path('api/order/<int:order_id>/timeline/', views_tracking.order_status_timeline_api, name='order_timeline_api'),
]

urlpatterns += tracking_patterns

# Shipper URLs
from . import views_shipper

shipper_patterns = [
    path('shipper/', views_shipper.shipper_dashboard, name='shipper_dashboard'),
    path('shipper/toggle-status/', views_shipper.toggle_status, name='shipper_toggle_status'),
    path('shipper/orders/', views_shipper.order_list, name='shipper_orders'),
    path('shipper/order/<int:order_id>/', views_shipper.order_detail, name='shipper_order_detail'),
    path('shipper/order/<int:order_id>/accept/', views_shipper.accept_order, name='shipper_accept_order'),
    path('shipper/order/<int:order_id>/picked/', views_shipper.mark_picked, name='shipper_mark_picked'),
    path('shipper/order/<int:order_id>/complete/', views_shipper.complete_order, name='shipper_complete_order'),
    path('shipper/order/<int:order_id>/map/', views_shipper.order_map, name='shipper_order_map'),
]

urlpatterns += shipper_patterns

# Store Admin URLs (Quản lý chi nhánh)
from . import views_store_admin

store_admin_patterns = [
    path('chi-nhanh/', views_store_admin.store_admin_dashboard, name='store_admin_dashboard'),
    path('chi-nhanh/don-hang/', views_store_admin.store_admin_orders, name='store_admin_orders'),
    path('chi-nhanh/don-hang/<int:pk>/', views_store_admin.store_admin_order_detail, name='store_admin_order_detail'),
    path('chi-nhanh/don-hang/<int:pk>/cap-nhat/', views_store_admin.store_admin_order_update_status, name='store_admin_order_update_status'),
    path('chi-nhanh/san-pham/', views_store_admin.store_admin_products, name='store_admin_products'),
    path('chi-nhanh/san-pham/them/', views_store_admin.store_admin_product_create, name='store_admin_product_create'),
    path('chi-nhanh/san-pham/<int:pk>/sua/', views_store_admin.store_admin_product_edit, name='store_admin_product_edit'),
    path('chi-nhanh/san-pham/<int:pk>/xoa/', views_store_admin.store_admin_product_delete, name='store_admin_product_delete'),
    path('chi-nhanh/kho/', views_store_admin.store_admin_inventory, name='store_admin_inventory'),
    
    # ✅ THÊM: Nhập/Xuất kho cho Store Admin
    path('chi-nhanh/kho/nhap-hang/', views_store_admin.store_admin_stock_import, name='store_admin_stock_import'),
    path('chi-nhanh/kho/xuat-hang/', views_store_admin.store_admin_stock_export, name='store_admin_stock_export'),
    
    # Export Inventory
    path('chi-nhanh/kho/xuat-pdf/', views_store_admin.export_transactions_pdf, name='export_transactions_pdf'),
    path('chi-nhanh/kho/xuat-excel/', views_store_admin.export_transactions_excel, name='export_transactions_excel'),
    path('chi-nhanh/kho/ton-kho-pdf/', views_store_admin.export_inventory_pdf, name='export_inventory_pdf'),
    path('chi-nhanh/kho/ton-kho-excel/', views_store_admin.export_inventory_excel, name='export_inventory_excel'),
    
    path('chi-nhanh/shipper/', views_store_admin.store_admin_shippers, name='store_admin_shippers'),
    path('chi-nhanh/shipper/them/', views_store_admin.store_admin_shipper_create, name='store_admin_shipper_create'),
    path('chi-nhanh/shipper/<int:pk>/sua/', views_store_admin.store_admin_shipper_edit, name='store_admin_shipper_edit'),
    path('chi-nhanh/shipper/<int:pk>/xoa/', views_store_admin.store_admin_shipper_delete, name='store_admin_shipper_delete'),
    path('chi-nhanh/bao-cao/', views_store_admin.store_admin_reports, name='store_admin_reports'),
]

urlpatterns += store_admin_patterns

