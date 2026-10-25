"""Check solver results and render the actual CAD triangulation and discharge."""
import csv,json,re
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
root=Path(__file__).resolve().parents[1]
out=root/'results'/'rack_motor'
rows=list(csv.DictReader((out/'RackMotor_res.csv').open()))
d={key:np.array([float(row[key]) for row in rows]) for key in rows[0]}
tips={}
for n in (20,40):
    s=(out/f'leaf_{n}.dat').read_text()
    tips[n]=float(re.search(rf'^\s*{n+1}\s+([-+\d.E]+)',s,re.M)[1])
assert abs(tips[40]-20)/20<.001
assert abs(tips[40]-20)<abs(tips[20]-20)
assert max(abs(d['residual']))<1e-6
assert min(d['extension'])>-1e-8 and min(d['v'])>-1e-8
checks=json.loads((out/'mesh_checks.json').read_text())
assert max(c['overlap_mm3'] for c in checks)<1e-6
summary={'stored_J':.5472,'spring_mass_kg_assumed':.0456,'spring_only_Wh_per_kg':.5472/3600/.0456,
 'initial_force_N':54.72,'initial_available_torque_Nm':.98496,'full_angle_deg':180/np.pi,
 'nominal_root_stress_MPa':136.8,'nominal_root_strain':.003,
 'peak_test_load_W':float(max(d['power'])),'peak_rpm':float(max(d['rpm'])),
 'delivered_J_at_0_6s':float(d['delivered'][-1]),'mesh_loss_J_at_0_6s':float(d['loss'][-1]),
 'max_energy_balance_error_J':float(max(abs(d['residual']))),'FE_tip_mm':tips,
 'max_tooth_overlap_mm3':max(c['overlap_mm3'] for c in checks)}
(out/'summary.json').write_text(json.dumps(summary,indent=2))
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig=plt.figure(figsize=(13,8),layout='constrained')
gs=fig.add_gridspec(2,2,width_ratios=[1.25,1])
ax=fig.add_subplot(gs[:,0])
colors=['#238d75','#667085','#e7a13c','#3e76bc','#39445b','#a0aabb','#a0aabb','#a0aabb','#b35555','#b35555']
for i,part in enumerate(json.loads((out/'geometry.json').read_text())):
    v=np.array(part['vertices']); tri=np.array(part['triangles'])
    # Front projection; omit rear bearing/guide faces to retain tooth visibility.
    if part['name'].startswith(('ShaftBearing','RackGuide','Slotted')): continue
    ax.add_collection(PolyCollection(v[tri,:2],facecolors=colors[i%len(colors)],edgecolors='none'))
ax.plot([0,0],[0,200],'--',color='#238d75',alpha=.5)
ax.annotate('S-2 glass/epoxy leaf\n200 x 30 x 4 mm',xy=(6,110),xytext=(45,110),arrowprops={'arrowstyle':'->'})
ax.annotate('20 mm charged stroke',xy=(20,188),xytext=(65,169),arrowprops={'arrowstyle':'->'})
ax.annotate('Module 2 / 20 teeth\n40 mm pitch diameter',xy=(100,240),xytext=(12,267),arrowprops={'arrowstyle':'->'})
ax.annotate('Rack returns left',xy=(65,200),xytext=(115,181),arrowprops={'arrowstyle':'->'})
ax.set(xlim=(-25,195),ylim=(-30,290),aspect='equal',xlabel='x (mm)',ylabel='y (mm)',title='Charged assembly | actual CAD front projection')
ax=fig.add_subplot(gs[0,1])
ax.plot(d['time'],d['torque'],label='Available drive torque (N m)')
ax.plot(d['time'],d['q']*1000/20,label='Released fraction')
ax.set(xlabel='Time (s)',title='Single-stroke discharge',xlim=(0,.3));ax.legend();ax.grid(alpha=.2)
ax=fig.add_subplot(gs[1,1])
ax.plot(d['time'],d['stored'],label='Spring')
ax.plot(d['time'],d['delivered'],label='Viscous test load')
ax.plot(d['time'],d['loss'],label='Assumed mesh loss')
ax.plot(d['time'],d['kinetic'],label='Kinetic')
ax.set(xlabel='Time (s)',ylabel='Energy (J)',xlim=(0,.3),title='Energy accounting | 0.5472 J initially');ax.legend();ax.grid(alpha=.2)
fig.suptitle('Spring-driven rack-and-pinion demonstrator',fontsize=18)
fig.savefig(out/'overview.png',dpi=170)
print(json.dumps(summary,indent=2))
