# ElasticEngine

Research and reproducible modeling for solid elastic energy storage and controlled mechanical release.

- [Literature survey](LITERATURE_SURVEY.md): evidence, materials, and release mechanisms.
- [Toolchain plan](TOOLCHAIN_PLAN.md): selection and intended validation sequence.
- [Executable paths](toolchain.json): project-relative tools; no PATH setup needed by project scripts.
- [Download provenance](tools-downloads.json): official sources and verified checksums.

## Reproduce the setup checks

From this project directory, run in PowerShell:

```powershell
./scripts/run-validation.ps1
```

The script uses the Python runtime bundled with FreeCAD. Tools may need normal user access to their configuration directories; running them inside a restricted sandbox can prevent initialization. OpenModelica may fetch its standard library on first use.

Generated files are placed in `results/` and excluded from Git. Tool binaries and downloaded installers are in `tools/`, also excluded from Git. Both directories remain inside this OneDrive-backed workspace and may be synchronized by OneDrive.

## Validation scope

1. FreeCAD creates a 100 × 10 × 10 mm rod and checks volume against 10,000 mm³. Outputs: `results/validation/rod.FCStd` and `rod.step`.
2. Gmsh meshes the exported STEP file. This separately verifies the CAD-to-mesh interface; the analytical axial benchmark uses structured meshes generated directly by the script.
3. CalculiX solves axial extension of the rod on two structured meshes (10 and 80 C3D8 elements). With E = 210,000 MPa, Poisson ratio 0.3, and imposed extension 0.1 mm, expected reaction is 21,000 N and stored energy is 1.05 J. The energy here is derived from half the final reaction times displacement for this linear test.
4. OpenModelica checks loading of the Modelica Standard Library and simulates a spring/inertia/damping system. Initial energy is 5 J. The check verifies total energy accounting over 20 seconds and more than 4.99 J transferred into the damping load. This load dissipates energy; it is not an electrical generator-efficiency demonstration.

The final machine-readable checks are saved to `results/validation_report.json`. This is toolchain validation, not validation of a CNT material law, a complete engine, a 100 kW output, or a 100 kWh store. Torsion, nonlinear contact, calibrated material behavior, and drivetrain design remain later analysis steps.

To open the generated CAD model interactively:

```powershell
./scripts/open-cad.ps1
```

## Modeling rules

- Structural input decks use mm, N, and MPa. N·mm converts to joules by dividing by 1,000.
- The Modelica model uses SI units (radians, seconds, N·m, kg·m², joules).
- Record material source, working strain, loading rate, hold time, and unloading behavior for every feasibility model.
- Report complete-system mass and net delivered energy separately from material-level energy density.
- Obtain user approval before downloading or installing additional tools beyond the approved stack.
