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

# Import ProductForm để không bị lỗi 'ProductForm' is not defined
from .forms import ProductForm
from .models import Product, Category, Farm, Customer, Cart, CartItem, Order, OrderItem, DeliveryZone
from gis_tools.gis_functions import MapGenerator


def home_view(request):
    """Trang chủ website"""
    # Lấy sản phẩm nổi bật
    featured_products = Product.objects.filter(is_available=True)[:8]
    
    # Lấy danh mục
    categories = Category.objects.all()[:6]
    
    # Lấy trang trại
    farms = Farm.objects.all()[:6]
    
    context = {
        'title': 'Trang chủ - Thực phẩm Sạch',
        'featured_products': featured_products,
        'categories': categories,
        'farms': farms,
    }
    return render(request, 'food_store/home.html', context)


def product_list_view(request):
    """Danh sách sản phẩm"""
    products = Product.objects.filter(is_available=True)
    
    # Lọc theo danh mục
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)
    
    # Lọc theo trang trại
    farm_id = request.GET.get('farm')
    if farm_id:
        products = products.filter(farm_id=farm_id)
    
    # Tìm kiếm
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Sắp xếp
    sort_by = request.GET.get('sort', 'name')
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')
    
    # Phân trang
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': 'Sản phẩm',
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'farms': Farm.objects.all(),
        'current_category': category_id,
        'current_farm': farm_id,
        'search_query': search_query,
        'sort_by': sort_by,
    }
    return render(request, 'food_store/product_list.html', context)


def product_detail_view(request, pk):
    """Chi tiết sản phẩm"""
    product = get_object_or_404(Product, pk=pk, is_available=True)
    
    # Sản phẩm liên quan (cùng danh mục)
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(pk=product.pk)[:4]
    
    context = {
        'title': product.name,
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'food_store/product_detail.html', context)


def category_list_view(request):
    """Danh sách danh mục"""
    categories = Category.objects.all()
    
    context = {
        'title': 'Danh mục sản phẩm',
        'categories': categories,
    }
    return render(request, 'food_store/category_list.html', context)


def farm_list_view(request):
    """Danh sách trang trại"""
    farms = Farm.objects.all()
    
    # Lọc theo chứng nhận hữu cơ
    organic_only = request.GET.get('organic')
    if organic_only:
        farms = farms.filter(organic_certified=True)
    
    # Tìm kiếm
    search_query = request.GET.get('search')
    if search_query:
        farms = farms.filter(
            Q(name__icontains=search_query) |
            Q(address__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Phân trang
    paginator = Paginator(farms, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': 'Trang trại',
        'page_obj': page_obj,
        'organic_only': organic_only,
        'search_query': search_query,
    }
    return render(request, 'food_store/farm_list.html', context)


def farm_detail_view(request, pk):
    """Chi tiết trang trại"""
    farm = get_object_or_404(Farm, pk=pk)
    
    # Sản phẩm của trang trại
    products = farm.product_set.filter(is_available=True)
    
    # Tạo bản đồ
    farm_map = MapGenerator.create_single_farm_map(farm)
    
    context = {
        'title': farm.name,
        'farm': farm,
        'products': products,
        'map_html': farm_map._repr_html_() if farm_map else None,
    }
    return render(request, 'food_store/farm_detail.html', context)


def register_view(request):
    """Đăng ký tài khoản"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Tạo profile khách hàng
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
    return render(request, 'registration/register.html', context)


@login_required
def profile_view(request):
    """Trang cá nhân"""
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        # Tạo profile nếu chưa có
        customer = Customer.objects.create(
            user=request.user,
            phone='',
            address=''
        )
    
    context = {
        'title': 'Trang cá nhân',
        'customer': customer,
    }
    return render(request, 'food_store/profile.html', context)


def about_view(request):
    """Trang giới thiệu"""
    context = {
        'title': 'Giới thiệu',
    }
    return render(request, 'food_store/about.html', context)


def contact_view(request):
    """Trang liên hệ"""
    context = {
        'title': 'Liên hệ',
    }
    return render(request, 'food_store/contact.html', context)


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
    """Hiển thị giỏ hàng"""
    cart = get_or_create_cart(request.user)
    
    context = {
        'title': 'Giỏ hàng',
        'cart': cart,
    }
    return render(request, 'food_store/cart.html', context)


@login_required
def add_to_cart_api(request):
    """API thêm sản phẩm vào giỏ hàng"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
            
            product = get_object_or_404(Product, pk=product_id, is_available=True)
            cart = get_or_create_cart(request.user)
            
            # Check if item already in cart
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
    """API cập nhật số lượng sản phẩm trong giỏ hàng"""
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
    """API xóa sản phẩm khỏi giỏ hàng"""
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
    """Trang checkout với bản đồ chọn địa chỉ"""
    cart = get_or_create_cart(request.user)
    
    if not cart.items.exists():
        messages.warning(request, 'Giỏ hàng của bạn đang trống!')
        return redirect('food_store:cart')
    
    context = {
        'title': 'Thanh toán',
        'cart': cart,
    }
    return render(request, 'food_store/checkout.html', context)


@login_required
def create_order_api(request):
    """API tạo đơn hàng"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            
            # Get delivery location
            latitude = float(data.get('latitude'))
            longitude = float(data.get('longitude'))
            delivery_address = data.get('delivery_address', '')
            notes = data.get('notes', '')
            
            # For now, assume delivery is available with fixed fee
            delivery_fee = 30000  # 30,000 VND
            
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
                    'delivery_fee': delivery_fee,
                    'delivery_time': '1-2 ngày',
                    'is_active': True
                }
            )
            
            # Create order
            order = Order.objects.create(
                customer=cart.customer,
                delivery_address=delivery_address,
                delivery_latitude=latitude,
                delivery_longitude=longitude,
                delivery_zone=delivery_zone,
                subtotal=cart.total_amount,
                delivery_fee=delivery_fee,
                total_amount=cart.total_amount + delivery_fee,
                notes=notes
            )
            
            # Create order items
            for cart_item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            
            # Clear cart
            cart.items.all().delete()
            
            return JsonResponse({
                'success': True,
                'order_id': order.id,
                'message': 'Đặt hàng thành công!',
                'total_amount': float(order.total_amount)
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
    
    context = {
        'title': 'Đặt hàng thành công',
        'order': order,
    }
    return render(request, 'food_store/order_success.html', context)


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
        return render(request, 'food_store/order_history.html', context)
        
    except Customer.DoesNotExist:
        context = {
            'title': 'Lịch sử đơn hàng',
            'page_obj': None,
        }
        return render(request, 'food_store/order_history.html', context)


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
        return render(request, 'food_store/order_detail.html', context)
        
    except Customer.DoesNotExist:
        messages.error(request, 'Không tìm thấy thông tin khách hàng')
        return redirect('food_store:home')

# --- QUẢN LÝ SẢN PHẨM ---

@login_required
def manage_products(request):
    """Trang liệt kê danh sách rau củ để quản lý"""
    products = Product.objects.all().order_by('-id')
    return render(request, 'food_store/manage_products.html', {
        'title': 'Quản lý kho rau sạch',
        'products': products
    })

@login_required
def add_product(request):
    """View thêm sản phẩm mới"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Đã thêm rau củ mới thành công!')
            return redirect('food_store:manage_products')
    else:
        form = ProductForm()
    
    return render(request, 'food_store/product_form.html', {
        'title': 'Thêm rau củ mới',
        'form': form,
        'edit_mode': False
    })

@login_required
def edit_product(request, pk):
    """View chỉnh sửa rau củ"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Cập nhật {product.name} thành công!')
            return redirect('food_store:manage_products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'food_store/product_form.html', {
        'title': f'Sửa: {product.name}',
        'form': form,
        'edit_mode': True
    })

@login_required
def delete_product_api(request, pk):
    """API xóa sản phẩm nhanh"""
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=pk)
        product_name = product.name
        product.delete()
        return JsonResponse({'success': True, 'message': f'Đã xóa {product_name}'})
    return JsonResponse({'success': False}, status=400)