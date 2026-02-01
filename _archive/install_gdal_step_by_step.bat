@echo off
echo ========================================
echo    GDAL Installation Helper Script
echo ========================================
echo.

echo Step 1: Download OSGeo4W
echo Please download OSGeo4W installer from:
echo https://trac.osgeo.org/osgeo4w/
echo.
echo Press any key after downloading...
pause

echo.
echo Step 2: Install OSGeo4W
echo 1. Run osgeo4w-setup.exe as Administrator
echo 2. Choose Express Install
echo 3. Select these packages:
echo    - gdal
echo    - python3-gdal
echo    - proj
echo    - proj-data
echo    - geos
echo.
echo Press any key after installation...
pause

echo.
echo Step 3: Setting Environment Variables
echo Adding GDAL paths to system PATH...

:: Add to PATH
setx PATH "%PATH%;C:\OSGeo4W\bin;C:\OSGeo4W\apps\gdal\bin" /M

:: Set GDAL variables
setx GDAL_DATA "C:\OSGeo4W\share\gdal" /M
setx PROJ_LIB "C:\OSGeo4W\share\proj" /M
setx GDAL_DRIVER_PATH "C:\OSGeo4W\bin\gdalplugins" /M

echo Environment variables set!
echo.

echo Step 4: Testing installation
echo Please restart Command Prompt and run:
echo   gdalinfo --version
echo   python check_gdal.py
echo.

echo ========================================
echo Installation helper completed!
echo Please restart your Command Prompt
echo ========================================
pause