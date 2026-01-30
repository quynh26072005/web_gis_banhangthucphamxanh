/**
 * Clean Food GIS - Main JavaScript
 * Interactive features and AJAX functionality
 */

// ==================== Global Variables ====================
const API_BASE_URL = '/gis-tools/api';

// ==================== Utility Functions ====================

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed top-0 end-0 m-3`;
    toast.style.zIndex = '9999';
    toast.style.minWidth = '300px';
    toast.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fas fa-${getIconForType(type)} me-2"></i>
            <span>${message}</span>
        </div>
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.classList.add('fade-in');
    }, 10);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function getIconForType(type) {
    const icons = {
        'success': 'check-circle',
        'danger': 'exclamation-circle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

/**
 * Format currency (Vietnamese Dong)
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(amount);
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ==================== Cart Functions ====================

/**
 * Add product to cart
 */
async function addToCart(productId, quantity = 1) {
    try {
        const response = await fetch('/api/cart/add/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: quantity
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Đã thêm sản phẩm vào giỏ hàng!', 'success');
            updateCartCount(data.cart_items_count);
            
            // Add animation to cart icon
            animateCartIcon();
        } else {
            showToast(data.message || 'Có lỗi xảy ra', 'danger');
        }
    } catch (error) {
        console.error('Error adding to cart:', error);
        showToast('Không thể thêm vào giỏ hàng', 'danger');
    }
}

/**
 * Update cart item quantity
 */
async function updateCartItem(itemId, quantity) {
    try {
        const response = await fetch('/api/cart/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                item_id: itemId,
                quantity: quantity
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            updateCartDisplay(data);
            showToast('Đã cập nhật giỏ hàng', 'success');
        } else {
            showToast(data.message || 'Có lỗi xảy ra', 'danger');
        }
    } catch (error) {
        console.error('Error updating cart:', error);
        showToast('Không thể cập nhật giỏ hàng', 'danger');
    }
}

/**
 * Remove item from cart
 */
async function removeFromCart(itemId) {
    if (!confirm('Bạn có chắc muốn xóa sản phẩm này khỏi giỏ hàng?')) {
        return;
    }
    
    try {
        const response = await fetch('/api/cart/remove/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                item_id: itemId
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Remove item from DOM
            const itemElement = document.getElementById(`cart-item-${itemId}`);
            if (itemElement) {
                itemElement.style.opacity = '0';
                setTimeout(() => itemElement.remove(), 300);
            }
            
            updateCartDisplay(data);
            showToast('Đã xóa sản phẩm khỏi giỏ hàng', 'success');
        } else {
            showToast(data.message || 'Có lỗi xảy ra', 'danger');
        }
    } catch (error) {
        console.error('Error removing from cart:', error);
        showToast('Không thể xóa khỏi giỏ hàng', 'danger');
    }
}

/**
 * Update cart count badge
 */
function updateCartCount(count) {
    const badge = document.getElementById('cart-count');
    if (badge) {
        badge.textContent = count;
        badge.classList.add('pulse');
        setTimeout(() => badge.classList.remove('pulse'), 500);
    }
}

/**
 * Update cart display
 */
function updateCartDisplay(data) {
    // Update total
    const totalElement = document.getElementById('cart-total');
    if (totalElement && data.cart_total !== undefined) {
        totalElement.textContent = formatCurrency(data.cart_total);
    }
    
    // Update count
    if (data.cart_items_count !== undefined) {
        updateCartCount(data.cart_items_count);
    }
}

/**
 * Animate cart icon
 */
function animateCartIcon() {
    const cartIcon = document.querySelector('.cart-icon');
    if (cartIcon) {
        cartIcon.classList.add('pulse');
        setTimeout(() => cartIcon.classList.remove('pulse'), 500);
    }
}

// ==================== GIS Functions ====================

/**
 * Find nearest farms
 */
async function findNearestFarms(latitude, longitude, maxDistance = 50) {
    try {
        const response = await fetch(`${API_BASE_URL}/find-nearest-farms/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                latitude: latitude,
                longitude: longitude,
                max_distance: maxDistance
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            return data.farms;
        } else {
            throw new Error(data.error || 'Failed to find farms');
        }
    } catch (error) {
        console.error('Error finding farms:', error);
        showToast('Không thể tìm trang trại gần nhất', 'danger');
        return [];
    }
}

/**
 * Check delivery availability
 */
async function checkDeliveryAvailability(latitude, longitude) {
    try {
        const response = await fetch(`${API_BASE_URL}/check-delivery/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                latitude: latitude,
                longitude: longitude
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            return data.delivery_info;
        } else {
            throw new Error(data.error || 'Failed to check delivery');
        }
    } catch (error) {
        console.error('Error checking delivery:', error);
        showToast('Không thể kiểm tra khả năng giao hàng', 'danger');
        return null;
    }
}

/**
 * Geocode address
 */
async function geocodeAddress(address) {
    try {
        const response = await fetch(`${API_BASE_URL}/geocode/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                address: address
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            return data.coordinates;
        } else {
            throw new Error(data.error || 'Failed to geocode');
        }
    } catch (error) {
        console.error('Error geocoding:', error);
        showToast('Không thể chuyển đổi địa chỉ', 'danger');
        return null;
    }
}

// ==================== Helper Functions ====================

/**
 * Get CSRF token from cookies
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/**
 * Smooth scroll to element
 */
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

/**
 * Initialize tooltips (Bootstrap)
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ==================== DOM Ready ====================
document.addEventListener('DOMContentLoaded', function() {
    console.log('Clean Food GIS initialized');
    
    // Initialize tooltips
    if (typeof bootstrap !== 'undefined') {
        initializeTooltips();
    }
    
    // Add fade-in animation to elements
    const animatedElements = document.querySelectorAll('.fade-in-up');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, { threshold: 0.1 });
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease-out';
        observer.observe(el);
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                scrollToElement(href.substring(1));
            }
        });
    });
});

// ==================== Export Functions ====================
window.CleanFoodGIS = {
    addToCart,
    updateCartItem,
    removeFromCart,
    findNearestFarms,
    checkDeliveryAvailability,
    geocodeAddress,
    showToast,
    formatCurrency
};
