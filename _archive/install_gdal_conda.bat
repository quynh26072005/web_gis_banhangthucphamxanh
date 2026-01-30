@echo off
echo Installing GDAL with Conda...
conda install -c conda-forge gdal
conda install -c conda-forge geos
conda install -c conda-forge proj
echo Done!