/**
 * Delivery Route Map for Admin Interface
 * Hiển thị đường đi giao hàng thực tế từ trang trại đến khách hàng
 */

// Global map instances
window.deliveryMaps = {};

/**
 * Initialize delivery route map
 */
function initDeliveryRouteMap(orderId, routeData) {
    const mapId = `delivery-route-map-${orderId}`;
    const mapContainer = document.getElementById(mapId);
    
    if (!mapContainer) {
        console.error(`Map container ${mapId} not found`);
        return;
    }

    try {
        // Initialize Leaflet map
        const map = L.map(mapId, {
            zoomControl: true,
            scrollWheelZoom: true
        });

        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 18
        }).addTo(map);

        // Farm marker (green)
        const farmIcon = L.divIcon({
            html: '<i class="fas fa-tractor" style="color: #28a745; font-size: 20px;"></i>',
            iconSize: [30, 30],
            className: 'custom-div-icon'
        });

        const farmMarker = L.marker([routeData.farmLat, routeData.farmLng], {
            icon: farmIcon
        }).addTo(map);

        farmMarker.bindPopup(`
            <div style="text-align: center;">
                <strong><i class="fas fa-tractor"></i> Trang trại</strong><br>
                <span style="color: #28a745;">${routeData.farmName}</span>
            </div>
        `);

        // Customer marker (red)
        const customerIcon = L.divIcon({
            html: '<i class="fas fa-home" style="color: #dc3545; font-size: 20px;"></i>',
            iconSize: [30, 30],
            className: 'custom-div-icon'
        });

        const customerMarker = L.marker([routeData.customerLat, routeData.customerLng], {
            icon: customerIcon
        }).addTo(map);

        customerMarker.bindPopup(`
            <div style="text-align: center;">
                <strong><i class="fas fa-home"></i> Khách hàng</strong><br>
                <span style="color: #dc3545;">${routeData.customerAddress}</span>
            </div>
        `);

        // Get and display route
        getDeliveryRoute(map, routeData);

        // Store map instance
        window.deliveryMaps[orderId] = map;

    } catch (error) {
        console.error('Error initializing delivery route map:', error);
        mapContainer.innerHTML = `
            <div style="padding: 20px; text-align: center; color: #dc3545;">
                <i class="fas fa-exclamation-triangle"></i> 
                Lỗi tải bản đồ: ${error.message}
            </div>
        `;
    }
}

/**
 * Get delivery route using OSRM (Open Source Routing Machine)
 */
async function getDeliveryRoute(map, routeData) {
    try {
        // OSRM API endpoint for driving directions
        const osrmUrl = `https://router.project-osrm.org/route/v1/driving/${routeData.farmLng},${routeData.farmLat};${routeData.customerLng},${routeData.customerLat}?overview=full&geometries=geojson&steps=true`;

        const response = await fetch(osrmUrl);
        const data = await response.json();

        if (data.routes && data.routes.length > 0) {
            const route = data.routes[0];
            const routeCoordinates = route.geometry.coordinates.map(coord => [coord[1], coord[0]]);

            // Draw route on map
            const routeLine = L.polyline(routeCoordinates, {
                color: '#007bff',
                weight: 5,
                opacity: 0.8,
                dashArray: '10, 5'
            }).addTo(map);

            // Add route info popup
            const midPoint = routeCoordinates[Math.floor(routeCoordinates.length / 2)];
            const routeInfo = L.popup({
                closeButton: false,
                autoClose: false,
                closeOnClick: false,
                className: 'route-info-popup'
            })
            .setLatLng(midPoint)
            .setContent(`
                <div style="text-align: center; font-size: 12px;">
                    <strong><i class="fas fa-route"></i> Đường đi giao hàng</strong><br>
                    <span style="color: #007bff;">
                        Khoảng cách: ${(route.distance / 1000).toFixed(1)} km<br>
                        Thời gian: ${Math.round(route.duration / 60)} phút
                    </span>
                </div>
            `)
            .addTo(map);

            // Fit map to show entire route
            const group = new L.featureGroup([routeLine]);
            map.fitBounds(group.getBounds().pad(0.1));

            // Add route steps if available
            if (route.legs && route.legs[0] && route.legs[0].steps) {
                addRouteSteps(map, route.legs[0].steps);
            }

        } else {
            // Fallback: draw straight line if no route found
            drawStraightLineRoute(map, routeData);
        }

    } catch (error) {
        console.error('Error getting route:', error);
        // Fallback: draw straight line
        drawStraightLineRoute(map, routeData);
    }
}

/**
 * Draw straight line route as fallback
 */
function drawStraightLineRoute(map, routeData) {
    const straightLine = L.polyline([
        [routeData.farmLat, routeData.farmLng],
        [routeData.customerLat, routeData.customerLng]
    ], {
        color: '#ffc107',
        weight: 3,
        opacity: 0.7,
        dashArray: '15, 10'
    }).addTo(map);

    // Calculate straight line distance
    const distance = map.distance(
        [routeData.farmLat, routeData.farmLng],
        [routeData.customerLat, routeData.customerLng]
    ) / 1000;

    const midPoint = [
        (routeData.farmLat + routeData.customerLat) / 2,
        (routeData.farmLng + routeData.customerLng) / 2
    ];

    L.popup({
        closeButton: false,
        autoClose: false,
        closeOnClick: false
    })
    .setLatLng(midPoint)
    .setContent(`
        <div style="text-align: center; font-size: 12px;">
            <strong><i class="fas fa-ruler"></i> Khoảng cách thẳng</strong><br>
            <span style="color: #ffc107;">
                ${distance.toFixed(1)} km<br>
                <small>(Đường đi thực tế sẽ dài hơn)</small>
            </span>
        </div>
    `)
    .addTo(map);

    // Fit map to show both points
    const group = new L.featureGroup([straightLine]);
    map.fitBounds(group.getBounds().pad(0.1));
}

/**
 * Add route steps as markers
 */
function addRouteSteps(map, steps) {
    const importantSteps = steps.filter(step => 
        step.maneuver.type === 'turn' || 
        step.maneuver.type === 'roundabout' ||
        step.distance > 1000 // Steps longer than 1km
    );

    importantSteps.forEach((step, index) => {
        if (index < 5) { // Limit to 5 important steps
            const stepIcon = L.divIcon({
                html: `<div style="background: #007bff; color: white; border-radius: 50%; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; font-size: 10px; font-weight: bold;">${index + 1}</div>`,
                iconSize: [20, 20],
                className: 'step-marker'
            });

            const stepMarker = L.marker([
                step.maneuver.location[1], 
                step.maneuver.location[0]
            ], {
                icon: stepIcon
            }).addTo(map);

            stepMarker.bindPopup(`
                <div style="font-size: 12px;">
                    <strong>Bước ${index + 1}</strong><br>
                    ${step.maneuver.instruction || 'Tiếp tục đi thẳng'}<br>
                    <small>${(step.distance / 1000).toFixed(1)} km</small>
                </div>
            `);
        }
    });
}

/**
 * Refresh route when order data changes
 */
function refreshDeliveryRoute(orderId, newRouteData) {
    if (window.deliveryMaps[orderId]) {
        window.deliveryMaps[orderId].remove();
        delete window.deliveryMaps[orderId];
    }
    initDeliveryRouteMap(orderId, newRouteData);
}

// CSS for custom markers
const style = document.createElement('style');
style.textContent = `
    .custom-div-icon {
        background: transparent !important;
        border: none !important;
    }
    
    .route-info-popup .leaflet-popup-content-wrapper {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .step-marker {
        background: transparent !important;
        border: none !important;
    }
    
    .leaflet-popup-content {
        margin: 8px 12px !important;
    }
`;
document.head.appendChild(style);