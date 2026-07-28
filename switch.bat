@echo off
setlocal
set BASE=%~dp0

echo === Farewell Orchestra — Profile Switcher ===
echo.
echo  1. V1 (Default) — deepseek-v4-flash + deepseek-free + north-mini-code  [WINNER]
echo  2. LIMITED — ollama/minimax-m3 + north-mini-code  [V1 base, flash replaced]
echo.
set /P CH="Choice (1-2): "

if "%CH%"=="1" set SRC=%BASE%profiles\hybrid-v1.jsonc
if "%CH%"=="2" set SRC=%BASE%profiles\opencode.limited.jsonc

if "%SRC%"=="" ( echo Invalid choice. & pause & exit /b 1 )
if not exist "%SRC%" ( echo ERROR: File missing — %SRC% & pause & exit /b 1 )

copy /Y "%SRC%" "%BASE%opencode.jsonc" >nul
if errorlevel 1 ( echo ERROR: Copy failed. & pause & exit /b 1 )

echo Copied to opencode.jsonc — Restart opencode to apply.
pause