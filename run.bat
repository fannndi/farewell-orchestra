@echo off
cd /d "%~dp0"
title Farewell Orchestra ? Profile Switcher

:menu
cls
echo.
echo   +------------------------------------------+
echo   ^|     Farewell Orchestra ? Profiles        ^|
echo   +------------------------------------------+
echo   ^|  1. Pro      deepseek-v4-pro + flash     ^|
echo   ^|  2. Flash    flash + mimo-v2.5           ^|
echo   ^|  3. Free     nemotron-free + openrouter   ^|
echo   ^|  4. Hybrid   flash + nemotron-free       ^|
echo   ^|  5. Exit                                 ^|
echo   +------------------------------------------+
echo.
set /p choice="  Pilih [1-5]: "

if "%choice%"=="1" set SRC=pro
if "%choice%"=="2" set SRC=flash
if "%choice%"=="3" set SRC=free
if "%choice%"=="4" set SRC=hybrid
if "%choice%"=="5" exit /b 0

if "%SRC%"=="" (
    echo  Invalid choice
    pause
    goto menu
)

copy /y "profile\%SRC%.opencode.jsonc" opencode.jsonc >nul
echo.
echo  [%SRC%] profile applied
echo  Run: opencode
echo.
pause
exit /b 0