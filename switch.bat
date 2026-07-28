@echo off
set BASE=%~dp0
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
    copy /Y "%BASE%profiles\opencode.paid.jsonc" "%BASE%opencode.jsonc"
    echo [OK] Profile: Paid
) else if "%choice%"=="2" (
    copy /Y "%BASE%profiles\opencode.hybrid.jsonc" "%BASE%opencode.jsonc"
    echo [OK] Profile: Hybrid
) else if "%choice%"=="3" (
    copy /Y "%BASE%profiles\opencode.free.jsonc" "%BASE%opencode.jsonc"
    echo [OK] Profile: Free
) else (
    echo [ERROR] Pilihan tidak valid: %choice%. Masukkan 1, 2, atau 3.
    exit /b 1
)

if not exist "%BASE%opencode.jsonc" (
    echo [ERROR] opencode.jsonc tidak ditemukan setelah switch.
    exit /b 1
)
echo [DONE] Config aktif: opencode.jsonc