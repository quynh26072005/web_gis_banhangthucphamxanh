@echo off
echo ========================================
echo    Installing GDAL with Conda
echo ========================================

set CONDA_PATH=C:\Users\Quynh\miniconda3\Scripts\conda.exe

echo Step 1: Check Conda version
"%CONDA_PATH%" --version
echo.

echo Step 2: Create conda environment for GIS project
"%CONDA_PATH%" create -n clean_food_gis python=3.9 -y
echo.

echo Step 3: Install GDAL and GIS packages
"%CONDA_PATH%" install -n clean_food_gis -c conda-forge gdal -y
"%CONDA_PATH%" install -n clean_food_gis -c conda-forge geos -y
"%CONDA_PATH%" install -n clean_food_gis -c conda-forge proj -y
"%CONDA_PATH%" install -n clean_food_gis -c conda-forge fiona -y
"%CONDA_PATH%" install -n clean_food_gis -c conda-forge shapely -y
echo.

echo Step 4: Install Django and other packages
"%CONDA_PATH%" install -n clean_food_gis django=4.2.7 -y
"%CONDA_PATH%" install -n clean_food_gis psycopg2 -y
"%CONDA_PATH%" install -n clean_food_gis pillow -y
"%CONDA_PATH%" install -n clean_food_gis folium -y
"%CONDA_PATH%" install -n clean_food_gis geopy -y
"%CONDA_PATH%" install -n clean_food_gis requests -y
echo.

echo Step 5: Install django-leaflet via pip
call "%CONDA_PATH%" activate clean_food_gis
pip install django-leaflet
echo.

echo ========================================
echo Installation completed!
echo ========================================
echo.
echo To activate the environment, run:
echo   conda activate clean_food_gis
echo.
echo Then test with:
echo   python check_gdal.py
echo.
pause