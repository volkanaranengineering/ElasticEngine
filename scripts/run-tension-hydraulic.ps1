$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$config = Get-Content (Join-Path $root 'toolchain.json') -Raw | ConvertFrom-Json
$out = Join-Path $root 'results/tension_hydraulic'
New-Item -ItemType Directory -Force $out | Out-Null
Push-Location $out
try {
    $env:OPENMODELICAHOME=Join-Path $root $config.openmodelica_home
    & (Join-Path $root $config.omc) (Join-Path $PSScriptRoot 'tension_hydraulic.mos') *> simulation.log
    $success = @(Select-String -Path simulation.log -SimpleMatch -Pattern 'The simulation finished successfully.')
    if ($success.Count -ne 3) { throw 'Not all three simulations succeeded. See simulation.log.' }
} finally { Pop-Location }
& (Join-Path $root $config.python) (Join-Path $PSScriptRoot 'analyze_tension_hydraulic.py')
if ($LASTEXITCODE -ne 0) { throw 'Hydraulic result verification failed' }
