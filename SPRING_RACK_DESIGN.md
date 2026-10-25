# First spring-driven rack-and-pinion model

## Material and literature selection

Select **unidirectional S-2 glass/epoxy**, with fibres running along the leaf. This is the preferred starting material for a tractable composite-spring demonstrator, not a claim that it is the highest-energy storage material or a commercially optimized choice. Spring steel would simplify procurement and fabrication; glass/epoxy better serves this project's composite energy-storage investigation.

1. **Start here:** Muñoz-Guijosa et al. (2019), [Using FRPs in elastic regime for the storage and handling of mechanical energy and power: Application in spiral springs](https://oa.upm.es/78448/). Demonstrates glass/epoxy and carbon/epoxy spiral-spring prototypes. It supports the material class and energy-storage approach; it does not validate the cantilever/rack geometry designed here.
2. **Numerical material basis:** [Polymers 2020, 12, 2834, Table 2](https://www.mdpi.com/2073-4360/12/12/2834). Reports manufacturer-derived cured-ply properties for AGY S-2 glass/913 epoxy: longitudinal modulus 45.6 GPa, fibre volume fraction 0.49, nominal ply thickness 153.8 micrometres, tensile failure strain 3.1%. We use only the longitudinal modulus for stiffness. The failure strain is not a fatigue or compression allowable. A nominal 4 mm leaf approximates 26 such plies; the actual cured thickness must be measured.
3. **Later geometry optimization:** [Silva et al. (2024), Automated resolution of the spiral torsion spring inverse design problem](https://www.nature.com/articles/s41598-024-53404-6). Relevant when replacing this deliberately simple leaf with a compact spiral spring.

Raw glass-fibre tensile strength and modulus must not be assigned to the complete composite laminate. Density here is an explicitly assumed 1900 kg/m3, used only for the spring mass estimate. No supplier or manufactured laminate has been qualified. See LITERATURE_SURVEY.md for nanotube results and unresolved identification of the remembered Stanford Gorilla Glass report.

## Mechanism

The vertical leaf is clamped at its bottom. Pulling the rack 20 mm to the right bends the leaf and charges it. Releasing it moves the rack left, rotating a module-2, 20-tooth involute pinion clockwise. A tip pin and conceptual vertical slotted coupling accommodate tip rotation and vertical displacement. Rear guides constrain rack motion, and a bearing supports the output shaft.

The CAD shows the charged state. The leaf shape follows the small-deflection beam curve; its displayed shape is not a geometrically nonlinear equilibrium solution. Guide blocks, clamp, bearing and coupling are layout placeholders, not detailed manufactured assemblies. The model omits a charging actuator, release latch, end stop, enclosure and one-way clutch. These must be designed before physical construction. An output clutch would prevent rewind from reversing a downstream load, but would not add energy.

## Dimensions and calculations

| Quantity | Value |
|---|---:|
| Free leaf length × width × thickness | 200 × 30 × 4 mm |
| Longitudinal elastic modulus | 45.6 GPa |
| Second moment, I = bt³/12 | 160 mm4 |
| Tip stiffness, k = 3EI/L³ | 2.736 N/mm |
| Charged tip deflection | 20 mm |
| Initial force, F = kx | 54.72 N |
| Stored energy, U = kx²/2 | 0.5472 J = 0.000152 Wh |
| Nominal root bending stress, 6FL/(bt²) | 136.8 MPa |
| Nominal root strain | 0.30% |
| Pinion pitch radius | 20 mm |
| Total rotation, stroke/radius | 1 rad = 57.30 degrees |
| Initial ideal torque, Fr | 1.0944 N m |
| Initial torque with assumed 90% mesh efficiency | 0.98496 N m |
| Assumed spring-only mass | 45.6 g |
| Spring-only specific energy at this operating point | 0.00333 Wh/kg |

This leaf stores little energy because the working strain is modest and bending stress is nonuniform through both the thickness and length. The 0.30% strain is a modeling choice, not a verified safe operating limit. Even without supports, 100 kWh at this operating point would require approximately 658 million leaves, or 30 million kg of spring material. This is arithmetic extrapolation, not a feasible design. A 100 kW load would exhaust one leaf's ideal energy in 5.47 microseconds; actual deliverable power is limited by mechanism dynamics and strength.

## Simulation and checks

OpenModelica models released travel q with x = 0.020 − q and:

    (m + J/r²) q'' = eta k x − b q'
    theta = q/r
    P_load = b (q')²

Assumptions: rack/coupler translating mass 0.15 kg; rotating inertia 0.0002 kg m²; equivalent viscous load b = 120 N s/m; forward mesh efficiency eta = 0.90. These are explicit design assumptions. The viscous load is a brake/dynamometer surrogate, not an electrical generator model. It slows the release without active speed regulation. Under this overdamped load, the rack approaches its unloaded position monotonically. The efficiency law applies to this forward discharge only; do not reuse it unchanged for charging or reversed motion.

Energy accounting includes spring energy, translation and rotation kinetic energy, viscous load energy and mesh loss. The simulation gives 13.75 W peak viscous-load power, 161.6 rpm peak speed and 0.49248 J delivered to the test load by 0.6 seconds. These are a short transient under the stated assumptions, not a continuous power rating. Maximum energy-accounting error is 3.42e-8 J. The reproducible checker verifies conservation, nonnegative extension/velocity, and beam convergence. CalculiX longitudinal effective-beam results under 54.72 N are 19.96737 mm for 20 elements and 19.99262 mm for 40 elements, versus the analytical 20 mm. This checks linear stiffness, not composite damage. The Poisson ratio 0.3 is assumed for the effective beam implementation; no complete orthotropic laminate model is claimed.

The rack uses 20-degree straight flanks and the pinion uses FreeCAD's involute profile. Tooth thickness includes a 0.10 mm rack allowance. CAD intersection tests at 21 positions over the stroke found zero tooth overlap. This verifies sampled clearance only; tooth contact, backlash take-up, root strength, friction and bearing reactions are not solved. The lumped dynamic model assumes continuously engaged gears.

Remaining mechanical uncertainties include geometric nonlinearity at displacement/length = 0.1, compression and interlaminar strength, clamp concentrations, fatigue, creep, environment and laminate quality. Neither lithium-ion-comparable storage nor 100 kW / 100 kWh feasibility is established by this model.

## Files and reproduction

- `results/rack_motor/spring_rack_motor.FCStd`: native CAD, separated parts.
- `results/rack_motor/spring_rack_motor.step`: exchange CAD.
- `models/RackMotor.mo`: editable dynamic model.
- `scripts/build_rack_motor.py`: parameterized geometry-generation source and FE input generation. Change geometry in the script and regenerate; this is not a fully constrained GUI assembly.
- `results/rack_motor/overview.png`: CAD projection and discharge plots.
- `results/rack_motor/summary.json`: computed results and verification metrics.
- `results/rack_motor/RackMotor_res.csv`: time histories.

From the project directory run `./scripts/run-rack-motor.ps1` with the installed toolchain. No further downloads are required. Open the FCStd in FreeCAD and use Fit All. For the next iteration, first characterize a real laminate coupon and refine the tip coupling, then add a latch and controllable load. Multiple staged cartridges or a longer rack would extend output duration; a transmission cannot increase stored energy.
