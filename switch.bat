@echo off
title Switch Profile — Farewell Orchestra
cd /d "%~dp0"
python profiles\generate.py --menu
pause
