@echo off
setlocal
cd /d "%~dp0.."
echo ============================================================
echo CMBX Web Workspace - Server Installation
echo Python environment, offline packages, and bundled CM runtime
echo ============================================================
call "%CD%\Install_CMBX_Web_Server.bat"

