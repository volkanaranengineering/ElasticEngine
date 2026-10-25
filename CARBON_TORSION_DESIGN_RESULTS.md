# Carbon torsional storage: theoretical 100 kW / 100 kWh study

Date: 25 October 2026. Status: literature-informed energy-flow model, not a validated machine design.

## Recommendation and boundary

Develop short, independently isolated, TPU-modified single-walled carbon nanotube (SWCNT) rope cells, mechanically grouped into cartridges. Sequential cartridges feed reversible variable-speed motor/generators and converters connected to a common DC bus. This is the preferred research architecture in this study, not proof of a global efficiency optimum or a commercially buildable plant.

The evaluated duty is **100 kW DC output for one hour**. Earlier glass calculations used mechanical shaft output. To obtain 100 kW shaft output through an additional drive with an assumed 95% efficiency, scale this model's power, energy and active mass by 1/0.95; the reference active mass becomes approximately 1.141 tonnes. That drive and its mass are not included here.

## Literature basis

[Utsumi et al., Nature Nanotechnology (2024)](https://www.nature.com/articles/s41565-024-01645-x) report TPU-modified SWCNT ropes storing up to 2.1 MJ/kg (583 Wh/kg). Their energy calculation includes axial and rotational work. The reported approximately 90% strain-energy recovery differs from the approximately 22% conversion in their rotating-disc demonstration. The test gauge is millimetric; the paper also reports length dependence and stress relaxation. These results support a candidate material, not a 100 kWh machine rating.

An [atomistic study by Zhan et al. (2020)](https://www.nature.com/articles/s41467-020-15807-7) reports still higher individual-CNT energy limits, including 6.81 MJ/kg. Such molecular limits are unsuitable as qualified bundle design allowables. We therefore use the experimental 2.1 MJ/kg reference and explicitly reduce it in scenarios.

## Architecture

1. Each short cell has a fixed termination, a rotating termination and an axial accommodation mechanism. Both torque and axial force must do useful work, or the uncollected component must be deducted.
2. Many cells form a cartridge with shared terminations and torque collection where feasible. A coupled axial-to-rotary mechanism is a research requirement; its geometry and efficiency have not been established.
3. Ten parallel conversion lanes each deliver 10 kW. Each lane selects twenty cartridges in sequence, three minutes per cartridge: 200 cartridges total, each delivering 0.5 kWh.
4. Each lane uses a variable-speed reversible machine and electrical converter. Electrical aggregation permits changing shaft speed as the rope unloads. Charge reverses the power path. Static latches hold inactive cartridges without continuous holding power.
5. Practical handovers require overlapping releases or a DC buffer. The present model assumes instantaneous lossless switching; it does not size that buffer, clutches or latches.

This removes hydraulic conversion from the proposed carbon architecture. Whether it is actually more efficient depends on achievable mechanical collection losses. A 1,000 m site length does not justify a 1,000 m torsion rope: short cells preserve the experimental basis more closely. Long layouts could house repeated modules.

## Assumptions

All values below are scenario assumptions rather than measured plant performance. The quadratic twist scaling is a surrogate, not a validated constitutive law or fatigue margin.

| Parameter | Optimistic laboratory-density case | Reference | Scale-up stress test |
|---|---:|---:|---:|
| Retained material energy density after scaling | 100% | 50% | 10% |
| Operating twist / laboratory twist | 100% | 70% | 50% |
| Effective loading-energy density, Wh/kg | 583.33 | 142.92 | 14.58 |
| Rope unloading recovery | 90% | 90% | 80% |
| Axial/torsional collection and transmission | 97% | 90% | 75% |
| Motor/generator efficiency | 97% | 95% | 90% |
| Electrical converter efficiency | 99% | 98% | 95% |
| Energy remaining after 1 h idle | 99% | 95% | 80% |
| End reserve relative to no-load remaining energy | 10% | 10% | 10% |

These cases vary several assumptions together; they are not a statistical confidence interval. The optimistic case has no reduction of laboratory twist and is not a service-life design.

## Model and calculation

Let s be the scale retention, q the twist fraction, and e_lab = 2.1 MJ/kg. Effective loading-energy density is e = e_lab s q^2. With idle retention r, lambda = -ln(r)/3600. During a cartridge's active interval,

    dE/dt = -lambda E - P/eta
    eta = eta_rope eta_collection eta_generator eta_converter

Outside its active interval only relaxation remains. P = 10,000 W per lane, interval d = 180 s, n = 20 cartridges per lane. Equal cartridge capacity is sized for the final slot:

    E0 = (P / (eta lambda)) (exp(lambda d)-1)
         exp(lambda (n-1)d) / (1-reserve)
    total active mass = 200 E0 / e

E is loading-work-equivalent inventory; the separate rope recovery factor accounts for unloading loss. Charge-path efficiency is eta_collection eta_generator eta_converter, with no second application of rope unloading loss. Refill input equals (initial inventory - final inventory)/charge efficiency. The round-trip estimate neglects relaxation during charging, auxiliaries and switching. It is optimistic on those points. It is a refill-cycle estimate from the retained residual state, not output divided by the first charge from empty.

## OpenModelica results

| Result | Optimistic | Reference | Stress test |
|---|---:|---:|---:|
| Active rope mass | 229.44 kg | 1,083.83 kg | 18,461.75 kg |
| Active mass per cartridge | 1.147 kg | 5.419 kg | 92.309 kg |
| Initial energy inventory | 133.84 kWh | 154.90 kWh | 269.23 kWh |
| DC energy delivered | 100.00 kWh | 100.00 kWh | 100.00 kWh |
| Discharge conversion loss | 19.28 kWh | 32.61 kWh | 94.93 kWh |
| Relaxation during discharge schedule | 0.74 kWh | 4.40 kWh | 33.63 kWh |
| Remaining inventory | 13.82 kWh | 17.89 kWh | 40.67 kWh |
| Electrical input for first charge from empty | 143.69 kWh | 184.86 kWh | 419.86 kWh |
| Electrical refill input | 128.85 kWh | 163.51 kWh | 356.43 kWh |
| Modeled refill-cycle efficiency | 77.61% | 61.16% | 28.06% |
| Delivered energy / active rope mass | 435.84 Wh/kg | 92.27 Wh/kg | 5.42 Wh/kg |

Reference discharge releases approximately 37.01 kWh as modeled losses over the hour, averaging 37.01 kW. This thermal load needs a cooling design. Its initial inventory is 557.63 MJ; cartridge isolation and containment require a structural analysis.

The reference active mass is approximately 131 times smaller than the earlier 141.83-tonne active-glass result. This is only a comparison of assumed active material requirements at slightly different output boundaries. It is not a plant mass comparison or an experimentally established advantage.

## What dominates feasibility

The missing mechanism mass is potentially decisive. As an illustrative sensitivity, if each independent cell contains 10 micrograms of active rope, the reference plant needs approximately 108 billion cells. One microgram of attachment/mechanism mass per cell adds 108 kg; ten micrograms adds 1,084 kg; one milligram adds approximately 108,383 kg. These cell masses are illustrative, not dimensions inferred from the paper. Shared fabrication and collective torque extraction would be essential.

Neither torque versus angle nor force versus axial travel has been fitted here. Consequently there is no defensible shaft speed, bearing size, gear ratio, cylinder size, cartridge volume or total plant mass yet. Imposing 100 kW in an energy-balance simulation establishes inventory sufficiency under the assumptions; it does not demonstrate stable power regulation or adequate mechanical power capability.

The highest-value next experiment is a short-cell cartridge with measured input/output work in BOTH degrees of freedom. Measure recoverable Wh/kg including all grips and mechanisms, retention, torque-speed envelope, cycle degradation and thermal losses. Those measurements should replace the assumed collection factor and energy derating before creating detailed CAD or claiming an optimal plant.

## Reproduction and verification

Run `./scripts/run-carbon-torsion.ps1` from the project directory using the existing toolchain. Model: `models/CarbonTorsionPlant.mo`; simulation commands: `scripts/carbon_torsion.mos`; analysis: `scripts/analyze_carbon_torsion.py`.

All three one-hour OpenModelica simulations completed successfully. Independent analytical end-energy checks passed for all twenty cartridge positions in each scenario. Delivered energy agreed with 360 MJ within 5 J; reserves stayed above their required bounds. Maximum numerical energy-accounting residual across all cases was approximately 0.0000021 J. This verifies the implemented equations, not the physical assumptions.

Machine-readable results and raw time series are in `results/carbon_torsion/`; the overview figure is `carbon_results.png`.
