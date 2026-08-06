@echo off
title Farewell Orchestra - Profile Switcher
cd /d "%~dp0"

where python >nul 2>nul || (
    echo ERROR: python tidak ditemukan di PATH.
    pause
    exit /b 1
)

:menu
cls
echo.
echo ========================================
echo   Farewell Orchestra - Profile Switcher
echo ========================================
echo.

REM Dynamically list profiles from profiles.json
python -c "import json; profiles=json.load(open('profiles.json'))['profiles']; [print(f'  {i+1}. {p[\"name\"]} ({p[\"label\"]})') for i,p in enumerate(profiles)]"

echo.
echo   0. Keluar
echo.
echo ========================================

set /p choice="Pilih profile (angka, 0 keluar): "

if "%choice%"=="0" exit /b 0

REM Get profile name by index
for /f "tokens=*" %%i in ('python -c "import json; profiles=json.load(open('profiles.json'))['profiles']; print(profiles[%choice%-1]['name'] if 0<int('%choice%')<=len(profiles) else '')"') do set profile_name=%%i

if "%profile_name%"=="" (
    echo.
    echo Pilihan tidak valid!
    pause
    goto menu
)

python generate.py "%profile_name%"

if errorlevel 1 (
    echo.
    echo ERROR: generate.py gagal.
) else (
    echo.
    echo Profile berhasil di-switch ke %profile_name%!
)
pause
