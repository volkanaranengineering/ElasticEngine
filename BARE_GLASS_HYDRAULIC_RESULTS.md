# Bare glass fibres tensioned by hydraulic cylinders

## What changed

The store is now aligned **bare S-2 glass fibres**, without an epoxy matrix. Hydraulic cylinders stretch the bundles during charging and are back-driven by fibre contraction during discharge. Keep the previous variable-displacement hydraulic motor architecture and assumed efficiencies, so the material change can be assessed directly.

The earlier 45.6 GPa modulus and 1,900 kg/m3 density described a composite laminate. They are replaced by **86.9 GPa and 2,460 kg/m3** for the glass itself. AGY's [S-Series manufacturer brochure, distributor-hosted copy](https://texbay.us/wp-content/uploads/2025/02/S-Series_High_PerfMatlsforAutomotiveAppls-Automotive.pdf) lists these values and a 4.89 GPa tensile strength at room temperature. AGY's [401 product information](https://texbay.us/wp-content/uploads/2025/02/401_S-2-Industrial.pdf) explicitly describes its mechanical table as average properties of a bare single filament; its modulus is slightly different at 89 GPa. We consistently use 86.9 GPa from the former brochure rather than mixing the two.

The 4.89 GPa strength is **not** a safe allowable for a long, anchored, repeatedly charged bundle. The following 0.5, 1 and 2 GPa cases are assumed working-stress scenarios, not qualified designs. The baseline at 0.30% strain is retained to distinguish material replacement from increased working stress. Perfect fibre load sharing, linear elasticity and complete elastic recovery before hydraulic losses are assumed. Sizing, protective coatings, packing voids and termination masses are excluded.

## Recomputed results

All four cases were simulated in OpenModelica, retaining independent analytical checks of stored energy, cutoff extension, discharge duration and energy conservation.

| Assumed peak stress | Peak strain | Gross fibre energy | Delivered specific energy | Minimum glass mass for 100 kWh |
|---|---:|---:|---:|---:|
| 0.2607 GPa: previous 0.30% strain | 0.300% | 0.04416 Wh/kg | 0.03551 Wh/kg | 2,816.3 tonnes |
| 0.5 GPa | 0.575% | 0.1624 Wh/kg | 0.1306 Wh/kg | 765.6 tonnes |
| 1.0 GPa | 1.151% | 0.6497 Wh/kg | 0.5224 Wh/kg | 191.4 tonnes |
| 2.0 GPa | 2.301% | 2.5988 Wh/kg | 2.0898 Wh/kg | 47.85 tonnes |

Minimum masses above use continuous energy sizing, before rounding into modules. They exclude cylinders, motors, anchors, frames, valves, pipes, tanks, supports, controls and buffers. At the unchanged strain, bare glass improves specific energy by only about 1.47 times versus the prior composite; the much larger gains in the higher-stress cases come from raising stress. They are not an automatic consequence of removing resin.

The calculation is:

    strain = stress / E
    gross specific energy [Wh/kg] = stress² / (2 E rho × 3600)
    eta = 0.95 cylinder × 0.95 motor volumetric × 0.90 motor mechanical
        = 0.81225
    usable fraction of gross energy = eta × (1 − 0.1²) = 0.8041275
    required fibre mass [kg] = 100,000 Wh / delivered specific energy

Ten percent residual extension is retained to avoid zero-force discharge, leaving one percent of initial elastic energy. Efficiencies are assumed constants, not hardware measurements. Strand friction, glass relaxation and damage are not included.

## Illustrative 1 GPa module

Retain a 100 m free length and 5,000 mm2 of actual glass cross-section per bundle. This is distributed among many fine fibres, not a 100 m monolithic glass bar. The equivalent solid circular diameter is 79.8 mm; an actual packed bundle is larger. A 100 m length supplies useful stroke but does not improve specific energy.

| Quantity | Result |
|---|---:|
| Fibre mass | 1,230 kg |
| Initial extension | 1.151 m |
| Useful cylinder travel | 1.036 m |
| Initial fibre/anchor force | 5.0 MN |
| Initial stored energy | 0.7991 kWh |
| Delivered shaft energy | 0.6426 kWh |
| Nominal shaft power | 10 kW |
| Cutoff time, including 0.25 s startup ramp | 231.46 s |
| Discharge pressure | 250 → 25 bar differential |
| Effective cylinder area | 0.190 m2 |
| Equivalent full-bore diameter | 491.85 mm |
| Nominal motor speed | 1,500 rpm, imposed |
| Motor displacement during nominal power delivery | approximately 17.8 → 177.8 cc/rev |
| Motor inlet flow during nominal power delivery | approximately 28.1 → 280.7 L/min |
| Shaft torque at 10 kW | 63.66 N m |

The cylinder bore is recomputed for each stress scenario to retain the same 250 bar initial discharge pressure. Keeping the old cylinder while increasing fibre stress would instead increase pressure. A rod-side actuator requires a larger geometric bore than this full-bore equivalent. Structural design and buckling of the rod are not checked.

Charging requires an external pump to move the cylinder against fibre tension. With the chosen 0.190 m2 effective area, 5 MN requires 263.2 bar even without charging friction; assuming 95% charging-cylinder efficiency raises it to approximately 277 bar. These are sizing calculations, not a complete charge-cycle simulation. A cylinder rated only for the 250 bar discharge point is not established as sufficient. Holding valves or mechanical locks must retain charge; their leakage and losses are unmodeled.

Arrange 10 independent 10 kW output lanes, each with 16 modules for the 1 GPa scenario:

- 160 modules total.
- 196.8 tonnes of glass, after equal-lane module rounding.
- 102.82 kWh calculated delivered capacity.
- Ideal energy-equivalent duration of approximately 1.028 hours at 100 kW.

This inventory has energy capacity for the target. It does **not** demonstrate uninterrupted 100 kW: module switching, startup deficits, pressure matching and buffer state must be modeled before making that guarantee. Unequal-pressure bundles cannot simply feed a common line without matching or conversion. Ten isolated motor circuits can combine output mechanically or electrically, with further losses accounted for.

## Other module scenarios

| Scenario | Initial force per bundle | Useful stroke | Equivalent cylinder bore | Modules rounded to ten lanes | Installed glass mass |
|---|---:|---:|---:|---:|---:|
| Previous 0.30% strain | 1.3035 MN | 0.270 m | 251.1 mm | 2,290 | 2,816.7 tonnes |
| 0.5 GPa | 2.5 MN | 0.518 m | 347.8 mm | 630 | 774.9 tonnes |
| 1 GPa | 5 MN | 1.036 m | 491.8 mm | 160 | 196.8 tonnes |
| 2 GPa | 10 MN | 2.071 m | 695.6 mm | 40 | 49.2 tonnes |

The upper scenario reduces fibre mass but substantially raises per-module force and travel. Dividing each bundle among more cylinders can reduce individual actuator forces; it cannot remove the total force, energy or material requirements.

## Evidence limits and next design decision

The maximum numerical energy-balance error across the runs is 0.179 J, below 0.000006% of each case's initial energy. The model reproduces the analytical energy and duration within the scripted tolerances. Power regulation remains ideal: speed is imposed, displacement changes instantly, and no fluid compressibility, inertia, valve dynamics or motor efficiency map is included. The stop event is instantaneous. The simulation demonstrates the consequences of assumptions, not a qualified motor or storage unit.

The critical missing evidence is now **recoverable working stress of the complete long fibre bundle and its terminations**. A ratio between listed single-filament ultimate strength and assumed working stress is not a demonstrated safety factor. Breakage distribution, equalization, surface damage, handling, environmental exposure, hold duration and repeated cycling must be characterized. Counting the listed tensile strength as a repetitive operating point would give an unsupported capacity estimate.

Recommended next gate: qualify a small, protected bundle and its actual termination at the target stress, record its force–extension loading/unloading loop after holding, and use the measured recoverable energy and residual strength to select between these scenarios. The 1 GPa case is a useful model reference, not a recommendation to operate an unqualified bundle at that stress.

## Files and reproduction

The previous composite simulations are preserved. `models/BareGlassHydraulic.mo` extends the existing hydraulic equations with glass properties and a peak-stress parameter. Run `./scripts/run-bare-glass.ps1` to rerun four scenarios and their checks. Results, CSV histories and the plot are in `results/bare_glass/`; the calculation and plotting source is `scripts/analyze_bare_glass.py`. No new software was downloaded.
