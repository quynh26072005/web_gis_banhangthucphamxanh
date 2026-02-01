"""
Django Admin configuration for Clean Food Store
"""
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Farm, Category, Product, DeliveryZone, Customer, Order, OrderItem


@admin.register(Farm)
class FarmAdmin(OSMGeoAdmin):
    """Admin for Farm model with GIS support"""
    list_display = ['name', 'phone', 'organic_certified', 'created_at']
    list_filter = ['organic_certified', 'created_at']
    search_fields = ['name', 'address', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'address', 'phone', 'email', 'description')
        }),
        ('Vị trí địa lý', {
            'fields': ('location',)
        }),
        ('Chứng nhận', {
            'fields': ('organic_certified', 'certification_number')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin for Category model"""
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin for Product model"""
    list_display = ['name', 'category', 'farm', 'price', 'stock_quantity', 'is_available']
    list_filter = ['category', 'farm', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Thông tin sản phẩm', {
            'fields': ('name', 'category', 'farm', 'description', 'image')
        }),
        ('Giá và kho hàng', {
            'fields': ('price', 'unit', 'stock_quantity', 'is_available')
        }),
        ('Thông tin bổ sung', {
            'fields': ('nutritional_info',)
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(OSMGeoAdmin):
    """Admin for DeliveryZone model with GIS support"""
    list_display = ['name', 'delivery_fee', 'delivery_time', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']


@admin.register(Customer)
class CustomerAdmin(OSMGeoAdmin):
    """Admin for Customer model with GIS support"""
    list_display = ['user', 'phone', 'address', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at']


class OrderItemInline(admin.TabularInline):
    """Inline admin for OrderItem"""
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']


@admin.register(Order)
class OrderAdmin(OSMGeoAdmin):
    """Admin for Order model with GIS support"""
    list_display = ['pk', 'customer', 'status', 'total_amount', 'created_at']
    list_filter = ['status', 'created_at', 'delivery_zone']
    search_fields = ['customer__user__username', 'customer__phone']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Thông tin đơn hàng', {
            'fields': ('customer', 'status', 'notes')
        }),
        ('Thông tin giao hàng', {
            'fields': ('delivery_address', 'delivery_location', 'delivery_zone')
        }),
        ('Thông tin thanh toán', {
            'fields': ('subtotal', 'delivery_fee', 'total_amount')
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
    )


# Customize admin site
admin.site.site_header = "Quản lý Website Thực phẩm Sạch"
admin.site.site_title = "Clean Food Admin"
admin.site.index_title = "Bảng điều khiển quản lý"