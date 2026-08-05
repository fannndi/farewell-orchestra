@echo off
title Farewell Orchestra - Profile Switcher
cd /d "%~dp0"

:: ── guard: python available? ──────────────────────────────────────
where python >nul 2>nul || (
    echo.
    echo  ERROR: python tidak ditemukan di PATH.
    echo  Install Python 3.10+ atau tambahkan ke PATH.
    echo.
    pause
    exit /b 1
)

:: ── banner ────────────────────────────────────────────────────────
echo.
echo  ==========================================================
echo  ^|                                                        ^|
echo  ^|         PROFILE SWITCHER - Farewell Orchestra          ^|
echo  ^|             opencode.jsonc profile manager             ^|
echo  ^|                                                        ^|
echo  ==========================================================
echo.
echo   Pilih profile dari menu di bawah (0 = keluar).
echo.

:: ── run menu ──────────────────────────────────────────────────────
python generate.py --menu
if errorlevel 1 (
    echo.
    echo  ERROR: generate.py gagal dijalankan.
    echo.
)

:: ── close ─────────────────────────────────────────────────────────
echo.
echo Tekan Enter untuk menutup jendela...
pause >nul
