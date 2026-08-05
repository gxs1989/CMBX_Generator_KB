param([int]$Port = 8765, [switch]$NoPause)

$ErrorActionPreference = "Stop"
$ruleName = "CMBX Web Workspace $Port"
$existing = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue

if ($existing) {
    Set-NetFirewallRule -DisplayName $ruleName -Enabled True -Profile Domain,Private
} else {
    New-NetFirewallRule `
        -DisplayName $ruleName `
        -Direction Inbound `
        -Action Allow `
        -Protocol TCP `
        -LocalPort $Port `
        -Profile Domain,Private | Out-Null
}

Write-Host "CMBX Web Workspace is allowed on Domain/Private networks at TCP $Port."
Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
    Where-Object { $_.IPAddress -notlike "127.*" -and $_.IPAddress -notlike "169.254.*" } |
    Sort-Object InterfaceMetric |
    ForEach-Object { Write-Host "LAN URL: http://$($_.IPAddress):$Port/" }
if (-not $NoPause) { Read-Host "Press Enter to close" }
