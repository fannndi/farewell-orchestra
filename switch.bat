@echo off
setlocal enabledelayedexpansion

if "%1"=="" (
    echo Usage: switch.bat pro ^| flash ^| free ^| custom
    echo.
    echo   pro    orchestrator=Pro,  workers=Flash ^(default^)
    echo   flash  orchestrator=Flash, workers=Free
    echo   free   all Free max hemat
    echo   custom edit .env lalu run ^"opencode^"
    exit /b 1
)

if /i "%1"=="pro" (
    set ORCHESTRA_HEAVY_MODEL=ocg/deepseek-v4-pro
    set ORCHESTRA_LIGHT_MODEL=ocg/deepseek-v4-flash
    echo [Pro] orchestrator=Pro  workers=Flash
) else if /i "%1"=="flash" (
    set ORCHESTRA_HEAVY_MODEL=ocg/deepseek-v4-flash
    set ORCHESTRA_LIGHT_MODEL=oc/deepseek-v4-flash-free
    echo [Flash] orchestrator=Flash  workers=Free
) else if /i "%1"=="free" (
    set ORCHESTRA_HEAVY_MODEL=oc/deepseek-v4-flash-free
    set ORCHESTRA_LIGHT_MODEL=oc/deepseek-v4-flash-free
    echo [Free] all Free max hemat
) else (
    echo Unknown profile: %1
    echo Use: pro, flash, free, custom
    exit /b 1
)

:: Write .env
(
    echo NINEROUTER_API_KEY=sk_9router
    echo ORCHESTRA_HEAVY_MODEL=!ORCHESTRA_HEAVY_MODEL!
    echo ORCHESTRA_LIGHT_MODEL=!ORCHESTRA_LIGHT_MODEL!
) > .env

echo .env updated. Starting OpenCode...
echo.
opencode
endlocal
