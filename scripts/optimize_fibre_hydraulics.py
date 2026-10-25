"""Discrete catalogue-envelope optimization; excludes foundations and balance of plant.
Cylinder weights: Rexroth RE17337/09.05 p2, CD MP3/MP5 without position sensor.
This old manufacturer table is a mass surrogate, not a current purchasable configuration.
"""
import json,math,csv,os
from pathlib import Path
import numpy as np
root=Path(__file__).resolve().parents[1]
out=root/'results'/'optimization';out.mkdir(parents=True,exist_ok=True)
os.environ['MPLCONFIGDIR']=str(out/'mplconfig')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

E,rho=72e9,2200
eta_ch,eta_c,eta_v,eta_m=.95,.95,.95,.90
eta=eta_c*eta_v*eta_m
lanes=10; P=100000/lanes; target=100*3.6e6; oil_density=850
catalog=[(40,28,8,1.2),(50,36,12,1.6),(63,45,26,2.6),(80,56,33,4.2),
 (100,70,58,5.7),(125,90,120,11.1),(140,100,167,13),(160,110,229,16.3),
 (180,125,317,19.5),(200,140,425,24.4),(220,160,514,37.8),
 (250,180,777,46.2),(280,200,915,59.7),(320,220,1200,68.3)]

def sweep(stress,diam_um=14,length_cap=1000,pressure_grid=None,stroke_step_mm=25,shared=False,latch_kg=0,objective='mass'):
    af=math.pi*(diam_um*1e-6)**2/4
    candidates=[]; best=None; by_pressure=[]
    scorekey='modeled_subtotal_tonnes' if objective=='mass' else 'total_parallel_filaments'
    for bar in (pressure_grid if pressure_grid is not None else range(200,351)):
        pcharge=bar*1e5; best_p=None
        for bore,rod,base,per100 in catalog:
            annulus=math.pi*((bore/1000)**2-(rod/1000)**2)/4
            nf=math.floor(eta_ch*pcharge*annulus/(stress*af))
            if nf<1:continue
            A=nf*af; force=stress*A; p0=eta_c*force/annulus
            # A6VM-family operating-envelope checks, not a selected motor.
            if p0*.1<25e5:continue
            flowmax=P/(eta_v*eta_m*p0*.1)
            if flowmax/annulus>.5:continue
            Dmax=flowmax*eta_v/25
            if Dmax>200e-6:continue
            for stroke_mm in range(stroke_step_mm,6001,stroke_step_mm):
                stroke=stroke_mm/1000
                length=stroke*E/stress
                if length>length_cap+1e-8:continue
                gross=.5*force*stroke
                useful=gross*eta*.99
                if shared and useful/P<60:continue
                per_lane=math.ceil(target/lanes/useful)
                modules=per_lane*lanes
                fibre_mass=modules*rho*A*length
                cylinders=20 if shared else modules
                cylinder_mass=cylinders*(base+per100*stroke_mm/100)
                # Conservative cylinder inventory: both chambers' maximum combined fluid.
                fluid_mass=cylinders*oil_density*(math.pi*(bore/1000)**2/4)*stroke
                latch_mass=modules*latch_kg if shared else 0
                subtotal=fibre_mass+cylinder_mass+fluid_mass+latch_mass
                result=dict(stress_GPa=stress/1e9,diameter_um=diam_um,length_m=length,
                  rated_stroke_m=stroke,useful_stroke_m=.9*stroke,charge_bar=force/(eta_ch*annulus)/1e5,
                  discharge_initial_bar=p0/1e5,discharge_cutoff_bar=.1*p0/1e5,
                  bore_mm=bore,rod_mm=rod,annulus_m2=annulus,fibres_per_module=nf,cylinders=cylinders,
                  glass_area_m2=A,force_N=force,modules=modules,modules_per_lane=per_lane,
                  total_parallel_filaments=nf*modules,total_filament_length_km=nf*modules*length/1000,
                  gross_kWh=modules*gross/3.6e6,delivered_kWh=modules*useful/3.6e6,
                  module_delivered_J=useful,module_nominal_duration_s=useful/P,
                  fibre_tonnes=fibre_mass/1000,cylinder_tonnes=cylinder_mass/1000,
                  cylinder_fluid_tonnes=fluid_mass/1000,latch_budget_tonnes=latch_mass/1000,
                  latch_kg_each_assumed=latch_kg,modeled_subtotal_tonnes=subtotal/1000,
                  piston_speed_max_m_s=flowmax/annulus,flow_max_L_min=flowmax*60000,
                  motor_Dmax_cc_rev=Dmax*1e6,
                  total_charged_anchor_force_MN=modules*force/1e6)
                if best_p is None or result[scorekey]<best_p[scorekey]:best_p=result
        if best_p is not None:
            by_pressure.append(best_p)
            if best is None or best_p[scorekey]<best[scorekey]:best=best_p
    return best,by_pressure

cases=[];pressure_curves=[]
for stress in [.5e9,1e9,2e9]:
    best,curve=sweep(stress)
    assert best and best['delivered_kWh']>=100
    assert best['length_m']<=1000 and best['rated_stroke_m']<=6
    cases.append(best);pressure_curves.append(curve)
chosen=cases[1]
short,_=sweep(1e9,length_cap=100)
fine,_=sweep(1e9,pressure_grid=[350],stroke_step_mm=1)
fibre9,_=sweep(1e9,diam_um=9,pressure_grid=[350],stroke_step_mm=1)
shared_cases=[]
for stress in [.5e9,1e9,2e9]:
    s,_=sweep(stress,shared=True)
    refined,_=sweep(stress,shared=True,pressure_grid=[round(s['charge_bar'])],stroke_step_mm=1)
    shared_cases.append(refined)
shared_sensitivity=[]
for allowance in [25,100]:
    s,_=sweep(1e9,shared=True,latch_kg=allowance)
    center=round(s['charge_bar'])
    refined,_=sweep(1e9,shared=True,latch_kg=allowance,pressure_grid=sorted(set([350]+list(range(max(278,center-2),min(350,center+2)+1)))),stroke_step_mm=1)
    shared_sensitivity.append(refined)
report={'scope':'Minimum of fibre + catalogue-estimated cylinders + cylinder oil only; not whole plant',
 'constraints':{'length_cap_m':1000,'stroke_cap_m':6,'max_charge_bar':350,'lanes':lanes,
   'max_piston_speed_m_s':.5,'min_motor_pressure_bar':25,'max_motor_displacement_cc_rev':200,
   'pressure_grid_bar':1,'coarse_stroke_grid_mm':25,'fine_stroke_grid_mm_at_350bar':1,
   'oil_density_kg_m3':oil_density},
 'stress_scenarios':cases,'dedicated_1GPa_refined':fine,'comparison_100m':short,'comparison_9um':fibre9,
 'shared_cylinder_scenarios_excluding_latches':shared_cases,'shared_latch_mass_sensitivity':shared_sensitivity,
 'selected_1GPa_refined':shared_sensitivity[0]}
report['constraints']['shared_minimum_nominal_discharge_s']=60
report['constraints']['selected_latch_budget_kg_per_bundle']=25
fewest,_=sweep(1e9,shared=True,latch_kg=25,objective='count')
report['fewest_filaments_1GPa_sampled']=fewest
(out/'optimization.json').write_text(json.dumps(report,indent=2))
with (out/'pressure_sweep.csv').open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=pressure_curves[0][0].keys());writer.writeheader()
    for curve in pressure_curves:writer.writerows(curve)

# Emit concrete optimized model and simulator input for the refined reference case.
c=shared_sensitivity[0]
model=f'''model OptimizedSilicaHydraulic
  extends FusedSilicaHydraulic(peakStress=1e9,L={c['length_m']:.15g},
    area={c['glass_area_m2']:.15g},Ac={c['annulus_m2']:.15g},p0={c['discharge_initial_bar']*1e5:.15g});
end OptimizedSilicaHydraulic;
'''
(root/'models'/'OptimizedSilicaHydraulic.mo').write_text(model)
mos='''loadModel(Modelica);
loadFile("../../models/TensionHydraulic.mo");
loadFile("../../models/BareGlassHydraulic.mo");
loadFile("../../models/FusedSilicaHydraulic.mo");
loadFile("../../models/OptimizedSilicaHydraulic.mo");
getErrorString();
simulate(OptimizedSilicaHydraulic, stopTime=%g, numberOfIntervals=3000, tolerance=1e-10, outputFormat="csv");
getErrorString();
'''%(c['module_nominal_duration_s']+2)
(root/'scripts'/'optimized_silica.mos').write_text(mos)

fig,axs=plt.subplots(1,2,figsize=(12,5),layout='constrained')
for curve,label in zip(pressure_curves,['0.5 GPa assumption','1 GPa assumption','2 GPa assumption']):
    axs[0].plot([r['charge_bar'] for r in curve],[r['modeled_subtotal_tonnes'] for r in curve],label=label)
axs[0].set(xlabel='Peak charging pressure (bar)',ylabel='Modeled core mass (tonnes)',title='Dedicated-cylinder architecture: pressure sweep',yscale='log');axs[0].legend()
items=[short,fine,shared_sensitivity[0]];bottom=[0,0,0]
for key,label,col in [('fibre_tonnes','Glass','#217a75'),('cylinder_tonnes','Cylinders','#d89439'),('cylinder_fluid_tonnes','Cylinder oil','#5379ad'),('latch_budget_tonnes','Latch allowance','#985ba5')]:
    vals=[item[key] for item in items]
    axs[1].bar([0,1,2],vals,bottom=bottom,label=label,color=col)
    bottom=[b+v for b,v in zip(bottom,vals)]
axs[1].set(xticks=[0,1,2],xticklabels=['100 m\ndedicated','1,000 m\ndedicated','1,000 m\nshared'],ylabel='Modeled core mass (tonnes)',title='1 GPa: architecture and length limit')
axs[1].legend();fig.suptitle('Constrained mass optimization | 100 kW / 100 kWh\nUnqualified fibre stresses; foundations and balance of plant excluded',fontsize=14)
fig.savefig(out/'optimization.png',dpi=160)
print(json.dumps(report,indent=2))
