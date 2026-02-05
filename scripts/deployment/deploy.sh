#!/bin/bash
# Deployment script for Clean Food GIS

echo "🚀 Starting deployment..."

# Pull latest code
git pull origin main

# Install/update dependencies
pip install -r requirements/production.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart services
sudo systemctl restart clean_food_gis
sudo systemctl restart nginx

echo "✅ Deployment completed!"
