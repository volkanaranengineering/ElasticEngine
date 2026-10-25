# Glass selection for hydraulic tensile energy storage

Research and simulation update: 24 October 2026.

## Selection

**Select protected, high-purity fused-silica continuous fibres as the next R&D candidate**, using Astroquartz's published modulus and density for the numerical model. Astroquartz II/III and Quartzel are concrete commercial material families to investigate. These are amorphous silica glass, despite the quartz trade names. Keep S-2 glass as the comparison material.

This is a selection for investigation, not a finding that commercial silica rovings are already the best qualified storage medium. No reviewed source establishes a repeated-use allowable for our 100 m anchored bundle, one-hour storage duty and required cycle life. The winning material ultimately maximizes **sigma_allowable² / (E rho)** using measured recoverable bundle performance. Highest filament strength or highest stiffness alone is not sufficient.

For the unreinforced fibre design, retain protective sizing/coatings and a dry protected enclosure as development options; “no epoxy matrix” does not mean that deliberately unprotected surfaces are desirable. Protection, packaging and terminations add mass. Their durability benefit must be measured rather than assumed.

## Evidence comparison

| Candidate | Useful evidence | Decision |
|---|---|---|
| High-purity fused silica: Astroquartz, Quartzel | Manufacturer filament, strand and dry-roving data; independent pristine-fibre fracture research | Leading energy-density candidate, subject to bundle qualification |
| S-2 glass | Strong commercial reference, already modeled; listed filament strength 4.89 GPa | Retain as benchmark; may win if its practical bundle allowable is sufficiently higher |
| E-glass | Lower published filament strength; accessible reference properties | Useful comparison, not selected from strength-limited screening |
| High-modulus S-3 UHM | AGY advertises 99 GPa modulus | Stiffness is not the storage objective; insufficient evidence here to displace silica or S-2 |
| Pristine silica nanowires | Experimental strengths above 10 GPa | Research frontier, not a demonstrated long load-bearing storage bundle |
| Silica tested in cryogenic/inert conditions | Very high measured fracture stresses | Exclude from room-temperature plant sizing |

### Manufacturer data and the distinction that changes this design

1. **JPS, Astroquartz technical handbook:** [manufacturer PDF](https://jpscm.com/wp-content/uploads/2025/06/JPS-Technical-Handbook-PDFs.pdf). Lists E = 72 GPa, rho = 2,200 kg/m3, 6 GPa virgin single-filament tensile strength, and 3.6 GPa for an **impregnated strand** on 20-end roving. Those two strengths describe different specimens; neither is a fatigue allowable for a dry 100 m bundle. The [current product page](https://jpscm.com/products/astroquartz/) describes continuous roving and 9/14 micrometre product families. These data support selecting a commercial fused-silica family, not assigning 6 GPa to the complete engine.

2. **Saint-Gobain, Quartzel roving sheet, February 2025:** [manufacturer PDF](https://www.advanced-ceramic-composites.saint-gobain.com/fr/files/2146/view). Provides dry-roving breaking forces and linear densities. For example, 400 tex with 22 daN corresponds approximately to 1.21 GPa using glass density 2,200 kg/m3; 1,600 tex with 48 daN corresponds to 0.66 GPa. Across the six listed constructions the estimate is 0.66–1.21 GPa. Conversion uses area = linear mass/density and treats nominal tex as glass mass; sizing and twist make it approximate. These are typical breaking values, not guaranteed minima or cyclic limits. Consequently **a 2 GPa service target is not supported for these off-the-shelf dry rovings**, and 1 GPa is near or above some listed breaking values. A [current yarn sheet](https://www.advanced-ceramic-composites.saint-gobain.com/fr/files/2141/view) also lists a 72 GPa modulus; older quartz datasheets sometimes use 78 GPa. We do not mix the modulus from one grade with the strength of another to claim a validated product.

3. **AGY:** [S-Series manufacturer brochure, distributor-hosted copy](https://texbay.us/wp-content/uploads/2025/02/S-Series_High_PerfMatlsforAutomotiveAppls-Automotive.pdf). Supplies E-glass and S-2 properties used for the like-for-like filament screening below. [S-3 UHM manufacturer catalogue, hosted copy](https://pdf.directindustry.com/pdf/agy/s-3-uhm-high-performance-fibers/50640-559249.html) emphasizes 99 GPa stiffness. That alone does not establish greater elastic storage.

### Independent research and durability

4. **Tokmakov et al. (2012), A study of the fracture mechanisms in pristine silica fibres utilising high speed imaging techniques.** [University record and abstract](https://pureportal.strath.ac.uk/en/publications/a-study-of-the-fracture-mechanisms-in-pristine-silica-fibres-util/), DOI 10.1016/j.jnoncrysol.2012.05.005. Carefully prepared Suprasil fibres reached 5–6 GPa; some weaker failures occurred at their ends. This supports silica's strength potential and the importance of fabrication/attachment, but not repetitive 100 m cable operation.

5. **Brambilla and Payne (2009), The ultimate strength of glass silica nanowires.** [Primary-paper abstract](https://pubmed.ncbi.nlm.nih.gov/19170550/), DOI 10.1021/nl803581r. Reports strength above 10 GPa, increasing as diameter decreases, with brittle rupture. No corresponding hydraulic bundle or 100 kWh cyclic storage system is demonstrated. We do not extrapolate this result through the present linear spring model at extreme strains.

6. **Tang et al. (2015), Using the two-point bend technique to determine failure stress of pristine glass fibers.** [University record](https://scholarsmine.mst.edu/matsci_eng_facwork/2373/), DOI 10.1016/j.jnoncrysol.2015.08.005. Distinguishes ambient and 77 K results and uses nonlinear modulus corrections for high-strain failure estimates. Two-point bending fracture stresses are not interchangeable with uniform room-temperature bundle tension or cyclic service ratings.

7. **Glaesemann et al., Corning WP1282 (issued May 2007), Mechanical Reliability of Corning Optical Fiber in Small Bend Scenarios.** [Manufacturer research paper](https://www.corning.com/content/dam/corning/media/worldwide/global/documents/sfiber%20WP1282_Mech%20Reliability%20of%20Corning%20Opt%20Fibers%20in%20Small%20Bend%20Scenarios.pdf). Discusses length-dependent strength distributions and moisture-assisted subcritical crack growth. Its optical-fibre bending application differs from our tensile store; it supports a reliability-testing requirement, not a numerical allowable borrowed into this model.

## Screening metric: why silica, and why the result is conditional

For ideal linear uniaxial tension:

    e_gross = sigma² / (2 E rho)
    e_delivered = e_gross × 0.81225 × 0.99

The factors retain the previous assumed cylinder and motor efficiencies and 10% residual extension. Estimated energy at listed filament rupture is a screening number only:

| Glass | E | Density | Listed filament strength | Linear rupture-energy screening estimate |
|---|---:|---:|---:|---:|
| E-glass | 72.3 GPa | 2,580 kg/m3 | 3.445 GPa | 8.84 Wh/kg |
| S-2 glass | 86.9 GPa | 2,460 kg/m3 | 4.89 GPa | 15.54 Wh/kg |
| Astroquartz fused silica | 72 GPa | 2,200 kg/m3 | 6.0 GPa | 31.57 Wh/kg |

These are **not recoverable service-energy ratings**. Near rupture, nonlinear elasticity, strength statistics and irreversible failure invalidate treating the linear estimate as a rechargeable battery capacity. In particular, the 31.57 Wh/kg figure is not used to size the plant.

At equal working stress, fused silica has 35% greater modeled specific energy, or about 26% less required fibre mass, than S-2. It must retain at least 86.1% of S-2's actual allowable working stress to preserve that advantage. If handling, moisture, terminations or dry-bundle load sharing reduce silica's allowable farther, S-2 wins.

At equal **strain**, the ranking reverses slightly: E/rho is smaller for fused silica. At the earlier 0.30% strain, minimum glass mass rises from 2,816 tonnes for S-2 to 3,040 tonnes for silica. Therefore simply changing glass without changing the validated stress/strain envelope does not guarantee an improvement.

## Rerun of the hydraulic model

`FusedSilicaHydraulic.mo` inherits the previous equations and changes only E to 72 GPa and density to 2,200 kg/m3. Keep 100 m free length, 5,000 mm2 solid glass area, 250 bar initial discharge pressure, 1,500 rpm prescribed motor speed and 10 kW nominal output per lane. Cylinder area is recomputed to match the selected force and pressure. Four cases were actually simulated, including the unchanged-strain comparison.

| Assumed peak stress | Silica strain | Net specific energy | Minimum fibre mass for 100 kWh | Rounded ten-lane inventory |
|---|---:|---:|---:|---:|
| 0.216 GPa / old 0.30% strain | 0.300% | 0.03290 Wh/kg | 3,039.9 t | 2,770 modules / 3,047 t |
| 0.5 GPa | 0.694% | 0.17627 Wh/kg | 567.3 t | 520 modules / 572 t |
| 1 GPa | 1.389% | 0.70508 Wh/kg | 141.8 t | 130 modules / 143 t |
| 2 GPa | 2.778% | 2.82031 Wh/kg | 35.46 t | 40 modules / 44 t |

All stresses remain scenario assumptions. Even 0.5 GPa is not automatically acceptable for repeated service. The higher cases describe the benefit **if improved protected bundles can be qualified**, not capability established by the dry-roving literature. Ten-lane rounding materially oversizes the 2 GPa inventory: it supplies 124.09 kWh rather than exactly 100 kWh. Smaller modules could reduce rounding waste.

### 1 GPa module: direct comparison with S-2

| Quantity | Previous S-2 | New fused silica |
|---|---:|---:|
| Fibre mass | 1,230 kg | 1,100 kg |
| Initial force | 5 MN | 5 MN |
| Effective full-bore cylinder diameter | 491.85 mm | 491.85 mm |
| Initial extension | 1.151 m | 1.389 m |
| Useful cylinder stroke | 1.036 m | 1.250 m |
| Initial stored energy | 0.7991 kWh | 0.9645 kWh |
| Delivered shaft energy | 0.6426 kWh | 0.7756 kWh |
| Cutoff time including startup ramp | 231.46 s | 279.34 s |

Ten lanes with thirteen silica modules each give 100.826 kWh of calculated capacity and 143 tonnes of glass. This is energy inventory, not verification of continuous 100 kW operation. The motor still needs the demanding approximately 18–178 cc/rev displacement range and 28–281 L/min flow range as pressure falls from 250 to 25 bar. Charging pressure, cylinder rod strength, force reaction and switching remain the same class of engineering problems as before, with a longer stroke.

The largest energy-accounting discrepancy across the reruns is 0.197 J, below 0.000002% of initial energy in that case; all analytic checks passed. This numerical result does not validate assumed material properties at working stress or ideal regulation. There is no inertia, fluid compressibility, measured motor efficiency map or switching-controller model. Plant mass includes much more than the glass.

## Updated recommendation

Proceed with **protected, aligned fused-silica strands as a candidate**, while retaining S-2 as a control. Do not select on a 6 GPa label or use untreated textile roving at 1–2 GPa on the strength of these results. The next material comparison should use the actual termination, intended free length, environment, charge-hold time and repeated unloading, measuring recoverable energy and failures. A proof-test programme must account for damage and service duration; passing one short pull is not fatigue qualification.

The literature supports silica as a promising family; it does not yet identify a glass product proven best for this complete storage duty. This iteration narrows the material search and makes the potential gain explicit without substituting fracture records for operating limits.

## Reproduction

- `models/FusedSilicaHydraulic.mo`: selected-candidate model.
- `scripts/run-fused-silica.ps1`: runs all four scenarios, checks and comparison plots. The comparison reads the preserved prior S-2 results.
- `scripts/compare_glass_candidates.py`: screening and dry-roving conversions.
- `results/fused_silica/summary.json`: solver-derived results.
- `results/fused_silica/material_screening.json`: screening arithmetic.
- `results/fused_silica/fused_silica_results.png`: module trajectories.
- `results/fused_silica/glass_comparison.png`: S-2 versus silica capacity sizing.

No new software or material was purchased or installed. Literature was read online; previous models/results remain preserved.

## Addendum: chemically strengthened glass (25 October 2026)

The user supplied [AIP's 2013 article on Gorilla Glass](https://www.aip.org/inside-science/what-stresses-gorilla-glass-makes-it-stronger). It describes residual stress and the ion-exchange mechanism: surface compression balanced by interior tension. This adds chemically strengthened aluminosilicate glass to the candidate list for damage-tolerant elastic elements. The article does not supply a cyclic spring allowable or recoverable energy-density measurement.

[Corning's primary explanation](https://www.corning.com/worldwide/en/innovation/the-glass-age/science-of-glass/how-it-works-strengthening-glass.html) confirms that ion exchange creates surface compression which helps suppress the propagation of surface flaws under applied tension. The design implication is potentially higher allowable applied stress after handling damage, not additional free energy on each discharge.

For an unchanged residual-stress field, a charge/discharge cycle returns to the same prestressed state. Its pre-existing manufacturing energy must therefore not be counted as repeatedly deliverable capacity. In the simplified uniform-modulus, uniaxial tension model, the axial residual stresses are self-equilibrated: their area integral is zero. The cross term with a uniform applied axial stress consequently integrates to zero, leaving incremental stored energy sigma_applied²/(2 E rho). This is an idealized derivation, not a complete three-dimensional residual-stress model.

[Corning's Gorilla Glass 3 sheet](https://www.corning.com/content/dam/corning/microsites/csm/gorillaglass/PI_Sheets/2020/Gorilla_Glass_3_ProdSheet.pdf) lists E = 70 GPa and density = 2,390 kg/m³. Using these properties for uniform axial tension gives:

| Assumed applied stress | Incremental energy | Ideal active mass for 100 kWh |
|---|---:|---:|
| 0.5 GPa | 0.208 Wh/kg | 481.82 t |
| 1.0 GPa | 0.830 Wh/kg | 120.46 t |
| 2.0 GPa | 3.321 Wh/kg | 30.11 t |

These stresses are sensitivity inputs, not demonstrated cyclic ratings. Mass excludes residual working energy, conversion losses and all hardware. A rectangular strip in pure bending stores one-third as much energy per mass as uniform tension at the same maximum applied stress under elementary linear beam theory; geometry matters when interpreting strong glass-sheet demonstrations.

For the next material comparison, specify a residual stress profile, compression-layer depth, central tension, flaw population, humidity, load duration and cycle count. Surface compression alone must not be substituted for tensile strength. A large compression layer relative to a thin filament's radius cannot simply be copied from a sheet: the stress field must remain self-equilibrated. Ordinary sodium/potassium exchange also cannot be assumed to work on the previously selected high-purity fused silica, which lacks the same alkali composition.

Decision: retain chemically strengthened aluminosilicate strips/rods as a candidate; do not increase the existing silica or carbon model allowables from this article. Qualification must show greater recoverable cyclic work per total mass than the protected-fibre alternatives. No solver rerun is justified until those inputs are available.
