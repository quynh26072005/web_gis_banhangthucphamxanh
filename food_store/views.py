"""
Views for Clean Food Store
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

from .models import Product, Category, Farm, Customer, Cart, CartItem, Order, OrderItem, DeliveryZone, StockTransaction
from gis_tools.gis_functions import MapGenerator


def home_view(request):
    """Homepage view"""
    featured_products = Product.objects.filter(is_available=True)[:8]
    categories = Category.objects.all()[:6]
    stores = Farm.objects.all()[:6]
    
    context = {
        'title': 'Trang chủ - Thực phẩm Sạch',
        'featured_products': featured_products,
        'categories': categories,
        'stores': stores,
    }
    return render(request, 'pages/home/home.html', context)


def product_list_view(request):
    """Product list view - Fixed version"""
    print(f"=== PRODUCT LIST VIEW FIXED ===")
    print(f"Request path: {request.path}")
    print(f"Request GET: {dict(request.GET)}")
    
    products = Product.objects.filter(is_available=True)
    print(f"Initial products: {products.count()}")
    
    category_param = request.GET.get('category', '').strip()
    store_param = request.GET.get('store', '').strip()
    search_param = request.GET.get('search', '').strip()
    sort_param = request.GET.get('sort', 'name').strip()
    
    print(f"Parameters: category='{category_param}', store='{store_param}', search='{search_param}'")
    
    current_category = None
    if category_param:
        try:
            current_category = int(category_param)
            products = products.filter(category_id=current_category)
            print(f"Applied category filter {current_category}: {products.count()} products")
        except (ValueError, TypeError):
            print(f"Invalid category: {category_param}")
    
    current_store = None
    if store_param:
        try:
            current_store = int(store_param)
            products = products.filter(farm_id=current_store)
            print(f"Applied store filter {current_store}: {products.count()} products")
        except (ValueError, TypeError):
            print(f"Invalid store: {store_param}")
    
    current_search = None
    if search_param:
        current_search = search_param
        products = products.filter(
            Q(name__icontains=search_param) |
            Q(description__icontains=search_param)
        )
        print(f"Applied search filter '{search_param}': {products.count()} products")
    
    if sort_param == 'price_low':
        products = products.order_by('price')
    elif sort_param == 'price_high':
        products = products.order_by('-price')
    elif sort_param == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')
    
    print(f"Final products count: {products.count()}")
    
    for i, product in enumerate(products[:3]):
        print(f"  {i+1}. {product.name} - {product.category.name} - {product.farm.name}")
    
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': 'Sản phẩm',
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'stores': Farm.objects.all(),
        'current_category': current_category,
        'current_store': current_store,
        'search_query': current_search,
        'sort_by': sort_param,
    }
    
    print(f"Context: category={current_category}, store={current_store}, products={page_obj.paginator.count}")
    
    return render(request, 'pages/products/product_list.html', context)


def simple_filter_view(request):
    """Simple filter view - DEPRECATED, use product_list_view instead"""
    from django.shortcuts import redirect
    return redirect('food_store:product_list')


def product_detail_view(request, pk):
    """Product detail view"""
    product = get_object_or_404(Product, pk=pk, is_available=True)
    
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(pk=product.pk)[:4]
    
    context = {
        'title': product.name,
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'pages/products/product_detail.html', context)


def category_list_view(request):
    """Category list view"""
    categories = Category.objects.all()
    
    context = {
        'title': 'Danh mục sản phẩm',
        'categories': categories,
    }
    return render(request, 'pages/products/category_list.html', context)


def farm_list_view(request):
    """Store list view"""
    farms = Farm.objects.all()
    
    organic_only = request.GET.get('organic')
    if organic_only:
        farms = farms.filter(organic_certified=True)
    
    search_query = request.GET.get('search')
    if search_query:
        farms = farms.filter(
            Q(name__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(farms.order_by('name'), 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': 'Cửa hàng',
        'page_obj': page_obj,
        'organic_only': organic_only,
        'search_query': search_query,
    }
    return render(request, 'pages/stores/farm_list.html', context)


def farm_detail_view(request, pk):
    """Store detail view"""
    farm = get_object_or_404(Farm, pk=pk)
    
    products = farm.product_set.filter(is_available=True)
    
    farm_map = MapGenerator.create_single_farm_map(farm)
    
    context = {
        'title': farm.name,
        'farm': farm,
        'products': products,
        'map_html': farm_map._repr_html_() if farm_map else None,
    }
    return render(request, 'pages/stores/farm_detail.html', context)


def register_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(
                user=user,
                phone='',
                address=''
            )
            login(request, user)
            messages.success(request, 'Đăng ký thành công!')
            return redirect('food_store:home')
    else:
        form = UserCreationForm()
    
    context = {
        'title': 'Đăng ký',
        'form': form,
    }
    return render(request, 'auth/register.html', context)


@login_required
def profile_view(request):
    """User profile view"""
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(
            user=request.user,
            phone='',
            address=''
        )
    
    # Check if user is store admin
    try:
        store_admin = request.user.storeadmin
        is_store_admin = True
    except:
        store_admin = None
        is_store_admin = False
    
    # Check if user is shipper
    try:
        shipper = request.user.shipper
        is_shipper = True
    except:
        shipper = None
        is_shipper = False
    
    context = {
        'title': 'Trang cá nhân',
        'customer': customer,
        'is_store_admin': is_store_admin,
        'store_admin': store_admin,
        'is_shipper': is_shipper,
        'shipper': shipper,
    }
    return render(request, 'pages/static_pages/profile.html', context)


@login_required
def order_history_view(request):
    """Order history view - temporarily empty"""
    context = {
        'title': 'Lịch sử đơn hàng',
        'page_obj': None,
    }
    return render(request, 'pages/orders/order_history.html', context)


@login_required
def order_detail_view(request, pk):
    """Order detail view - temporarily empty"""
    context = {
        'title': f'Đơn hàng #{pk}',
        'order': None,
    }
    return render(request, 'pages/orders/order_detail.html', context)


def about_view(request):
    """About page view"""
    context = {
        'title': 'Giới thiệu',
    }
    return render(request, 'pages/static_pages/about.html', context)


def contact_view(request):
    """Contact page view"""
    context = {
        'title': 'Liên hệ',
    }
    return render(request, 'pages/static_pages/contact.html', context)


# Cart Views
def get_or_create_cart(user):
    """Get or create cart for user"""
    try:
        customer = user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(
            user=user,
            phone='',
            address=''
        )
    
    cart, created = Cart.objects.get_or_create(customer=customer)
    return cart


@login_required
def cart_view(request):
    """Shopping cart view"""
    cart = get_or_create_cart(request.user)
    
    context = {
        'title': 'Giỏ hàng',
        'cart': cart,
    }
    return render(request, 'pages/orders/cart.html', context)


@login_required
def add_to_cart_api(request):
    """API to add product to cart"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
            
            product = get_object_or_404(Product, pk=product_id, is_available=True)
            cart = get_or_create_cart(request.user)
            
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Đã thêm {product.name} vào giỏ hàng',
                'cart_total_items': cart.total_items,
                'cart_total_amount': float(cart.total_amount)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


@login_required
def update_cart_item_api(request):
    """API to update cart item quantity"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            item_id = data.get('item_id')
            quantity = int(data.get('quantity', 1))
            
            cart = get_or_create_cart(request.user)
            cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
            
            if quantity <= 0:
                cart_item.delete()
                message = f'Đã xóa {cart_item.product.name} khỏi giỏ hàng'
            else:
                cart_item.quantity = quantity
                cart_item.save()
                message = f'Đã cập nhật số lượng {cart_item.product.name}'
            
            return JsonResponse({
                'success': True,
                'message': message,
                'cart_total_items': cart.total_items,
                'cart_total_amount': float(cart.total_amount)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


@login_required
def remove_from_cart_api(request):
    """API to remove product from cart"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            item_id = data.get('item_id')
            
            cart = get_or_create_cart(request.user)
            cart_item = get_object_or_404(CartItem, pk=item_id, cart=cart)
            product_name = cart_item.product.name
            cart_item.delete()
            
            return JsonResponse({
                'success': True,
                'message': f'Đã xóa {product_name} khỏi giỏ hàng',
                'cart_total_items': cart.total_items,
                'cart_total_amount': float(cart.total_amount)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


# Checkout Views
@login_required
def checkout_view(request):
    """Trang checkout với bản đồ đơn giản (không cần API key)"""
    cart = get_or_create_cart(request.user)
    
    if not cart.items.exists():
        messages.warning(request, 'Giỏ hàng của bạn đang trống!')
        return redirect('food_store:cart')
    
    context = {
        'title': 'Thanh toán',
        'cart': cart,
        'user': request.user,
    }
    
    # Sử dụng template đơn giản với Leaflet + CartoDB tiles
    return render(request, 'pages/orders/checkout_simple.html', context)


@login_required
def create_order_api(request):
    """API tạo đơn hàng"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            
            # Get delivery location
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            delivery_address = data.get('delivery_address', '')
            notes = data.get('notes', '')
            payment_method = data.get('payment_method', 'cod')  # ✅ THÊM payment_method
            
            # Validate coordinates
            if not latitude or not longitude:
                return JsonResponse({
                    'success': False,
                    'error': 'Vui lòng nhấn "Lấy vị trí hiện tại" hoặc "Tìm từ địa chỉ" để xác định tọa độ giao hàng'
                }, status=400)
            
            try:
                latitude = float(latitude)
                longitude = float(longitude)
            except (ValueError, TypeError):
                return JsonResponse({
                    'success': False,
                    'error': 'Tọa độ không hợp lệ. Vui lòng thử lại'
                }, status=400)

            
            # Get cart
            cart = get_or_create_cart(request.user)
            
            if not cart.items.exists():
                return JsonResponse({
                    'success': False,
                    'error': 'Giỏ hàng trống'
                }, status=400)
            
            # Find or create default delivery zone
            delivery_zone, created = DeliveryZone.objects.get_or_create(
                name="TP. Hồ Chí Minh",
                defaults={
                    'area_description': 'Khu vực TP. Hồ Chí Minh',
                    'delivery_fee': 30000,  # Default, will be overridden
                    'delivery_time': '1-2 ngày',
                    'is_active': True
                }
            )
            
            # Create order first (without farm assignment)
            order = Order.objects.create(
                customer=cart.customer,
                delivery_address=delivery_address,
                delivery_latitude=latitude,
                delivery_longitude=longitude,
                delivery_zone=delivery_zone,
                delivery_fee=0,  # Will be set after routing
                total_amount=cart.total_amount,  # Will be updated
                notes=notes,
                payment_method=payment_method  # ✅ LƯU payment_method
            )
            
            # Auto-assign farm và tính phí ship dựa trên đường đi thực tế
            route_info = order.auto_assign_nearest_farm()
            
            if route_info:
                # Cập nhật phí ship và routing info
                from decimal import Decimal
                order.delivery_fee = Decimal(str(route_info['shipping_fee']))
                order.delivery_distance_km = route_info['distance_km']
                order.delivery_duration_min = route_info['duration_min']
                order.total_amount = cart.total_amount + Decimal(str(route_info['shipping_fee']))
                order.save()
                
                shipping_info = {
                    'distance_km': round(route_info['distance_km'], 2),
                    'duration_min': round(route_info['duration_min'], 0),
                    'fee_breakdown': {
                        'base_fee': 15000,
                        'distance_fee': route_info['shipping_fee'] - 15000,
                        'total': route_info['shipping_fee']
                    }
                }
            else:
                # Fallback: không tìm được farm, dùng phí cố định
                order.delivery_fee = 30000
                order.total_amount = cart.total_amount + 30000
                order.save()
                
                shipping_info = {
                    'distance_km': None,
                    'duration_min': None,
                    'fee_breakdown': {
                        'base_fee': 30000,
                        'distance_fee': 0,
                        'total': 30000
                    }
                }
            
            # Create order items and update stock
            for cart_item in cart.items.all():
                product = cart_item.product
                quantity = cart_item.quantity
                
                # ✅ KIỂM TRA TỒN KHO trước khi tạo order
                if product.stock_quantity < quantity:
                    # Xóa order vừa tạo nếu không đủ hàng
                    order.delete()
                    return JsonResponse({
                        'success': False,
                        'error': f'Sản phẩm "{product.name}" không đủ hàng! Còn {product.stock_quantity} {product.unit}, bạn đặt {quantity} {product.unit}'
                    }, status=400)
                
                # Tạo order item
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price
                )
                
                # ✅ TRỪ TỒN KHO và TẠO STOCK TRANSACTION
                try:
                    StockTransaction.objects.create(
                        product=product,
                        farm=order.assigned_farm if order.assigned_farm else product.farm,
                        transaction_type='export',
                        quantity=quantity,
                        unit_price=product.price,
                        order=order,
                        notes=f'Xuất kho cho đơn hàng #{order.id}',
                        created_by=None  # System auto
                    )
                    # Model StockTransaction.save() sẽ TỰ ĐỘNG trừ tồn kho
                except Exception as e:
                    # Nếu lỗi, xóa order và rollback
                    order.delete()
                    return JsonResponse({
                        'success': False,
                        'error': f'Lỗi cập nhật kho: {str(e)}'
                    }, status=400)
            
            # Clear cart
            cart.items.all().delete()
            
            return JsonResponse({
                'success': True,
                'order_id': order.id,
                'message': 'Đặt hàng thành công!',
                'total_amount': float(order.total_amount),
                'payment_method': order.payment_method,  # ✅ TRẢ VỀ payment_method
                'shipping_info': shipping_info  # Include detailed shipping info
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


@login_required
def order_success_view(request, order_id):
    """Trang thành công sau khi đặt hàng"""
    order = get_object_or_404(Order, pk=order_id, customer__user=request.user)
    
    # Calculate subtotal
    subtotal = order.total_amount - order.delivery_fee
    
    # Calculate fee breakdown for display
    fee_breakdown = ''
    if order.delivery_distance_km:
        distance = float(order.delivery_distance_km)
        if distance <= 3:
            fee_breakdown = '15,000 VNĐ (phí cơ bản)'
        elif distance <= 10:
            extra_km = distance - 3
            fee_breakdown = f'15,000 VNĐ + {extra_km:.1f} km × 3,000 VNĐ/km'
        elif distance <= 20:
            extra_km = distance - 10
            fee_breakdown = f'36,000 VNĐ + {extra_km:.1f} km × 2,500 VNĐ/km'
        else:
            extra_km = distance - 20
            fee_breakdown = f'61,000 VNĐ + {extra_km:.1f} km × 2,000 VNĐ/km'
    
    context = {
        'title': 'Đặt hàng thành công',
        'order': order,
        'subtotal': subtotal,
        'fee_breakdown': fee_breakdown,
    }
    return render(request, 'pages/orders/order_success.html', context)


@login_required
def order_history_view(request):
    """Lịch sử đơn hàng"""
    try:
        customer = request.user.customer
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        
        # Phân trang
        paginator = Paginator(orders, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'title': 'Lịch sử đơn hàng',
            'page_obj': page_obj,
        }
        return render(request, 'pages/orders/order_history.html', context)
        
    except Customer.DoesNotExist:
        context = {
            'title': 'Lịch sử đơn hàng',
            'page_obj': None,
        }
        return render(request, 'pages/orders/order_history.html', context)


@login_required
def order_detail_view(request, pk):
    """Chi tiết đơn hàng"""
    try:
        customer = request.user.customer
        order = get_object_or_404(Order, pk=pk, customer=customer)
        
        # Tạo bản đồ theo dõi
        tracking_map = MapGenerator.create_order_tracking_map(order.id)
        
        context = {
            'title': f'Đơn hàng #{order.pk}',
            'order': order,
            'map_html': tracking_map._repr_html_() if tracking_map else None,
        }
        return render(request, 'pages/orders/order_detail.html', context)
        
    except Customer.DoesNotExist:
        messages.error(request, 'Không tìm thấy thông tin khách hàng')
        return redirect('food_store:home')


@login_required
def get_stores_api(request):
    """API to get all stores with coordinates"""
    from django.http import JsonResponse
    
    stores = Farm.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).values('id', 'name', 'address', 'latitude', 'longitude')
    
    return JsonResponse({
        'success': True,
        'stores': list(stores)
    })


@login_required
def cart_count_api(request):
    """API to get cart item count"""
    try:
        cart = get_or_create_cart(request.user)
        return JsonResponse({
            'success': True,
            'cart_total_items': cart.total_items,
            'cart_total_amount': float(cart.total_amount)
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'cart_total_items': 0
        })
