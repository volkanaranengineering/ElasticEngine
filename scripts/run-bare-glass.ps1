$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$config = Get-Content (Join-Path $root 'toolchain.json') -Raw | ConvertFrom-Json
$out = Join-Path $root 'results/bare_glass'
New-Item -ItemType Directory -Force $out | Out-Null
Push-Location $out
try {
    $env:OPENMODELICAHOME=Join-Path $root $config.openmodelica_home
    & (Join-Path $root $config.omc) (Join-Path $PSScriptRoot 'bare_glass.mos') *> simulation.log
    $success = @(Select-String -Path simulation.log -SimpleMatch -Pattern 'The simulation finished successfully.')
    if ($success.Count -ne 4) { throw 'Not all glass simulations succeeded; inspect simulation.log' }
} finally { Pop-Location }
& (Join-Path $root $config.python) (Join-Path $PSScriptRoot 'analyze_bare_glass.py')
if ($LASTEXITCODE -ne 0) { throw 'Glass results verification failed' }
