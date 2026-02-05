#!/bin/bash
# Backup script for Clean Food GIS

BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p $BACKUP_DIR

echo "💾 Creating backup..."

# Backup database
pg_dump clean_food_gis_db > $BACKUP_DIR/database.sql

# Backup media files
cp -r media/ $BACKUP_DIR/

# Create archive
tar -czf $BACKUP_DIR.tar.gz $BACKUP_DIR/
rm -rf $BACKUP_DIR/

echo "✅ Backup created: $BACKUP_DIR.tar.gz"
