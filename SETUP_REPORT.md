# Setup report — 24 October 2026

The approved CAD/CAE stack is installed and its initial scripted validation passed.

| Component | Verified version | Deployment |
|---|---|---|
| FreeCAD | 1.1.4 | Official portable Windows distribution under tools/ |
| CalculiX | 2.22 | Bundled with FreeCAD |
| Gmsh | 4.15.0 | Bundled with FreeCAD |
| Python | 3.11.14 | Bundled with FreeCAD |
| OpenModelica | 1.27.1, 64-bit | Official installer targeting tools/OpenModelica |
| Modelica Standard Library | 4.1.0 | Successfully loaded; installer cache expanded into the user library directory |

The FreeCAD archive matched its official SHA-256. OpenModelica matched its published MD5 and Windows reported a valid Authenticode signature. A local SHA-256 is recorded for repeatability. See tools-downloads.json for source URLs and hashes.

## Passed checks

- FreeCAD Python automation generated rod.FCStd and rod.step. Calculated volume: 9,999.999999999998 mm³; expected: 10,000 mm³.
- Gmsh generated rod.msh from the exported STEP geometry.
- CalculiX axial benchmarks on 10- and 80-element structured meshes both returned 21,000 N at the precision printed by the solver; expected: 21,000 N. Linear stored energy inferred from reaction/displacement: 1.05 J.
- OpenModelica compiled and simulated SpringDischarge for 20 seconds. Initial energy: 5 J. Energy dissipated in the test load: 4.999999059180183 J. Maximum energy-balance residual: 9.359977690692745e-7 J, below the 1e-5 J acceptance threshold.

Detailed numerical results: results/validation_report.json. Reproduction: scripts/run-validation.ps1. Instructions: README.md.

## Operational notes and remaining scope

Executable paths are explicit in toolchain.json; project scripts do not require global PATH configuration. FreeCAD stores normal per-user preferences, and OpenModelica stores standard libraries under the user's AppData/Roaming/.openmodelica/libraries directory. Restricted sandbox execution caused configuration/temporary-file failures and blocked OpenModelica's MSYS compiler runtime; the complete successful run used approved execution outside that sandbox.

The tool folders and downloads are inside the OneDrive-backed workspace. They are excluded from Git, but Git exclusions do not exclude OneDrive synchronization.

This validates the installation and basic scripted workflows. It does not validate torsional rope physics, fatigue, nonlinear contact, a controlled spring-bank engine, or the 100 kW / 100 kWh target. The discharge check uses a damping load, not a generator, and the axial benchmark deliberately has a simple uniform analytical solution.
