param([switch]$NoBrowser)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$serviceRoot = Join-Path $env:ProgramData "CMBX Web Service"
$configPath = Join-Path $serviceRoot "server.env.ps1"
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $python)) {
    throw "Server dependencies are not installed. Run Install_CMBX_Web_Server.ps1 first."
}
if (Test-Path -LiteralPath $configPath) { . $configPath }
if (-not $env:CMBX_WEB_HOST) { $env:CMBX_WEB_HOST = "0.0.0.0" }
if (-not $env:CMBX_WEB_PORT) { $env:CMBX_WEB_PORT = "8765" }
if (-not $env:CMBX_WEB_STATE_ROOT) { $env:CMBX_WEB_STATE_ROOT = $serviceRoot }
if (-not $env:CMBX_CHROMELEON_BIN) {
    $env:CMBX_CHROMELEON_BIN = Join-Path $serviceRoot "runtime\chromeleon"
}

$logRoot = Join-Path $env:CMBX_WEB_STATE_ROOT "logs"
New-Item -ItemType Directory -Path $logRoot -Force | Out-Null
$pidPath = Join-Path $env:CMBX_WEB_STATE_ROOT "cmbx-web.pid"
if (Test-Path -LiteralPath $pidPath) {
    $oldPid = (Get-Content -LiteralPath $pidPath -Raw).Trim()
    if ($oldPid -and (Get-Process -Id $oldPid -ErrorAction SilentlyContinue)) {
        Write-Host "CMBX Web Workspace is already running (PID $oldPid)."
        if (-not $NoBrowser) { Start-Process "http://127.0.0.1:$env:CMBX_WEB_PORT/" }
        exit 0
    }
}

$logFile = Join-Path $logRoot "server.log"
$env:CMBX_WEB_LOG_FILE = $logFile
$info = [Diagnostics.ProcessStartInfo]::new()
$info.FileName = $python
$info.Arguments = "-B `"$(Join-Path $projectRoot 'run_web_workspace.py')`""
$info.WorkingDirectory = $projectRoot
$info.UseShellExecute = $false
$info.CreateNoWindow = $true
$info.WindowStyle = [Diagnostics.ProcessWindowStyle]::Hidden
$process = [Diagnostics.Process]::Start($info)
$process.Id | Set-Content -LiteralPath $pidPath -Encoding ASCII

$health = "http://127.0.0.1:$env:CMBX_WEB_PORT/api/health"
$ready = $false
for ($attempt = 0; $attempt -lt 30; $attempt++) {
    Start-Sleep -Milliseconds 500
    try {
        $response = Invoke-WebRequest -UseBasicParsing -Uri $health -TimeoutSec 2
        if ($response.StatusCode -eq 200) { $ready = $true; break }
    } catch {
        $status = $_.Exception.Response.StatusCode.value__
        if ($status -eq 401 -or $status -eq 403) { $ready = $true; break }
    }
    if ($process.HasExited) { break }
}
if (-not $ready) {
    throw "The server did not become ready. Review $logFile"
}

Write-Host "CMBX Web Workspace is running (PID $($process.Id))." -ForegroundColor Green
Write-Host "Local: http://127.0.0.1:$env:CMBX_WEB_PORT/"
Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
    Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" } |
    Sort-Object InterfaceMetric |
    ForEach-Object { Write-Host "LAN:   http://$($_.IPAddress):$env:CMBX_WEB_PORT/" }
if (-not $NoBrowser) { Start-Process "http://127.0.0.1:$env:CMBX_WEB_PORT/" }
