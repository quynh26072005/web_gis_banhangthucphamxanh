# Hướng dẫn cài đặt GDAL cho Django GIS trên Windows

## 🎯 Phương pháp 1: OSGeo4W (Khuyến nghị)

### Bước 1: Tải OSGeo4W
1. Truy cập: **https://trac.osgeo.org/osgeo4w/**
2. Click **"Download"** 
3. Tải **OSGeo4W network installer** (osgeo4w-setup.exe)

### Bước 2: Cài đặt OSGeo4W
1. **Chạy installer với quyền Administrator** (Right-click → Run as administrator)
2. Chọn **"Express Install"**
3. Chọn các packages sau:
   - ✅ **gdal** (GDAL library)
   - ✅ **python3-gdal** (Python bindings)
   - ✅ **proj** (Projection library)
   - ✅ **proj-data** (Projection data)
   - ✅ **geos** (Geometry library)
4. Click **"Next"** và chờ download + install

### Bước 3: Cấu hình Environment Variables
1. Mở **System Properties** (Windows + R → sysdm.cpl)
2. Tab **"Advanced"** → **"Environment Variables"**
3. Trong **"System Variables"**, tìm **"Path"** và click **"Edit"**
4. Thêm các đường dẫn sau (thay đổi nếu cài ở vị trí khác):
   ```
   C:\OSGeo4W\bin
   C:\OSGeo4W\apps\gdal\bin
   C:\OSGeo4W\apps\Python39\Scripts
   ```

### Bước 4: Cấu hình GDAL Variables
Thêm các biến môi trường mới:
- **GDAL_DATA**: `C:\OSGeo4W\share\gdal`
- **PROJ_LIB**: `C:\OSGeo4W\share\proj`
- **GDAL_DRIVER_PATH**: `C:\OSGeo4W\bin\gdalplugins`

### Bước 5: Restart Command Prompt
Đóng tất cả Command Prompt/PowerShell và mở lại để áp dụng thay đổi.

---

## 🎯 Phương pháp 2: Conda (Nếu có Anaconda/Miniconda)

### Cài đặt qua Conda
```bash
conda install -c conda-forge gdal
conda install -c conda-forge geos
conda install -c conda-forge proj
```

---

## 🎯 Phương pháp 3: Pip với pre-compiled wheels

### Cài đặt GDAL qua pip
```bash
pip install GDAL
pip install Fiona
pip install Shapely
```

**Lưu ý**: Phương pháp này có thể gặp lỗi compilation trên Windows.

---

## 🧪 Kiểm tra cài đặt

### Test 1: Kiểm tra GDAL command line
```bash
gdalinfo --version
```
**Kết quả mong đợi**: `GDAL 3.x.x, released 202x/xx/xx`

### Test 2: Kiểm tra Python GDAL
```python
from osgeo import gdal
print(gdal.VersionInfo())
```

### Test 3: Kiểm tra Django GIS
```python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clean_food_gis.settings')
django.setup()

from django.contrib.gis.geos import Point
test_point = Point(106.6297, 10.8231)
print(f"Point created: {test_point}")
```

---

## 🔧 Troubleshooting

### Lỗi "Could not find the GDAL library"
**Giải pháp**:
1. Kiểm tra PATH có chứa `C:\OSGeo4W\bin`
2. Thêm vào settings.py:
```python
import os
if os.name == 'nt':  # Windows
    GDAL_LIBRARY_PATH = r'C:\OSGeo4W\bin\gdal306.dll'  # Thay số version
    GEOS_LIBRARY_PATH = r'C:\OSGeo4W\bin\geos_c.dll'
```

### Lỗi "No module named 'osgeo'"
**Giải pháp**:
1. Cài đặt lại python3-gdal trong OSGeo4W
2. Hoặc: `pip install GDAL==$(gdal-config --version) --global-option=build_ext --global-option="-IC:\OSGeo4W\include" --global-option="-LC:\OSGeo4W\lib"`

### Lỗi DLL load failed
**Giải pháp**:
1. Cài đặt Microsoft Visual C++ Redistributable
2. Restart máy tính
3. Kiểm tra PATH variables

---

## 📋 Checklist cài đặt hoàn tất

- [ ] OSGeo4W installer đã chạy thành công
- [ ] Các packages (gdal, python3-gdal, proj, geos) đã được cài
- [ ] Environment Variables đã được thêm vào PATH
- [ ] GDAL_DATA và PROJ_LIB đã được set
- [ ] Command `gdalinfo --version` hoạt động
- [ ] Python có thể import osgeo.gdal
- [ ] Django GIS có thể tạo Point objects

---

## 🚀 Sau khi cài đặt thành công

1. **Kiểm tra**: `python check_gdal.py`
2. **Kích hoạt GIS**: `python enable_gis_features.py`
3. **Migration**: `python migrate_to_gis.py`
4. **Chạy server**: `python manage.py runserver`
5. **Truy cập GIS Tools**: http://localhost:8000/gis-tools/

---

## 💡 Tips

- **Luôn chạy installer với quyền Administrator**
- **Restart Command Prompt sau khi cài**
- **Kiểm tra version compatibility giữa GDAL và Django**
- **Backup dữ liệu trước khi migration**