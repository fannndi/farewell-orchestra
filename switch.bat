@echo off
setlocal enabledelayedexpansion
title Farewell Orchestra -- Profile Selector
set "PROFILE=None"
color 0B

:menu
cls
echo.
echo   +==================================+
echo   ^|    FAREWELL ORCHESTRA            ^|
echo   ^|    Profile Selector              ^|
echo   +==================================+
echo.
echo     Profile: %PROFILE%
echo     -----------------------------
echo     [1] Paid   - deepseek-v4-pro + flash
echo     [2] Hybrid - paid flash + free
echo     [3] Free   - nemotron-3-ultra + north-mini
echo     [4] Backup - OpenRouter via 9router
echo     [5] Exit
echo     -----------------------------
echo.
set "CHOICE="
set /p "CHOICE=    Choice [1-5]: "
if "%CHOICE%"=="1" goto :paid
if "%CHOICE%"=="2" goto :hybrid
if "%CHOICE%"=="3" goto :free
if "%CHOICE%"=="4" goto :backup
if "%CHOICE%"=="5" goto :exit
echo.
echo     [!] Invalid choice
echo.
pause >nul
goto :menu

:paid
set "PROFILE=Paid [deepseek-v4-pro + flash]"
opencode -c profiles\opencode.paid.jsonc
goto :menu

:hybrid
set "PROFILE=Hybrid [paid flash + free]"
opencode -c profiles\opencode.hybrid.jsonc
goto :menu

:free
set "PROFILE=Free [nemotron-3-ultra + north-mini]"
opencode -c profiles\opencode.free.jsonc
goto :menu

:backup
set "PROFILE=Backup [OpenRouter via 9router]"
opencode -c profiles\opencode.free-backup.jsonc
goto :menu

:exit
cls
echo.
echo   Goodbye.
timeout /t 1 /nobreak >nul
exit /b 0
