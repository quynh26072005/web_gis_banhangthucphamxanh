# Hướng dẫn Cài đặt Chi tiết

## Yêu cầu Hệ thống

### Python và Django
- Python 3.8+
- Django 4.2
- Django GIS extensions

### Database
**Tùy chọn 1: PostgreSQL + PostGIS (Khuyến nghị cho production)**
- PostgreSQL 12+
- PostGIS extension

**Tùy chọn 2: SQLite + SpatiaLite (Cho development)**
- SQLite với SpatiaLite extension

## Cài đặt từng bước

### Bước 1: Tạo Virtual Environment
```bash
# Tạo virtual environment
python -m venv clean_food_env

# Kích hoạt virtual environment
# Windows:
clean_food_env\Scripts\activate
# Linux/Mac:
source clean_food_env/bin/activate
```

### Bước 2: Cài đặt Dependencies
```bash
pip install -r requirements.txt
```

### Bước 3: Cấu hình Database

#### Tùy chọn A: PostgreSQL + PostGIS

1. **Cài đặt PostgreSQL và PostGIS**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib postgis

   # Windows: Tải từ https://www.postgresql.org/download/
   # Mac: brew install postgresql postgis
   ```

2. **Tạo Database**
   ```sql
   -- Đăng nhập PostgreSQL
   sudo -u postgres psql

   -- Tạo database
   CREATE DATABASE clean_food_gis_db;

   -- Tạo user
   CREATE USER clean_food_user WITH PASSWORD 'your_password';

   -- Cấp quyền
   GRANT ALL PRIVILEGES ON DATABASE clean_food_gis_db TO clean_food_user;

   -- Kích hoạt PostGIS
   \c clean_food_gis_db
   CREATE EXTENSION postgis;
   ```

3. **Cấu hình settings.py**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.contrib.gis.db.backends.postgis',
           'NAME': 'clean_food_gis_db',
           'USER': 'clean_food_user',
           'PASSWORD': 'your_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

#### Tùy chọn B: SQLite + SpatiaLite (Đơn giản hơn)

1. **Cài đặt SpatiaLite**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install spatialite-bin libspatialite7

   # Windows: Tải từ https://www.gaia-gis.it/gaia-sins/
   # Mac: brew install spatialite-tools
   ```

2. **Cấu hình settings.py**
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.contrib.gis.db.backends.spatialite',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }
   ```

### Bước 4: Migration
```bash
# Tạo migration files
python manage.py makemigrations food_store
python manage.py makemigrations gis_tools

# Chạy migrations
python manage.py migrate
```

### Bước 5: Tạo Superuser
```bash
python manage.py createsuperuser
```

### Bước 6: Tạo dữ liệu mẫu (Optional)
```bash
python manage.py shell
```

Trong Django shell:
```python
from django.contrib.gis.geos import Point, Polygon
from food_store.models import Farm, Category, Product, DeliveryZone

# Tạo danh mục
category = Category.objects.create(
    name="Rau củ quả",
    description="Rau củ quả tươi sạch"
)

# Tạo trang trại
farm = Farm.objects.create(
    name="Trang trại Xanh",
    address="Đồng Nai, Việt Nam",
    phone="0123456789",
    email="farm@example.com",
    description="Trang trại sản xuất rau sạch",
    location=Point(106.8, 10.9),  # longitude, latitude
    organic_certified=True,
    certification_number="ORG001"
)

# Tạo sản phẩm
product = Product.objects.create(
    name="Rau cải xanh",
    category=category,
    farm=farm,
    description="Rau cải xanh tươi ngon",
    price=25000,
    unit="kg",
    stock_quantity=100,
    is_available=True
)

# Tạo khu vực giao hàng (polygon cho TP.HCM)
coords = [
    (106.6, 10.7),
    (106.8, 10.7),
    (106.8, 10.9),
    (106.6, 10.9),
    (106.6, 10.7)
]
polygon = Polygon(coords)

delivery_zone = DeliveryZone.objects.create(
    name="TP. Hồ Chí Minh",
    area=polygon,
    delivery_fee=30000,
    delivery_time="1-2 ngày",
    is_active=True
)

print("Dữ liệu mẫu đã được tạo!")
```

### Bước 7: Chạy Server
```bash
python manage.py runserver
```

## Kiểm tra Cài đặt

### 1. Truy cập Website
- Trang chủ: http://localhost:8000/
- Django Admin: http://localhost:8000/admin/
- GIS Tools: http://localhost:8000/gis-tools/

### 2. Test GIS Functions
Trong Django shell:
```python
from gis_tools.gis_functions import FarmLocationAnalyzer
from django.contrib.gis.geos import Point

# Test tìm trang trại gần nhất
customer_location = Point(106.7, 10.8)
farms = FarmLocationAnalyzer.find_nearest_farms(customer_location)
print(f"Tìm thấy {farms.count()} trang trại")
```

## Troubleshooting

### Lỗi thường gặp

1. **ImportError: No module named 'django.contrib.gis'**
   - Cài đặt GDAL, GEOS, PROJ libraries
   - Ubuntu: `sudo apt-get install gdal-bin libgdal-dev`

2. **Database connection error**
   - Kiểm tra PostgreSQL service đang chạy
   - Kiểm tra username/password trong settings.py

3. **PostGIS extension not found**
   - Cài đặt PostGIS: `sudo apt-get install postgis`
   - Kích hoạt extension: `CREATE EXTENSION postgis;`

4. **SpatiaLite not found**
   - Cài đặt SpatiaLite: `sudo apt-get install spatialite-bin`

### Debug Commands

```bash
# Kiểm tra Django GIS
python manage.py shell -c "from django.contrib.gis.utils import layermapping; print('GIS OK')"

# Kiểm tra database connection
python manage.py dbshell

# Xem migrations
python manage.py showmigrations

# Reset database (cẩn thận!)
python manage.py flush
```

## Deployment (Production)

### 1. Cấu hình Production Settings
Tạo file `production_settings.py`:
```python
from .settings import *

DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']

# Security settings
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Database với connection pooling
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'clean_food_gis_prod',
        'USER': 'prod_user',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
        'CONN_MAX_AGE': 60,
    }
}
```

### 2. Static Files
```bash
python manage.py collectstatic
```

### 3. Web Server
Sử dụng Nginx + Gunicorn hoặc Apache + mod_wsgi

## Tài liệu tham khảo

- [Django GIS Documentation](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/)
- [PostGIS Documentation](https://postgis.net/documentation/)
- [Leaflet Documentation](https://leafletjs.com/reference.html)
- [Folium Documentation](https://python-visualization.github.io/folium/)