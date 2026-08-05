param(
    [switch]$SkipFirewall,
    [switch]$SkipPythonPackages
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$serviceRoot = Join-Path $env:ProgramData "CMBX Web Service"
$workspaceRoot = Join-Path $env:ProgramData "CMBX Data Explorer Workspace"
$runtimeRoot = Join-Path $serviceRoot "runtime\chromeleon"
$configPath = Join-Path $serviceRoot "server.env.ps1"
$venvPython = Join-Path $projectRoot ".venv\Scripts\python.exe"

function Test-Administrator {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = [Security.Principal.WindowsPrincipal]::new($identity)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Resolve-Python311 {
    $candidates = @(
        (Join-Path $env:LocalAppData "Programs\Python\Python311\python.exe"),
        (Join-Path $env:ProgramFiles "Python311\python.exe"),
        (Join-Path ${env:ProgramFiles(x86)} "Python311\python.exe")
    )
    foreach ($candidate in $candidates) {
        if ($candidate -and (Test-Path -LiteralPath $candidate)) { return $candidate }
    }
    $python = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($python) {
        $version = & $python.Source -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"
        if ($version -eq "3.11") { return $python.Source }
    }
    $py = Get-Command py.exe -ErrorAction SilentlyContinue
    if ($py) {
        $resolved = & $py.Source -3.11 -c "import sys; print(sys.executable)" 2>$null
        if ($LASTEXITCODE -eq 0 -and $resolved) { return $resolved.Trim() }
    }
    return $null
}

Write-Host "Installing CMBX Web Workspace server dependencies..." -ForegroundColor Cyan
$python = Resolve-Python311
if (-not $python) {
    $winget = Get-Command winget.exe -ErrorAction SilentlyContinue
    if (-not $winget) {
        throw "Python 3.11 is required. Install it from python.org, then run this installer again."
    }
    Write-Host "Python 3.11 was not found. Installing it with winget..."
    & $winget.Source install --id Python.Python.3.11 -e --accept-package-agreements --accept-source-agreements
    if ($LASTEXITCODE -ne 0) { throw "Python 3.11 installation failed." }
    $python = Resolve-Python311
    if (-not $python) { throw "Python 3.11 was installed but could not be located. Reopen PowerShell and rerun the installer." }
}

if (-not (Test-Path -LiteralPath $venvPython)) {
    Write-Host "Creating isolated Python environment..."
    & $python -m venv (Join-Path $projectRoot ".venv")
    if ($LASTEXITCODE -ne 0) { throw "Could not create the Python virtual environment." }
}
if (-not $SkipPythonPackages) {
    Write-Host "Installing pinned Python dependencies..."
    & $venvPython -m pip install --upgrade pip
    $wheelhouse = Join-Path $projectRoot "deployment\wheelhouse"
    if (Test-Path -LiteralPath $wheelhouse) {
        & $venvPython -m pip install --no-index --find-links $wheelhouse -r (Join-Path $projectRoot "requirements-server.txt")
    } else {
        & $venvPython -m pip install -r (Join-Path $projectRoot "requirements-server.txt")
    }
    if ($LASTEXITCODE -ne 0) { throw "Python dependency installation failed." }
}

New-Item -ItemType Directory -Path $serviceRoot, $workspaceRoot, $runtimeRoot -Force | Out-Null
$runtimeZip = Join-Path $projectRoot "deployment\runtime\chromeleon-runtime.zip"
if (-not (Test-Path -LiteralPath $runtimeZip)) { throw "Bundled Chromeleon runtime is missing: $runtimeZip" }
Write-Host "Deploying the approved Chromeleon runtime..."
if (Test-Path -LiteralPath $runtimeRoot) { Remove-Item -LiteralPath $runtimeRoot -Recurse -Force }
New-Item -ItemType Directory -Path $runtimeRoot -Force | Out-Null
Expand-Archive -LiteralPath $runtimeZip -DestinationPath $runtimeRoot -Force

$mappingRoot = Join-Path $workspaceRoot "DB MAPPING"
$templateRoot = Join-Path $workspaceRoot "KB\FOQ Template"
New-Item -ItemType Directory -Path $mappingRoot, $templateRoot -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $projectRoot "deployment\assets\FOQResultLocations_V2.83.xls") -Destination $mappingRoot -Force
Copy-Item -LiteralPath (Join-Path $projectRoot "deployment\assets\TEMPERATURE_CALIBRATION_720.cmbx") -Destination $templateRoot -Force
Copy-Item -LiteralPath (Join-Path $projectRoot "deployment\assets\TEMP_HEAT_UP_DOWN_20_50_20.cmbx") -Destination $templateRoot -Force

Write-Host "Deploying the versioned knowledge vault..."
& $venvPython (Join-Path $projectRoot "tools\sync_kb_vault.py") deploy
if ($LASTEXITCODE -ne 0) { throw "Knowledge-vault deployment failed." }

$sharedRoot = ""
$oneDrive = $env:OneDriveCommercial
if ($oneDrive) {
    $candidate = Join-Path $oneDrive "CIC HPCS V&V-CMBX Workstation - CMBX"
    if (Test-Path -LiteralPath $candidate) { $sharedRoot = $candidate }
}
$config = @(
    "`$env:CMBX_CHROMELEON_BIN = '$($runtimeRoot.Replace("'", "''"))'",
    "`$env:CMBX_WEB_STATE_ROOT = '$($serviceRoot.Replace("'", "''"))'",
    "`$env:CMBX_WEB_HOST = '0.0.0.0'",
    "`$env:CMBX_WEB_PORT = '8765'"
)
if ($sharedRoot) {
    $config += "`$env:CMBX_WEB_SHARED_ROOT = '$($sharedRoot.Replace("'", "''"))'"
}
$config | Set-Content -LiteralPath $configPath -Encoding UTF8

$operator = if ($env:USERDOMAIN) { "$env:USERDOMAIN\$env:USERNAME" } else { $env:USERNAME }
Write-Host "Granting the server operator modify access to runtime state..."
& icacls.exe $serviceRoot /grant "${operator}:(OI)(CI)M" /T /C | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Could not grant $operator modify access to $serviceRoot." }

if (-not $SkipFirewall) {
    if (Test-Administrator) {
        & (Join-Path $projectRoot "Configure_CMBX_Web_LAN.ps1") -NoPause
    } else {
        Write-Warning "Firewall configuration needs Administrator rights. Run Configure_CMBX_Web_LAN.ps1 as Administrator before LAN use."
    }
}

& (Join-Path $projectRoot "Test_CMBX_Web_Server.ps1")
if ($LASTEXITCODE -ne 0) { throw "Server preflight failed. Review the messages above." }
Write-Host "Installation complete. Run Start_CMBX_Web_Workspace.bat." -ForegroundColor Green
