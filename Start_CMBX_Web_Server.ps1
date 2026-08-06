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

function Publish-WebEntry([string]$Port) {
    $computerName = [Net.Dns]::GetHostName()
    $hostUrl = "http://${computerName}:$Port/"
    $localUrl = "http://127.0.0.1:$Port/"
    $lanUrls = @(
        Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
            Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" } |
            Sort-Object InterfaceMetric |
            ForEach-Object { "http://$($_.IPAddress):$Port/" }
    )
    $shortcut = @("[InternetShortcut]", "URL=$hostUrl", "IconIndex=0") -join "`r`n"
    $addressText = @(
        "CMBX Web Workspace",
        "Stable LAN entry: $hostUrl",
        "Local server entry: $localUrl",
        "Current IP fallback entries:"
    ) + @($lanUrls | ForEach-Object { "  $_" })
    $launcherRoots = @(
        (Join-Path $projectRoot "launcher"),
        (Join-Path (Split-Path $projectRoot -Parent) "launcher"),
        $serviceRoot
    ) | Select-Object -Unique
    foreach ($root in $launcherRoots) {
        if (-not (Test-Path -LiteralPath $root)) { continue }
        $shortcut | Set-Content -LiteralPath (Join-Path $root "CMBX Web LAN Entry.url") -Encoding ASCII
        $addressText | Set-Content -LiteralPath (Join-Path $root "CMBX Web Server Address.txt") -Encoding UTF8
    }
    return [pscustomobject]@{ HostUrl = $hostUrl; LocalUrl = $localUrl; LanUrls = $lanUrls }
}

$logRoot = Join-Path $env:CMBX_WEB_STATE_ROOT "logs"
New-Item -ItemType Directory -Path $logRoot -Force | Out-Null
$pidPath = Join-Path $env:CMBX_WEB_STATE_ROOT "cmbx-web.pid"
$listener = Get-NetTCPConnection -LocalPort ([int]$env:CMBX_WEB_PORT) -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
if ($listener) {
    $listenerProcess = Get-CimInstance Win32_Process -Filter "ProcessId=$($listener.OwningProcess)" -ErrorAction SilentlyContinue
    $listenerCommand = [string]$listenerProcess.CommandLine
    if ($listenerCommand -match 'run_web_workspace\.py') {
        $listener.OwningProcess | Set-Content -LiteralPath $pidPath -Encoding ASCII
        $entry = Publish-WebEntry $env:CMBX_WEB_PORT
        Write-Host "CMBX Web Workspace is already running (PID $($listener.OwningProcess))."
        Write-Host "LAN entry: $($entry.HostUrl)" -ForegroundColor Cyan
        if (-not $NoBrowser) { Start-Process $entry.LocalUrl }
        exit 0
    }
    throw "TCP port $env:CMBX_WEB_PORT is occupied by PID $($listener.OwningProcess). Stop that process or choose another port."
}
if (Test-Path -LiteralPath $pidPath) {
    $oldPid = (Get-Content -LiteralPath $pidPath -Raw).Trim()
    if ($oldPid -and (Get-Process -Id $oldPid -ErrorAction SilentlyContinue)) {
        $entry = Publish-WebEntry $env:CMBX_WEB_PORT
        Write-Host "CMBX Web Workspace is already running (PID $oldPid)."
        Write-Host "LAN entry: $($entry.HostUrl)" -ForegroundColor Cyan
        if (-not $NoBrowser) { Start-Process $entry.LocalUrl }
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
    if ($process.HasExited) { break }
    try {
        $response = Invoke-WebRequest -UseBasicParsing -Uri $health -TimeoutSec 2
        if ($response.StatusCode -eq 200) { $ready = $true; break }
    } catch {
        $status = $_.Exception.Response.StatusCode.value__
        if ($status -eq 401 -or $status -eq 403) { $ready = $true; break }
    }
}
if ($ready) {
    $activeListener = Get-NetTCPConnection -LocalPort ([int]$env:CMBX_WEB_PORT) -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
    $activeProcess = if ($activeListener) {
        Get-CimInstance Win32_Process -Filter "ProcessId=$($activeListener.OwningProcess)" -ErrorAction SilentlyContinue
    } else {
        $null
    }
    # A venv python.exe on Windows is a launcher process. The process that
    # actually owns the Uvicorn socket therefore has a different PID.
    if (-not $activeListener -or [string]$activeProcess.CommandLine -notmatch 'run_web_workspace\.py') {
        $ready = $false
    } else {
        $activeListener.OwningProcess | Set-Content -LiteralPath $pidPath -Encoding ASCII
    }
}
if (-not $ready) {
    Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
    Remove-Item -LiteralPath $pidPath -Force -ErrorAction SilentlyContinue
    throw "The server did not become ready. Review $logFile"
}

$serverPid = (Get-Content -LiteralPath $pidPath -Raw).Trim()
Write-Host "CMBX Web Workspace is running (PID $serverPid)." -ForegroundColor Green
$entry = Publish-WebEntry $env:CMBX_WEB_PORT
Write-Host "Local:     $($entry.LocalUrl)"
Write-Host "LAN entry: $($entry.HostUrl)" -ForegroundColor Cyan
$entry.LanUrls | ForEach-Object { Write-Host "IP backup: $_" }
Write-Host "A reusable LAN shortcut was generated in the launcher folder."
if (-not $NoBrowser) { Start-Process $entry.LocalUrl }
