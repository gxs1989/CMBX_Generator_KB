$ErrorActionPreference = "Stop"
$serviceRoot = Join-Path $env:ProgramData "CMBX Web Service"
$configPath = Join-Path $serviceRoot "server.env.ps1"
if (Test-Path -LiteralPath $configPath) { . $configPath }
if (-not $env:CMBX_WEB_PORT) { $env:CMBX_WEB_PORT = "8765" }
$pidPath = Join-Path $serviceRoot "cmbx-web.pid"
$stopped = @()
if (Test-Path -LiteralPath $pidPath) {
    $serverPid = (Get-Content -LiteralPath $pidPath -Raw).Trim()
    if ($serverPid -and (Get-Process -Id $serverPid -ErrorAction SilentlyContinue)) {
        Stop-Process -Id $serverPid -Force -ErrorAction SilentlyContinue
        $stopped += [int]$serverPid
    }
}
$listener = Get-NetTCPConnection -LocalPort ([int]$env:CMBX_WEB_PORT) -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
if ($listener -and $stopped -notcontains $listener.OwningProcess) {
    $listenerProcess = Get-CimInstance Win32_Process -Filter "ProcessId=$($listener.OwningProcess)" -ErrorAction SilentlyContinue
    if ([string]$listenerProcess.CommandLine -match 'run_web_workspace\.py') {
        Stop-Process -Id $listener.OwningProcess -Force -ErrorAction SilentlyContinue
        $stopped += $listener.OwningProcess
    }
}
Remove-Item -LiteralPath $pidPath -Force -ErrorAction SilentlyContinue
if ($stopped.Count) {
    Write-Host "CMBX Web Workspace stopped (PID $($stopped -join ', '))."
} else {
    Write-Host "CMBX Web Workspace is not running."
}
