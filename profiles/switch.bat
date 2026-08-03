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
echo   1. default   - ocg flash + codex + free
echo   2. mix       - codex + ollama + free
echo   3. low-cost  - hy3 + mimo (small flipped)
echo   4. free      - 100%% FREE, adik belajar
echo.
echo   Ketik nomor profile, 0 = keluar.
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
