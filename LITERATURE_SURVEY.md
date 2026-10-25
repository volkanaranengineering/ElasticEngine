# ElasticEngine: initial literature survey

Research date: 24 October 2026. Scope: reversible solid elastic storage and delivery of useful mechanical work. This is a focused starting bibliography, not a systematic review or a validated engine design. Findings distinguish measured results, theoretical predictions, and our own engineering calculations.

The strongest high-specific-energy experimental lead located is twisted carbon-nanotube rope. Ordinary glass and commercial carbon fiber do not reach lithium-ion specific energy under the simple tensile calculation below. Controllable spring arrays already have experimental precedent, but integrating them with high-energy microscopic fibers remains an open engineering problem.

## The remembered Stanford paper

The older Stanford student report mentioning Gorilla Glass has **not been positively identified**. Searches covered Gorilla Glass, glass springs, elastic/mechanical energy storage, and PH240 coursework. Do not cite a guessed title or treat the remembered claim as established.

A different, verified Stanford project is [Elastic energy storage proof of concept and scalability](https://sustainability-accelerator.stanford.edu/project/elastic-energy-storage-proof-concept-and-scalability), by David Camarillo, Steve Collins, Ovijit Chaudhuri, and Gordon Avery. Its institutional summary describes screening elastomers and glass fibers, testing relaxation and fatigue, and selecting medium-stiffness polyurethane as a promising tested elastomer. It favors long horizontal tension cables. This is a cost-oriented stationary-storage investigation; the page does not establish battery-equivalent gravimetric performance or provide a completed peer-reviewed feasibility study.

## Basic quantities and fair comparison

An elastic engine comprises a charged elastic store, a holding/release mechanism, a transmission, and a load. Its running time comes from previously supplied charging work.

For uniform linear tensile loading, with stress sigma, strain epsilon, Young's modulus Y, and density rho:

    u = sigma²/(2Y) = Y epsilon²/2              [J/m³]
    e = sigma²/(2Y rho)                         [J/kg]
    e_Wh/kg = e/3600

Thus the strength-limited material selection index is sigma_allowable²/(Y rho). High stiffness alone does not imply high storage capacity. For nonlinear materials, integrate the measured stress–strain curve; for usable energy, integrate the unloading curve after the intended hold time. Do not substitute toughness-to-fracture for recoverable energy.

At the device level:

    W_return = integral(F dx + torque dtheta) along unloading
    P_shaft = torque × angular_speed
    e_system = (m_active × e_return × transmission_efficiency
                - control_energy) / m_complete_system

Use consistent energy units in the last expression. The mass denominator includes anchors, support frame, bearings, clutches, transmission, containment, and controls. Add generator/electronics/motor losses if output travels through an electrical path. Avoid counting tensile and torsional work twice when deformation is coupled.

For background on spring geometries and nonuniform stress, see Alexander Slocum's [FUNdaMENTALS of Design, Topic 7: Energy Storage—Springs](https://www-mdp.eng.cam.ac.uk/web/library/enginfo/textbooks_dvd_only/slocum/topic7.pdf). Uniform tension can exploit material more completely than bending, where some material is weakly stressed. Practical displacement and attachment requirements still matter.

## Material screening

The following values have different evidence levels; they are not interchangeable device specifications.

| Material/reference | Specific energy | Evidence and limitation |
|---|---:|---|
| Molicel P50B lithium-ion cell | 260 Wh/kg; 714 Wh/L | Manufacturer cell rating; benchmark, not a complete battery pack or motor system |
| Gorilla Glass 3, assumed 1 GPa uniform tensile stress | 0.83 Wh/kg | Our illustrative calculation; 1 GPa is an assumption, not a qualified working stress |
| AGY S-2 glass fiber | 15.5 Wh/kg | Our ideal linear estimate at listed tensile strength; excludes fatigue margin and all supporting material |
| Toray T1100G carbon fiber | 11.7 Wh/kg | Same upper-bound screening calculation at listed tensile strength; not composite or device capacity |
| TPU-modified SWCNT rope, Utsumi et al. (2024) | Up to 583 Wh/kg | Experimental microscopic rope result; not complete-system output |
| Carbon nanothread bundle, Zhan et al. (2020) | Up to 489 Wh/kg | Simulation for pure tension; not a manufactured motor/storage demonstration |

Source inputs and calculation audit:

- [Molicel P50B product page](https://www.molicel.com/product/inr-21700-p50b/): use the declared 260 Wh/kg and 714 Wh/L as a concrete baseline. A universal “three times lithium-ion” claim depends on the battery selected.
- [Corning Gorilla Glass 3 data sheet](https://www.corning.com/microsites/csm/gorillaglass/PI_Sheets/2020/Gorilla_Glass_3_ProdSheet.pdf): Y = 70 GPa and rho = 2,390 kg/m³. Extrapolating the linear formula to 260 Wh/kg requires approximately 17.7 GPa and 25% strain. That extrapolation is not a prediction of glass capability. The sheet does not establish such an operating range. Scratch resistance and hardness do not establish reversible tensile storage capacity; chemical strengthening's residual stresses cannot simply be counted as repeatedly rechargeable work.
- [AGY manufacturer brochure, distributor-hosted copy](https://texbay.us/wp-content/uploads/2025/02/S-Series_High_PerfMatlsforAutomotiveAppls-Automotive.pdf): tensile strength 4.89 GPa, Y = 86.9 GPa, rho = 2,460 kg/m³. Calculation: sigma²/(2Y rho × 3600). This is a fiber-level estimate near rupture, not a service rating.
- [Toray T1100G data sheet](https://www.toraycma.com/wp-content/uploads/T1100G-Data-Sheet.pdf): strength 7 GPa, Y = 324 GPa, rho = 1,790 kg/m³. The same calculation gives 11.7 Wh/kg. Halving allowable stress reduces this estimate to one quarter. Resin, terminations, and frame further change system performance.

Rubber/polyurethane remain useful control-prototype materials, supported by the Stanford screening project, but this survey found no basis for assigning them battery-equivalent recoverable specific energy. NiTi, aramids, UHMWPE, and other candidates require dedicated unloading, creep, and fatigue evidence before quantitative ranking. Transformation work, thermal actuation, and energy absorbed in fracture must be kept separate from passive recoverable strain energy.

## Core materials reading list

**1. Hill, Havel, and Livermore (2009).** [Modeling mechanical energy storage in springs based on carbon nanotubes](https://doi.org/10.1088/0957-4484/20/25/255704). *Nanotechnology* 20, 255704. Start here for analytical comparisons of tension, compression, bending, and torsion. The models include buckling and packing constraints and favor aligned small-diameter SWCNT bundles in tension. The paper also models a portable power source. Its high energy-density estimates are idealized predictions, not measured packaged performance.

**2. Fthenakis et al. (2013).** [Limits of mechanical energy storage and structural changes in twisted carbon nanotube ropes](https://doi.org/10.1103/PhysRevB.88.245402). *Physical Review B* 88, 245402. Atomistic calculations examine coupled deformation and the boundary between reversible storage and irreversible bonding changes. Useful for understanding why twisting a bundle is more complicated than twisting a homogeneous wire. Predicted battery-beating performance is conditional on ideal structures and loading.

**3. Zhan et al. (2020).** [High density mechanical energy storage with carbon nanothread bundle](https://doi.org/10.1038/s41467-020-15807-7). *Nature Communications* 11, 1905. Molecular dynamics and continuum modeling predict 1.76 MJ/kg under tension. Bundle size and coupled failure reduce performance. The paper discusses screw-based extension and escapement concepts, connecting materials to mechanisms. Treat nanothreads as a research alternative, with manufacturability and low-rate cycling still requiring validation.

**4. Utsumi et al. (2024).** [Giant nanomechanical energy storage capacity in twisted single-walled carbon nanotube ropes](https://doi.org/10.1038/s41565-024-01645-x). *Nature Nanotechnology* 19, 1007–1015. Reports 2.1 MJ/kg in TPU-modified ropes, approximately 583 Wh/kg. Typical rope diameters were 30–100 micrometers; measurement hook spacing was 5 mm. The paper reports 450 cycles, declining performance with length, and rate dependence. Its rotating-disc demonstration achieved 22% conversion efficiency, distinct from roughly 90% strain-energy recovery. The body also discusses relaxation losses, qualifying the abstract's retention language. Proposed pulley/textile packing is not a demonstrated battery-scale engine. Prioritize replication and mass-denominator verification before extrapolation.

**5. Background review, optional:** [Storage of Mechanical Energy Based on Carbon Nanotubes with High Energy Density and Power Density](https://doi.org/10.1002/adma.201800680), *Advanced Materials* 31, 1800680 (2019; online 2018). Useful as a bibliography map. Its flywheel figures concern kinetic storage and must not be mixed with static elastic storage. The conclusions above use primary studies and manufacturer data.

## Controlled release of many small elastic elements

Three primary references address complementary parts of this problem:

**6. Krimsky and Collins (2024).** [Elastic energy-recycling actuators for efficient robots](https://doi.org/10.1126/scirobotics.adj7246). *Science Robotics* 9, eadj7246. Demonstrates a motor with individually selectable parallel springs and paired electroadhesive clutches that preserve stored energy when disconnected. This is the strongest architectural precedent found for selectively releasing many elastic elements. It demonstrates task-specific energy recycling, not battery-like storage density or autonomous continuous rotation powered by CNT fibers.

**7. Dresscher (2016).** [Controlled passive actuation: Concepts for energy efficient actuation using mechanical storage elements and continuously variable transmissions](https://doi.org/10.3990/1.9789036541886). University of Twente doctoral thesis. Develops and experimentally investigates mechanical storage coupled to variable transmissions. Relevant to matching decreasing spring force/torque to the load while reducing dissipative regulation.

**8. Yu et al. (2016).** [Low speed control and implementation of permanent magnet synchronous motor for mechanical elastic energy storage device with simultaneous variations of inertia and torque](https://doi.org/10.1049/iet-epa.2015.0159). *IET Electric Power Applications*. Models and tests control for a spiral-spring storage unit with changing torque and inertia. Relevant to motor/generator interfacing and feedback control; it does not validate nanotube storage.

**9. Bergbreiter, Mahajan, and Pister (2009).** [A reusable micromechanical energy storage/quick release system with assembled elastomers](https://doi.org/10.1088/0960-1317/19/5/055009). *Journal of Micromechanics and Microengineering* 19, 055009. [Author-hosted paper](https://people.eecs.berkeley.edu/~pister/publications/2009/Bergbreiter%20jmm9_5_055009.pdf). Demonstrates microrubber-band storage integrated into silicon structures. Relevant to microscale assembly and latching; quick release alone does not solve sustained speed regulation.

The following are engineering deductions and candidate architectures, not demonstrated CNT-engine results:

| Architecture | Role | Main unresolved issue |
|---|---|---|
| Parallel fibers with shared end fixtures | Add force or torque at common displacement/angle | Unequal load sharing, defects, and attachment mass |
| Elements in series | Add displacement or angular travel at common load | More interfaces and alignment requirements |
| Independently latched cartridges, clutched to a shaft | Dispatch stored energy in stages | Switching losses, torque ripple, clutch mass and power |
| Variable-radius drum/cam or CVT | Match declining force to useful shaft torque | Friction, finite ratio range, contact stress |
| Generator plus controlled electrical load and motor | Decouple storage motion from final motor speed | Conversion losses and extra components |
| Escapement with small inertia buffer | Meter small packets and smooth pulsation | Wear and impact losses; poor choice for some continuous loads |

For a tensile element, shaft torque = F × effective drum radius. A shaped radius can compensate falling force over a finite stroke. It cannot produce constant nonzero torque down to zero force with a finite radius. For a simple linear elastic store, stopping at half its initial force leaves one quarter of its initial energy stored.

A candidate first architecture is a bank of short cartridges, each with a holding latch and output clutch, sharing a transmission and encoder-controlled output shaft. Engage the next cartridge before the previous one drops below useful torque, with matched speeds to limit engagement losses. A small inertia buffer can smooth switching. This trades one extremely long fiber for many attachments; whether that trade is favorable must be measured.

## Feasibility questions to answer next

1. **Reproducibility:** measure loading and unloading work directly, including torque and angle, specimen mass, rate, temperature, and uncertainty. Check whether the quoted mass includes polymer and inactive specimen ends.
2. **Retention:** measure recovered work after realistic hold times. A static clamp does not prevent internal stress relaxation.
3. **Service life:** determine repeatable working strain below failure. Track energy loss, permanent set, termination slip, and breakage over the intended duty cycle.
4. **Scale:** compare one short specimen, one longer specimen, and multiple short specimens at equal active mass. Measure end-fixture overhead explicitly.
5. **Useful output:** measure shaft torque and speed over time and subtract sensing, clutch, and controller consumption. Free rotation or return angle is not sufficient evidence of delivered energy.
6. **Complete comparison:** report net Wh/kg, Wh/L, output watts, runtime, and efficiency for the whole mechanism. Compare with a battery-plus-motor system at the same output duty, not bare battery and bare fiber selectively.

As an independent illustration, assume an active material stores 500 Wh/kg, constitutes 20% of device mass, and delivers 60% of that energy through the discharge path. The system then delivers 60 Wh/kg before control consumption. These are hypothetical assumptions, not measurements. This simple mass budget is why high material energy density alone cannot establish engine feasibility.

Recommended reading order: Slocum for basics; Hill for storage mechanics; Utsumi for experimental evidence; Krimsky–Collins for selective release; Dresscher and Yu for transmission and control. The immediate project decision is whether the target is a compact energy source, a high-power burst actuator, or cyclic energy recovery: each rewards different properties.
