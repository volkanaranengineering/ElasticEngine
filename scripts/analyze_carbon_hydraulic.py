import csv,json,math,os
from pathlib import Path
root=Path(__file__).resolve().parents[1]; out=root/'results/carbon_hydraulic'
os.environ['MPLCONFIGDIR']=str(out/'mplconfig')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
eta=.95*.97*.95*.95
specs=[('t1100_reference',3.5e9,324e9,1790,100),('t1100_lower_stress',2e9,324e9,1790,100),('cnt_extrapolation',6.25e9,370e9,1666.66666666667,100),('t1100_long',3.5e9,324e9,1790,500)]
results=[];curves={}
for name,stress,E,rho,L in specs:
    with (out/f'{name}_res.csv').open() as f: rows=list(csv.DictReader(f))
    d={key:np.array([float(r[key]) for r in rows]) for key in rows[0]};curves[name]=d
    E0=10000*180/(eta*.91); x0=stress*L/E; A=2*E0*E/(stress**2*L); Ac=.95*stress*A/30e6
    for j in range(1,21):
        target=x0*x0*(1-.91*np.clip((d['time']-(j-1)*180)/180,0,1))
        assert max(abs(d[f'y[{j}]']-target))/x0**2<1e-6
    assert abs(d['delivered'][-1]-360e6)<5
    assert max(abs(d['residual']))<10
    assert abs(d['oilThroughput'][-1]-200*Ac*x0*.7)<1e-4
    for j in range(1,21):
        on=d[f'Q[{j}]']>0
        assert max(abs(d[f'p[{j}]'][on]*d[f'Q[{j}]'][on]*.97*.95*.95-10000))<1e-4
    r=dict(case=name,length_m=L,stress_GPa=stress/1e9,active_mass_kg=200*A*L*rho,
        bundle_mass_kg=A*L*rho,area_mm2=A*1e6,solid_equivalent_diameter_mm=math.sqrt(4*A/math.pi)*1000,
        peak_extension_m=x0,working_travel_m=.7*x0,peak_bundle_force_kN=stress*A/1000,
        cylinder_effective_area_cm2=Ac*1e4,full_bore_equivalent_mm=math.sqrt(4*Ac/math.pi)*1000,
        initial_kWh=200*E0/3.6e6,remaining_kWh=d['stored'][-1]/3.6e6,output_kWh=d['delivered'][-1]/3.6e6,
        cylinder_loss_kWh=d['cylinderLoss'][-1]/3.6e6,line_loss_kWh=d['lineLoss'][-1]/3.6e6,motor_loss_kWh=d['motorLoss'][-1]/3.6e6,
        max_velocity_m_s=max(d['velocity[1]']),oil_throughput_m3=d['oilThroughput'][-1],
        peak_total_flow_L_min=max(d['totalFlow'])*60000,
        motor_displacement_max_cc_rev=max(d['displacement[1]'])*1e6,
        max_balance_error_J=float(max(abs(d['residual']))))
    results.append(r)
(out/'summary.json').write_text(json.dumps(results,indent=2))
d=curves['t1100_reference']; t=d['time']/60
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,ax=plt.subplots(2,2,figsize=(12,8),layout='constrained')
ax[0,0].plot(t,d['shaftPower']/1000);ax[0,0].set(xlabel='Time (min)',ylabel='Shaft output (kW)',ylim=(0,115),title='Ideal sequential dispatch')
for key,label in [('stored','Stored'),('delivered','Delivered'),('cylinderLoss','Cylinder loss'),('lineLoss','Line loss'),('motorLoss','Motor loss')]:ax[0,1].plot(t,d[key]/3.6e6,label=label)
ax[0,1].legend(fontsize=8);ax[0,1].set(xlabel='Time (min)',ylabel='Energy (kWh)',title='Plant energy balance')
mask=d['time']<180
ax[1,0].plot(d['time'][mask],d['p[1]'][mask]/1e5,label='Cylinder pressure (bar)')
ax[1,0].plot(d['time'][mask],d['displacement[1]'][mask]*1e6,label='Motor displacement (cc/rev)')
ax[1,0].legend(fontsize=8);ax[1,0].set(xlabel='Time within first discharge (s)',title='One lane: pressure and displacement',ylabel='Values in legend units')
ax[1,1].plot(t,d['totalFlow']*60000,color='#217a75');ax[1,1].set(xlabel='Time (min)',ylabel='Aggregate flow (L/min)',title='Ten lanes switch together in this model')
for a in ax.flat:a.grid(alpha=.2)
fig.suptitle('Carbon tension / hydraulic motor | 100 kW shaft for one hour\nQuasi-static model; prescribed control, no switching transients')
fig.savefig(out/'carbon_hydraulic_results.png',dpi=160)
# A vector schematic is an engineering communication artifact, not dimensional CAD.
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="440" viewBox="0 0 1200 440"><rect width="1200" height="440" fill="#f7fafc"/><style>text{font-family:Arial;fill:#17324a} .box{fill:#e1f2ed;stroke:#217a75;stroke-width:2} .line{stroke:#217a75;stroke-width:3;fill:none}</style><text x="35" y="38" font-size="25">Carbon tension storage — one of ten 10 kW lanes</text><rect class="box" x="35" y="85" width="250" height="100" rx="8"/><text x="55" y="120" font-size="19">20 × 100 m tension bundles</text><text x="55" y="152" font-size="16">Separate cylinders and hold latches</text><path class="line" d="M285 135 H355"/><rect class="box" x="355" y="85" width="220" height="100" rx="8"/><text x="373" y="120" font-size="19">Selection / isolation valves</text><text x="373" y="152" font-size="16">One bundle active for 180 s</text><path class="line" d="M575 135 H645"/><rect class="box" x="645" y="85" width="220" height="100" rx="8"/><text x="663" y="120" font-size="19">Variable-displacement</text><text x="663" y="152" font-size="16">hydraulic motor / pump</text><path class="line" d="M865 135 H925"/><text x="940" y="130" font-size="20">10 kW shaft</text><text x="940" y="158" font-size="16">1,000 rpm assumed</text><path class="line" d="M755 185 V275 H465 V185"/><rect class="box" x="520" y="240" width="175" height="75" rx="8"/><text x="535" y="270" font-size="17">Return tank / cooler</text><text x="535" y="295" font-size="14">Low-pressure circuit</text><text x="35" y="360" font-size="18">Discharge cylinder pressure: 300 → 90 bar. Charging reverses the power path.</text><text x="35" y="395" font-size="16">Functional schematic only. Accumulator, relief valves, detailed porting and switching dynamics remain to be sized.</text></svg>'''
(out/'hydraulic_architecture.svg').write_text(svg.replace('20 × 100 m','20 × 500 m'),encoding='utf-8')
print(json.dumps(results,indent=2))
