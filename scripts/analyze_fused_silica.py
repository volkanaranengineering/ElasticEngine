import csv,json,math,os
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'results'/'fused_silica'
os.environ['MPLCONFIGDIR']=str(out/'mplconfig')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
E,rho,A,L=72e9,2200,.005,100
eta=.95*.95*.9
mass=rho*A*L
specs=[('silica_same_strain',216e6),('silica_0_5GPa',.5e9),('silica_1GPa',1e9),('silica_2GPa',2e9)]
results=[]; curves={}
for name,stress in specs:
    rows=list(csv.DictReader((out/f'{name}_res.csv').open()))
    d={key:np.array([float(row[key]) for row in rows]) for key in rows[0]};curves[name]=d
    x0=stress/E*L; U=stress**2/(2*E)*A*L; delivered=U*eta*.99
    specific=delivered/3600/mass
    n=10*math.ceil(10000*3600/delivered)
    assert abs(d['delivered'][-1]-delivered)/delivered<2e-6
    assert abs(d['x'][-1]-.1*x0)<1e-6
    assert max(abs(d['residual']))/U<2e-6
    active=np.where(d['shaftPower']>1)[0]
    end=float(d['time'][active[-1]])
    assert abs(end-(delivered/10000+.125))<.3
    assert n*delivered/3.6e6>=100
    r={'case':name,'stress_GPa':stress/1e9,'strain_percent':stress/E*100,
       'gross_Wh_kg':U/3600/mass,'net_Wh_kg':specific,
       'energy_only_minimum_fibre_tonnes':100000/specific/1000,
       'module_mass_kg':mass,'module_initial_force_MN':stress*A/1e6,
       'module_initial_extension_m':x0,'useful_stroke_m':.9*x0,
       'cylinder_equivalent_bore_mm':math.sqrt(4*.95*stress*A/25e6/math.pi)*1000,
       'module_gross_kWh':U/3.6e6,'module_delivered_kWh':delivered/3.6e6,
       'discharge_end_s_including_ramp':end,
       'modules_rounded_to_10_lanes':n,'installed_fibre_tonnes':n*mass/1000,
       'installed_delivered_kWh':n*delivered/3.6e6,
       'max_energy_error_J':float(max(abs(d['residual'])))}
    results.append(r)
(out/'summary.json').write_text(json.dumps({'material':'High-purity fused silica; Astroquartz modulus and density','E_Pa':E,'rho_kg_m3':rho,'assumed_discharge_efficiency':eta,'cases':results},indent=2))
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(2,2,figsize=(12,8),layout='constrained')
d=curves['silica_1GPa']
axs[0,0].plot(d['time'],d['shaftPower']/1000,color='#217a75')
axs[0,0].set(title='1 GPa scenario: one module',xlabel='Time (s)',ylabel='Shaft output (kW)')
mask=d['shaftPower']>1
axs[0,1].plot(d['time'][mask],d['sourcePressure'][mask]/1e5,label='Pressure (bar)')
axs[0,1].plot(d['time'][mask],d['flowRate'][mask]*60000,label='Flow (L/min)')
axs[0,1].set(title='Required hydraulic operating envelope',xlabel='Time (s)');axs[0,1].legend()
axs[1,0].plot(d['time'],d['stored']/3.6e6,label='Remaining glass energy')
axs[1,0].plot(d['time'],d['delivered']/3.6e6,label='Delivered to shaft')
axs[1,0].plot(d['time'],(d['cylinderLoss']+d['motorLoss'])/3.6e6,label='Hydraulic losses')
axs[1,0].set(xlabel='Time (s)',ylabel='Energy (kWh)',title='Module energy balance');axs[1,0].legend(fontsize=8)
vals=[r['energy_only_minimum_fibre_tonnes'] for r in results]
axs[1,1].bar(['0.216 GPa\n0.30% strain','0.5 GPa','1 GPa','2 GPa'],vals,color=['#999999','#60a9a3','#217a75','#c58142'])
axs[1,1].set(yscale='log',ylim=(20,6000),ylabel='Fibre mass (tonnes; log scale)',title='100 kWh: sensitivity to ASSUMED working stress')
for i,v in enumerate(vals):axs[1,1].text(i,v*1.15,f'{v:,.1f} t',ha='center')
for ax in axs.flat:ax.grid(alpha=.2)
fig.suptitle('Fused-silica fibres tensioned by hydraulic cylinders\nIdeal load sharing; working stresses are unqualified scenarios',fontsize=15)
fig.savefig(out/'fused_silica_results.png',dpi=160)
print(json.dumps(results,indent=2))

