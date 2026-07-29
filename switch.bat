@echo off
setlocal
set BASE=%~dp0

echo === Farewell Orchestra — Profile Switcher ===
echo.
echo  1. DEFAULT  — deepseek-v4-flash (paid) + OC free      [CHAMPION]
echo  2. DEF-OR   — deepseek-v4-flash + OpenRouter free
echo  3. OLLAMA   — ollama/minimax-m3 (local) + OC free
echo  4. OLL-OR   — ollama/minimax-m3 + OpenRouter free
echo.
set /P CH="Choice (1-4): "

if "%CH%"=="1" set SRC=%BASE%profiles\opencode.default.jsonc
if "%CH%"=="2" set SRC=%BASE%profiles\opencode.default-or.jsonc
if "%CH%"=="3" set SRC=%BASE%profiles\opencode.ollama.jsonc
if "%CH%"=="4" set SRC=%BASE%profiles\opencode.ollama-or.jsonc

if "%SRC%"=="" ( echo Invalid choice. & pause & exit /b 1 )
if not exist "%SRC%" ( echo ERROR: File missing — %SRC% & pause & exit /b 1 )

copy /Y "%SRC%" "%BASE%opencode.jsonc" >nul
if errorlevel 1 ( echo ERROR: Copy failed. & pause & exit /b 1 )

echo Copied to opencode.jsonc — Restart opencode to apply.
pause
