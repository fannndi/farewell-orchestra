@echo off
title Farewell Orchestra - Profile Switcher
cd /d "%~dp0"

where python >nul 2>nul || (
    echo ERROR: python tidak ditemukan di PATH.
    pause
    exit /b 1
)

if "%~1"=="" (
    echo.
    echo Usage: switch.bat ^<profile-name^>
    echo.
    echo Profiles: Pro, Codex Main, Daily, Eco, Backup
    echo.
    echo Contoh: switch.bat Pro
    echo.
    pause
    exit /b 0
)

python generate.py %~1
if errorlevel 1 (
    echo.
    echo ERROR: generate.py gagal.
    echo.
)

pause
