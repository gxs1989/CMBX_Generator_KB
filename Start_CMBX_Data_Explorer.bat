@echo off
setlocal
cd /d "%~dp0" || (
    echo Could not enter application folder.
    pause
    exit /b 1
)
set "LOG_DIR=%CD%\logs"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"
set "LOG_FILE=%LOG_DIR%\launcher_last.log"
echo [%date% %time%] Starting CMBX Data Explorer > "%LOG_FILE%"

set "PYW="
for /f "delims=" %%P in ('where python 2^>nul') do (
    echo %%P >> "%LOG_FILE%"
    if not defined PYW if exist "%%~dpPpythonw.exe" set "PYW=%%~dpPpythonw.exe"
)

if defined PYW (
    echo Launching detached GUI with "%PYW%" >> "%LOG_FILE%"
    start "CMBX Data Explorer" "%PYW%" -B run_app.py
    exit /b 0
)

where python >> "%LOG_FILE%" 2>&1
if not errorlevel 1 (
    echo Launching detached GUI with python.exe >> "%LOG_FILE%"
    start "CMBX Data Explorer" python -B run_app.py
    exit /b 0
)

echo Python was not found. >> "%LOG_FILE%"
echo Python was not found. See "%LOG_FILE%".
pause
exit /b 1
