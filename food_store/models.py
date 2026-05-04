"""
Models for Clean Food Store
"""
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Farm(models.Model):
    """Model for stores that supply clean food"""
    name = models.CharField(max_length=200)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    description = models.TextField(blank=True)
    
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    organic_certified = models.BooleanField(default=False)
    certification_number = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Store"
        verbose_name_plural = "Stores"
    
    def __str__(self):
        return self.name


class Category(models.Model):
    """Product categories"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Clean food products"""
    name = models.CharField(max_length=200, verbose_name="Tên sản phẩm")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Danh mục")
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, verbose_name="Cửa hàng")
    
    description = models.TextField(verbose_name="Mô tả")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Giá")
    unit = models.CharField(max_length=20, default="kg", verbose_name="Đơn vị")
    
    image = models.ImageField(upload_to='products/', verbose_name="Hình ảnh")
    
    stock_quantity = models.PositiveIntegerField(default=0, verbose_name="Số lượng tồn kho")
    is_available = models.BooleanField(default=True, verbose_name="Còn hàng")
    
    nutritional_info = models.TextField(blank=True, verbose_name="Thông tin dinh dưỡng")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Sản phẩm"
        verbose_name_plural = "Sản phẩm"
    
    def __str__(self):
        return f"{self.name} - {self.farm.name}"
    
    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'pk': self.pk})


class DeliveryZone(models.Model):
    """Delivery zones"""
    name = models.CharField(max_length=100)
    area_description = models.TextField()
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2)
    delivery_time = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Delivery Zone"
        verbose_name_plural = "Delivery Zones"
    
    def __str__(self):
        return self.name


class Customer(models.Model):
    """Customer profile with delivery location"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Người dùng")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    address = models.TextField(verbose_name="Địa chỉ")
    latitude = models.FloatField(null=True, blank=True, verbose_name="Vĩ độ")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Kinh độ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Khách hàng"
        verbose_name_plural = "Khách hàng"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.phone}"


class Shipper(models.Model):
    """Shipper/Delivery person profile"""
    STATUS_CHOICES = [
        ('available', 'Sẵn sàng'),
        ('busy', 'Đang giao hàng'),
        ('offline', 'Đang nghỉ'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Người dùng")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    vehicle_number = models.CharField(max_length=50, verbose_name="Biển số xe")
    
    # Assign to specific farm/store
    assigned_farm = models.ForeignKey(
        'Farm',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='shippers',
        verbose_name="Chi nhánh phụ trách"
    )
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='offline', verbose_name="Trạng thái")
    
    # Statistics
    total_deliveries = models.IntegerField(default=0, verbose_name="Tổng số đơn đã giao")
    today_deliveries = models.IntegerField(default=0, verbose_name="Số đơn hôm nay")
    cod_holding = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Tiền COD đang giữ")
    today_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name="Thu nhập hôm nay")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Shipper"
        verbose_name_plural = "Shippers"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.phone}"


class StoreAdmin(models.Model):
    """Store Admin - Quản lý chi nhánh"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Người dùng")
    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name='store_admins',
        verbose_name="Chi nhánh quản lý"
    )
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    
    # Permissions
    can_manage_products = models.BooleanField(default=True, verbose_name="Quản lý sản phẩm")
    can_manage_orders = models.BooleanField(default=True, verbose_name="Quản lý đơn hàng")
    can_manage_inventory = models.BooleanField(default=True, verbose_name="Quản lý kho")
    can_manage_shippers = models.BooleanField(default=True, verbose_name="Quản lý shipper")
    can_view_reports = models.BooleanField(default=True, verbose_name="Xem báo cáo")
    
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    
    class Meta:
        verbose_name = "Quản lý chi nhánh"
        verbose_name_plural = "Quản lý chi nhánh"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.farm.name}"


class Cart(models.Model):
    """Shopping cart for customers"""
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
    
    def __str__(self):
        return f"Cart - {self.customer.user.get_full_name()}"
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
    
    @property
    def total_amount(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    """Items in shopping cart"""
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
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
        ('shipping', 'Đang giao hàng'),
        ('delivered', 'Đã giao hàng'),
        ('cancelled', 'Đã hủy'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('cod', 'Thanh toán khi nhận hàng (COD)'),
        ('bank_transfer', 'Chuyển khoản ngân hàng'),
        ('momo', 'Ví MoMo'),
        ('zalopay', 'ZaloPay'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Khách hàng")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    
    # Payment fields
    payment_method = models.CharField(
        max_length=20, 
        choices=PAYMENT_METHOD_CHOICES, 
        default='cod',
        verbose_name="Phương thức thanh toán"
    )
    payment_reference = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name="Mã tham chiếu thanh toán"
    )
    payment_status = models.CharField(
        max_length=20,
        default='pending',
        verbose_name="Trạng thái thanh toán"
    )
    payment_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Số tiền thanh toán"
    )
    payment_date = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Ngày thanh toán"
    )
    
    delivery_address = models.TextField(verbose_name="Địa chỉ giao hàng")
    delivery_latitude = models.FloatField(null=True, blank=True, verbose_name="Vĩ độ")
    delivery_longitude = models.FloatField(null=True, blank=True, verbose_name="Kinh độ")
    delivery_zone = models.ForeignKey(DeliveryZone, on_delete=models.SET_NULL, null=True, verbose_name="Khu vực giao hàng")
    
    assigned_farm = models.ForeignKey(
        Farm, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_orders',
        verbose_name="Cửa hàng phụ trách"
    )
    
    # Shipper fields
    assigned_shipper = models.ForeignKey(
        'Shipper',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_orders',
        verbose_name="Shipper phụ trách"
    )
    shipper_accepted_at = models.DateTimeField(null=True, blank=True, verbose_name="Thời gian nhận đơn")
    shipper_picked_at = models.DateTimeField(null=True, blank=True, verbose_name="Thời gian lấy hàng")
    shipper_notes = models.TextField(blank=True, verbose_name="Ghi chú của shipper")
    proof_image = models.ImageField(upload_to='delivery_proofs/', blank=True, null=True, verbose_name="Ảnh chứng minh giao hàng")
    
    delivery_distance_km = models.FloatField(null=True, blank=True, verbose_name="Khoảng cách giao hàng (km)")
    delivery_duration_min = models.FloatField(null=True, blank=True, verbose_name="Thời gian giao hàng (phút)")
    
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Phí giao hàng")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Tổng tiền")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")
    delivered_at = models.DateTimeField(blank=True, null=True, verbose_name="Ngày giao hàng")
    
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    
    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order #{self.pk} - {self.customer.user.get_full_name()}"
    
    def auto_assign_nearest_farm(self):
        """Auto assign nearest farm based on actual road distance"""
        if not self.delivery_latitude or not self.delivery_longitude:
            return None
        
        from gis_tools.gis_functions import FarmLocationAnalyzer
        
        try:
            nearest_farms = FarmLocationAnalyzer.find_nearest_farms_by_road(
                self.delivery_latitude,
                self.delivery_longitude,
                max_distance_km=50
            )
        except:
            from django.db.models import Q
            import math
            
            farms = Farm.objects.filter(
                latitude__isnull=False,
                longitude__isnull=False
            )
            
            nearest_farm = None
            min_distance = float('inf')
            
            for farm in farms:
                lat1, lon1 = math.radians(self.delivery_latitude), math.radians(self.delivery_longitude)
                lat2, lon2 = math.radians(farm.latitude), math.radians(farm.longitude)
                
                dlat = lat2 - lat1
                dlon = lon2 - lon1
                a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
                c = 2 * math.asin(math.sqrt(a))
                distance = 6371 * c
                
                if distance < min_distance:
                    min_distance = distance
                    nearest_farm = farm
            
            if nearest_farm:
                self.assigned_farm = nearest_farm
                
                base_fee = 15000
                distance_fee = min_distance * 2000
                total_fee = base_fee + distance_fee
                
                if total_fee > 50000:
                    total_fee = 50000
                
                return {
                    'farm': nearest_farm,
                    'distance_km': min_distance,
                    'duration_min': min_distance * 2,
                    'shipping_fee': float(total_fee),
                    'route_geometry': None,
                    'is_free_shipping': total_fee == 0,
                    'breakdown': {
                        'base_fee': base_fee,
                        'distance_fee': distance_fee,
                        'total': total_fee
                    }
                }
            
            return None
        
        if nearest_farms:
            nearest_farm = nearest_farms[0]
            self.assigned_farm = nearest_farm
            
            base_fee = 15000
            distance_km = getattr(nearest_farm, 'distance_km', 10)
            distance_fee = distance_km * 2000
            total_fee = base_fee + distance_fee
            
            if total_fee > 50000:
                total_fee = 50000
            
            return {
                'farm': nearest_farm,
                'distance_km': distance_km,
                'duration_min': distance_km * 2,
                'shipping_fee': float(total_fee),
                'route_geometry': None,
                'is_free_shipping': total_fee == 0,
                'breakdown': {
                    'base_fee': base_fee,
                    'distance_fee': distance_fee,
                    'total': total_fee
                }
            }
        
        return None
    
    def save(self, *args, **kwargs):
        """Override save to auto assign farm if not set"""
        if not self.assigned_farm and self.delivery_latitude and self.delivery_longitude:
            self.auto_assign_nearest_farm()
        
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Items in an order"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def total_price(self):
        return self.quantity * self.price



class Supplier(models.Model):
    """Nhà cung cấp"""
    name = models.CharField(max_length=200, verbose_name="Tên nhà cung cấp")
    contact_person = models.CharField(max_length=100, verbose_name="Người liên hệ")
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    email = models.EmailField(blank=True, verbose_name="Email")
    address = models.TextField(verbose_name="Địa chỉ")
    tax_code = models.CharField(max_length=50, blank=True, verbose_name="Mã số thuế")
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Nhà cung cấp"
        verbose_name_plural = "Nhà cung cấp"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name


class StockTransaction(models.Model):
    """Giao dịch xuất nhập kho"""
    TRANSACTION_TYPE_CHOICES = [
        ('import', 'Nhập kho'),
        ('export', 'Xuất kho'),
        ('adjustment', 'Điều chỉnh'),
        ('return', 'Trả hàng'),
        ('damaged', 'Hư hỏng'),
    ]
    
    transaction_type = models.CharField(
        max_length=20, 
        choices=TRANSACTION_TYPE_CHOICES,
        verbose_name="Loại giao dịch"
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        related_name='stock_transactions',
        verbose_name="Sản phẩm"
    )
    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name='stock_transactions',
        verbose_name="Cửa hàng"
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Nhà cung cấp"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='stock_transactions',
        verbose_name="Đơn hàng"
    )
    
    quantity = models.IntegerField(verbose_name="Số lượng")  # Dương = nhập, Âm = xuất
    unit_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Đơn giá"
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Tổng tiền"
    )
    
    stock_before = models.IntegerField(verbose_name="Tồn kho trước")
    stock_after = models.IntegerField(verbose_name="Tồn kho sau")
    
    reference_number = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Số chứng từ"
    )
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Người tạo"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Giao dịch kho"
        verbose_name_plural = "Giao dịch kho"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['product', '-created_at']),
            models.Index(fields=['farm', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.product.name} ({self.quantity})"
    
    def save(self, *args, **kwargs):
        # Tính tổng tiền
        if self.unit_price and self.quantity:
            self.total_amount = abs(self.quantity) * self.unit_price
        
        # Lưu tồn kho trước
        if not self.pk:  # Chỉ khi tạo mới
            self.stock_before = self.product.stock_quantity
            
            # Kiểm tra tồn kho trước khi xuất
            if self.transaction_type in ['export', 'damaged']:
                if abs(self.quantity) > self.product.stock_quantity:
                    from django.core.exceptions import ValidationError
                    raise ValidationError(
                        f'Không đủ hàng trong kho! '
                        f'Tồn kho hiện tại: {self.product.stock_quantity}, '
                        f'Số lượng xuất: {abs(self.quantity)}'
                    )
            
            # Cập nhật tồn kho sản phẩm
            if self.transaction_type == 'import':
                self.product.stock_quantity += abs(self.quantity)
            elif self.transaction_type in ['export', 'damaged']:
                self.product.stock_quantity -= abs(self.quantity)
            elif self.transaction_type == 'adjustment':
                self.product.stock_quantity = abs(self.quantity)
            elif self.transaction_type == 'return':
                self.product.stock_quantity += abs(self.quantity)
            
            # Đảm bảo không âm
            if self.product.stock_quantity < 0:
                self.product.stock_quantity = 0
            
            self.stock_after = self.product.stock_quantity
            self.product.save()
        
        super().save(*args, **kwargs)


class StockAlert(models.Model):
    """Cảnh báo tồn kho"""
    ALERT_TYPE_CHOICES = [
        ('low_stock', 'Sắp hết hàng'),
        ('out_of_stock', 'Hết hàng'),
        ('overstock', 'Tồn kho quá nhiều'),
        ('expiring_soon', 'Sắp hết hạn'),
    ]
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='stock_alerts',
        verbose_name="Sản phẩm"
    )
    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name='stock_alerts',
        verbose_name="Cửa hàng"
    )
    alert_type = models.CharField(
        max_length=20,
        choices=ALERT_TYPE_CHOICES,
        verbose_name="Loại cảnh báo"
    )
    threshold = models.IntegerField(
        verbose_name="Ngưỡng cảnh báo",
        help_text="Số lượng tồn kho để kích hoạt cảnh báo"
    )
    current_stock = models.IntegerField(verbose_name="Tồn kho hiện tại")
    is_resolved = models.BooleanField(default=False, verbose_name="Đã xử lý")
    resolved_at = models.DateTimeField(null=True, blank=True, verbose_name="Ngày xử lý")
    resolved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_alerts',
        verbose_name="Người xử lý"
    )
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Cảnh báo tồn kho"
        verbose_name_plural = "Cảnh báo tồn kho"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.product.name}"


class InventoryReport(models.Model):
    """Báo cáo kiểm kê"""
    farm = models.ForeignKey(
        Farm,
        on_delete=models.CASCADE,
        related_name='inventory_reports',
        verbose_name="Cửa hàng"
    )
    report_date = models.DateField(verbose_name="Ngày kiểm kê")
    total_products = models.IntegerField(default=0, verbose_name="Tổng số sản phẩm")
    total_quantity = models.IntegerField(default=0, verbose_name="Tổng số lượng")
    total_value = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Tổng giá trị"
    )
    notes = models.TextField(blank=True, verbose_name="Ghi chú")
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Người tạo"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    
    class Meta:
        verbose_name = "Báo cáo kiểm kê"
        verbose_name_plural = "Báo cáo kiểm kê"
        ordering = ['-report_date']
    
    def __str__(self):
        return f"Kiểm kê {self.farm.name} - {self.report_date}"


# ============================================
# Email Verification & Password Reset Models
# ============================================

from datetime import timedelta
from django.utils import timezone
import random
import string


class EmailVerification(models.Model):
    """
    Model lưu mã OTP để xác thực email khi đăng ký
    """
    email = models.EmailField(verbose_name="Email")
    otp_code = models.CharField(max_length=6, verbose_name="Mã OTP")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian tạo")
    expires_at = models.DateTimeField(verbose_name="Thời gian hết hạn")
    is_verified = models.BooleanField(default=False, verbose_name="Đã xác thực")
    attempts = models.IntegerField(default=0, verbose_name="Số lần thử")
    
    # Thông tin đăng ký tạm thời
    username = models.CharField(max_length=150, verbose_name="Username")
    password = models.CharField(max_length=255, verbose_name="Password (hashed)")
    first_name = models.CharField(max_length=150, blank=True, verbose_name="Họ")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="Tên")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Số điện thoại")
    
    class Meta:
        verbose_name = "Xác thực Email"
        verbose_name_plural = "Xác thực Email"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} - {self.otp_code}"
    
    @staticmethod
    def generate_otp():
        """Tạo mã OTP 6 số"""
        return ''.join(random.choices(string.digits, k=6))
    
    def is_expired(self):
        """Kiểm tra mã OTP đã hết hạn chưa"""
        return timezone.now() > self.expires_at
    
    def can_retry(self):
        """Kiểm tra còn được thử lại không (tối đa 5 lần)"""
        return self.attempts < 5
    
    @classmethod
    def create_verification(cls, email, username, password, first_name='', last_name='', phone=''):
        """
        Tạo mã xác thực mới
        Xóa các mã cũ chưa xác thực của email này
        """
        # Xóa các mã cũ chưa xác thực
        cls.objects.filter(email=email, is_verified=False).delete()
        
        # Tạo mã mới
        otp_code = cls.generate_otp()
        expires_at = timezone.now() + timedelta(minutes=10)  # Hết hạn sau 10 phút
        
        return cls.objects.create(
            email=email,
            otp_code=otp_code,
            expires_at=expires_at,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone=phone
        )


class PasswordReset(models.Model):
    """
    Model lưu mã OTP để reset password
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User")
    email = models.EmailField(verbose_name="Email")
    otp_code = models.CharField(max_length=6, verbose_name="Mã OTP")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian tạo")
    expires_at = models.DateTimeField(verbose_name="Thời gian hết hạn")
    is_used = models.BooleanField(default=False, verbose_name="Đã sử dụng")
    attempts = models.IntegerField(default=0, verbose_name="Số lần thử")
    
    class Meta:
        verbose_name = "Reset Password"
        verbose_name_plural = "Reset Password"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.otp_code}"
    
    @staticmethod
    def generate_otp():
        """Tạo mã OTP 6 số"""
        return ''.join(random.choices(string.digits, k=6))
    
    def is_expired(self):
        """Kiểm tra mã OTP đã hết hạn chưa"""
        return timezone.now() > self.expires_at
    
    def can_retry(self):
        """Kiểm tra còn được thử lại không (tối đa 5 lần)"""
        return self.attempts < 5
    
    @classmethod
    def create_reset(cls, user):
        """
        Tạo mã reset password mới
        Xóa các mã cũ chưa sử dụng của user này
        """
        # Xóa các mã cũ chưa sử dụng
        cls.objects.filter(user=user, is_used=False).delete()
        
        # Tạo mã mới
        otp_code = cls.generate_otp()
        expires_at = timezone.now() + timedelta(minutes=10)  # Hết hạn sau 10 phút
        
        return cls.objects.create(
            user=user,
            email=user.email,
            otp_code=otp_code,
            expires_at=expires_at
        )
