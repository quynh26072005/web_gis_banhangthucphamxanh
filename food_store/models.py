"""
Models for Clean Food Store - Cart Test Version (without GIS)
"""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Farm(models.Model):
    """Model for farms that supply clean food"""
    name = models.CharField(max_length=200, verbose_name="Tên trang trại")
    address = models.TextField(verbose_name="Địa chỉ")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    email = models.EmailField(blank=True, verbose_name="Email")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    
    # Temporary coordinates as float fields
    latitude = models.FloatField(null=True, blank=True, verbose_name="Vĩ độ")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Kinh độ")
    
    # Certification info
    organic_certified = models.BooleanField(default=False, verbose_name="Chứng nhận hữu cơ")
    certification_number = models.CharField(max_length=100, blank=True, verbose_name="Số chứng nhận")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Trang trại"
        verbose_name_plural = "Trang trại"
    
    def __str__(self):
        return self.name


class Category(models.Model):
    """Product categories"""
    name = models.CharField(max_length=100, verbose_name="Tên danh mục")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    image = models.ImageField(upload_to='categories/', blank=True, verbose_name="Hình ảnh")
    
    class Meta:
        verbose_name = "Danh mục"
        verbose_name_plural = "Danh mục"
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Clean food products"""
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Danh mục")
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, verbose_name="Trang trại")
    
    description = models.TextField(verbose_name="Mô tả sản phẩm")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá (VNĐ)")
    unit = models.CharField(max_length=20, default="kg", verbose_name="Đơn vị")
    
    # Product images
    image = models.ImageField(upload_to='products/', verbose_name="Hình ảnh chính")
    
    # Stock management
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Số lượng tồn kho")
    is_available = models.BooleanField(default=True, verbose_name="Còn hàng")
    
    # Nutritional info
    nutritional_info = models.TextField(blank=True, verbose_name="Thông tin dinh dưỡng")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"
    
    def __str__(self):
        return f"{self.name} - {self.farm.name}"
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})


class DeliveryZone(models.Model):
    """Delivery zones"""
    name = models.CharField(max_length=100, verbose_name="Tên khu vực giao hàng")
    
    # Temporary area description
    area_description = models.TextField(verbose_name="Mô tả khu vực")
    
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Phí giao hàng")
    delivery_time = models.CharField(max_length=50, verbose_name="Thời gian giao hàng")
    
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    
    class Meta:
        verbose_name = "Khu vực giao hàng"
        verbose_name_plural = "Khu vực giao hàng"
    
    def __str__(self):
        return self.name


class Customer(models.Model):
    """Customer profile with delivery location"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    address = models.TextField(verbose_name="Địa chỉ")
    
    # Temporary coordinates as float fields
    latitude = models.FloatField(null=True, blank=True, verbose_name="Vĩ độ")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Kinh độ")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Khách hàng"
        verbose_name_plural = "Khách hàng"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.phone}"


class Cart(models.Model):
    """Shopping cart for customers"""
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, verbose_name="Khách hàng")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Giỏ hàng"
        verbose_name_plural = "Giỏ hàng"
    
    def __str__(self):
        return f"Giỏ hàng - {self.customer.user.get_full_name()}"
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    """Items in shopping cart"""
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Sản phẩm")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Số lượng")
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Sản phẩm trong giỏ hàng"
        verbose_name_plural = "Sản phẩm trong giỏ hàng"
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def total_price(self):
        return self.quantity * self.product.price


class Order(models.Model):
    """Customer orders"""
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('confirmed', 'Đã xác nhận'),
        ('preparing', 'Đang chuẩn bị'),
        ('shipping', 'Đang giao hàng'),
        ('delivered', 'Đã giao hàng'),
        ('cancelled', 'Đã hủy'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Khách hàng")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    
    # Delivery info
    delivery_address = models.TextField(verbose_name="Địa chỉ giao hàng")
    delivery_latitude = models.FloatField(null=True, blank=True, verbose_name="Vĩ độ giao hàng")
    delivery_longitude = models.FloatField(null=True, blank=True, verbose_name="Kinh độ giao hàng")
    delivery_zone = models.ForeignKey(DeliveryZone, on_delete=models.SET_NULL, null=True, verbose_name="Khu vực giao hàng")
    
    # Auto-assigned farm for optimized delivery
    assigned_farm = models.ForeignKey(
        Farm, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_orders',
        verbose_name="Trang trại được gán",
        help_text="Trang trại gần nhất được tự động gán để giao hàng"
    )
    
    # Routing information (for customer display)
    delivery_distance_km = models.FloatField(
        null=True, 
        blank=True, 
        verbose_name="Khoảng cách giao hàng (km)",
        help_text="Khoảng cách đường bộ thực tế từ farm đến khách hàng"
    )
    delivery_duration_min = models.FloatField(
        null=True, 
        blank=True, 
        verbose_name="Thời gian giao hàng (phút)",
        help_text="Thời gian di chuyển ước tính"
    )
    
    # Order totals
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Tổng tiền hàng")
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Phí giao hàng")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Tổng thanh toán")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày đặt hàng")
    updated_at = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(blank=True, null=True, verbose_name="Ngày giao hàng")
    
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    
    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Đơn hàng #{self.pk} - {self.customer.user.get_full_name()}"
    
    def auto_assign_nearest_farm(self):
        """Tự động gán farm gần nhất dựa trên ĐƯỜNG ĐI THỰC TẾ"""
        if not self.delivery_latitude or not self.delivery_longitude:
            return None
        
        from gis_tools.gis_functions import FarmLocationAnalyzer
        
        # Tìm farm gần nhất theo ROAD ROUTING
        nearest_farms = FarmLocationAnalyzer.find_nearest_farms_by_road(
            self.delivery_latitude,
            self.delivery_longitude,
            max_distance_km=50
        )
        
        if nearest_farms:
            # Lấy farm đầu tiên (gần nhất theo đường bộ)
            nearest_farm = nearest_farms[0]
            self.assigned_farm = nearest_farm
            
            # Return route info để caller có thể dùng
            return {
                'farm': nearest_farm,
                'distance_km': nearest_farm.distance_km,
                'duration_min': nearest_farm.duration_min,
                'shipping_fee': nearest_farm.shipping_fee,
                'route_geometry': nearest_farm.route_geometry
            }
        
        return None
    
    def save(self, *args, **kwargs):
        """Override save để tự động gán farm nếu chưa có"""
        # Chỉ auto-assign nếu chưa có assigned_farm
        if not self.assigned_farm and self.delivery_latitude and self.delivery_longitude:
            self.auto_assign_nearest_farm()
        
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Items in an order"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Sản phẩm")
    quantity = models.PositiveIntegerField(verbose_name="Số lượng")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá")
    
    class Meta:
        verbose_name = "Sản phẩm trong đơn hàng"
        verbose_name_plural = "Sản phẩm trong đơn hàng"
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def total_price(self):
        return self.quantity * self.price