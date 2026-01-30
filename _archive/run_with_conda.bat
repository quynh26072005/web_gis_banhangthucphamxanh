@echo off
echo Activating conda environment and running Django...
call C:\Users\Quynh\miniconda3\Scripts\activate.bat clean_food_gis

echo.
echo Environment activated! Available commands:
echo   python check_gdal.py          - Test GDAL installation
echo   python migrate_to_gis.py      - Run GIS migrations  
echo   python manage.py runserver    - Start Django server
echo.

cmd /k