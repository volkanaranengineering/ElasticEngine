$ErrorActionPreference='Stop'
$root=Split-Path $PSScriptRoot -Parent
$config=Get-Content (Join-Path $root 'toolchain.json') -Raw | ConvertFrom-Json
$out=Join-Path $root 'results/carbon_torsion'
New-Item -ItemType Directory -Force $out | Out-Null
Push-Location $out
try {
    $env:OPENMODELICAHOME=Join-Path $root $config.openmodelica_home
    & (Join-Path $root $config.omc) (Join-Path $PSScriptRoot 'carbon_torsion.mos') *> simulation.log
    if (@(Select-String -Path simulation.log -Pattern 'The simulation finished successfully.' -SimpleMatch).Count -ne 3) { throw 'Carbon simulations failed; inspect simulation.log' }
} finally { Pop-Location }
& (Join-Path $root $config.python) (Join-Path $PSScriptRoot 'analyze_carbon_torsion.py')
if ($LASTEXITCODE -ne 0) { throw 'Carbon analysis checks failed' }
