param(
    [string]$Version = "0.2.0"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
$Dist = Join-Path $ProjectRoot "dist"
$Stage = Join-Path $Dist "GameCrashAgent-$Version"
$Archive = Join-Path $Dist "GameCrashAgent-$Version-win.zip"

$ProjectRootFull = [IO.Path]::GetFullPath($ProjectRoot).TrimEnd('\')
$StageFull = [IO.Path]::GetFullPath($Stage)
if (-not $StageFull.StartsWith($ProjectRootFull + '\', [StringComparison]::OrdinalIgnoreCase)) {
    throw "Refusing to package outside the project directory: $StageFull"
}

if (Test-Path $Stage) { Remove-Item -LiteralPath $Stage -Recurse -Force }
if (Test-Path $Archive) { Remove-Item -LiteralPath $Archive -Force }
New-Item -ItemType Directory -Force -Path $Stage | Out-Null

$Files = @(
    "gamecrashagent",
    "scripts\run.ps1",
    "main.py",
    "config.json",
    "README.md",
    "PRIVACY.md",
    "SECURITY.md",
    "SUPPORT.md",
    "CHANGELOG.md",
    "LICENSE"
)

foreach ($Relative in $Files) {
    $Source = Join-Path $ProjectRoot $Relative
    $Destination = Join-Path $Stage $Relative
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Destination) | Out-Null
    Copy-Item -LiteralPath $Source -Destination $Destination -Recurse -Force
}

Get-ChildItem -LiteralPath $Stage -Recurse -Directory -Filter "__pycache__" |
    Remove-Item -Recurse -Force
Get-ChildItem -LiteralPath $Stage -Recurse -File -Filter "*.pyc" |
    Remove-Item -Force

Compress-Archive -LiteralPath $Stage -DestinationPath $Archive -CompressionLevel Optimal
Write-Host "Created $Archive"
