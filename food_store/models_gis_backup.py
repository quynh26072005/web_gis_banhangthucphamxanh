"""
Models for Clean Food Store with GIS integration
"""
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Farm(models.Model):
    """Model for farms that supply clean food"""
    name = models.CharField(max_length=200, verbose_name="Tên trang trại")
    address = models.TextField(verbose_name="Địa chỉ")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    email = models.EmailField(blank=True, verbose_name="Email")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    
    # GIS field for farm location
    location = models.PointField(verbose_name="Vị trí trang trại", help_text="Chọn vị trí trên bản đồ")
    
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
    """Delivery zones with GIS polygon"""
    name = models.CharField(max_length=100, verbose_name="Tên khu vực giao hàng")
    
    # GIS field for delivery area
    area = models.PolygonField(verbose_name="Khu vực giao hàng")
    
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
    
    # GIS field for customer location
    location = models.PointField(blank=True, null=True, verbose_name="Vị trí giao hàng")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Khách hàng"
        verbose_name_plural = "Khách hàng"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.phone}"


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
    delivery_location = models.PointField(verbose_name="Vị trí giao hàng")
    delivery_zone = models.ForeignKey(DeliveryZone, on_delete=models.SET_NULL, null=True, verbose_name="Khu vực giao hàng")
    
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