@echo off
setlocal
cd /d "%~dp0"
if not defined CMBX_WEB_HOST set "CMBX_WEB_HOST=0.0.0.0"
if not defined CMBX_WEB_PORT set "CMBX_WEB_PORT=8765"
if not defined CMBX_WEB_STATE_ROOT set "CMBX_WEB_STATE_ROOT=%PROGRAMDATA%\CMBX Web Service"
if not defined CMBX_WEB_SHARED_ROOT if exist "%OneDriveCommercial%\CIC HPCS V&V-CMBX Workstation - CMBX" set "CMBX_WEB_SHARED_ROOT=%OneDriveCommercial%\CIC HPCS V&V-CMBX Workstation - CMBX"
start "CMBX Web Workspace" python -B run_web_workspace.py
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:%CMBX_WEB_PORT%/"
