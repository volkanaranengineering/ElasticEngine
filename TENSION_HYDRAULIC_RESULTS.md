# Tension-bundle hydraulic storage: model and results

## Finding

Uniform tension improves material utilization, but this S-2 glass/epoxy baseline still requires approximately **4,152 tonnes of composite for 100 kWh delivered** with the assumed hydraulic efficiencies. A fixed-pressure manifold with simple throttling raises that estimate to **8,208 tonnes**. Neither value includes machinery, anchors, supports, reservoirs or transient buffers.

The variable-displacement architecture is the preferable one of the three modeled cases for further investigation. It requires a wide motor operating range and isolated pressure circuits, or pressure-matched switching. The previously proposed common pressure line is not intrinsically lossless: unequal-pressure bundles need matching, conversion or throttling.

These are actual OpenModelica simulations of a reduced-order energy/flow model, checked against independent analytical integrals. Constant speed and ideal regulation are imposed boundary conditions, not demonstrated controller performance. This is not a complete hydraulic transient, fatigue, structural or plant simulation.

## Module definition

| Parameter | Model input/result |
|---|---:|
| Material | Longitudinal UD S-2 glass/epoxy |
| Elastic modulus | 45.6 GPa |
| Assumed density | 1,900 kg/m3 |
| Free bundle length | 100 m |
| Total composite area | 5,000 mm2 |
| Initial strain / nominal stress | 0.30% / 136.8 MPa |
| Initial extension | 300 mm |
| Bundle stiffness | 2,280,000 N/m |
| Initial bundle force | 684 kN |
| Composite mass per module | 950 kg |
| Initial stored energy | 102.6 kJ = 28.5 Wh |
| Effective cylinder area | 25,992 mm2 |
| Equivalent full-bore cylinder diameter | 181.9 mm |
| Initial differential pressure | 250 bar |
| Prescribed motor speed | 1,500 rpm |
| Nominal shaft output per active lane | 10 kW |

The area is total load-bearing composite, not the gross area of a loosely packed cable. Uniform strain and equal bundle load sharing are assumed. An actual rod-side cylinder needs a larger bore to provide the same effective area. Anchors, gripping length, piston rods and cylinder strength have not been sized. The 100 m length creates useful cylinder travel without increasing specific energy; coiling or routing it introduces bending and friction not modeled here.

Material stiffness is taken from [Polymers 2020, 12, 2834, Table 2](https://www.mdpi.com/2073-4360/12/12/2834), which reports manufacturer-derived cured-ply properties. Density, working strain and hydraulic efficiencies are assumptions. The nominal working strain is not a qualified fatigue limit. Cylinder and motor relationships follow ordinary pressure/flow/torque balances; see Bosch Rexroth's [Hydraulics in Mobile Working Machines, section 2.3](https://www.boschrexroth.com.cn/xrm-cn/media/global/training_1/digital_media/reference_books/hydraulik-in-mobilen-arbeitsmaschinen-en.pdf). No commercial motor has been selected or shown to operate across the calculated envelope.

## Equations and assumptions

For remaining extension x, bundle area A, length L and effective cylinder area Ac:

    k = E A / L
    F = k x
    U = k x² / 2
    p_source = eta_c F / Ac
    Q = Ac (-dx/dt)
    P_shaft = eta_v eta_m p_motor Q
    D = eta_v Q / n
    torque = P_shaft / (2 pi n)

Assumed cylinder efficiency eta_c = 0.95, motor volumetric efficiency eta_v = 0.95, and motor mechanical efficiency eta_m = 0.90 give a combined 0.81225. These constant efficiencies are optimistic placeholders across the full pressure/displacement range. Line loss, standby leakage, motor displacement limits, compressibility, actuator inertia, shaft inertia, valve dynamics, cavitation, storage relaxation and auxiliaries are omitted. Net pressures are above return pressure; the ideal return is zero gauge.

Each case starts with a prescribed 0.25-second ramp in flow/power command. The motor is already at a prescribed 1,500 rpm boundary: the ramp does not simulate spinning it up from rest. Flow stops at the residual-extension cutoff with an ideal isolation valve. That abrupt cutoff is a mathematical event, not a physically designed shutdown.

The model integrates output energy, cylinder loss, throttling loss and motor loss separately and checks their sum with remaining spring energy against 102.6 kJ. The largest observed balance discrepancy is 0.053 J, approximately 0.000052% of initial energy. Independent checks also verify discharge energy, cutoff extension and event time for each case. Numerical agreement validates bookkeeping within the model, not the physical assumptions.

## Three configurations compared

| Result per module | Variable displacement motor | Fixed displacement motor | Fixed-pressure header |
|---|---:|---:|---:|
| Motor pressure during discharge | 250 → 25 bar | 250 → 25 bar | 125 bar |
| Output behavior after startup ramp | 10 kW until cutoff | Falls toward 1 kW | 10 kW until cutoff |
| End of discharge, including ramp | 8.375 s | 15.126 s | 4.292 s |
| Delivered shaft energy | 82.503 kJ | 82.503 kJ | 41.668 kJ |
| Remaining spring energy | 1.026 kJ | 1.026 kJ | 25.650 kJ |
| Cylinder loss | 5.079 kJ | 5.079 kJ | 3.8475 kJ |
| Throttle loss | 0 | 0 | 24.3675 kJ |
| Motor loss | 13.992 kJ | 13.992 kJ | 7.0666 kJ |
| Peak inlet flow | 280.7 L/min | 28.07 L/min | 56.14 L/min |
| Peak demanded displacement | 177.78 cc/rev | 17.78 cc/rev | 35.56 cc/rev |

**Variable motor:** useful stroke is 270 mm, ending at 30 mm remaining extension. During nominal 10 kW operation, required displacement changes approximately from 17.8 to 177.8 cc/rev, and flow from 28.1 to 280.7 L/min. The startup ramp initially demands displacement below that nominal range, including zero at time zero. Maximum piston speed is 0.180 m/s; output torque is 63.66 N m. Constant power is possible in the equations because displacement is commanded without lag or limits. A real motor's minimum displacement, efficiency map and control response may prevent this behavior.

**Fixed motor:** after the ideal startup ramp, displacement is fixed at 17.78 cc/rev and inlet flow at 28.07 L/min. Pressure and torque decline, so output falls toward 1 kW before isolation. It recovers approximately the same energy under the assumed constant efficiencies, but ten such lanes do not maintain 100 kW. More simultaneous modules, variable gearing or electrical aggregation would be needed.

**Fixed header:** a reducing valve maintains 125 bar until source pressure reaches that value, leaving half the original extension and one quarter of the original spring energy. The useful stroke is 150 mm. Pressure above 125 bar becomes throttle heat. For a single fixed header at fraction alpha of initial pressure, the ideal shaft-energy fraction is eta_total × 2 alpha (1 − alpha); alpha = 0.5 maximizes it. Thus 125 bar is the best energy point for this simple one-stage throttling scheme, not an arbitrarily poor choice. Multiple pressure stages or pressure transformers could improve recovery but are outside these three cases.

## Scaling to 100 kW / 100 kWh

For the variable-motor concept, define ten 10 kW lanes. Use isolated lane pressure circuits and mechanically combine their outputs, or electrically combine generator outputs with separately accounted electrical losses. Stagger module switching and use a buffer; do not directly connect unequal source pressures to one lossless common line.

| Quantity | Variable motor | Fixed pressure header |
|---|---:|---:|
| Modules per lane, energy sizing | 437 | 864 |
| Total modules across 10 lanes | 4,370 | 8,640 |
| Calculated delivered capacity | 100.150 kWh | 100.004 kWh |
| Composite-only mass | 4,151.5 tonnes | 8,208 tonnes |
| Composite-only specific delivered energy | 0.024124 Wh/kg | 0.012184 Wh/kg |

Counts are rounded for ten equal lanes and sized for energy only. They exclude operational reserve and do not prove one-hour constant output. In particular, each isolated module has a startup ramp and an abrupt cutoff: sequentially concatenating these curves produces power dips. Overlapping modules, controllable load sharing and an explicitly modeled buffer are required to guarantee 100 kW. A 0.25-second linear startup ramp in one 10 kW lane has a 1.25 kJ output-energy deficit relative to an immediate 10 kW step; this gives a first buffer/load-sharing requirement, before other transients.

At 100 kW steady shaft output, the variable-motor efficiency assumption implies about **23.1 kW of losses** while actively discharging, excluding additional equipment losses. Electrical output is not included. The installed variable-motor bundle inventory contains about 124.545 kWh initially and 2,185 m3 of solid composite. These are material quantities, not site volume or plant mass.

The fixed motor has the same energy-only module count as the variable motor under the simplifying efficiencies, but no corresponding 100 kW dispatch design is claimed.

## Why the improvement remains insufficient

For uniform axial tension, specific energy is E epsilon²/(2 rho). For the original rectangular end-loaded cantilever at the same maximum strain, it is E epsilon²/(18 rho). Hence the theoretical geometry benefit is **ninefold**, before losses. The new gross specific energy is 0.03 Wh/kg, versus 0.003333 Wh/kg for the leaf. Hydraulic assumptions then reduce usable energy to 0.024124 Wh/kg.

The previous estimate of roughly 3,700 tonnes assumed the same 90% efficiency as the rack concept. Explicit cylinder and motor efficiencies now give 81.225%, increasing the estimate to roughly 4,152 tonnes. This is a refinement of the loss assumption, not a contradiction of the ninefold geometry factor.

The result supports tension rather than bending for material utilization, but it does not establish practical 100 kWh feasibility. The next useful investigation is measured cyclic tensile energy and relaxation of candidate bundles, followed by a realistic motor efficiency/displacement map and pressure-matched switching model. More hydraulic complexity cannot remove the material energy-density limit.

## Files and reproduction

- `models/TensionHydraulic.mo`: three-mode equation model.
- `scripts/tension_hydraulic.mos`: OpenModelica simulation commands.
- `scripts/analyze_tension_hydraulic.py`: independent checks, sizing and plots.
- `scripts/run-tension-hydraulic.ps1`: complete reproduction with installed tools.
- `results/tension_hydraulic/summary.json`: computed metrics.
- `results/tension_hydraulic/*_res.csv`: solver time histories.
- `results/tension_hydraulic/module_results.png`: discharge curves.
- `results/tension_hydraulic/system_comparison.png`: mass and energy comparison.

Run `./scripts/run-tension-hydraulic.ps1` from the project directory. No additional software or downloads are required.
