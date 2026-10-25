# Fibre-count and hydraulic-pressure optimization

Updated 25 October 2026. User constraint: allow straight fibre lengths up to 1,000 m.

## Result and its scope

The lightest sampled reference design at an **assumed 1 GPa fibre stress** uses **14 micrometre fused-silica fibres, approximately 305 m free bundle length, 350 bar charging pressure and shared cylinders**. Its modeled subtotal is **176.66 tonnes**, including glass, catalogue-estimated cylinders, cylinder-fluid inventory and a provisional latch allowance.

This is **not the lightest proven complete plant**. Foundation/anchor structures, fibre supports and protection, motors, charging pump, manifolds, piping, electrical equipment, transfer mechanism, buffer, reservoir hardware and operational reserves are not sized. The 25 kg per bundle latch allowance is an explicit scenario, not a designed or catalogued 353 kN latch. The 1 GPa cyclic bundle allowable also remains unqualified. These omissions could materially change the architecture ranking.

The major improvement is to **share actuators**, rather than install one cylinder on every charged bundle. The optimized dedicated-cylinder reference is approximately 695.6 tonnes even before holding hardware; its cylinders alone weigh approximately 509.5 tonnes. Sharing reduces the actuator count to 20, at the cost of a mechanically demanding engagement/transfer system.

## Optimization domain

- Target: at least 100 kWh delivered mechanically; ten output lanes nominally providing 10 kW each.
- Material: fused-silica model, E = 72 GPa, density 2,200 kg/m3. Investigate 0.5, 1 and 2 GPa separately; none is a qualified repeated-use limit.
- Compare 9 and 14 micrometre filaments with the same assumed stress capability. The manufacturer's dimensional options support both, but equal fatigue strength is an assumption.
- Fibre length at most 1,000 m; full charging-cylinder stroke at most 6 m. Discharge uses 90% of full extension.
- Fourteen catalogue bore/rod combinations spanning 40/28 to 320/220 mm.
- Charging pressure 200–350 bar, sampled every 1 bar; full stroke every 25 mm initially, refined to 1 mm at selected pressures. The shared reference includes refinement around the best coarse pressure and at 350 bar. This is a discrete search, not a proof of a global continuous optimum.
- Cylinder speed at most 0.5 m/s; motor pressure at least 25 bar through cutoff; demanded motor displacement at most 200 cc/rev at 1,500 rpm. These are screening limits, not a configured motor's performance guarantee.
- Shared architecture: two actuators per lane, twenty total, to allow a second actuator to prepare for handover. Each bundle must deliver at least 60 seconds of nominal 10 kW output; this is an engineering assumption to avoid unrealistic rapid switching.
- Nominal cylinder efficiency 95% each direction; motor volumetric/mechanical efficiencies 95%/90%. Residual extension 10%, leaving 1% of elastic energy.

The current [Bosch Rexroth CDH3 product page](https://www.boschrexroth.com/es/es/p/cilindro-hidraulico-r900999031/) lists a 350 bar family, 40–320 mm bores, 28–220 mm rods and strokes up to 6,000 mm. For numerical mass estimates, use the older **manufacturer RE17337/09.05 table, page 2**, [distributor-hosted PDF](https://www.cmafh.com/images/Master%20PDFs/BRH%20CYL/Rexroth%20CDH3%20CGH3%20%28350%20Bar%29%20%28ISO%203320%29%20-%20re17337_2005-09.pdf). It provides zero-stroke masses and added mass per 100 mm stroke. We use CD MP3/MP5 masses without position sensing. These are historical mass surrogates, not a current quote or verification that every diameter/stroke combination can be ordered. For the 160/110 mm case the estimate is 229 kg + 16.3 kg per 100 mm of stroke.

The motor pressure constraint is informed by the manufacturer [A6VM Series 63 sheet, hosted copy](https://hydba.com/wp-content/uploads/pdfs/ficha_tecnica_motor_de_pistones_axiales_cilindrada_variable_A6VM_Serie_63_Bosch_Rexroth.pdf). An actual selected motor still needs its speed/displacement/pressure/efficiency map checked. Higher-pressure custom systems were not optimized because no comparable validated cylinder/motor mass model was established for them. Consequently, 350 bar is the best point within this supported envelope, not a universal optimum pressure.

## Reference design at 1 GPa

| Quantity | Best sampled mass design |
|---|---:|
| Fibre diameter | 14 micrometres |
| Straight free fibre length | 304.776 m |
| Fibres per bundle | 2,290,178 |
| Total bundle count | 600; 60 per lane |
| Total individual filament lengths | 1,374,106,800 |
| Total filament length | approximately 418.8 million km |
| Solid glass area per bundle | 352.55 mm2 |
| Bundle force at full charge | 352.55 kN |
| Shared cylinders | 20; two per lane |
| Cylinder bore / rod diameter | 160 / 110 mm |
| Full charging stroke | 4.233 m |
| Useful discharge stroke | 3.8097 m |
| Peak charging pressure | approximately 350 bar |
| Discharge pressure | 315.87 → 31.59 bar |
| Maximum piston speed | 0.349 m/s |
| Maximum flow per active 10 kW path | 222.16 L/min |
| Demanded motor displacement | approximately 14.07 → 140.70 cc/rev at nominal power |
| Delivered energy per bundle | 600.010 kJ = 0.16667 kWh |
| Nominal energy-equivalent duration | 60.001 s at 10 kW |
| Installed delivered capacity | 100.00164 kWh |

Counts refer to separate full-length filaments in all bundles, not the number of actuators or separately controlled fibres. Fibres must be terminated and equalized in groups; there is no proposal to attach a separate cylinder to each filament. The assumed area corresponds to about a 21.2 mm solid circular diameter; packing and protective material make the real bundle larger.

The numerical optimum has essentially no capacity reserve. It is a sizing reference, not a defensible 100 kW / one-hour guarantee with degradation or switching losses. A production specification needs reserve and a demonstrated handover/buffer energy balance.

### Mass accounting

| Included component | Estimated mass |
|---|---:|
| Fused-silica fibres | 141.831 t |
| Twenty shared cylinders | 18.380 t |
| Cylinder fluid inventory | 1.447 t |
| Holding/engagement latch budget: 25 kg × 600 bundles | 15.000 t |
| **Modeled subtotal** | **176.657 t** |

Fluid inventory is estimated conservatively as full-bore swept volume times 850 kg/m3 across the twenty cylinders. It excludes dead volume, pipe inventory and additional reservoir fluid. Low-pressure oil returning to a tank is not separately counted a second time. No reservoir structure is included.

The sum of the individual charged-bundle force magnitudes is approximately 211.5 MN. This is not a single net force on a building; it indicates the scale of the distributed reactions that must be carried locally. No foundation mass has been inferred from this number.

## Why 1,000 m is not selected

Fibre extension is sigma L/E. At 1 GPa, a 1,000 m bundle needs **13.89 m full cylinder travel**. It exceeds the selected 6 m cylinder envelope. The longest direct-drive bundle in this envelope is 432 m. Even below that limit, length trades fewer terminations and less holding hardware against heavier, longer cylinders. The 25 kg latch scenario's mass optimum is approximately 305 m; a larger latch mass shifts the optimum toward longer bundles.

The catalogue strokes also assume tensile rod loading in a pull-cylinder arrangement: pressure on the annulus retracts the rod to stretch the fibres, and fibre contraction extends it while expelling annular-side fluid. This avoids claiming an unchecked compressively loaded long rod. Rod alignment, lateral support, sag, port flow capacity and transfer fixture strength are still unresolved.

## Minimum fibre count is a different objective

At fixed energy, stress and material, total glass volume is approximately fixed. Increasing filament diameter or length reduces the number of filament lengths but does not materially reduce glass mass. At the same length and total area, 14 micrometre fibres need about 59% fewer filaments than 9 micrometre fibres; they do not save 59% of material mass. The measured strength distribution could differ with diameter.

| Objective at 1 GPa | Lowest sampled modeled mass | Fewest sampled filaments |
|---|---:|---:|
| Bundle length | 304.776 m | 432 m |
| Peak charging pressure | 350 bar | 283 bar |
| Bundle count | 600 | 310 |
| Total filament lengths | 1.374 billion | 0.970 billion |
| Cylinder bore / rod | 160 / 110 mm | 220 / 160 mm |
| Modeled subtotal including 25 kg latch allowance | 176.66 t | 209.11 t |

The strict fewest-filament result is sensitive to discrete module and integer-fibre rounding; 283 bar is not a general recommendation. It gives about 29% fewer filament lengths but approximately 18% more modeled mass. If low mass is the priority, select the first design for further development.

## Pressure, stress and holding-hardware sensitivity

Charging and discharging pressures differ because cylinder efficiency changes the force balance:

    area_annulus = pi (bore² − rod²) / 4
    F_max <= eta_charge × p_charge × area_annulus
    p_discharge,start = eta_discharge × F_max / area_annulus
                      ≈ 0.9025 × p_charge

Thus a 350 bar charge does not produce 350 bar discharge: it produces about 315.9 bar initially. To keep the cutoff above the 25 bar screening limit with a tenfold force drop, charging pressure must be at least approximately 277 bar. Lower pressure candidates were excluded by this requirement or piston-speed limits.

At a fixed allowable fibre stress, higher pressure cannot lower the approximately 141.8 t theoretical fibre requirement for 100 kWh. It changes cylinder size, force capacity, flow and hardware count. In the dedicated-cylinder sweep, the best modeled mass decreases toward the upper pressure boundary. Raising pressure beyond the envelope requires different hardware data and cannot be extrapolated as a free improvement.

For the shared architecture at 1 GPa, increasing the per-bundle latch allowance from 25 to 100 kg shifts the sampled optimum to approximately 420.5 m bundles, 350 bundles, 180/125 mm cylinders, and **208.48 t** modeled subtotal. This is why the transfer and holding hardware must be designed before declaring a total-system optimum.

The stress study's shared-cylinder subtotals **before any latch allowance** are approximately 587.3 t at 0.5 GPa, 161.7 t at 1 GPa and 55.3 t at 2 GPa. They retain the same hydraulic assumptions. The 2 GPa case is mathematically lighter but is **not supported as a repeated-use working stress for the commercial dry rovings reviewed**. Stress cannot be raised solely to make an optimizer return less mass. See GLASS_SELECTION_AND_ITERATION.md for the evidence gap.

## Shared-actuator sequence and unresolved work

Each storage bundle has a permanently anchored end and a movable end held by a mechanical latch. A shared cylinder attaches to that movable end, takes the load, releases the latch and meters the return stroke through the hydraulic motor. The unloaded bundle is isolated and the actuator engages another bundle. Two actuators per lane provide a candidate arrangement for alternating operation; charge uses the external hydraulic supply to restore extension and re-engage the holding latch.

The design must transfer approximately 353 kN without shock, compensate alignment and avoid dragging the charged fibres through a damaging path. A carriage or engagement system must reach every bundle endpoint. Its mass, footprint, losses and time are absent from the current model. A 25 kg latch is merely an allowance to expose the tradeoff, not evidence that these operations can be achieved with that mass.

At handover, source pressures differ. Parallel connection to one lossless common pressure line is not assumed. Independent motor circuits, pressure conversion or a buffer must be modeled. The twenty shared cylinders alone do not prove continuous output. The 60-second minimum discharge and 0.25-second model ramp are scheduling assumptions, not demonstrated mechanical transfer times.

## Verification and files

The selected 350 bar design was rerun in OpenModelica. Simulated output energy is 600,009.84 J versus 600,009.85 J analytical. Maximum energy-accounting discrepancy is 0.014 J. The ideal-regulation module reaches cutoff at about 60.126 s including the ramp. Constraint checks passed for energy, travel, pressure, flow-derived speed and integer-fibre area.

This validates the reduced-order arithmetic only. Motor speed is imposed; fibre fatigue, strength scatter, relaxation, hydraulic compressibility, dynamic stability, actuator transfer and the full plant are not validated.

- `scripts/optimize_fibre_hydraulics.py`: search, catalogue-mass data and generated model.
- `models/OptimizedSilicaHydraulic.mo`: selected reference module.
- `scripts/check_optimized_silica.py`: independent checks.
- `scripts/run-optimization.ps1`: reproduces optimization and simulation.
- `results/optimization/optimization.json`: all design candidates summarized.
- `results/optimization/pressure_sweep.csv`: best dedicated-cylinder candidate at each pressure.
- `results/optimization/optimization.png`: pressure and architecture comparisons.

Recommended next work is a force-rated holding/transfer concept and measured long-bundle cyclic allowable. Those two results determine whether the shared-cylinder design remains lightest after the presently excluded hardware is counted.
