@echo off
echo ========================================
echo   Farewell Orchestra — Profile Switcher
echo ========================================
echo.
echo Pilih profile:
echo   1. Paid       (DeepSeek V4 Pro + Flash)
echo   2. Hybrid     (2 paid + 2 free)
echo   3. Free       (Nemotron + North Mini)
echo.
set /p choice="Pilihan (1-3): "

if "%choice%"=="1" (
    copy /Y profiles\opencode.paid.jsonc opencode.jsonc
    echo [OK] Profile: Paid
) else if "%choice%"=="2" (
    copy /Y profiles\opencode.hybrid.jsonc opencode.jsonc
    echo [OK] Profile: Hybrid
) else if "%choice%"=="3" (
    copy /Y profiles\opencode.free.jsonc opencode.jsonc
    echo [OK] Profile: Free
) else (
    echo [ERROR] Pilihan tidak valid.
)

pause
