$ErrorActionPreference = "Stop"
$serviceRoot = Join-Path $env:ProgramData "CMBX Web Service"
$pidPath = Join-Path $serviceRoot "cmbx-web.pid"
if (-not (Test-Path -LiteralPath $pidPath)) {
    Write-Host "CMBX Web Workspace is not running."
    exit 0
}
$serverPid = (Get-Content -LiteralPath $pidPath -Raw).Trim()
if ($serverPid) {
    Stop-Process -Id $serverPid -ErrorAction SilentlyContinue
}
Remove-Item -LiteralPath $pidPath -Force -ErrorAction SilentlyContinue
Write-Host "CMBX Web Workspace stopped."
