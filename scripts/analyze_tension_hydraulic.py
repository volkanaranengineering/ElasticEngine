"""Validate reduced-order hydraulic results against independent integrals."""
import csv,json,math,os
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'results'/'tension_hydraulic'
os.environ['MPLCONFIGDIR']=str(out/'mplconfig')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

E,rho,L,A,eps=45.6e9,1900,100,.005,.003
k=E*A/L; x0=eps*L; U=.5*k*x0*x0; mass=rho*A*L
etaC,etaV,etaM=.95,.95,.90
eta=etaC*etaV*etaM
Ac=etaC*k*x0/25e6
names=['variable_motor','fixed_motor','fixed_header']
labels=['Variable displacement / variable pressure','Fixed displacement / falling power','Fixed pressure / throttling']
curves={}; results={}
for name in names:
    rows=list(csv.DictReader((out/f'{name}_res.csv').open()))
    d={key:np.array([float(row[key]) for row in rows]) for key in rows[0]}
    curves[name]=d
    header=name=='fixed_header'
    expected=eta*U*(.5 if header else .99)
    cutoff=.5 if header else .1
    assert abs(d['delivered'][-1]-expected)<.1,(name,d['delivered'][-1],expected)
    assert abs(d['x'][-1]-cutoff*x0)<1e-6
    assert max(abs(d['residual']))<.1
    assert min(d['valveLoss'])>-.01
    idx=np.where(d['shaftPower']>1)[0]
    per_lane=math.ceil(10000*3600/expected)
    module_count=per_lane*10
    results[name]={
      'delivered_J':float(d['delivered'][-1]),'expected_delivered_J':expected,
      'end_time_s':float(d['time'][idx[-1]]),'residual_energy_J':float(d['stored'][-1]),
      'cylinder_loss_J':float(d['cylinderLoss'][-1]),'valve_loss_J':float(d['valveLoss'][-1]),
      'motor_loss_J':float(d['motorLoss'][-1]),'max_energy_error_J':float(max(abs(d['residual']))),
      'peak_flow_L_min':float(max(d['flowRate'])*60000),
      'peak_required_displacement_cc_rev':float(max(d['displacement'])*1e6),
      'peak_piston_speed_m_s':float(max(d['velocity'])),
      'modules_for_100kWh_energy_only':module_count,
      'spring_mass_tonnes':module_count*mass/1000,
      'installed_delivered_kWh':module_count*expected/3.6e6,
      'net_specific_energy_Wh_kg':expected/3600/mass}
    assert results[name]['installed_delivered_kWh']>=100
    # Independent duration including the 0.25 s startup ramp.
    expected_time=(eta*k*x0*(x0-cutoff*x0)/10000 if name=='fixed_motor' else expected/10000)+.125
    assert abs(results[name]['end_time_s']-expected_time)<.012,(name,expected_time)

summary={'basis':{'length_m':L,'area_m2':A,'strain':eps,'mass_kg':mass,'gross_energy_J':U,
 'force_initial_N':k*x0,'cylinder_effective_area_m2':Ac,'equivalent_bore_mm':math.sqrt(4*Ac/math.pi)*1000,
 'initial_pressure_bar':250,'useful_stroke_m':.27,'eta_assumed':eta,'gross_specific_Wh_kg':U/3600/mass,
 'tension_vs_endloaded_leaf_energy_ratio':9},'cases':results}
(out/'summary.json').write_text(json.dumps(summary,indent=2))

plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(2,2,figsize=(13,8),layout='constrained')
colors=['#217a75','#c47c20','#7356a6']
for name,label,color in zip(names,labels,colors):
    d=curves[name]
    axs[0,0].plot(d['time'],d['shaftPower']/1000,label=label,color=color)
    mask=d['shaftPower']>1
    axs[0,1].plot(d['time'][mask],d['motorPressure'][mask]/1e5,color=color)
    axs[1,0].plot(d['time'],d['delivered']/1000,color=color)
axs[0,0].set(title='One module: prescribed-speed output',ylabel='Shaft power (kW)',xlabel='Time (s)')
axs[0,0].legend(fontsize=8)
axs[0,1].set(title='Motor differential pressure while flowing',ylabel='Pressure (bar)',xlabel='Time (s)')
axs[1,0].set(title='Delivered shaft energy',ylabel='Energy (kJ)',xlabel='Time (s)')
d=curves['variable_motor']; mask=d['shaftPower']>1
axs[1,1].plot(d['time'][mask],d['flowRate'][mask]*60000,label='Inlet flow (L/min)',color='#217a75')
axs[1,1].plot(d['time'][mask],d['displacement'][mask]*1e6,label='Displacement (cc/rev)',color='#ae4655')
axs[1,1].set(title='Variable motor: required operating envelope',xlabel='Time (s)')
axs[1,1].legend(fontsize=9)
for ax in axs.flat: ax.grid(alpha=.2)
fig.suptitle('Tension bundle + hydraulics | reduced-order OpenModelica results',fontsize=16)
fig.savefig(out/'module_results.png',dpi=160)

fig,axs=plt.subplots(1,2,figsize=(12,5),layout='constrained')
metrics=[33698.4,results['variable_motor']['spring_mass_tonnes'],results['fixed_header']['spring_mass_tonnes']]
axs[0].bar(['Leaf + rack\nprevious model','Tension +\nvariable motor','Tension +\nfixed header'],metrics,color=['#999999','#217a75','#7356a6'])
for i,val in enumerate(metrics): axs[0].text(i,val+500,f'{val:,.0f} t',ha='center')
axs[0].set(ylabel='Spring material only (tonnes)',title='100 kWh delivered: energy-only sizing',ylim=(0,39000))
for j,name in enumerate(['variable_motor','fixed_header']):
    d=curves[name]; bottom=0
    for key,label,color in zip(['delivered','stored','cylinderLoss','valveLoss','motorLoss'],['Output','Residual','Cylinder loss','Valve loss','Motor loss'],['#217a75','#aaaaaa','#dfaa55','#7356a6','#ae4655']):
        val=d[key][-1]/1000
        axs[1].bar(j,val,bottom=bottom,color=color,label=label if j==0 else None)
        bottom+=val
axs[1].set(xticks=[0,1],xticklabels=['Variable motor','Fixed header'],ylabel='Energy per module (kJ)',title='Where the initial 102.6 kJ goes')
axs[1].legend(fontsize=8,loc='upper right')
fig.savefig(out/'system_comparison.png',dpi=160)
print(json.dumps(summary,indent=2))

