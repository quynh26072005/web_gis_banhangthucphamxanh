"""
Simple Django Admin configuration without GIS
"""
from django.contrib import admin
from .models import Farm, Category, Product, Customer


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    """Admin for Farm model without GIS"""
    list_display = ['name', 'phone', 'organic_certified', 'created_at']
    list_filter = ['organic_certified', 'created_at']
    search_fields = ['name', 'address', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'address', 'phone', 'email', 'description')
        }),
        ('Vị trí địa lý', {
            'fields': ('latitude', 'longitude')
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
            'fields': ('name', 'category', 'farm', 'description')
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


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin for Customer model"""
    list_display = ['user', 'phone', 'address', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at']


# Customize admin site
admin.site.site_header = "Quản lý Website Thực phẩm Sạch"
admin.site.site_title = "Clean Food Admin"
admin.site.index_title = "Bảng điều khiển quản lý"