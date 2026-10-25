$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$config = Get-Content (Join-Path $root 'toolchain.json') -Raw | ConvertFrom-Json
function Resolve-Tool([string]$relative) { Join-Path $root $relative }
& (Resolve-Tool $config.freecad_cmd) (Join-Path $PSScriptRoot 'validate_cad.py')
if ($LASTEXITCODE -ne 0) { throw 'CAD generation failed' }
Push-Location (Join-Path $root 'results/validation')
try {
    $gmsh = Start-Process -FilePath (Resolve-Tool $config.gmsh) -ArgumentList 'rod.step -3 -clmax 5 -format msh2 -o rod.msh -v 3' -WindowStyle Hidden -PassThru -Wait -RedirectStandardOutput gmsh.stdout.log -RedirectStandardError gmsh.stderr.log
    if ($gmsh.ExitCode -ne 0 -or !(Test-Path rod.msh)) { throw 'Gmsh failed' }
    foreach ($mesh in 1,2) {
        & (Resolve-Tool $config.calculix) "axial_$mesh" *> "axial_$mesh.log"
        if ($LASTEXITCODE -ne 0) { throw "CalculiX mesh $mesh failed" }
    }
} finally { Pop-Location }
New-Item -ItemType Directory -Force (Join-Path $root 'results/modelica') | Out-Null
Push-Location (Join-Path $root 'results/modelica')
try {
    $env:OPENMODELICAHOME = Resolve-Tool $config.openmodelica_home
    & (Resolve-Tool $config.omc) (Join-Path $PSScriptRoot 'validate_modelica.mos') *> 'simulation.log'
    if ($LASTEXITCODE -ne 0) { throw 'OpenModelica failed' }
    if (!(Select-String -Path 'simulation.log' -SimpleMatch 'The simulation finished successfully.' -Quiet)) {
        throw 'OpenModelica did not report a successful simulation; inspect results/modelica/simulation.log'
    }
} finally { Pop-Location }
& (Resolve-Tool $config.python) (Join-Path $PSScriptRoot 'check_results.py')
if ($LASTEXITCODE -ne 0) { throw 'Validation failed' }
