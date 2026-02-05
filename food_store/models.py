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
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=20, default="kg")
    
    image = models.ImageField(upload_to='products/')
    
    stock_quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    
    nutritional_info = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
    
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
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.phone}"


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
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('shipping', 'Shipping'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    delivery_address = models.TextField()
    delivery_latitude = models.FloatField(null=True, blank=True)
    delivery_longitude = models.FloatField(null=True, blank=True)
    delivery_zone = models.ForeignKey(DeliveryZone, on_delete=models.SET_NULL, null=True)
    
    assigned_farm = models.ForeignKey(
        Farm, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assigned_orders'
    )
    
    delivery_distance_km = models.FloatField(null=True, blank=True)
    delivery_duration_min = models.FloatField(null=True, blank=True)
    
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
    
    notes = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
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