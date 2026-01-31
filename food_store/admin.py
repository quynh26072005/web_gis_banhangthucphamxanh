"""
Admin configuration for Clean Food Store
Modern UI with Dashboard Statistics
"""
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db import models
from django.utils.html import mark_safe
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum, Count
from .models import Farm, Category, Product, Customer, Cart, CartItem, Order, OrderItem, DeliveryZone


class CleanFoodAdminSite(AdminSite):
    """Custom Admin Site with Dashboard Statistics"""
    site_header = "Thực phẩm Sạch - Quản trị hệ thống"
    site_title = "Clean Food Store Admin"
    index_title = "Dashboard Quản Trị"
    
    def index(self, request, extra_context=None):
        """Add statistics to admin dashboard"""
        extra_context = extra_context or {}
        
        # Get statistics
        extra_context['total_products'] = Product.objects.count()
        extra_context['total_orders'] = Order.objects.count()
        extra_context['total_customers'] = Customer.objects.count()
        extra_context['total_farms'] = Farm.objects.count()
        
        # Get recent orders
        extra_context['recent_orders'] = Order.objects.select_related(
            'customer', 'customer__user'
        ).order_by('-created_at')[:10]
        
        return super().index(request, extra_context)


# Create custom admin site instance
admin_site = CleanFoodAdminSite(name='clean_food_admin')

# Keep backward compatibility with default site headers
admin.site.site_header = "Thực phẩm Sạch - Quản trị hệ thống"
admin.site.site_title = "Clean Food Store Admin"
admin.site.index_title = "Dashboard Quản Trị"


class ProductInline(admin.TabularInline):
    """Inline view for products in Farm"""
    model = Product
    extra = 0
    fields = ('name', 'price', 'stock_quantity', 'is_available')
    readonly_fields = ('price', 'stock_quantity')
    show_change_link = True


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    """Admin for Farm model"""
    list_display = ['name', 'address', 'phone', 'is_organic_icon', 'created_at']
    list_filter = ['organic_certified', 'created_at']
    search_fields = ['name', 'address', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ProductInline]
    
    fieldsets = (
        ('Thông tin chung', {
            'fields': ('name', 'description')
        }),
        ('Liên hệ', {
            'fields': ('address', 'phone', 'email')
        }),
        ('Vị trí & Chứng nhận', {
            'fields': (('latitude', 'longitude'), ('organic_certified', 'certification_number'))
        }),
    )
    
    def is_organic_icon(self, obj):
        if obj.organic_certified:
            return mark_safe('<span style="color:green">✔ Có chứng nhận</span>')
        return mark_safe('<span style="color:gray">✘ Không</span>')
    is_organic_icon.short_description = 'Hữu cơ'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin for Category model"""
    list_display = ['name', 'image_preview', 'description']
    search_fields = ['name']
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit:cover; border-radius: 4px;" />')
        return "No Image"
    image_preview.short_description = 'Hình ảnh'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin for Product model"""
    # Thay price_display bằng price để hỗ trợ list_editable
    list_display = ['image_preview', 'name', 'category', 'farm', 'price', 'stock_quantity', 'is_available']
    list_filter = ['category', 'farm', 'is_available', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['stock_quantity', 'is_available', 'price']
    
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
    
    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="60" height="60" style="object-fit:cover; border-radius: 4px;" />')
        return "No Image"
    image_preview.short_description = 'Ảnh'


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    """Admin for DeliveryZone model"""
    # Thay delivery_fee_display bằng delivery_fee để hỗ trợ list_editable
    list_display = ['name', 'delivery_fee', 'delivery_time', 'is_active', 'area_description']
    list_filter = ['is_active']
    search_fields = ['name']
    list_editable = ['delivery_fee', 'is_active', 'delivery_time']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin for Customer model"""
    list_display = ['user_info', 'phone', 'address', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    readonly_fields = ['created_at']
    
    def user_info(self, obj):
        return f"{obj.user.username} ({obj.user.email})"
    user_info.short_description = "Tài khoản"


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['total_price']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Admin for Cart model"""
    list_display = ['customer', 'get_total_items', 'get_total_amount', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]
    
    def get_total_items(self, obj):
        return obj.items.aggregate(total=models.Sum('quantity'))['total'] or 0
    get_total_items.short_description = "Tổng số lượng"

    def get_total_amount(self, obj):
        # Calculate in python to avoid complex annotations if simple
        total = 0
        for item in obj.items.all():
            if item.product and item.product.price:
                total += item.quantity * item.product.price
        return f"{total:,.0f} đ"
    get_total_amount.short_description = "Tổng tiền"


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    # Use fields that definitely exist. total_price might be property.
    # Check OrderItem model: quantity, price. 
    fields = ['product', 'quantity', 'price'] 
    readonly_fields = ['price']
    
    # If total_price is a property in model, we can add it to readonly
    # But safer to remove if unsure.
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin for Order model"""
    list_display = ['id', 'customer_link', 'status_colored', 'assigned_farm_display', 'total_amount_display', 'created_at', 'delivery_zone']
    list_filter = ['status', 'created_at', 'delivery_zone', 'assigned_farm']
    # Removed 'id' from search_fields to prevent Postgres integer error
    search_fields = ['customer__user__username', 'delivery_address'] 
    readonly_fields = ['created_at', 'updated_at', 'show_route_map']
    inlines = [OrderItemInline]
    actions = ['mark_as_confirmed', 'mark_as_shipping', 'mark_as_delivered', 'recalculate_route']
    
    fieldsets = (
        ('Thông tin đơn hàng', {
            'fields': ('customer', 'status', 'created_at')
        }),
        ('Thông tin giao hàng', {
            'fields': ('delivery_address', ('delivery_latitude', 'delivery_longitude'), 'delivery_zone', 'assigned_farm')
        }),
        ('Bản đồ Route', {
            'fields': ('show_route_map',),
            'classes': ('wide',),
            'description': 'Đường đi từ trang trại đến khách hàng'
        }),
        ('Thông tin thanh toán', {
            'fields': (('subtotal', 'delivery_fee', 'total_amount'),)
        }),
        ('Ghi chú', {
            'fields': ('notes', 'delivered_at')
        }),
    )
    
    def customer_link(self, obj):
        if obj.customer:
            url = reverse('admin:food_store_customer_change', args=[obj.customer.id])
            return mark_safe(f'<a href="{url}">{obj.customer}</a>')
        return "-"
    customer_link.short_description = "Khách hàng"
    
    def total_amount_display(self, obj):
        return f"{obj.total_amount:,.0f} đ"
    total_amount_display.short_description = "Tổng cộng"
    
    def status_colored(self, obj):
        colors = {
            'pending': 'orange',
            'confirmed': 'blue',
            'preparing': 'purple',
            'shipping': '#17a2b8',
            'delivered': 'green',
            'cancelled': 'red'
        }
        color = colors.get(obj.status, 'black')
        # Handle choice display safe way
        display = obj.get_status_display() if hasattr(obj, 'get_status_display') else obj.status
        return mark_safe(f'<span style="color: {color}; font-weight: bold;">{display.upper()}</span>')
    status_colored.short_description = "Trạng thái"

    # Actions
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')
    mark_as_confirmed.short_description = "Đánh dấu: Đã xác nhận"

    def mark_as_shipping(self, request, queryset):
        queryset.update(status='shipping')
    mark_as_shipping.short_description = "Đánh dấu: Đang giao hàng"
    
    def mark_as_delivered(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='delivered', delivered_at=timezone.now())
    mark_as_delivered.short_description = "Đánh dấu: Đã giao hàng"
    
    def recalculate_route(self, request, queryset):
        """Admin action để tính lại route cho các đơn hàng được chọn"""
        updated_count = 0
        for order in queryset:
            if order.auto_assign_nearest_farm():
                order.save()
                updated_count += 1
        
        self.message_user(request, f"Đã tính lại route cho {updated_count} đơn hàng")
    recalculate_route.short_description = "🔄 Tính lại route giao hàng"
    
    # Display methods
    def assigned_farm_display(self, obj):
        """Hiển thị farm được gán với icon"""
        if obj.assigned_farm:
            return mark_safe(f'<span style="color: green;">✓ {obj.assigned_farm.name}</span>')
        return mark_safe('<span style="color: orange;">⚠ Chưa gán</span>')
    assigned_farm_display.short_description = "Trang trại"
    
    def show_route_map(self, obj):
        """Hiển thị bản đồ route giao hàng trong admin"""
        if not obj.id:
            return "Chưa có bản đồ (lưu đơn hàng trước)"
        
        if not obj.delivery_latitude or not obj.delivery_longitude:
            return mark_safe('<p style="color: orange;">⚠ Chưa có tọa độ giao hàng</p>')
        
        if not obj.assigned_farm:
            return mark_safe('<p style="color: orange;">⚠ Chưa có trang trại được gán. Hãy lưu đơn hàng để tự động gán.</p>')
        
        try:
            from gis_tools.gis_functions import MapGenerator
            route_map = MapGenerator.create_order_tracking_map(obj.id)
            
            if route_map:
                map_html = route_map._repr_html_()
                # Wrap in container for better display
                return mark_safe(f'''
                    <div style="margin: 10px 0;">
                        <h4 style="color: #4CAF50;">📍 Route: {obj.assigned_farm.name} → Khách hàng</h4>
                        <div style="border: 2px solid #ddd; border-radius: 8px; overflow: hidden;">
                            {map_html}
                        </div>
                        <p style="margin-top: 10px; color: #666;">
                            <em>Đường đi được tính tự động dựa trên trang trại gần nhất</em>
                        </p>
                    </div>
                ''')
            else:
                return mark_safe('<p style="color: red;">❌ Không thể tạo bản đồ</p>')
        except Exception as e:
            return mark_safe(f'<p style="color: red;">❌ Lỗi: {str(e)}</p>')
    
    show_route_map.short_description = "Bản đồ Route giao hàng"

    def mark_as_delivered(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='delivered', delivered_at=timezone.now())
    mark_as_delivered.short_description = "Đánh dấu: Đã giao hàng"