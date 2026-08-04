$ErrorActionPreference = "Stop"
$ruleName = "CMBX Web Workspace 8765"
$existing = Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue

if ($existing) {
    Set-NetFirewallRule -DisplayName $ruleName -Enabled True -Profile Domain,Private
} else {
    New-NetFirewallRule `
        -DisplayName $ruleName `
        -Direction Inbound `
        -Action Allow `
        -Protocol TCP `
        -LocalPort 8765 `
        -Profile Domain,Private | Out-Null
}

Write-Host "CMBX Web Workspace is allowed on Domain/Private networks at TCP 8765."
Write-Host "LAN URL: http://10.68.182.125:8765/"
Read-Host "Press Enter to close"
