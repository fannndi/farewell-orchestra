@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
title Farewell Orchestra - Profile Switcher

:: Check opencode exists
where opencode >nul 2>&1 || (
  echo.
  echo   [X] 'opencode' not found. Install it first.
  echo   https://opencode.ai
  echo.
  pause
  exit /b 1
)

color 0B

:menu
cls
echo.
echo   +==========================================+
echo   ^|     Farewell Orchestra - Profiles        ^|
echo   +==========================================+
echo   ^|  1. Paid     deepseek-v4-pro + flash     ^|
echo   ^|  2. Hybrid   flash + north-mini-free     ^|
echo   ^|  3. Free     nemotron-3-ultra-free       ^|
echo   ^|  4. Backup   OpenRouter via 9router      ^|
echo   ^|  5. Exit                                 ^|
echo   +==========================================+
echo.
set /p "choice=  Pilih [1-5]: "

if "%choice%"=="1" set "SRC=paid"   & set "NAME=Paid"
if "%choice%"=="2" set "SRC=hybrid" & set "NAME=Hybrid"
if "%choice%"=="3" set "SRC=free"   & set "NAME=Free"
if "%choice%"=="4" set "SRC=free-backup" & set "NAME=Free Backup"
if "%choice%"=="5" exit /b 0

if "%SRC%"=="" (
  echo   [X] Invalid choice
  timeout /t 1 /nobreak >nul
  goto menu
)

:: Copy profile to root config
copy /y "profiles\opencode.%SRC%.jsonc" opencode.jsonc >nul 2>&1
if errorlevel 1 (
  echo   [X] Failed to copy profiles\opencode.%SRC%.jsonc
  pause
  goto menu
)

echo.
echo   [OK] %NAME% profile applied.
echo   Launching opencode...
timeout /t 1 /nobreak >nul

:: Launch opencode with the new config
opencode
if errorlevel 1 (
  echo.
  echo   [X] opencode exited with error %errorlevel%
  echo   Check: API key in .env? 9Router at 127.0.0.1:20128?
  pause >nul
)

goto menu
