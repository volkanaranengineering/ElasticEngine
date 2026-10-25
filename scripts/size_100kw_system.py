"""Algebraic sizing, not a validated plant simulation. SI units throughout."""
import json, math
from pathlib import Path

root=Path(__file__).resolve().parents[1]
E,rho=45.6e9,1900
L,b,t,x0,r=2.0,.30,.040,.20,.20
eta,remaining=.90,.10
leaves_per_module,lanes=100,10
module_power=10000
I=b*t**3/12
k=3*E*I/L**3
leaf_energy=.5*k*x0*x0
leaf_mass=rho*L*b*t
gross=leaves_per_module*leaf_energy
usable=eta*gross*(1-remaining**2)
seconds=usable/module_power
per_lane=math.ceil(3600/seconds)
count=per_lane*lanes
F=leaves_per_module*k*x0
v0=module_power/(eta*F)
data={
 'target_output_kW':100,'target_delivered_kWh':100,'eta_assumed':eta,
 'leaf_dimensions_m':[L,b,t],'leaf_stroke_m':x0,'leaf_stiffness_N_per_m':k,
 'leaf_energy_J':leaf_energy,'leaf_mass_kg':leaf_mass,
 'root_stress_MPa':6*(k*x0)*L/(b*t*t)/1e6,
 'leaves_per_module':leaves_per_module,'module_power_kW':10,
 'module_gross_J':gross,'module_delivered_J':usable,'module_duration_s':seconds,
 'lanes':lanes,'modules_per_lane':per_lane,'total_modules':count,
 'total_leaves':count*leaves_per_module,
 'total_spring_mass_tonnes':count*leaves_per_module*leaf_mass/1000,
 'solid_spring_volume_m3':count*leaves_per_module*L*b*t,
 'initial_stored_kWh':count*gross/3.6e6,
 'delivered_capacity_kWh':count*usable/3.6e6,
 'residual_energy_kWh':count*gross*remaining**2/3.6e6,
 'discharge_loss_kWh':count*gross*(1-remaining**2)*(1-eta)/3.6e6,
 'duration_at_100kW_s':per_lane*seconds,
 'module_force_start_end_N':[F,F*remaining],
 'module_available_torque_start_end_Nm':[eta*F*r,eta*F*r*remaining],
 'module_rack_speed_start_end_m_per_s':[v0,v0/remaining],
 'module_pinion_rpm_start_end':[v0/r*30/math.pi,v0/remaining/r*30/math.pi],
 'pinion_rotation_deg':x0*(1-remaining)/r*180/math.pi,
 'central_torque_at_1500rpm_Nm':100000/(1500*math.pi/30),
 'energy_only_minimum_mass_tonnes':100000/(.0033333333333333335*eta*(1-remaining**2))/1000,
 'roundtrip_efficiency_if_charge_eta_90percent':eta*.9,
}
assert abs(data['initial_stored_kWh']-sum(data[q] for q in ['delivered_capacity_kWh','residual_energy_kWh','discharge_loss_kWh']))<1e-8
assert data['delivered_capacity_kWh']>=100
out=root/'results'/'system_100kw'
out.mkdir(parents=True,exist_ok=True)
(out/'sizing.json').write_text(json.dumps(data,indent=2))
print(json.dumps(data,indent=2))
