"""
URL configuration for food_store app
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'food_store'

urlpatterns = [
    # Main pages
    path('', views.home_view, name='home'),
    path('products/', views.product_list_view, name='product_list'),
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
]