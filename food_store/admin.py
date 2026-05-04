"""
Admin configuration for Clean Food Store - Enhanced UI
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Count, Sum
from django.contrib.admin import SimpleListFilter
from django.utils import timezone
from .models import (
    Farm, Category, Product, Customer, Order, OrderItem, DeliveryZone,
    Supplier, StockTransaction, StockAlert, InventoryReport, Shipper
)

# Customize Admin Site
admin.site.site_header = "Clean Food GIS - Quản Trị Hệ Thống"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Dashboard Quản Lý"


class StockLevelFilter(SimpleListFilter):
    """Filter products by stock level"""
    title = 'Mức tồn kho'
    parameter_name = 'stock_level'

    def lookups(self, request, model_admin):
        return (
            ('high', 'Nhiều (>50)'),
            ('medium', 'Trung bình (10-50)'),
            ('low', 'Ít (<10)'),
            ('out', 'Hết hàng'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'high':
            return queryset.filter(stock_quantity__gt=50)
        if self.value() == 'medium':
            return queryset.filter(stock_quantity__gte=10, stock_quantity__lte=50)
        if self.value() == 'low':
            return queryset.filter(stock_quantity__gt=0, stock_quantity__lt=10)
        if self.value() == 'out':
            return queryset.filter(stock_quantity=0)


class OrderStatusFilter(SimpleListFilter):
    """Filter orders by status"""
    title = 'Trạng thái đơn hàng'
    parameter_name = 'order_status'

    def lookups(self, request, model_admin):
        return Order.STATUS_CHOICES

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    """Enhanced Admin for Farm model with draggable map"""
    list_display = ['name', 'address', 'phone', 'organic_status', 'location_status', 'products_count', 'created_at']
    list_filter = ['organic_certified', 'created_at']
    search_fields = ['name', 'address', 'phone', 'email']
    readonly_fields = ['created_at', 'updated_at', 'products_count', 'location_map_picker']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'address', 'phone', 'email'),
            'classes': ('wide',)
        }),
        ('Vị trí GPS - Chọn trên bản đồ', {
            'fields': ('location_map_picker', 'latitude', 'longitude'),
            'classes': ('wide',),
            'description': 'Kéo thả marker trên bản đồ để chọn vị trí cửa hàng'
        }),
        ('Chứng nhận', {
            'fields': ('organic_certified', 'certification_number'),
            'classes': ('wide',)
        }),
        ('Mô tả', {
            'fields': ('description',),
            'classes': ('wide',)
        }),
        ('Thống kê', {
            'fields': ('products_count',),
            'classes': ('collapse',)
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    class Media:
        css = {
            'all': ('https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',)
        }
        js = (
            'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js',
        )
    
    def location_status(self, obj):
        """Display GPS location status"""
        if obj.latitude and obj.longitude:
            return mark_safe(
                '<span style="color: #28a745;"><i class="fas fa-map-marker-alt"></i> Có GPS</span>'
            )
        return mark_safe(
            '<span style="color: #dc3545;"><i class="fas fa-map-marker-alt"></i> Chưa có GPS</span>'
        )
    location_status.short_description = 'Vị trí GPS'
    
    def organic_status(self, obj):
        if obj.organic_certified:
            return mark_safe(
                '<span class="organic-badge"><i class="fas fa-store"></i> Hữu cơ</span>'
            )
        return mark_safe('<span style="color: #6c757d;">Thông thường</span>')
    organic_status.short_description = 'Chứng nhận'
    
    def products_count(self, obj):
        count = obj.product_set.count()
        url = reverse('admin:food_store_product_changelist') + '?farm__id__exact={}'.format(obj.id)
        return format_html('<a href="{}">{} sản phẩm</a>', url, count)
    products_count.short_description = 'Số sản phẩm'
    
    def location_map_picker(self, obj):
        """Interactive map for selecting farm location"""
        
        # Default location (Ho Chi Minh City center)
        default_lat = 10.762622
        default_lng = 106.660172
        default_zoom = 12
        
        # Use existing coordinates if available
        if obj.latitude and obj.longitude:
            default_lat = obj.latitude
            default_lng = obj.longitude
            default_zoom = 15
        
        map_html = f"""
        <div style="margin-bottom: 20px;">
            <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; border-left: 4px solid #2196f3; margin-bottom: 15px;">
                <h4 style="margin: 0 0 10px 0; color: #1976d2;">
                    <i class="fas fa-map-marked-alt"></i> Chọn Vị trí Cửa hàng
                </h4>
                <p style="margin: 0; color: #555;">
                    <strong>Hướng dẫn:</strong> Kéo thả marker <i class="fas fa-map-marker-alt" style="color: #dc3545;"></i> 
                    trên bản đồ để chọn vị trí chính xác của cửa hàng. 
                    Tọa độ GPS sẽ tự động cập nhật vào các trường bên dưới.
                </p>
            </div>
            
            <div id="farm-location-picker-map" style="height: 500px; width: 100%; border: 2px solid #ddd; border-radius: 8px; margin-bottom: 15px;"></div>
            
            <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #dee2e6;">
                <div class="row">
                    <div class="col-md-4">
                        <strong><i class="fas fa-crosshairs"></i> Vĩ độ (Latitude):</strong>
                        <div id="current-lat" style="font-size: 18px; color: #28a745; font-weight: bold;">{default_lat:.6f}</div>
                    </div>
                    <div class="col-md-4">
                        <strong><i class="fas fa-crosshairs"></i> Kinh độ (Longitude):</strong>
                        <div id="current-lng" style="font-size: 18px; color: #28a745; font-weight: bold;">{default_lng:.6f}</div>
                    </div>
                    <div class="col-md-4">
                        <button type="button" id="use-current-location" class="btn btn-primary btn-sm" style="width: 100%;">
                            <i class="fas fa-location-arrow"></i> Dùng Vị trí Hiện tại
                        </button>
                    </div>
                </div>
                <div style="margin-top: 10px; padding-top: 10px; border-top: 1px solid #dee2e6;">
                    <small style="color: #666;">
                        <i class="fas fa-info-circle"></i> 
                        <strong>Mẹo:</strong> Bạn có thể tìm kiếm địa chỉ trên Google Maps, 
                        sau đó click chuột phải và chọn tọa độ để copy vào đây.
                    </small>
                </div>
            </div>
        </div>
        
        <script>
        (function() {{
            // Wait for DOM to be ready
            if (document.readyState === 'loading') {{
                document.addEventListener('DOMContentLoaded', initFarmLocationPicker);
            }} else {{
                initFarmLocationPicker();
            }}
            
            function initFarmLocationPicker() {{
                // Check if Leaflet is loaded
                if (typeof L === 'undefined') {{
                    console.error('Leaflet not loaded!');
                    document.getElementById('farm-location-picker-map').innerHTML = 
                        '<div style="padding: 50px; text-align: center; color: #dc3545;">' +
                        '<i class="fas fa-exclamation-triangle fa-3x"></i><br><br>' +
                        '<strong>Lỗi: Leaflet library chưa được tải</strong><br>' +
                        'Vui lòng refresh trang hoặc kiểm tra kết nối internet.' +
                        '</div>';
                    return;
                }}
                
                console.log('Initializing farm location picker map...');
                
                // Initialize map
                const map = L.map('farm-location-picker-map').setView([{default_lat}, {default_lng}], {default_zoom});
                
                // Add OpenStreetMap tiles
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    attribution: '© OpenStreetMap contributors',
                    maxZoom: 19,
                    crossOrigin: true
                }}).addTo(map);
                
                // Create draggable marker
                const marker = L.marker([{default_lat}, {default_lng}], {{
                    draggable: true,
                    autoPan: true,
                    icon: L.icon({{
                        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
                        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png',
                        iconSize: [25, 41],
                        iconAnchor: [12, 41],
                        popupAnchor: [1, -34],
                        shadowSize: [41, 41]
                    }})
                }}).addTo(map);
                
                marker.bindPopup('<strong>Kéo thả marker này để chọn vị trí!</strong>').openPopup();
                
                // Update coordinates display and form fields
                function updateCoordinates(lat, lng) {{
                    document.getElementById('current-lat').textContent = lat.toFixed(6);
                    document.getElementById('current-lng').textContent = lng.toFixed(6);
                    
                    // Update form fields
                    const latField = document.getElementById('id_latitude');
                    const lngField = document.getElementById('id_longitude');
                    
                    if (latField) latField.value = lat.toFixed(6);
                    if (lngField) lngField.value = lng.toFixed(6);
                    
                    // Update popup
                    marker.setPopupContent(
                        '<div style="text-align: center;">' +
                        '<strong><i class="fas fa-map-marker-alt"></i> Vị trí đã chọn</strong><br>' +
                        '<small>Lat: ' + lat.toFixed(6) + '<br>Lng: ' + lng.toFixed(6) + '</small>' +
                        '</div>'
                    );
                }}
                
                // Handle marker drag
                marker.on('dragend', function(e) {{
                    const position = marker.getLatLng();
                    updateCoordinates(position.lat, position.lng);
                    console.log('Marker moved to:', position.lat, position.lng);
                }});
                
                // Handle map click
                map.on('click', function(e) {{
                    marker.setLatLng(e.latlng);
                    updateCoordinates(e.latlng.lat, e.latlng.lng);
                    marker.openPopup();
                }});
                
                // Use current location button
                const useLocationBtn = document.getElementById('use-current-location');
                if (useLocationBtn) {{
                    useLocationBtn.addEventListener('click', function() {{
                        if (navigator.geolocation) {{
                            useLocationBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Đang lấy vị trí...';
                            useLocationBtn.disabled = true;
                            
                            navigator.geolocation.getCurrentPosition(
                                function(position) {{
                                    const lat = position.coords.latitude;
                                    const lng = position.coords.longitude;
                                    
                                    marker.setLatLng([lat, lng]);
                                    map.setView([lat, lng], 16);
                                    updateCoordinates(lat, lng);
                                    marker.openPopup();
                                    
                                    useLocationBtn.innerHTML = '<i class="fas fa-check"></i> Đã cập nhật!';
                                    setTimeout(function() {{
                                        useLocationBtn.innerHTML = '<i class="fas fa-location-arrow"></i> Dùng Vị trí Hiện tại';
                                        useLocationBtn.disabled = false;
                                    }}, 2000);
                                }},
                                function(error) {{
                                    alert('Không thể lấy vị trí hiện tại: ' + error.message);
                                    useLocationBtn.innerHTML = '<i class="fas fa-location-arrow"></i> Dùng Vị trí Hiện tại';
                                    useLocationBtn.disabled = false;
                                }}
                            );
                        }} else {{
                            alert('Trình duyệt không hỗ trợ Geolocation!');
                        }}
                    }});
                }}
                
                // Sync form fields to map when manually edited
                const latField = document.getElementById('id_latitude');
                const lngField = document.getElementById('id_longitude');
                
                if (latField && lngField) {{
                    function syncFormToMap() {{
                        const lat = parseFloat(latField.value);
                        const lng = parseFloat(lngField.value);
                        
                        if (!isNaN(lat) && !isNaN(lng)) {{
                            marker.setLatLng([lat, lng]);
                            map.setView([lat, lng], 15);
                            updateCoordinates(lat, lng);
                        }}
                    }}
                    
                    latField.addEventListener('change', syncFormToMap);
                    lngField.addEventListener('change', syncFormToMap);
                }}
                
                console.log('Farm location picker initialized successfully!');
            }}
        }})();
        </script>
        
        <style>
        .leaflet-container {{
            font-family: inherit;
        }}
        
        #farm-location-picker-map {{
            cursor: crosshair;
        }}
        
        .leaflet-popup-content {{
            text-align: center;
            font-size: 14px;
        }}
        </style>
        """
        
        return mark_safe(map_html)
    location_map_picker.short_description = 'Bản đồ chọn vị trí'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Enhanced Admin for Category model"""
    list_display = ['name', 'description', 'products_count']
    search_fields = ['name', 'description']
    
    def products_count(self, obj):
        count = obj.product_set.count()
        url = reverse('admin:food_store_product_changelist') + '?category__id__exact={}'.format(obj.id)
        return format_html('<a href="{}">{} sản phẩm</a>', url, count)
    products_count.short_description = 'Số sản phẩm'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Enhanced Admin for Product model"""
    list_display = ['name', 'category', 'farm_link', 'price_display', 'unit', 'stock_status', 'availability_status', 'is_available', 'created_at']
    list_filter = ['category', 'farm', 'is_available', StockLevelFilter, 'created_at']
    search_fields = ['name', 'description', 'farm__name']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_available']
    
    fieldsets = (
        ('Thông tin sản phẩm', {
            'fields': ('name', 'category', 'farm', 'description'),
            'classes': ('wide',)
        }),
        ('Giá và đơn vị', {
            'fields': ('price', 'unit'),
            'classes': ('wide',)
        }),
        ('Kho hàng', {
            'fields': ('stock_quantity', 'is_available'),
            'classes': ('wide',)
        }),
        ('Hình ảnh và thông tin bổ sung', {
            'fields': ('image', 'nutritional_info'),
            'classes': ('wide',)
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def farm_link(self, obj):
        url = reverse('admin:food_store_farm_change', args=[obj.farm.id])
        organic = '<i class="fas fa-store" style="color: #28a745;"></i>' if obj.farm.organic_certified else ''
        return format_html('<a href="{}">{}</a> {}', url, obj.farm.name, organic)
    farm_link.short_description = 'Cửa hàng'
    
    def price_display(self, obj):
        return format_html('<span class="price-display">{} VNĐ</span>', "{:,.0f}".format(float(obj.price)))
    price_display.short_description = 'Giá'
    
    def stock_status(self, obj):
        if obj.stock_quantity == 0:
            return mark_safe('<span class="stock-low">Hết hàng</span>')
        elif obj.stock_quantity < 10:
            return format_html('<span class="stock-low">{}</span>', obj.stock_quantity)
        elif obj.stock_quantity < 50:
            return format_html('<span class="stock-medium">{}</span>', obj.stock_quantity)
        else:
            return format_html('<span class="stock-high">{}</span>', obj.stock_quantity)
    stock_status.short_description = 'Tồn kho'
    
    def availability_status(self, obj):
        if obj.is_available:
            return mark_safe('<span style="color: #28a745;"><i class="fas fa-check-circle"></i> Có sẵn</span>')
        return mark_safe('<span style="color: #dc3545;"><i class="fas fa-times-circle"></i> Không có</span>')
    availability_status.short_description = 'Trạng thái'


@admin.register(DeliveryZone)
class DeliveryZoneAdmin(admin.ModelAdmin):
    """Enhanced Admin for DeliveryZone model"""
    list_display = ['name', 'delivery_fee_display', 'delivery_time', 'orders_count', 'status', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name', 'area_description']
    list_editable = ['is_active']
    
    def delivery_fee_display(self, obj):
        return format_html('<span class="price-display">{} VNĐ</span>', "{:,.0f}".format(float(obj.delivery_fee)))
    delivery_fee_display.short_description = 'Phí giao hàng'
    
    def orders_count(self, obj):
        from .models import Order
        count = Order.objects.filter(delivery_zone=obj).count()
        url = reverse('admin:food_store_order_changelist') + '?delivery_zone__id__exact={}'.format(obj.id)
        return format_html('<a href="{}">{} đơn hàng</a>', url, count)
    orders_count.short_description = 'Số đơn hàng'
    
    def status(self, obj):
        from django.utils.safestring import mark_safe
        if obj.is_active:
            return mark_safe('<span style="color: #28a745;"><i class="fas fa-check-circle"></i> Hoạt động</span>')
        else:
            return mark_safe('<span style="color: #dc3545;"><i class="fas fa-times-circle"></i> Tạm dừng</span>')
    status.short_description = 'Trạng thái'


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Enhanced Admin for Customer model"""
    list_display = ['user_info', 'phone', 'address', 'orders_count', 'total_spent', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone', 'address']
    readonly_fields = ['created_at', 'orders_count', 'total_spent']
    
    def user_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><small>{}</small>',
            obj.user.get_full_name() or obj.user.username,
            obj.user.email
        )
    user_info.short_description = 'Thông tin người dùng'
    
    def orders_count(self, obj):
        count = obj.order_set.count()
        url = reverse('admin:food_store_order_changelist') + '?customer__id__exact={}'.format(obj.id)
        return format_html('<a href="{}">{} đơn hàng</a>', url, count)
    orders_count.short_description = 'Số đơn hàng'
    
    def total_spent(self, obj):
        total = obj.order_set.aggregate(total=Sum('total_amount'))['total'] or 0
        return format_html('<span class="price-display">{} VNĐ</span>', "{:,.0f}".format(float(total)))
    total_spent.short_description = 'Tổng chi tiêu'


class OrderItemInline(admin.TabularInline):
    """Inline for Order Items"""
    model = OrderItem
    extra = 0
    readonly_fields = ['total_price']
    
    def total_price(self, obj):
        if obj.pk:
            return format_html('<span class="price-display">{} VNĐ</span>', "{:,.0f}".format(float(obj.total_price)))
        return '-'
    total_price.short_description = 'Thành tiền'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Enhanced Admin for Order model"""
    list_display = ['order_id', 'customer_info', 'status_display', 'total_amount_display', 'delivery_zone', 'created_at']
    list_filter = [OrderStatusFilter, 'delivery_zone', 'created_at']
    search_fields = ['customer__user__username', 'customer__user__email', 'delivery_address']
    readonly_fields = ['created_at', 'updated_at', 'items_summary', 'delivery_route_map']
    list_editable = []
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Thông tin đơn hàng', {
            'fields': ('customer', 'status', 'payment_status'),
            'classes': ('wide',),
            'description': 'Cập nhật trạng thái đơn hàng và thanh toán'
        }),
        ('Thông tin giao hàng', {
            'fields': ('delivery_address', 'delivery_latitude', 'delivery_longitude', 'delivery_zone', 'assigned_farm'),
            'classes': ('wide',)
        }),
        ('Đường đi giao hàng', {
            'fields': ('delivery_route_map',),
            'classes': ('wide',)
        }),
        ('Thông tin thanh toán', {
            'fields': ('payment_method', 'payment_reference', 'payment_amount', 'payment_date', 'delivery_fee', 'total_amount'),
            'classes': ('wide',)
        }),
        ('Sản phẩm', {
            'fields': ('items_summary',),
            'classes': ('wide',)
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
        ('Ghi chú', {
            'fields': ('notes',),
            'classes': ('wide',)
        }),
    )
    
    def order_id(self, obj):
        return format_html('<strong>#{}</strong>', obj.id)
    order_id.short_description = 'Mã đơn hàng'
    
    def customer_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><small>{}</small>',
            obj.customer.user.get_full_name() or obj.customer.user.username,
            obj.customer.phone
        )
    customer_info.short_description = 'Khách hàng'
    
    def status_display(self, obj):
        status_colors = {
            'pending': 'warning',
            'confirmed': 'info',
            'preparing': 'primary',
            'shipping': 'info',
            'delivered': 'success',
            'cancelled': 'danger',
        }
        color = status_colors.get(obj.status, 'secondary')
        return format_html(
            '<span class="status-badge status-{}">{}</span>',
            obj.status, obj.get_status_display()
        )
    status_display.short_description = 'Trạng thái'
    
    def total_amount_display(self, obj):
        return format_html('<span class="price-display">{} VNĐ</span>', "{:,.0f}".format(float(obj.total_amount)))
    total_amount_display.short_description = 'Tổng tiền'
    
    def items_summary(self, obj):
        if obj.pk:
            items = obj.items.all()
            summary = []
            for item in items:
                summary.append(f"{item.product.name} x {item.quantity}")
            return mark_safe('<br>'.join(summary))
        return '-'
    items_summary.short_description = 'Sản phẩm đã đặt'
    
    def delivery_route_map(self, obj):
        """Hiển thị bản đồ với đường đi giao hàng thực tế"""
        if not obj.assigned_farm or not obj.delivery_latitude or not obj.delivery_longitude:
            return mark_safe('<span style="color: #6c757d;">Chưa có thông tin giao hàng hoặc chưa gán cửa hàng</span>')
        
        # Kiểm tra tọa độ farm
        if not obj.assigned_farm.latitude or not obj.assigned_farm.longitude:
            return mark_safe('<span style="color: #dc3545;">Cửa hàng chưa có tọa độ GPS</span>')
        
        # Tạo HTML cho bản đồ với route - Version đơn giản để debug
        map_html = f"""
        <div style="margin-bottom: 15px; padding: 15px; background: #f8f9fa; border-radius: 8px; border-left: 4px solid #007bff;">
            <h5 style="margin: 0 0 10px 0; color: #007bff;">
                <i class="fas fa-route"></i> Thông tin đường đi giao hàng
            </h5>
            <div class="row">
                <div class="col-md-6">
                    <p style="margin: 5px 0;">
                        <i class="fas fa-tractor" style="color: #28a745;"></i> 
                        <strong>Từ cửa hàng:</strong> {obj.assigned_farm.name}<br>
                        <small>📍 {obj.assigned_farm.latitude}, {obj.assigned_farm.longitude}</small>
                    </p>
                </div>
                <div class="col-md-6">
                    <p style="margin: 5px 0;">
                        <i class="fas fa-store" style="color: #dc3545;"></i> 
                        <strong>Đến khách hàng:</strong><br>
                        <small>📍 {obj.delivery_latitude}, {obj.delivery_longitude}</small><br>
                        <small>📍 {obj.delivery_address}</small>
                    </p>
                </div>
            </div>
            <div class="row mt-2">
                <div class="col-md-4">
                    <span style="background: #e3f2fd; padding: 4px 8px; border-radius: 4px; font-size: 12px;">
                        <i class="fas fa-route" style="color: #1976d2;"></i> 
                        {obj.delivery_distance_km or 'N/A'} km
                    </span>
                </div>
                <div class="col-md-4">
                    <span style="background: #fff3e0; padding: 4px 8px; border-radius: 4px; font-size: 12px;">
                        <i class="fas fa-clock" style="color: #f57c00;"></i> 
                        {obj.delivery_duration_min or 'N/A'} phút
                    </span>
                </div>
                <div class="col-md-4">
                    <span style="background: #e8f5e8; padding: 4px 8px; border-radius: 4px; font-size: 12px;">
                        <i class="fas fa-money-bill" style="color: #388e3c;"></i> 
                        {obj.delivery_fee or 'N/A'} VNĐ
                    </span>
                </div>
            </div>
        </div>
        
        <div id="delivery-route-map-{obj.id}" style="height: 400px; width: 100%; border: 1px solid #ddd; border-radius: 8px; position: relative;">
            <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; z-index: 1000;">
                <i class="fas fa-spinner fa-spin fa-2x" style="color: #007bff;"></i>
                <p style="margin: 10px 0 0 0; color: #666;">Đang tải bản đồ...</p>
            </div>
        </div>
        
        <div style="margin-top: 10px; text-align: center;">
            <a href="https://www.google.com/maps/dir/{obj.assigned_farm.latitude},{obj.assigned_farm.longitude}/{obj.delivery_latitude},{obj.delivery_longitude}" 
               target="_blank" class="btn btn-sm btn-outline-primary">
                <i class="fas fa-external-link-alt"></i> Xem trên Google Maps
            </a>
        </div>
        
        <script>
        console.log('🗺️ Initializing delivery route map for Order #{obj.id}');
        
        document.addEventListener('DOMContentLoaded', function() {{
            console.log('📍 DOM loaded, checking for Leaflet...');
            
            if (typeof L === 'undefined') {{
                console.error('❌ Leaflet not loaded!');
                document.getElementById('delivery-route-map-{obj.id}').innerHTML = 
                    '<div style="padding: 20px; text-align: center; color: #dc3545; background: #f8d7da; border-radius: 4px;">' +
                    '<i class="fas fa-exclamation-triangle"></i> Lỗi: Leaflet library chưa được tải' +
                    '</div>';
                return;
            }}
            
            console.log('✅ Leaflet loaded, initializing map...');
            
            try {{
                const mapId = 'delivery-route-map-{obj.id}';
                const mapContainer = document.getElementById(mapId);
                
                if (!mapContainer) {{
                    console.error('❌ Map container not found:', mapId);
                    return;
                }}
                
                // Clear loading message
                mapContainer.innerHTML = '';
                
                // Initialize map
                const map = L.map(mapId, {{
                    zoomControl: true,
                    scrollWheelZoom: true
                }});
                
                // Add tiles with proper referer policy
                L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                    attribution: '© OpenStreetMap contributors',
                    maxZoom: 18,
                    crossOrigin: true
                }}).addTo(map);
                
                // Farm marker
                const farmMarker = L.marker([{obj.assigned_farm.latitude}, {obj.assigned_farm.longitude}], {{
                    title: 'Cửa hàng: {obj.assigned_farm.name}'
                }}).addTo(map);
                
                farmMarker.bindPopup(`
                    <div style="text-align: center; min-width: 200px;">
                        <h6 style="margin: 0 0 8px 0; color: #28a745;">
                            <i class="fas fa-tractor"></i> Cửa hàng
                        </h6>
                        <strong>{obj.assigned_farm.name}</strong><br>
                        <small style="color: #666;">
                            📍 {obj.assigned_farm.latitude}, {obj.assigned_farm.longitude}
                        </small>
                    </div>
                `);
                
                // Customer marker
                const customerMarker = L.marker([{obj.delivery_latitude}, {obj.delivery_longitude}], {{
                    title: 'Khách hàng'
                }}).addTo(map);
                
                customerMarker.bindPopup(`
                    <div style="text-align: center; min-width: 200px;">
                        <h6 style="margin: 0 0 8px 0; color: #dc3545;">
                            <i class="fas fa-store"></i> Khách hàng
                        </h6>
                        <strong>{obj.delivery_address}</strong><br>
                        <small style="color: #666;">
                            📍 {obj.delivery_latitude}, {obj.delivery_longitude}
                        </small>
                    </div>
                `);
                
                // Draw simple line between points
                const routeLine = L.polyline([
                    [{obj.assigned_farm.latitude}, {obj.assigned_farm.longitude}],
                    [{obj.delivery_latitude}, {obj.delivery_longitude}]
                ], {{
                    color: '#007bff',
                    weight: 3,
                    opacity: 0.7,
                    dashArray: '10, 5'
                }}).addTo(map);
                
                // Fit map to show both points
                const group = new L.featureGroup([farmMarker, customerMarker, routeLine]);
                map.fitBounds(group.getBounds().pad(0.1));
                
                console.log('✅ Map initialized successfully!');
                
                // Try to get real route
                setTimeout(() => {{
                    console.log('🛣️ Attempting to get real route...');
                    getRealRoute(map, {obj.assigned_farm.latitude}, {obj.assigned_farm.longitude}, {obj.delivery_latitude}, {obj.delivery_longitude});
                }}, 1000);
                
            }} catch (error) {{
                console.error('❌ Error initializing map:', error);
                document.getElementById('delivery-route-map-{obj.id}').innerHTML = 
                    '<div style="padding: 20px; text-align: center; color: #dc3545; background: #f8d7da; border-radius: 4px;">' +
                    '<i class="fas fa-exclamation-triangle"></i> Lỗi tải bản đồ: ' + error.message +
                    '</div>';
            }}
        }});
        
        // Function to get real route
        function getRealRoute(map, farmLat, farmLng, customerLat, customerLng) {{
            const osrmUrl = `https://router.project-osrm.org/route/v1/driving/${{farmLng}},${{farmLat}};${{customerLng}},${{customerLat}}?overview=full&geometries=geojson`;
            
            fetch(osrmUrl)
                .then(response => response.json())
                .then(data => {{
                    if (data.routes && data.routes.length > 0) {{
                        const route = data.routes[0];
                        const routeCoordinates = route.geometry.coordinates.map(coord => [coord[1], coord[0]]);
                        
                        // Remove old simple line
                        map.eachLayer(layer => {{
                            if (layer instanceof L.Polyline && !(layer instanceof L.Polygon)) {{
                                map.removeLayer(layer);
                            }}
                        }});
                        
                        // Add real route
                        const realRoute = L.polyline(routeCoordinates, {{
                            color: '#28a745',
                            weight: 4,
                            opacity: 0.8
                        }}).addTo(map);
                        
                        // Add route info
                        const midPoint = routeCoordinates[Math.floor(routeCoordinates.length / 2)];
                        L.popup({{
                            closeButton: false,
                            autoClose: false,
                            closeOnClick: false
                        }})
                        .setLatLng(midPoint)
                        .setContent(`
                            <div style="text-align: center; font-size: 12px;">
                                <strong><i class="fas fa-route"></i> Đường đi thực tế</strong><br>
                                <span style="color: #28a745;">
                                    ${{(route.distance / 1000).toFixed(1)}} km - ${{Math.round(route.duration / 60)}} phút
                                </span>
                            </div>
                        `)
                        .addTo(map);
                        
                        console.log('✅ Real route loaded successfully!');
                    }} else {{
                        console.log('⚠️ No route found, keeping simple line');
                    }}
                }})
                .catch(error => {{
                    console.log('⚠️ Route API failed, keeping simple line:', error);
                }});
        }}
        </script>
        """
        return mark_safe(map_html)
    delivery_route_map.short_description = 'Đường đi giao hàng'
    
    def save_model(self, request, obj, form, change):
        """Override save to auto update delivered_at when status changes to delivered"""
        if change:  # Khi edit
            # Lấy giá trị cũ từ database
            old_obj = Order.objects.get(pk=obj.pk)
            
            # Nếu status chuyển sang 'delivered' và chưa có delivered_at
            if obj.status == 'delivered' and old_obj.status != 'delivered':
                if not obj.delivered_at:
                    obj.delivered_at = timezone.now()
                # Tự động cập nhật payment_status
                if obj.payment_method == 'cod':
                    obj.payment_status = 'completed'
                    obj.payment_amount = obj.total_amount
                    obj.payment_date = timezone.now()
        
        super().save_model(request, obj, form, change)


# Cart and CartItem admin classes removed as requested


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Enhanced Admin for OrderItem model"""
    list_display = ['order_id', 'product', 'quantity', 'price_display', 'total_price_display']
    readonly_fields = ['total_price_display']
    
    def order_id(self, obj):
        url = reverse('admin:food_store_order_change', args=[obj.order.id])
        return format_html('<a href="{}">#{}</a>', url, obj.order.id)
    order_id.short_description = 'Đơn hàng'
    
    def price_display(self, obj):
        return format_html('<span class="price-display">{} VNĐ</span>', "{:,.0f}".format(float(obj.price)))
    price_display.short_description = 'Đơn giá'
    
    def total_price_display(self, obj):
        return format_html('<span class="price-display">{} VNĐ</span>', "{:,.0f}".format(float(obj.total_price)))
    total_price_display.short_description = 'Thành tiền'


# Customize Admin Site
admin.site.site_header = "Clean Food GIS Admin"
admin.site.site_title = "Clean Food Admin"
admin.site.index_title = "Dashboard Quản Trị"

# Custom Admin Actions
def mark_orders_as_confirmed(modeladmin, request, queryset):
    """Mark selected orders as confirmed"""
    updated = queryset.update(status='confirmed')
    modeladmin.message_user(request, f'{updated} đơn hàng đã được xác nhận.')
mark_orders_as_confirmed.short_description = "Xác nhận đơn hàng đã chọn"

def mark_orders_as_shipping(modeladmin, request, queryset):
    """Mark selected orders as shipping"""
    updated = queryset.update(status='shipping')
    modeladmin.message_user(request, f'{updated} đơn hàng đã chuyển sang trạng thái giao hàng.')
mark_orders_as_shipping.short_description = "Chuyển sang giao hàng"

def mark_orders_as_delivered(modeladmin, request, queryset):
    """Mark selected orders as delivered"""
    from django.utils import timezone
    updated = queryset.update(status='delivered', delivered_at=timezone.now())
    modeladmin.message_user(request, f'{updated} đơn hàng đã được giao thành công.')
mark_orders_as_delivered.short_description = "Đánh dấu đã giao hàng"

def mark_products_as_available(modeladmin, request, queryset):
    """Mark selected products as available"""
    updated = queryset.update(is_available=True)
    modeladmin.message_user(request, f'{updated} sản phẩm đã được đánh dấu có sẵn.')
mark_products_as_available.short_description = "Đánh dấu có sẵn"

def mark_products_as_unavailable(modeladmin, request, queryset):
    """Mark selected products as unavailable"""
    updated = queryset.update(is_available=False)
    modeladmin.message_user(request, f'{updated} sản phẩm đã được đánh dấu không có sẵn.')
mark_products_as_unavailable.short_description = "Đánh dấu không có sẵn"

# Add actions to admin classes
OrderAdmin.actions = [mark_orders_as_confirmed, mark_orders_as_shipping, mark_orders_as_delivered]
ProductAdmin.actions = [mark_products_as_available, mark_products_as_unavailable]

# Export CSV Actions
import csv
from django.http import HttpResponse

def export_orders_csv(modeladmin, request, queryset):
    """Export selected orders to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="orders.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Mã đơn hàng', 'Khách hàng', 'Email', 'Điện thoại', 
        'Trạng thái', 'Địa chỉ giao hàng', 'Tổng tiền', 
        'Phí giao hàng', 'Ngày đặt', 'Ghi chú'
    ])
    
    for order in queryset:
        writer.writerow([
            order.id,
            order.customer.user.get_full_name() or order.customer.user.username,
            order.customer.user.email,
            order.customer.phone,
            order.get_status_display(),
            order.delivery_address,
            order.total_amount,
            order.delivery_fee,
            order.created_at.strftime('%d/%m/%Y %H:%M'),
            order.notes
        ])
    
    return response
export_orders_csv.short_description = "Xuất CSV đơn hàng đã chọn"

def export_products_csv(modeladmin, request, queryset):
    """Export selected products to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Tên sản phẩm', 'Danh mục', 'Cửa hàng', 'Giá', 
        'Đơn vị', 'Tồn kho', 'Có sẵn', 'Hữu cơ', 'Ngày tạo'
    ])
    
    for product in queryset:
        writer.writerow([
            product.name,
            product.category.name,
            product.farm.name,
            product.price,
            product.unit,
            product.stock_quantity,
            'Có' if product.is_available else 'Không',
            'Có' if product.farm.organic_certified else 'Không',
            product.created_at.strftime('%d/%m/%Y')
        ])
    
    return response
export_products_csv.short_description = "Xuất CSV sản phẩm đã chọn"

def export_customers_csv(modeladmin, request, queryset):
    """Export selected customers to CSV"""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="customers.csv"'
    
    writer = csv.writer(response)
    writer.writerow([
        'Tên đăng nhập', 'Họ tên', 'Email', 'Điện thoại', 
        'Địa chỉ', 'Số đơn hàng', 'Tổng chi tiêu', 'Ngày đăng ký'
    ])
    
    for customer in queryset:
        total_orders = customer.order_set.count()
        total_spent = sum(order.total_amount for order in customer.order_set.all())
        
        writer.writerow([
            customer.user.username,
            customer.user.get_full_name() or '',
            customer.user.email,
            customer.phone,
            customer.address,
            total_orders,
            total_spent,
            customer.created_at.strftime('%d/%m/%Y')
        ])
    
    return response
export_customers_csv.short_description = "Xuất CSV khách hàng đã chọn"

# Add export actions
OrderAdmin.actions.extend([export_orders_csv])
ProductAdmin.actions.extend([export_products_csv])
CustomerAdmin.actions = [export_customers_csv]
# Custom dashboard functionality removed for minimal version



# ============================================
# QUẢN LÝ XUẤT NHẬP KHO
# ============================================

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """Quản lý nhà cung cấp"""
    list_display = ['name', 'contact_person', 'phone', 'email', 'is_active_status', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'contact_person', 'phone', 'email', 'tax_code']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = []
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('name', 'contact_person', 'phone', 'email'),
            'classes': ('wide',)
        }),
        ('Địa chỉ và thuế', {
            'fields': ('address', 'tax_code'),
            'classes': ('wide',)
        }),
        ('Trạng thái', {
            'fields': ('is_active', 'notes'),
            'classes': ('wide',)
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_active_status(self, obj):
        if obj.is_active:
            return mark_safe('<span style="color: #28a745;"><i class="fas fa-check-circle"></i> Hoạt động</span>')
        return mark_safe('<span style="color: #dc3545;"><i class="fas fa-times-circle"></i> Ngừng</span>')
    is_active_status.short_description = 'Trạng thái'


class TransactionTypeFilter(SimpleListFilter):
    """Filter by transaction type"""
    title = 'Loại giao dịch'
    parameter_name = 'transaction_type'
    
    def lookups(self, request, model_admin):
        return StockTransaction.TRANSACTION_TYPE_CHOICES
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(transaction_type=self.value())


@admin.register(StockTransaction)
class StockTransactionAdmin(admin.ModelAdmin):
    """Quản lý giao dịch xuất nhập kho"""
    list_display = [
        'id', 'transaction_type_badge', 'product', 'farm', 'quantity_display',
        'unit_price', 'total_amount', 'stock_change', 'created_by', 'created_at'
    ]
    list_filter = [TransactionTypeFilter, 'farm', 'created_at']
    search_fields = ['product__name', 'reference_number', 'notes']
    readonly_fields = ['stock_before', 'stock_after', 'created_at', 'total_amount']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Thông tin giao dịch', {
            'fields': ('transaction_type', 'product', 'farm', 'quantity'),
            'classes': ('wide',)
        }),
        ('Liên kết', {
            'fields': ('supplier', 'order', 'reference_number'),
            'classes': ('wide',)
        }),
        ('Giá trị', {
            'fields': ('unit_price', 'total_amount'),
            'classes': ('wide',)
        }),
        ('Tồn kho', {
            'fields': ('stock_before', 'stock_after'),
            'classes': ('wide',)
        }),
        ('Ghi chú', {
            'fields': ('notes',),
            'classes': ('wide',)
        }),
        ('Thông tin tạo', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def transaction_type_badge(self, obj):
        colors = {
            'import': '#28a745',
            'export': '#dc3545',
            'adjustment': '#ffc107',
            'return': '#17a2b8',
            'damaged': '#6c757d',
        }
        icons = {
            'import': 'fa-arrow-down',
            'export': 'fa-arrow-up',
            'adjustment': 'fa-edit',
            'return': 'fa-undo',
            'damaged': 'fa-exclamation-triangle',
        }
        color = colors.get(obj.transaction_type, '#6c757d')
        icon = icons.get(obj.transaction_type, 'fa-circle')
        return mark_safe(
            f'<span style="color: {color}; font-weight: bold;">'
            f'<i class="fas {icon}"></i> {obj.get_transaction_type_display()}'
            f'</span>'
        )
    transaction_type_badge.short_description = 'Loại'
    
    def quantity_display(self, obj):
        if obj.transaction_type == 'import':
            return mark_safe(f'<span style="color: #28a745; font-weight: bold;">+{obj.quantity}</span>')
        elif obj.transaction_type in ['export', 'damaged']:
            return mark_safe(f'<span style="color: #dc3545; font-weight: bold;">-{abs(obj.quantity)}</span>')
        return obj.quantity
    quantity_display.short_description = 'Số lượng'
    
    def stock_change(self, obj):
        change = obj.stock_after - obj.stock_before
        if change > 0:
            return mark_safe(
                f'<span style="color: #28a745;">'
                f'{obj.stock_before} → {obj.stock_after} (+{change})'
                f'</span>'
            )
        elif change < 0:
            return mark_safe(
                f'<span style="color: #dc3545;">'
                f'{obj.stock_before} → {obj.stock_after} ({change})'
                f'</span>'
            )
        return f'{obj.stock_before} → {obj.stock_after}'
    stock_change.short_description = 'Thay đổi tồn kho'
    
    def has_delete_permission(self, request, obj=None):
        # Không cho xóa giao dịch kho để đảm bảo tính toàn vẹn dữ liệu
        return False
    
    def has_change_permission(self, request, obj=None):
        # Không cho sửa giao dịch kho để đảm bảo tính toàn vẹn dữ liệu
        # Vì logic cập nhật tồn kho chỉ chạy khi tạo mới (if not self.pk)
        # Nếu cho phép sửa, tồn kho sẽ không được cập nhật đúng
        return False


class AlertTypeFilter(SimpleListFilter):
    """Filter by alert type"""
    title = 'Loại cảnh báo'
    parameter_name = 'alert_type'
    
    def lookups(self, request, model_admin):
        return StockAlert.ALERT_TYPE_CHOICES
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(alert_type=self.value())


@admin.register(StockAlert)
class StockAlertAdmin(admin.ModelAdmin):
    """Quản lý cảnh báo tồn kho"""
    list_display = [
        'id', 'alert_type_badge', 'product', 'farm', 'current_stock',
        'threshold', 'status_badge', 'created_at'
    ]
    list_filter = [AlertTypeFilter, 'is_resolved', 'farm', 'created_at']
    search_fields = ['product__name', 'notes']
    readonly_fields = ['created_at', 'resolved_at']
    date_hierarchy = 'created_at'
    actions = ['mark_as_resolved']
    
    fieldsets = (
        ('Thông tin cảnh báo', {
            'fields': ('alert_type', 'product', 'farm'),
            'classes': ('wide',)
        }),
        ('Số liệu', {
            'fields': ('current_stock', 'threshold'),
            'classes': ('wide',)
        }),
        ('Xử lý', {
            'fields': ('is_resolved', 'resolved_at', 'resolved_by', 'notes'),
            'classes': ('wide',)
        }),
        ('Thời gian', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def alert_type_badge(self, obj):
        colors = {
            'low_stock': '#ffc107',
            'out_of_stock': '#dc3545',
            'overstock': '#17a2b8',
            'expiring_soon': '#fd7e14',
        }
        icons = {
            'low_stock': 'fa-exclamation-triangle',
            'out_of_stock': 'fa-times-circle',
            'overstock': 'fa-boxes',
            'expiring_soon': 'fa-clock',
        }
        color = colors.get(obj.alert_type, '#6c757d')
        icon = icons.get(obj.alert_type, 'fa-bell')
        return mark_safe(
            f'<span style="color: {color}; font-weight: bold;">'
            f'<i class="fas {icon}"></i> {obj.get_alert_type_display()}'
            f'</span>'
        )
    alert_type_badge.short_description = 'Loại cảnh báo'
    
    def status_badge(self, obj):
        if obj.is_resolved:
            return mark_safe(
                '<span style="color: #28a745;"><i class="fas fa-check-circle"></i> Đã xử lý</span>'
            )
        return mark_safe(
            '<span style="color: #dc3545;"><i class="fas fa-exclamation-circle"></i> Chưa xử lý</span>'
        )
    status_badge.short_description = 'Trạng thái'
    
    def mark_as_resolved(self, request, queryset):
        updated = queryset.update(
            is_resolved=True,
            resolved_at=timezone.now(),
            resolved_by=request.user
        )
        self.message_user(request, f'Đã đánh dấu {updated} cảnh báo là đã xử lý.')
    mark_as_resolved.short_description = 'Đánh dấu đã xử lý'


@admin.register(InventoryReport)
class InventoryReportAdmin(admin.ModelAdmin):
    """Quản lý báo cáo kiểm kê"""
    list_display = [
        'id', 'farm', 'report_date', 'total_products', 'total_quantity',
        'total_value_display', 'created_by', 'created_at'
    ]
    list_filter = ['farm', 'report_date', 'created_at']
    search_fields = ['farm__name', 'notes']
    readonly_fields = ['created_at']
    date_hierarchy = 'report_date'
    
    fieldsets = (
        ('Thông tin kiểm kê', {
            'fields': ('farm', 'report_date'),
            'classes': ('wide',)
        }),
        ('Thống kê', {
            'fields': ('total_products', 'total_quantity', 'total_value'),
            'classes': ('wide',)
        }),
        ('Ghi chú', {
            'fields': ('notes',),
            'classes': ('wide',)
        }),
        ('Thông tin tạo', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def total_value_display(self, obj):
        if obj.total_value:
            formatted_value = "{:,.0f}".format(float(obj.total_value))
            return format_html(
                '<span style="color: #28a745; font-weight: bold;">{} VNĐ</span>',
                formatted_value
            )
        return format_html('<span style="color: #6c757d;">0 VNĐ</span>')
    total_value_display.short_description = 'Tổng giá trị'


@admin.register(Shipper)
class ShipperAdmin(admin.ModelAdmin):
    """Admin for Shipper model"""
    list_display = ['user_full_name', 'phone', 'vehicle_display', 'status_badge', 'total_deliveries', 'rating_display', 'is_active']
    list_filter = ['status', 'vehicle_type', 'is_active', 'delivery_zones']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone', 'vehicle_number']
    readonly_fields = ['total_deliveries', 'created_at', 'updated_at', 'last_location_update']
    filter_horizontal = ['delivery_zones']
    
    fieldsets = (
        ('Thông tin cơ bản', {
            'fields': ('user', 'phone', 'is_active')
        }),
        ('Phương tiện', {
            'fields': ('vehicle_type', 'vehicle_number')
        }),
        ('Vị trí hiện tại', {
            'fields': ('current_latitude', 'current_longitude', 'last_location_update'),
            'classes': ('collapse',)
        }),
        ('Trạng thái & Khu vực', {
            'fields': ('status', 'delivery_zones')
        }),
        ('Thống kê', {
            'fields': ('total_deliveries', 'rating'),
            'classes': ('collapse',)
        }),
        ('Thời gian', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    user_full_name.short_description = 'Tên shipper'
    
    def vehicle_display(self, obj):
        vehicle_icons = {
            'bike': '🚲',
            'motorbike': '🏍️',
            'car': '🚗'
        }
        icon = vehicle_icons.get(obj.vehicle_type, '🚗')
        return format_html(
            '{} {} ({})',
            icon,
            obj.get_vehicle_type_display(),
            obj.vehicle_number
        )
    vehicle_display.short_description = 'Phương tiện'
    
    def status_badge(self, obj):
        colors = {
            'available': 'success',
            'busy': 'warning',
            'offline': 'secondary'
        }
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            colors.get(obj.status, 'secondary'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Trạng thái'
    
    def rating_display(self, obj):
        stars = '⭐' * int(obj.rating)
        return format_html('{} ({})', stars, obj.rating)
    rating_display.short_description = 'Đánh giá'
    
    actions = ['mark_available', 'mark_offline']
    
    def mark_available(self, request, queryset):
        updated = queryset.update(status='available')
        self.message_user(request, f'{updated} shipper đã được đánh dấu sẵn sàng.')
    mark_available.short_description = 'Đánh dấu sẵn sàng'
    
    def mark_offline(self, request, queryset):
        updated = queryset.update(status='offline')
        self.message_user(request, f'{updated} shipper đã được đánh dấu offline.')
    mark_offline.short_description = 'Đánh dấu offline'
