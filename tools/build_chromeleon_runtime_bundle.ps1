param(
    [string]$SourceBin = "C:\Program Files (x86)\Thermo\Chromeleon\bin",
    [string]$OutputDirectory = ""
)

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
if (-not $OutputDirectory) {
    $OutputDirectory = Join-Path $projectRoot "deployment\runtime"
}
$source = (Resolve-Path -LiteralPath $SourceBin).Path
$output = [IO.Path]::GetFullPath($OutputDirectory)
$stage = Join-Path $env:TEMP "cmbx_chromeleon_runtime_bundle"
$zipPath = Join-Path $output "chromeleon-runtime.zip"
$manifestPath = Join-Path $output "RUNTIME_MANIFEST.json"

New-Item -ItemType Directory -Path $output -Force | Out-Null
if (Test-Path -LiteralPath $stage) {
    Remove-Item -LiteralPath $stage -Recurse -Force
}
New-Item -ItemType Directory -Path $stage | Out-Null

$seeds = @(
    "Dionex.DataCommon.dll",
    "Dionex.RawData.dll",
    "Dionex.RawDataInterfaces.dll",
    "Dionex.Chromeleon.Common.dll",
    "Dionex.Controls.dll",
    "Dionex.CmLzmaImplementationx86.dll",
    "Dionex.CmLzmaImplementationx64.dll",
    "Dionex.InstrumentServerInterfaces.dll",
    "Dionex.Serialization.dll"
)
$nativeSideBySideFiles = @(
    "Formula1SideBySideActivationContext.manifest",
    "VCFI5.sxs.manifest",
    "VCFI5.OCX",
    "CM7RE.sxs.manifest",
    "CM7RE.OCX"
)
$queue = [Collections.Generic.Queue[string]]::new()
$seen = [Collections.Generic.HashSet[string]]::new([StringComparer]::OrdinalIgnoreCase)
$seeds | ForEach-Object { $queue.Enqueue($_) }

while ($queue.Count -gt 0) {
    $name = $queue.Dequeue()
    if (-not $seen.Add($name)) { continue }
    $path = Join-Path $source $name
    if (-not (Test-Path -LiteralPath $path)) { continue }
    try {
        [Reflection.Assembly]::ReflectionOnlyLoadFrom($path).GetReferencedAssemblies() | ForEach-Object {
            $candidate = "$($_.Name).dll"
            if (Test-Path -LiteralPath (Join-Path $source $candidate)) {
                $queue.Enqueue($candidate)
            }
        }
    } catch {
        Write-Warning "Could not inspect ${name}: $($_.Exception.Message)"
    }
}

$nativeSideBySideFiles | ForEach-Object {
    if (-not (Test-Path -LiteralPath (Join-Path $source $_))) {
        throw "Required FormulaOne side-by-side runtime file is missing: $_"
    }
    $seen.Add($_) | Out-Null
}

$files = @()
foreach ($name in ($seen | Sort-Object)) {
    $sourceFile = Join-Path $source $name
    if (-not (Test-Path -LiteralPath $sourceFile)) { continue }
    Copy-Item -LiteralPath $sourceFile -Destination (Join-Path $stage $name)
    $item = Get-Item -LiteralPath $sourceFile
    $files += [ordered]@{
        name = $name
        size = $item.Length
        sha256 = (Get-FileHash -LiteralPath $sourceFile -Algorithm SHA256).Hash.ToLowerInvariant()
        file_version = $item.VersionInfo.FileVersion
        product_version = $item.VersionInfo.ProductVersion
    }
}

$manifest = [ordered]@{
    schema = 1
    created_utc = (Get-Date).ToUniversalTime().ToString("o")
    source = $source
    purpose = "Approved internal Chromeleon runtime closure for CMBX reading and FormulaOne operations"
    redistribution = "Internal Thermo Fisher use only; do not publish as a standalone public runtime"
    seeds = $seeds
    native_side_by_side_files = $nativeSideBySideFiles
    file_count = $files.Count
    files = $files
}
$json = $manifest | ConvertTo-Json -Depth 5
$json | Set-Content -LiteralPath (Join-Path $stage "RUNTIME_MANIFEST.json") -Encoding UTF8
$json | Set-Content -LiteralPath $manifestPath -Encoding UTF8
if (Test-Path -LiteralPath $zipPath) { Remove-Item -LiteralPath $zipPath -Force }
Compress-Archive -Path (Join-Path $stage "*") -DestinationPath $zipPath -CompressionLevel Optimal
Remove-Item -LiteralPath $stage -Recurse -Force

Write-Host "Chromeleon runtime bundle created: $zipPath"
Write-Host "DLL count: $($files.Count)"
