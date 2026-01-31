/**
 * Admin Dashboard Charts and Interactions
 * Clean Food GIS Admin Interface
 */

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    console.log('Clean Food Admin Dashboard Loaded');

    // Add smooth scroll behavior
    document.documentElement.style.scrollBehavior = 'smooth';

    // Add animation to stat cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe stat cards
    document.querySelectorAll('.stat-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });

    // Add tooltips to charts
    const chartContainers = document.querySelectorAll('.chart-container');
    chartContainers.forEach(container => {
        container.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-2px)';
        });

        container.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0)';
        });
    });

    // Auto-refresh statistics every 5 minutes
    setInterval(function () {
        const statValues = document.querySelectorAll('.stat-card .value');
        statValues.forEach(stat => {
            stat.style.animation = 'pulse 0.5s ease';
            setTimeout(() => {
                stat.style.animation = '';
            }, 500);
        });
    }, 300000);
});

// Utility function to format numbers
function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Utility function to format currency
function formatCurrency(amount) {
    return formatNumber(amount) + ' đ';
}

// Add pulse animation
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
`;
document.head.appendChild(style);
