# API Documentation

## Overview
Clean Food GIS provides REST APIs for:
- Store location services
- Delivery zone management
- Order tracking
- Product catalog

## Endpoints
- `/gis/api/find-nearest-farms/` - Find nearest stores
- `/gis/api/delivery-zones-geojson/` - Get delivery zones
- `/gis/api/get-route-to-farm/` - Get route information

## Authentication
Most endpoints require authentication. Use Django's built-in authentication system.
