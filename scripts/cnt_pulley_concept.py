"""Closed-form energy/scheduling model; no torque/control validation."""
import csv,json,math,os
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'results/cnt_pulley_concept';out.mkdir(parents=True,exist_ok=True)
os.environ['MPLCONFIGDIR']=str(out/'mplconfig')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
cases=[('optimistic',2.1e6,.9*.95*.97,.99),('reference',2.1e6*.5*.7**2,.9*.85*.95,.95),('low_conversion_sensitivity',2.1e6*.5*.7**2,.22,.95)]
results=[];allcurves={}
for name,e,eta,ret in cases:
    lam=-math.log(ret)/3600;P=10000;dt=180;n=20;lanes=10
    E0=P/(eta*lam)*math.expm1(lam*dt)*math.exp(lam*(n-1)*dt)/.9
    t=np.arange(3601,dtype=float);energies=[]
    for j in range(n):
        elapsed=np.clip(t-j*dt,0,dt)
        after=np.maximum(t-(j+1)*dt,0)
        energies.append(E0*np.exp(-lam*t)-P/(eta*lam)*(-np.expm1(-lam*elapsed))*np.exp(-lam*after))
    energies=np.array(energies);stored=lanes*energies.sum(axis=0)
    delivered=100000*t;conversion=delivered*(1/eta-1)
    relaxation=lanes*n*E0-stored-delivered-conversion
    # Independent numerical integration of relaxation rate checks the analytical inventory.
    integrated=np.trapz(lam*stored,t)
    assert abs(integrated-relaxation[-1])<100
    assert abs(energies[-1,-1]/E0-.1*ret)<1e-10
    assert np.min(energies)>0
    assert abs(delivered[-1]-360e6)<1
    mass=lanes*n*E0/e
    r=dict(case=name,material_J_kg=e,discharge_efficiency=eta,hour_idle_retention=ret,
      active_mass_kg=mass,active_mass_per_cartridge_kg=mass/200,initial_kWh=200*E0/3.6e6,
      delivered_kWh=100,conversion_loss_kWh=conversion[-1]/3.6e6,
      relaxation_loss_kWh=relaxation[-1]/3.6e6,residual_kWh=stored[-1]/3.6e6,
      total_mass_if_half_active_kg=2*mass,delivered_Wh_kg_if_half_active=100000/(2*mass),
      relaxation_integral_error_J=abs(integrated-relaxation[-1]))
    results.append(r);allcurves[name]=(t,stored,delivered,conversion,relaxation,energies)
    with (out/f'{name}.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['time_s','stored_J','delivered_J','conversion_loss_J','relaxation_loss_J'])
        w.writerows(zip(t,stored,delivered,conversion,relaxation))
(out/'summary.json').write_text(json.dumps(results,indent=2))
fig,ax=plt.subplots(1,2,figsize=(12,4.8),layout='constrained')
t,stored,delivered,conversion,relaxation,energies=allcurves['reference']
for y,label in [(stored,'Remaining inventory'),(delivered,'Shaft energy'),(conversion,'Conversion loss'),(relaxation,'Relaxation loss')]:ax[0].plot(t/60,y/3.6e6,label=label)
ax[0].set(xlabel='Time (min)',ylabel='Energy (kWh)',title='Reference case: 100 kW for one hour');ax[0].legend(fontsize=8)
for j in [0,9,19]:ax[1].plot(t/60,energies[j]/3.6e6,label=f'Cartridge {j+1} per lane')
ax[1].set(xlabel='Time (min)',ylabel='Cartridge inventory (kWh)',title='20 sequential cartridges in each of 10 lanes');ax[1].legend(fontsize=8)
for a in ax:a.grid(alpha=.2)
fig.suptitle('CNT pulley battery concept — analytical energy model, unvalidated scale-up')
fig.savefig(out/'energy_schedule.png',dpi=160)
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="1250" height="460" viewBox="0 0 1250 460"><rect width="1250" height="460" fill="#f6f9fb"/><style>text{font-family:Arial;fill:#16354a}.b{fill:#e0f1ec;stroke:#267e72;stroke-width:2}.l{stroke:#267e72;stroke-width:3;fill:none}</style><text x="30" y="40" font-size="25">CNT pulley battery — 100 kWh delivered / 100 kW shaft</text><rect class="b" x="30" y="80" width="290" height="155" rx="10"/><text x="48" y="112" font-size="20">200 storage cartridges</text><text x="48" y="145" font-size="16">Short rope segments, shared guides</text><text x="48" y="173" font-size="16">Axial + torsional energy collection</text><text x="48" y="204" font-size="16">0.5 kWh delivered per cartridge</text><path class="l" d="M320 158 H370"/><rect class="b" x="370" y="80" width="275" height="155" rx="10"/><text x="388" y="112" font-size="20">10 independent output lanes</text><text x="388" y="145" font-size="16">20 cartridges selected sequentially</text><text x="388" y="173" font-size="16">Clutch + variable-ratio transmission</text><text x="388" y="204" font-size="16">10 kW per lane, 180 s per cartridge</text><path class="l" d="M645 158 H695"/><rect class="b" x="695" y="80" width="240" height="155" rx="10"/><text x="712" y="112" font-size="20">Common output shaft</text><text x="712" y="145" font-size="16">1,000 rpm target</text><text x="712" y="173" font-size="16">955 N m total output torque</text><text x="712" y="204" font-size="16">Reversible charging path</text><path class="l" d="M935 158 H985"/><text x="1000" y="150" font-size="24">100 kW</text><text x="1000" y="184" font-size="18">for 60 minutes</text><path class="l" d="M815 235 V285"/><rect class="b" x="695" y="285" width="355" height="65" rx="8"/><text x="710" y="312" font-size="17">Optional flywheel: 20 kJ usable buffer</text><text x="710" y="336" font-size="15">Bridges 0.2 s; additional hardware required</text><text x="30" y="392" font-size="17">Paper basis: Utsumi et al. (2024), Figure 6. Cartridge and transmission design are proposed extensions.</text><text x="30" y="425" font-size="16">Functional architecture only: no established pulley dimensions, rope count, gearbox ratio or total machine mass.</text></svg>'''
(out/'architecture.svg').write_text(svg,encoding='utf-8')
print(json.dumps(results,indent=2))
