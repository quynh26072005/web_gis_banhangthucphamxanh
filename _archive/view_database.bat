@echo off
echo ========================================
echo    PostgreSQL Database Viewer
echo ========================================

set PGPASSWORD=26072005
set PSQL_PATH="C:\Program Files\PostgreSQL\18\bin\psql.exe"

echo Connecting to database...
%PSQL_PATH% -U postgres -h localhost -d clean_food_gis_db

pause