$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$config = Get-Content (Join-Path $root 'toolchain.json') -Raw | ConvertFrom-Json
& (Join-Path $root $config.freecad_cmd) (Join-Path $PSScriptRoot 'build_rack_motor.py')
if ($LASTEXITCODE -ne 0) { throw 'CAD generation failed' }
Push-Location (Join-Path $root 'results/rack_motor')
try {
    foreach ($n in 20,40) {
        & (Join-Path $root $config.calculix) "leaf_$n" *> "leaf_$n.log"
        if ($LASTEXITCODE -ne 0) { throw 'FE solve failed' }
    }
    $env:OPENMODELICAHOME=Join-Path $root $config.openmodelica_home
    & (Join-Path $root $config.omc) (Join-Path $PSScriptRoot 'rack_motor.mos') *> simulation.log
    if (!(Select-String simulation.log -SimpleMatch 'The simulation finished successfully.' -Quiet)) { throw 'Simulation failed' }
} finally { Pop-Location }
& (Join-Path $root $config.python) (Join-Path $PSScriptRoot 'plot_rack_motor.py')
if ($LASTEXITCODE -ne 0) { throw 'Result checks failed' }
