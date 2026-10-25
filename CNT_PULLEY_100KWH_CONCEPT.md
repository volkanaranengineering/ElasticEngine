# CNT pulley battery: 100 kWh / 100 kW mechanical-output concept

Date: 25 October 2026. Status: research concept with a reproducible analytical energy model. This is not a dimensioned or validated machine.

## Paper used and evidence boundary

Utsumi et al., **Giant nanomechanical energy storage capacity in twisted single-walled carbon nanotube ropes**, Nature Nanotechnology 19, 1007–1015 (2024), [DOI and full text](https://www.nature.com/articles/s41565-024-01645-x).

The paper reports up to 2.1 MJ/kg in TPU-modified SWCNT ropes. Its work measurement includes axial and rotational contributions. Figure 6 proposes compact composite-pulley and stitched arrangements. The experimental hook spacing is 5 mm; longer samples lose specific capacity. Reported strain-energy recovery reaches about 90%, whereas the rotating-disc demonstration reaches about 22% conversion. These are different measurements. The paper supports the material and packing concept, not the plant below.

## 1. Functional specification

Deliver **100 kW at a mechanical output shaft for 3,600 seconds**, totaling 100 kWh. The output-speed target is 1,000 rpm, requiring approximately 955 N m total shaft torque. Electrical generation would add generator/converter losses and mass. The plant starts fully charged immediately before the modeled one-hour discharge; a longer storage interval is not included.

Use ten independently controlled 10 kW lanes. Each lane contains twenty replaceable cartridges, giving 200 cartridges overall. A cartridge delivers 0.5 kWh over 180 seconds. Each lane contributes 95.5 N m at the specified shaft speed. The identical cartridge capacities are sized for the final discharge slot, which has the longest idle time.

## 2. Architecture derived from Figure 6

Each cartridge contains many short, thin, twistable rope segments organized into repeated pulley/guide cells. Shared guide structures and terminations are the proposed route to avoiding a bearing and gear for every microscopic segment. The paper's compact routing concept is retained, but independent subcells and cartridge-level selection are design extensions.

The collector must permit rope twist and axial displacement. A candidate arrangement uses a rotating collector on an axially translating carriage: rotary work passes to a shaft, while carriage work is returned through a reversible linear-to-rotary transmission. Its detailed kinematics must be fitted to measured force, torque, length and twist data; a fixed helical pitch cannot be assumed to collect both contributions efficiently throughout the cycle.

Opposed cell banks may balance some collector reactions. They do not eliminate local loads or the mass of grips and supports. Pulley diameter, bend radius, bearing friction and rope/sliding contact are unresolved. Long ropes cannot simply be folded into a box while retaining the specimen capacity.

Each cartridge has a static holding latch, isolating clutch and monitored collector. The selected cartridge feeds a lane-level variable-ratio transmission; ten lane outputs combine on the common shaft. A load controller commands clutch engagement and ratio based on shaft speed and torque. The next cartridge is engaged during a controlled overlap. Recharge reverses the mechanical path and restores each cartridge to its commanded twist/extension state.

This is a functional mechanical architecture, not a claim that a lightweight transmission with the required range exists. The energy model prescribes output and ideal switching; it does not solve motor control, shaft dynamics or torque-sharing.

## 3. Assumptions

| Parameter | Optimistic laboratory-density case | Reference design target | Low-conversion sensitivity |
|---|---:|---:|---:|
| Effective loading-work density | 583.33 Wh/kg | 142.92 Wh/kg | 142.92 Wh/kg |
| Rope unloading recovery | 90% | 90% | Included in combined factor |
| Collection efficiency | 95% | 85% | Included in combined factor |
| Final mechanical transmission efficiency | 97% | 95% | Included in combined factor |
| Combined discharge efficiency | 82.935% | 72.675% | 22% |
| Inventory retained after 1 h idle | 99% | 95% | 95% |
| Final reserve / no-load remaining inventory | 10% | 10% | 10% |

Reference material density is 2.1 MJ/kg multiplied by 0.5 for scale retention and by 0.7 squared for a reduced operating twist. Quadratic twist scaling is a surrogate, not a validated constitutive law or fatigue allowance. The reference assumptions are not a statistical forecast.

The 22% case uses the disc-demonstration number only as a sensitivity to poor useful conversion. It is not a direct scale-up of the apparatus or evidence of a continuous-power plant efficiency. No separate 90% rope factor is applied in that case, avoiding double counting.

## 4. Energy model

Define r as one-hour idle retention, lambda = -ln(r)/3600, eta as combined discharge efficiency, P = 10,000 W per lane, d = 180 s and n = 20 cartridges per lane. Inventory is expressed as loading-work-equivalent energy. For each cartridge:

    dE/dt = -lambda E - P/eta  during its discharge slot
    dE/dt = -lambda E          otherwise

With reserve fraction b = 0.10, initial energy per identical cartridge is:

    E0 = P/(eta lambda) × [exp(lambda d)-1]
         × exp(lambda (n-1)d)/(1-b)

Active material mass is 200 E0/e_material. The latest cartridge finishes at b times its no-load inventory; earlier cartridges retain more energy because they are sized identically. Initial inventory equals delivered output plus conversion losses, relaxation losses and remaining inventory.

## 5. Calculated results

| Result | Optimistic | Reference | Low-conversion sensitivity |
|---|---:|---:|---:|
| Active rope mass | 231.93 kg | **1,124.63 kg** | 3,715.11 kg |
| Active rope per cartridge | 1.160 kg | **5.623 kg** | 18.576 kg |
| Initial inventory | 135.293 kWh | **160.728 kWh** | 530.951 kWh |
| Shaft energy delivered | 100 kWh | **100 kWh** | 100 kWh |
| Conversion loss | 20.576 kWh | **37.599 kWh** | 354.545 kWh |
| Relaxation loss during schedule | 0.749 kWh | **4.567 kWh** | 15.087 kWh |
| Remaining inventory | 13.968 kWh | **18.562 kWh** | 61.319 kWh |

The reference cartridge initially stores 0.8036 kWh. The plant releases approximately 42.17 kWh as modeled conversion/relaxation losses during the hour, averaging 42.17 kW of heat. That requires a substantial thermal-management design; no cooling mass is included.

These results establish an energy budget under assumptions. They do not establish manufacturable rope length, number of cells, package volume, attainable torque, transmission ratio or cycle life. High specimen-specific power does not independently demonstrate that its mechanism can deliver 100 kW under regulation.

## 6. Total-mass budget, not a mass prediction

If active rope constitutes 50% of total plant mass, the reference system has a **2,249 kg mass budget** and delivers **44.46 Wh/kg**. The other 1,125 kg must accommodate every termination, guide, collector, clutch, transmission, frame, enclosure, buffer and cooling component. This is a target to test, not a calculated hardware mass.

Under the same mass-fraction assumption, the optimistic case gives 464 kg and 215.58 Wh/kg; the low-conversion case gives 7,430 kg and 13.46 Wh/kg. The optimistic case is conditional on retaining laboratory material performance with no twist reduction.

As a manufacturing sensitivity, assuming 10 micrograms of active material per independent cell implies approximately 112 billion cells in the reference plant. This cell mass is illustrative, not inferred from the specimens. One microgram of hardware per cell would add about 112 kg, while 1 mg per cell would add about 112,000 kg. Shared collection must therefore be demonstrated before claiming a lightweight plant. Simple scale-up with individual miniature bearings is not supported by this budget.

## 7. Handover buffer

A 0.2-second interruption at 100 kW requires 20 kJ usable buffer energy, or 5.56 Wh. An optional high-speed flywheel is a compatible mechanical buffer. For an illustrative speed range of 6,000 to 5,400 rpm:

    usable energy = 0.5 I (omega_high² - omega_low²)
    required inertia ≈ 0.533 kg m²

An ideal thin ring at 0.25 m radius would have approximately 8.53 kg rotor mass. This excludes bearings, shaft, enclosure, containment and speed-conversion hardware, and does not constitute a stress-qualified rotor design. At 6,000 rpm it stores about 105 kJ in total, not just its 20 kJ usable window. Additional capacity is required for conversion losses. Buffer dynamics are not included in the energy model.

The hour-long plant schedule currently accounts for 100 kWh delivered through ideal switching. A real buffer's losses must be added before final storage sizing; it is not an extra source of energy.

## 8. Development gates

First reproduce coupled axial and torsional work recovery on a short specimen, including grip mass. Then build a multi-cell pulley/collector coupon and measure work in/out, friction, relaxation and unequal load sharing. Demonstrate that the assembly improves delivered Wh/kg as cell count increases.

Next develop a small cartridge with controlled shaft output, instrumented bearings and measured heat rejection. Obtain torque-angle-length trajectories to size the ratio range and control bandwidth. Only then progress toward the 0.5 kWh / 10 kW cartridge, followed by a full twenty-cartridge lane. A 100 kWh assembly is justified only after material retention and complete-cartridge mass targets are demonstrated.

The high-risk assumptions are simultaneous retention of energy density, low collection friction, high active mass fraction and repeated-cycle durability. No source presently establishes those together at the proposed scale.

## 9. Reproducibility and artifacts

Run the existing bundled Python with `scripts/cnt_pulley_concept.py`. No new software installation or download is needed. This is a closed-form analytical model evaluated at one-second intervals, not a new OpenModelica dynamic simulation.

- `results/cnt_pulley_concept/summary.json`: scenario results.
- `results/cnt_pulley_concept/reference.csv` and companion CSVs: time histories.
- `results/cnt_pulley_concept/energy_schedule.png`: calculated trajectories.
- `results/cnt_pulley_concept/architecture.svg`: functional schematic; not CAD.

Checks confirm positive cartridge inventories, the specified latest-slot reserve, and 360 MJ output. Independently integrating the relaxation rate agrees with the closed-form inventory accounting within 0.03 J across the three cases. This checks the arithmetic, not the material or mechanism assumptions.
