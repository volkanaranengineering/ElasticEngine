$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$config = Get-Content (Join-Path $root 'toolchain.json') -Raw | ConvertFrom-Json
$out = Join-Path $root 'results/fused_silica'
New-Item -ItemType Directory -Force $out | Out-Null
Push-Location $out
try {
    $env:OPENMODELICAHOME=Join-Path $root $config.openmodelica_home
    & (Join-Path $root $config.omc) (Join-Path $PSScriptRoot 'fused_silica.mos') *> simulation.log
    $success = @(Select-String -Path simulation.log -SimpleMatch -Pattern 'The simulation finished successfully.')
    if ($success.Count -ne 4) { throw 'Not all glass simulations succeeded; inspect simulation.log' }
} finally { Pop-Location }
& (Join-Path $root $config.python) (Join-Path $PSScriptRoot 'analyze_fused_silica.py')
if ($LASTEXITCODE -ne 0) { throw 'Glass results verification failed' }
& (Join-Path $root $config.python) (Join-Path $PSScriptRoot 'compare_glass_candidates.py')
if ($LASTEXITCODE -ne 0) { throw 'Glass comparison generation failed' }

