$ErrorActionPreference = "Continue"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$serviceRoot = Join-Path $env:ProgramData "CMBX Web Service"
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
$runtime = Join-Path $serviceRoot "runtime\chromeleon"
$failures = 0

function Confirm-Item([string]$Label, [bool]$Condition, [string]$Detail) {
    if ($Condition) { Write-Host "[OK]   $Label - $Detail" -ForegroundColor Green }
    else { Write-Host "[FAIL] $Label - $Detail" -ForegroundColor Red; $script:failures++ }
}

Confirm-Item "Python environment" (Test-Path -LiteralPath $python) $python
if (Test-Path -LiteralPath $python) {
    & $python -c "import fastapi, uvicorn, httpx, multipart, openpyxl, xlrd, pyodbc; print('[OK]   Python imports')"
    if ($LASTEXITCODE -ne 0) { $failures++ }
}
Confirm-Item "Chromeleon runtime" (Test-Path -LiteralPath (Join-Path $runtime "Dionex.DataCommon.dll")) $runtime
$formulaOneFiles = @(
    "Dionex.Controls.dll",
    "Formula1SideBySideActivationContext.manifest",
    "VCFI5.sxs.manifest",
    "VCFI5.OCX",
    "CM7RE.sxs.manifest",
    "CM7RE.OCX"
)
$missingFormulaOne = @($formulaOneFiles | Where-Object { -not (Test-Path -LiteralPath (Join-Path $runtime $_)) })
Confirm-Item "FormulaOne runtime" ($missingFormulaOne.Count -eq 0) $(
    if ($missingFormulaOne.Count -eq 0) { $runtime }
    else { "missing: $($missingFormulaOne -join ', ')" }
)
Confirm-Item ".NET x86 compiler" (Test-Path -LiteralPath "C:\Windows\Microsoft.NET\Framework\v4.0.30319\csc.exe") "required for FormulaOne workbook operations"
Confirm-Item "FOQ mapping" (Test-Path -LiteralPath (Join-Path $env:ProgramData "CMBX Data Explorer Workspace\DB MAPPING\FOQResultLocations_V2.83.xls")) "ProgramData deployment"
Confirm-Item "CM 7.2 method carrier" (Test-Path -LiteralPath (Join-Path $env:ProgramData "CMBX Data Explorer Workspace\KB\FOQ Template\TEMPERATURE_CALIBRATION_720.cmbx")) "ProgramData deployment"

$writeProbe = Join-Path $serviceRoot ".write-test"
try {
    "ok" | Set-Content -LiteralPath $writeProbe -Encoding ASCII -ErrorAction Stop
    Remove-Item -LiteralPath $writeProbe -Force -ErrorAction Stop
    Confirm-Item "Server-state write access" $true $serviceRoot
} catch {
    if (Test-Path -LiteralPath $writeProbe) {
        Remove-Item -LiteralPath $writeProbe -Force -ErrorAction SilentlyContinue
    }
    Confirm-Item "Server-state write access" $false "$serviceRoot ($($_.Exception.Message))"
}

try {
    $drivers = Get-OdbcDriver -ErrorAction Stop | Where-Object { $_.Name -like "*ODBC Driver * for SQL Server*" }
    if ($drivers) { Write-Host "[OK]   SQL Server ODBC driver - $($drivers[0].Name)" -ForegroundColor Green }
    else { Write-Warning "SQL Server ODBC Driver 17/18 is not installed. Core workflows run, but database workflows need the Microsoft driver." }
} catch {
    Write-Warning "Could not enumerate ODBC drivers: $($_.Exception.Message)"
}

if ($failures -gt 0) {
    Write-Host "Preflight failed with $failures mandatory issue(s)." -ForegroundColor Red
    exit 1
}
Write-Host "Server preflight passed." -ForegroundColor Green
exit 0
