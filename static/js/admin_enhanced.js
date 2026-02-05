// Enhanced Admin Interface JavaScript for Clean Food GIS

document.addEventListener('DOMContentLoaded', function() {
    
    // ===== ERROR HANDLING AND CLICK SAFETY =====
    function addClickSafety() {
        // Add error handling for all admin links
        const adminLinks = document.querySelectorAll('a[href*="/admin/"]');
        adminLinks.forEach(link => {
            link.addEventListener('click', function(e) {
                try {
                    // Check if link is valid
                    const href = this.getAttribute('href');
                    if (!href || href === '#' || href === 'javascript:void(0)') {
                        e.preventDefault();
                        console.warn('Invalid link detected:', this);
                        return false;
                    }
                    
                    // Add loading state
                    if (!this.target || this.target === '_self') {
                        this.style.opacity = '0.7';
                        this.style.pointerEvents = 'none';
                        
                        // Reset after 3 seconds as fallback
                        setTimeout(() => {
                            this.style.opacity = '1';
                            this.style.pointerEvents = 'auto';
                        }, 3000);
                    }
                } catch (error) {
                    console.error('Error handling link click:', error);
                    e.preventDefault();
                    return false;
                }
            });
        });
        
        // Handle form submissions safely
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                try {
                    const submitBtn = this.querySelector('input[type="submit"], button[type="submit"]');
                    if (submitBtn && !submitBtn.disabled) {
                        // Store original text
                        const originalText = submitBtn.value || submitBtn.textContent;
                        submitBtn.setAttribute('data-original-text', originalText);
                        
                        // Add loading state
                        submitBtn.disabled = true;
                        if (submitBtn.tagName === 'INPUT') {
                            submitBtn.value = 'Đang xử lý...';
                        } else {
                            submitBtn.innerHTML = '<span class="loading-spinner"></span> Đang xử lý...';
                        }
                        
                        // Re-enable after 10 seconds as fallback
                        setTimeout(() => {
                            submitBtn.disabled = false;
                            if (submitBtn.tagName === 'INPUT') {
                                submitBtn.value = originalText;
                            } else {
                                submitBtn.innerHTML = originalText;
                            }
                        }, 10000);
                    }
                } catch (error) {
                    console.error('Error handling form submission:', error);
                }
            });
        });
    }
    
    // ===== MOBILE MENU FUNCTIONALITY =====
    function initMobileMenu() {
        try {
            if (window.innerWidth <= 768) {
                // Create mobile menu toggle if it doesn't exist
                if (!document.querySelector('.mobile-menu-toggle')) {
                    const toggleBtn = document.createElement('button');
                    toggleBtn.className = 'mobile-menu-toggle';
                    toggleBtn.innerHTML = '☰';
                    toggleBtn.setAttribute('aria-label', 'Toggle navigation menu');
                    toggleBtn.setAttribute('type', 'button');
                    
                    document.body.appendChild(toggleBtn);
                    
                    toggleBtn.addEventListener('click', function(e) {
                        e.preventDefault();
                        try {
                            const sidebar = document.getElementById('nav-sidebar');
                            if (sidebar) {
                                sidebar.classList.toggle('show');
                                this.innerHTML = sidebar.classList.contains('show') ? '✕' : '☰';
                                this.setAttribute('aria-expanded', sidebar.classList.contains('show'));
                            }
                        } catch (error) {
                            console.error('Error toggling mobile menu:', error);
                        }
                    });
                }
                
                // Close sidebar when clicking outside
                document.addEventListener('click', function(e) {
                    try {
                        const sidebar = document.getElementById('nav-sidebar');
                        const toggleBtn = document.querySelector('.mobile-menu-toggle');
                        
                        if (sidebar && sidebar.classList.contains('show') && 
                            !sidebar.contains(e.target) && e.target !== toggleBtn) {
                            sidebar.classList.remove('show');
                            if (toggleBtn) {
                                toggleBtn.innerHTML = '☰';
                                toggleBtn.setAttribute('aria-expanded', 'false');
                            }
                        }
                    } catch (error) {
                        console.error('Error handling outside click:', error);
                    }
                });
            }
        } catch (error) {
            console.error('Error initializing mobile menu:', error);
        }
    }
    
    // ===== SIDEBAR ENHANCEMENTS =====
    function enhanceSidebar() {
        try {
            const sidebar = document.getElementById('nav-sidebar');
            if (!sidebar) return;
            
            // Add icons to navigation links
            const navLinks = sidebar.querySelectorAll('.module li a');
            navLinks.forEach(link => {
                try {
                    const href = link.getAttribute('href') || '';
                    const text = link.textContent.trim();
                    
                    // Create icon span if it doesn't exist
                    if (!link.querySelector('.icon')) {
                        const iconSpan = document.createElement('span');
                        iconSpan.className = 'icon';
                        
                        // Add appropriate icon based on URL or text
                        if (href.includes('product') || text.includes('Product') || text.includes('Sản phẩm')) {
                            iconSpan.innerHTML = '🍎';
                        } else if (href.includes('order') || text.includes('Order') || text.includes('Đơn hàng')) {
                            iconSpan.innerHTML = '📋';
                        } else if (href.includes('customer') || text.includes('Customer') || text.includes('Khách hàng')) {
                            iconSpan.innerHTML = '👥';
                        } else if (href.includes('farm') || text.includes('Farm') || text.includes('Trang trại')) {
                            iconSpan.innerHTML = '🏡';
                        } else if (href.includes('category') || text.includes('Category') || text.includes('Danh mục')) {
                            iconSpan.innerHTML = '📂';
                        } else if (href.includes('delivery') || text.includes('Delivery') || text.includes('Giao hàng')) {
                            iconSpan.innerHTML = '🚚';
                        } else if (href.includes('user') || text.includes('User') || text.includes('Người dùng')) {
                            iconSpan.innerHTML = '👤';
                        } else if (href.includes('group') || text.includes('Group') || text.includes('Nhóm')) {
                            iconSpan.innerHTML = '👥';
                        } else {
                            iconSpan.innerHTML = '📄';
                        }
                        
                        link.insertBefore(iconSpan, link.firstChild);
                    }
                } catch (error) {
                    console.error('Error adding icon to link:', error);
                }
            });
            
            // Add smooth scrolling to sidebar
            sidebar.style.scrollBehavior = 'smooth';
        } catch (error) {
            console.error('Error enhancing sidebar:', error);
        }
    }
    
    // ===== FORM ENHANCEMENTS =====
    function enhanceForms() {
        try {
            // Add floating labels effect
            const inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"], input[type="number"], textarea');
            inputs.forEach(input => {
                try {
                    if (input.value) {
                        input.classList.add('has-value');
                    }
                    
                    input.addEventListener('focus', function() {
                        this.classList.add('focused');
                    });
                    
                    input.addEventListener('blur', function() {
                        this.classList.remove('focused');
                        if (this.value) {
                            this.classList.add('has-value');
                        } else {
                            this.classList.remove('has-value');
                        }
                    });
                } catch (error) {
                    console.error('Error enhancing input:', error);
                }
            });
            
            // Enhance file inputs
            const fileInputs = document.querySelectorAll('input[type="file"]');
            fileInputs.forEach(input => {
                try {
                    if (input.closest('.file-input-wrapper')) return; // Already enhanced
                    
                    const wrapper = document.createElement('div');
                    wrapper.className = 'file-input-wrapper';
                    wrapper.innerHTML = `
                        <button type="button" class="file-input-btn">
                            <span class="icon">📁</span>
                            <span class="text">Chọn file</span>
                        </button>
                        <span class="file-name">Chưa chọn file nào</span>
                    `;
                    
                    input.parentNode.insertBefore(wrapper, input);
                    wrapper.appendChild(input);
                    
                    const btn = wrapper.querySelector('.file-input-btn');
                    const fileName = wrapper.querySelector('.file-name');
                    
                    btn.addEventListener('click', (e) => {
                        e.preventDefault();
                        input.click();
                    });
                    
                    input.addEventListener('change', function() {
                        if (this.files.length > 0) {
                            fileName.textContent = this.files[0].name;
                            wrapper.classList.add('has-file');
                        } else {
                            fileName.textContent = 'Chưa chọn file nào';
                            wrapper.classList.remove('has-file');
                        }
                    });
                    
                    input.style.display = 'none';
                } catch (error) {
                    console.error('Error enhancing file input:', error);
                }
            });
        } catch (error) {
            console.error('Error enhancing forms:', error);
        }
    }
    
    // ===== TABLE ENHANCEMENTS =====
    function enhanceTables() {
        try {
            const tables = document.querySelectorAll('.results table, #result_list');
            tables.forEach(table => {
                try {
                    // Add hover effects
                    const rows = table.querySelectorAll('tbody tr');
                    rows.forEach(row => {
                        row.addEventListener('mouseenter', function() {
                            this.style.transform = 'translateY(-1px)';
                            this.style.boxShadow = '0 2px 10px rgba(0,0,0,0.1)';
                        });
                        
                        row.addEventListener('mouseleave', function() {
                            this.style.transform = 'translateY(0)';
                            this.style.boxShadow = 'none';
                        });
                    });
                    
                    // Make table responsive
                    if (!table.closest('.table-responsive')) {
                        const wrapper = document.createElement('div');
                        wrapper.className = 'table-responsive';
                        table.parentNode.insertBefore(wrapper, table);
                        wrapper.appendChild(table);
                    }
                } catch (error) {
                    console.error('Error enhancing table:', error);
                }
            });
        } catch (error) {
            console.error('Error enhancing tables:', error);
        }
    }
    
    // ===== NOTIFICATIONS =====
    function enhanceNotifications() {
        try {
            const messages = document.querySelectorAll('.messages .success, .messages .error, .messages .info, .messages .warning');
            messages.forEach(message => {
                try {
                    // Add close button if it doesn't exist
                    if (!message.querySelector('.message-close')) {
                        const closeBtn = document.createElement('button');
                        closeBtn.innerHTML = '✕';
                        closeBtn.className = 'message-close';
                        closeBtn.setAttribute('type', 'button');
                        closeBtn.setAttribute('aria-label', 'Close message');
                        closeBtn.style.cssText = `
                            position: absolute;
                            top: 10px;
                            right: 15px;
                            background: none;
                            border: none;
                            color: inherit;
                            font-size: 1.2em;
                            cursor: pointer;
                            opacity: 0.7;
                        `;
                        
                        message.style.position = 'relative';
                        message.appendChild(closeBtn);
                        
                        closeBtn.addEventListener('click', function(e) {
                            e.preventDefault();
                            message.style.animation = 'slideOutRight 0.3s ease-out forwards';
                            setTimeout(() => {
                                if (message.parentNode) {
                                    message.remove();
                                }
                            }, 300);
                        });
                    }
                    
                    // Auto-hide after 5 seconds
                    setTimeout(() => {
                        if (message.parentNode) {
                            message.style.animation = 'fadeOut 0.5s ease-out forwards';
                            setTimeout(() => {
                                if (message.parentNode) {
                                    message.remove();
                                }
                            }, 500);
                        }
                    }, 5000);
                } catch (error) {
                    console.error('Error enhancing message:', error);
                }
            });
        } catch (error) {
            console.error('Error enhancing notifications:', error);
        }
    }
    
    // ===== SEARCH ENHANCEMENTS =====
    function enhanceSearch() {
        try {
            const searchInputs = document.querySelectorAll('input[name="q"], .search input');
            searchInputs.forEach(input => {
                try {
                    if (input.closest('.search-wrapper')) return; // Already enhanced
                    
                    // Add search icon
                    const wrapper = document.createElement('div');
                    wrapper.className = 'search-wrapper';
                    wrapper.style.cssText = 'position: relative; display: inline-block;';
                    
                    input.parentNode.insertBefore(wrapper, input);
                    wrapper.appendChild(input);
                    
                    const icon = document.createElement('span');
                    icon.innerHTML = '🔍';
                    icon.style.cssText = `
                        position: absolute;
                        right: 10px;
                        top: 50%;
                        transform: translateY(-50%);
                        pointer-events: none;
                        opacity: 0.5;
                    `;
                    wrapper.appendChild(icon);
                    
                    input.style.paddingRight = '35px';
                } catch (error) {
                    console.error('Error enhancing search input:', error);
                }
            });
        } catch (error) {
            console.error('Error enhancing search:', error);
        }
    }
    
    // ===== KEYBOARD SHORTCUTS =====
    function addKeyboardShortcuts() {
        try {
            document.addEventListener('keydown', function(e) {
                try {
                    // Ctrl/Cmd + K for search
                    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                        e.preventDefault();
                        const searchInput = document.querySelector('input[name="q"], .search input');
                        if (searchInput) {
                            searchInput.focus();
                        }
                    }
                    
                    // Ctrl/Cmd + S for save
                    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
                        const submitBtn = document.querySelector('input[type="submit"], button[type="submit"]');
                        if (submitBtn && !submitBtn.disabled) {
                            e.preventDefault();
                            submitBtn.click();
                        }
                    }
                    
                    // Escape to close mobile menu
                    if (e.key === 'Escape') {
                        const sidebar = document.getElementById('nav-sidebar');
                        const toggleBtn = document.querySelector('.mobile-menu-toggle');
                        if (sidebar && sidebar.classList.contains('show')) {
                            sidebar.classList.remove('show');
                            if (toggleBtn) {
                                toggleBtn.innerHTML = '☰';
                                toggleBtn.setAttribute('aria-expanded', 'false');
                            }
                        }
                    }
                } catch (error) {
                    console.error('Error handling keyboard shortcut:', error);
                }
            });
        } catch (error) {
            console.error('Error adding keyboard shortcuts:', error);
        }
    }
    
    // ===== INITIALIZE ALL ENHANCEMENTS =====
    function init() {
        try {
            addClickSafety();
            initMobileMenu();
            enhanceSidebar();
            enhanceForms();
            enhanceTables();
            enhanceNotifications();
            enhanceSearch();
            addKeyboardShortcuts();
            
            console.log('✅ Admin enhancements loaded successfully');
        } catch (error) {
            console.error('❌ Error loading admin enhancements:', error);
        }
    }
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    // Re-initialize on window resize
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            try {
                initMobileMenu();
            } catch (error) {
                console.error('Error on resize:', error);
            }
        }, 250);
    });
    
    // Handle page visibility changes
    document.addEventListener('visibilitychange', function() {
        if (document.visibilityState === 'visible') {
            // Re-enable any disabled buttons when page becomes visible again
            const disabledButtons = document.querySelectorAll('input[type="submit"]:disabled, button[type="submit"]:disabled');
            disabledButtons.forEach(btn => {
                const originalText = btn.getAttribute('data-original-text');
                if (originalText) {
                    btn.disabled = false;
                    if (btn.tagName === 'INPUT') {
                        btn.value = originalText;
                    } else {
                        btn.innerHTML = originalText;
                    }
                }
            });
        }
    });
});

// ===== GLOBAL ERROR HANDLER =====
window.addEventListener('error', function(e) {
    console.error('Global error caught:', e.error);
    // Don't let errors break the admin interface
    return true;
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
    // Don't let promise rejections break the admin interface
    e.preventDefault();
});

// ===== CSS ANIMATIONS =====
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        to { transform: translateX(100%); opacity: 0; }
    }
    
    @keyframes fadeOut {
        to { opacity: 0; }
    }
    
    .loading-spinner {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        border-top-color: white;
        animation: spin 1s ease-in-out infinite;
    }
    
    .file-input-wrapper {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 10px;
        border: 2px dashed #e9ecef;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    .file-input-wrapper:hover {
        border-color: #28a745;
        background: rgba(40, 167, 69, 0.05);
    }
    
    .file-input-wrapper.has-file {
        border-color: #28a745;
        background: rgba(40, 167, 69, 0.1);
    }
    
    .file-input-btn {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 15px;
        cursor: pointer;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.3s ease;
    }
    
    .file-input-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 2px 10px rgba(40, 167, 69, 0.3);
    }
    
    .file-name {
        color: #6c757d;
        font-style: italic;
    }
    
    .has-file .file-name {
        color: #28a745;
        font-weight: 600;
        font-style: normal;
    }
    
    .table-responsive {
        overflow-x: auto;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    }
    
    .search-wrapper input {
        transition: all 0.3s ease;
    }
    
    .search-wrapper input:focus {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(40, 167, 69, 0.2);
    }
    
    /* Mobile menu toggle styles */
    .mobile-menu-toggle {
        position: fixed !important;
        top: 20px !important;
        left: 20px !important;
        z-index: 1001 !important;
        background: #28a745 !important;
        color: white !important;
        border: none !important;
        border-radius: 50% !important;
        width: 50px !important;
        height: 50px !important;
        font-size: 1.2em !important;
        cursor: pointer !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2) !important;
        transition: all 0.3s ease !important;
        display: none !important;
    }
    
    .mobile-menu-toggle:hover {
        background: #20c997 !important;
        transform: scale(1.1) !important;
    }
    
    @media (max-width: 768px) {
        .mobile-menu-toggle {
            display: block !important;
        }
    }
`;
document.head.appendChild(style);