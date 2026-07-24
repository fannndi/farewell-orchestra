@echo off
cd /d "%~dp0"
for /f "usebackq tokens=*" %%i in (".env") do set %%i
opencode %*