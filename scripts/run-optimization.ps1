$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$config=Get-Content (Join-Path $root 'toolchain.json') -Raw | ConvertFrom-Json
& (Join-Path $root $config.python) (Join-Path $PSScriptRoot 'optimize_fibre_hydraulics.py')
if ($LASTEXITCODE -ne 0) { throw 'Optimization failed' }
Push-Location (Join-Path $root 'results/optimization')
try {
    $env:OPENMODELICAHOME=Join-Path $root $config.openmodelica_home
    & (Join-Path $root $config.omc) (Join-Path $PSScriptRoot 'optimized_silica.mos') *> simulation.log
    if (!(Select-String -Path simulation.log -Pattern 'The simulation finished successfully.' -SimpleMatch -Quiet)) { throw 'Simulation failed' }
} finally { Pop-Location }
& (Join-Path $root $config.python) (Join-Path $PSScriptRoot 'check_optimized_silica.py')
if ($LASTEXITCODE -ne 0) { throw 'Verification failed' }
