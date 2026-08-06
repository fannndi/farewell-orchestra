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
echo   1. Pro
echo   2. Codex Main
echo   3. Daily
echo   4. Eco
echo   5. Backup
echo.
echo   0. Keluar
echo.
echo ========================================

set /p choice="Pilih profile (1-5, 0 keluar): "

if "%choice%"=="1" (
    python generate.py Pro
    goto done
)
if "%choice%"=="2" (
    python generate.py "Codex Main"
    goto done
)
if "%choice%"=="3" (
    python generate.py Daily
    goto done
)
if "%choice%"=="4" (
    python generate.py Eco
    goto done
)
if "%choice%"=="5" (
    python generate.py Backup
    goto done
)
if "%choice%"=="0" (
    exit /b 0
)

echo.
echo Pilihan tidak valid!
pause
goto menu

:done
if errorlevel 1 (
    echo.
    echo ERROR: generate.py gagal.
) else (
    echo.
    echo Profile berhasil di-switch!
)
pause
