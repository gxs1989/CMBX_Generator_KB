@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0Start_CMBX_Web_Server.ps1"
if errorlevel 1 pause
