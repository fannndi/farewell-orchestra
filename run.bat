@echo off
cd /d "%~dp0"
title Farewell Orchestra
for /f "usebackq tokens=*" %%i in (".env") do set %%i
echo.
echo  Farewell Orchestra -- Model Loaded
echo.
echo  MODEL_A=%MODEL_A%
echo  MODEL_B=%MODEL_B%
echo.
echo  0. Exit
echo.
choice /c 0 /n /m "  Pilih: "
if errorlevel 1 exit /b 0