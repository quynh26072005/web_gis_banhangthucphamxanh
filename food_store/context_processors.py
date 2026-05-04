"""
Context processors for Clean Food Store
"""
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from .models import Product, Order, Customer, Farm, Cart


def dashboard_stats(request):
    """Add dashboard statistics to context"""
    if not request.path.startswith('/admin/'):
        return {}
    
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # Basic counts
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    total_customers = Customer.objects.count()
    total_farms = Farm.objects.count()
    
    # Revenue stats
    revenue_today = Order.objects.filter(
        created_at__date=today,
        status__in=['confirmed', 'preparing', 'shipping', 'delivered']
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    revenue_this_week = Order.objects.filter(
        created_at__date__gte=week_ago,
        status__in=['confirmed', 'preparing', 'shipping', 'delivered']
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Low stock count
    low_stock_count = Product.objects.filter(stock_quantity__lt=10, is_available=True).count()
    
    # Active carts
    active_carts = Cart.objects.filter(items__isnull=False).distinct().count()
    
    # Recent orders
    recent_orders = Order.objects.select_related('customer__user', 'delivery_zone').order_by('-created_at')[:10]
    
    # Low stock products
    low_stock_products = Product.objects.filter(stock_quantity__lt=10, is_available=True).order_by('stock_quantity')[:10]
    
    # Top products
    top_products = Product.objects.annotate(
        total_sold=Sum('orderitem__quantity')
    ).filter(total_sold__isnull=False).order_by('-total_sold')[:10]
    
    return {
        'stats': {
            'total_products': total_products,
            'total_orders': total_orders,
            'total_customers': total_customers,
            'total_farms': total_farms,
            'revenue_today': revenue_today,
            'revenue_this_week': revenue_this_week,
            'low_stock_count': low_stock_count,
            'active_carts': active_carts,
        },
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'top_products': top_products,
    }