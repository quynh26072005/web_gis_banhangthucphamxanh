@echo off
echo ========================================
echo    Django GIS Migrations
echo ========================================

set PYTHON_PATH=C:\Users\Quynh\miniconda3\envs\clean_food_gis\python.exe

echo Step 1: Making migrations...
%PYTHON_PATH% manage.py makemigrations
if %errorlevel% neq 0 (
    echo Error in makemigrations
    pause
    exit /b 1
)

echo.
echo Step 2: Running migrate...
%PYTHON_PATH% manage.py migrate
if %errorlevel% neq 0 (
    echo Error in migrate
    pause
    exit /b 1
)

echo.
echo Step 3: Creating superuser (if needed)...
echo from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@test.com', 'admin123') | %PYTHON_PATH% manage.py shell

echo.
echo Step 4: Creating GIS sample data...
%PYTHON_PATH% create_gis_data.py

echo.
echo ========================================
echo Migrations completed successfully!
echo ========================================
echo.
echo You can now run:
echo   python manage.py runserver
echo.
pause