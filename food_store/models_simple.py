"""
Simple models without GIS for testing
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
    
    # Temporary: Store coordinates as text instead of GIS field
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
    # Remove image field for now
    
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


class Customer(models.Model):
    """Customer profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name="Số điện thoại")
    address = models.TextField(verbose_name="Địa chỉ")
    
    # Temporary: Store coordinates as text instead of GIS field
    latitude = models.FloatField(null=True, blank=True, verbose_name="Vĩ độ")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Kinh độ")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Khách hàng"
        verbose_name_plural = "Khách hàng"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.phone}"