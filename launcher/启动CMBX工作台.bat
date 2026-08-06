@echo off
setlocal
cd /d "%~dp0.." || (
    echo Could not enter the CMBX application folder.
    pause
    exit /b 1
)

set "LOG_DIR=%CD%\logs"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set "LOG_FILE=%LOG_DIR%\business_hub_launcher.log"
echo [%date% %time%] Starting CMBX Workspace (venv) > "%LOG_FILE%"

set "VENV_PYW=%CD%\.venv\Scripts\pythonw.exe"
set "VENV_PY=%CD%\.venv\Scripts\python.exe"

if exist "%VENV_PYW%" (
    echo Launching detached GUI with venv pythonw "%VENV_PYW%" >> "%LOG_FILE%"
    start "CMBX Workspace" "%VENV_PYW%" -B run_business_hub.py
    exit /b 0
)

if exist "%VENV_PY%" (
    echo Launching detached GUI with venv python "%VENV_PY%" >> "%LOG_FILE%"
    start "CMBX Workspace" "%VENV_PY%" -B run_business_hub.py
    exit /b 0
)

rem Fall back to the system Python search used by Start_CMBX_Workspace.bat
set "PYW="
for /f "delims=" %%P in ('where python 2^>nul') do (
    echo %%P >> "%LOG_FILE%"
    if not defined PYW if exist "%%~dpPpythonw.exe" set "PYW=%%~dpPpythonw.exe"
)

if defined PYW (
    echo Launching detached GUI with system pythonw "%PYW%" >> "%LOG_FILE%"
    start "CMBX Workspace" "%PYW%" -B run_business_hub.py
    exit /b 0
)

where python >> "%LOG_FILE%" 2>&1
if not errorlevel 1 (
    echo Launching detached GUI with system python >> "%LOG_FILE%"
    start "CMBX Workspace" python -B run_business_hub.py
    exit /b 0
)

echo Python was not found. >> "%LOG_FILE%"
echo Python was not found. See "%LOG_FILE%".
pause
exit /b 1
