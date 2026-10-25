"""Screening calculations: rupture estimates are NOT allowable energy ratings."""
import json,math,os
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'results'/'fused_silica'
os.environ['MPLCONFIGDIR']=str(out/'mplconfig')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
eta=.95*.95*.9*.99
materials=[('E-glass',72.3e9,2580,3.445e9),('S-2 glass',86.9e9,2460,4.89e9),('Fused silica (Astroquartz)',72e9,2200,6e9)]
data=[]
for name,E,rho,strength in materials:
    data.append({'name':name,'E_GPa':E/1e9,'rho_kg_m3':rho,'listed_filament_strength_GPa':strength/1e9,
      'linear_rupture_screen_Wh_kg_NOT_working_rating':strength**2/(2*E*rho*3600),
      'net_Wh_kg_at_ASSUMED_1GPa':1e18/(2*E*rho*3600)*eta,
      'minimum_fibre_tonnes_100kWh_at_ASSUMED_1GPa':100000/(1e18/(2*E*rho*3600)*eta)/1000})
rovings=[(267,14),(400,22),(640,30),(667,34),(960,38),(1600,48)]
roving_data=[{'tex':tex,'typical_break_force_daN':force,'approx_break_stress_GPa':force*10*2200/(tex*1e-6)/1e9} for tex,force in rovings]
report={'screening':data,'quartzel_dry_roving_conversions':roving_data,
 'silica_to_S2_mass_ratio_at_same_stress':72*2200/(86.9*2460),
 'silica_required_allowable_stress_ratio_for_equal_specific_energy':math.sqrt(72*2200/(86.9*2460))}
(out/'material_screening.json').write_text(json.dumps(report,indent=2))
old=json.loads((root/'results'/'bare_glass'/'summary.json').read_text())['cases'][1:]
new=json.loads((out/'summary.json').read_text())['cases'][1:]
fig,ax=plt.subplots(figsize=(9,5),layout='constrained')
x=list(range(3))
a=[c['energy_only_minimum_fibre_tonnes'] for c in old]
b=[c['energy_only_minimum_fibre_tonnes'] for c in new]
ax.bar([i-.18 for i in x],a,width=.36,label='S-2 glass',color='#999999')
ax.bar([i+.18 for i in x],b,width=.36,label='Fused silica',color='#217a75')
for i in x:
    ax.text(i-.18,a[i]+10,f'{a[i]:.1f}',ha='center')
    ax.text(i+.18,b[i]+10,f'{b[i]:.1f}',ha='center')
ax.set(xticks=x,xticklabels=['0.5 GPa','1 GPa','2 GPa'],ylabel='Minimum fibre mass (tonnes)',xlabel='ASSUMED repeated-use stress: not yet qualified',ylim=(0,900),title='100 kWh delivered: fused silica versus S-2 glass\nIdentical efficiency and residual-extension assumptions')
ax.legend();ax.spines[['top','right']].set_visible(False)
fig.savefig(out/'glass_comparison.png',dpi=170)
print(json.dumps(report,indent=2))
