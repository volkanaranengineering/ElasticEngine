$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$config=Get-Content (Join-Path $root 'toolchain.json') -Raw | ConvertFrom-Json
$out=Join-Path $root 'results/carbon_hydraulic'
New-Item -ItemType Directory -Force $out | Out-Null
Push-Location $out
try {
    $env:OPENMODELICAHOME=Join-Path $root $config.openmodelica_home
    & (Join-Path $root $config.omc) (Join-Path $PSScriptRoot 'carbon_hydraulic.mos') *> simulation.log
    if (@(Select-String -Path simulation.log -Pattern 'The simulation finished successfully.' -SimpleMatch).Count -ne 4) { throw 'Hydraulic simulations failed; inspect simulation.log' }
} finally { Pop-Location }
& (Join-Path $root $config.python) (Join-Path $PSScriptRoot 'analyze_carbon_hydraulic.py')
if ($LASTEXITCODE -ne 0) { throw 'Hydraulic analysis failed' }
