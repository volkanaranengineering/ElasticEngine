$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$config = Get-Content (Join-Path $root 'toolchain.json') -Raw | ConvertFrom-Json
$model = Join-Path $root 'results/validation/rod.FCStd'
if (!(Test-Path $model)) { throw 'Run scripts/run-validation.ps1 first.' }
# This launcher is explicitly for opening the model interactively.
Start-Process -FilePath (Join-Path $root $config.freecad_gui) -ArgumentList ('"' + $model + '"')
