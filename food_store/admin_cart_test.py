"""
Admin configuration for Clean Food Store - Non-GIS version
"""
from django.contrib import admin
# from django.contrib.gis.admin import OSMGeoAdmin
from .models import Farm, Category, Product, Customer, Cart, CartItem, Order, OrderItem, DeliveryZone


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    """Admin for Farm model"""
    list_display = ['name', 'address', 'phone', 'organic_certified', 'created_at']
    list_filter = ['organic_certified', 'created_at']
    search_fields = ['name', 'address', 'phone']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin for Category model"""
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin for Product model"""
    list_display = ['name', 'category', 'farm', 'price', 'unit', 'stock_quantity', 'is_available']
    list_filter = ['category', 'farm', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'category', 'farm', 'description')
        }),
        ('Giá và kho', {
            'fields': ('price', 'unit', 'stock_quantity', 'is_available')
        }),
        ('Hình ảnh và dinh dưỡng', {
            'fields': ('image', 'nutritional_info')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    """Admin for DeliveryZone model"""
    list_display = ['name', 'delivery_fee', 'delivery_time', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin for Customer model"""
    list_display = ['user', 'phone', 'address', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin for Cart model"""
    list_display = ['customer', 'total_items', 'total_amount', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Admin for CartItem model"""
    list_display = ['cart', 'product', 'quantity', 'total_price', 'added_at']
    readonly_fields = ['added_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin for Order model"""
    list_display = ['id', 'customer', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at', 'delivery_zone']
    search_fields = ['customer__user__username', 'delivery_address']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Thông tin đơn hàng', {
            'fields': ('customer', 'status')
        }),
        ('Thông tin giao hàng', {
            'fields': ('delivery_address', 'delivery_latitude', 'delivery_longitude', 'delivery_zone')
        }),
        ('Thông tin thanh toán', {
            'fields': ('subtotal', 'delivery_fee', 'total_amount')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at', 'delivered_at')
        }),
        ('Ghi chú', {
            'fields': ('notes',)
        }),
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Admin for OrderItem model"""
    list_display = ['order', 'product', 'quantity', 'price', 'total_price']