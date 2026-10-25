# ElasticEngine toolchain selection

Date: 2026-10-24. Status: approved, installed, and initial toolchain checks passed. See SETUP_REPORT.md for verified versions and scope. Further tools still require user approval.

## Selection

Use FreeCAD for scripted parametric geometry and human-readable CAD files; its bundled Gmsh/CalculiX components for initial meshing and structural analysis; OpenModelica for spring-bank, drivetrain, and control simulation.

Selection criteria: scriptable operation, inspectable model inputs, batch parameter sweeps, numerical output extraction, Windows deployment, and a GUI for the user's review. These are architectural recommendations, not locally verified compatibility results.

Local inspection found no matching tools on PATH, in the queried uninstall registry entries, or in common application folders. This does not rule out portable copies elsewhere. Python commands on PATH point to WindowsApps aliases, not a confirmed usable interpreter. Hardware queries were unavailable; no hardware capacity conclusion was drawn.

## Proposed deployment after approval

1. Download an official stable Windows FreeCAD distribution, preferring a portable package if supplied. Extract into a project-local tools directory where practical. Inspect included FreeCADCmd, CalculiX, and Gmsh executables before adding any separate dependency.
2. Download the official stable OpenModelica Windows distribution, including required compiler and Modelica Standard Library dependencies. Use a per-user location if supported. Keep project scripts tied to explicit executable paths.
3. Record versions, source URLs, and file hashes. Avoid global PATH changes. Ask again before introducing an additional tool outside this scope.
4. Run validation models before using results for feasibility claims.

## First validation models

- Scripted CAD: generate a parameterized straight rod; save FCStd and STEP; verify dimensions and volume against an analytical result.
- Structural: impose axial displacement; compare reaction force and strain energy with EA*displacement/L and EA*displacement^2/(2L). Refine mesh and verify convergence. Explicitly document units.
- Torsion: compare a simple shaft with GJ*angle/L before attempting nonlinear ropes or spiral springs.
- System: simulate a spring driving inertia and a load; verify energy accounting, then introduce gearing, friction, clutches, and controlled release. Export numerical histories.
- Coupling: transfer calculated/measured torque-angle curves to the system model. This is sequential model transfer initially, not live co-simulation.

Deliverables: model-generation scripts, input files, numerical outputs, plots, CAD files, run instructions, and a validation report. CNT-rope material laws require experimental calibration; a generic elastic solid model does not reproduce nanotube bundle physics automatically.

## Alternatives considered

- CadQuery: strong script-first geometry option, but adds a Python/OpenCASCADE dependency environment. Defer because FreeCAD supplies an editable GUI model plus the initial FEM workflow.
- PrePoMax: useful CalculiX GUI for manual analysis setup/review; defer because our initial workflow can use solver input files directly.
- FEBio: add if hyperelastic/viscoelastic materials become central and the initial solver workflow is insufficient. MIT source and separately licensed distributed binaries need to be distinguished.
- Project Chrono: defer until detailed 3D flexible multibody motion is needed; OpenModelica is the smaller conceptual starting point for drivetrain energy accounting.

## Official references

- [FreeCAD Python and parametric features](https://www.freecad.org/features.php)
- [FreeCAD headless documentation](https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/Headless_FreeCAD.md)
- [FreeCAD FEM setup and bundled Windows components](https://freecad.github.io/Website/news/getting-started-with-fem/)
- [CalculiX solver and distributions](https://www.dhondt.de/)
- [OpenModelica scripting](https://git.openmodelica.org/Documentation/OpenModelica.Scripting.html)
- [OpenModelica simulation command](https://git.openmodelica.org/Documentation/OpenModelica.Scripting.simulate.html)
- [OpenModelica Windows downloads](https://openmodelica.org/download/download-windows/)
- [CadQuery installation](https://cadquery.readthedocs.io/en/stable/installation.html)
- [PrePoMax features](https://prepomax.fs.um.si/features/)
- [FEBio licensing](https://febio.org/)
- [Chrono overview](https://projectchrono.org/faq/)
