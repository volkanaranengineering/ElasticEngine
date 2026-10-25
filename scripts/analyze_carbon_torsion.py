import csv,json,math,os
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'results'/'carbon_torsion'
os.environ['MPLCONFIGDIR']=str(out/'mplconfig')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
specs=[('carbon_upper',1,1,.9,.97,.97,.99,.99),('carbon_reference',.5,.7,.9,.9,.95,.98,.95),('carbon_derated',.1,.5,.8,.75,.9,.95,.8)]
results=[];curves={}
for name,scale,twist,er,ec,eg,ei,ret in specs:
    rows=list(csv.DictReader((out/f'{name}_res.csv').open()))
    d={key:np.array([float(row[key]) for row in rows]) for key in rows[0]};curves[name]=d
    eta=er*ec*eg*ei;lam=-math.log(ret)/3600
    E0=10000/eta/lam*math.expm1(lam*180)*math.exp(lam*3420)/.9
    mass=200*E0/(2.1e6*scale*twist**2)
    # Analytic solution for every cartridge, independent of the solver integrator.
    end_expected=[]
    for j in range(20):
        end_expected.append(E0*ret-(10000/eta/lam)*math.expm1(lam*180)*math.exp(-lam*(3600-j*180)))
        assert abs(d[f'E[{j+1}]'][-1]-end_expected[-1])/E0<2e-6
    assert abs(d['delivered'][-1]-360e6)<5
    assert min(d['availableRatio'])>=.1*ret-1e-6
    assert max(abs(d['residual']))<10
    # Charge-path assumes generator operated as motor at same efficiency, no second rope-loss factor.
    eta_charge=ec*eg*ei
    refill=(200*E0-d['stored'][-1])/eta_charge
    r=dict(case=name,scale_factor=scale,twist_fraction=twist,eta_discharge=eta,
      assumed_hour_retention=ret,active_rope_mass_kg=mass,cartridge_mass_kg=mass/200,
      energy_initial_kWh=200*E0/3.6e6,delivered_kWh=d['delivered'][-1]/3.6e6,
      conversion_loss_kWh=d['conversionLoss'][-1]/3.6e6,
      relaxation_loss_kWh=d['relaxationLoss'][-1]/3.6e6,
      residual_kWh=d['stored'][-1]/3.6e6,
      first_charge_electrical_kWh=200*E0/eta_charge/3.6e6,
      modeled_refill_electrical_kWh=refill/3.6e6,
      modeled_cycle_efficiency=360e6/refill,
      max_energy_error_J=float(max(abs(d['residual']))),
      inventory_level_delivered_Wh_per_kg=100000/mass,
      cell_count_if_10microgram=mass/1e-8,
      attachment_mass_kg_if_1microgram_per_cell=mass/10)
    results.append(r)
(out/'summary.json').write_text(json.dumps(results,indent=2))
plt.rcParams.update({'font.size':10,'axes.spines.top':False,'axes.spines.right':False})
fig,axs=plt.subplots(2,2,figsize=(12,8),layout='constrained')
d=curves['carbon_reference'];time=d['time']/60
axs[0,0].plot(time,d['electricalPower']/1000,color='#217a75')
axs[0,0].set(xlabel='Time (min)',ylabel='DC output (kW)',ylim=(0,115),title='Ideal dispatch: ten 10 kW lanes')
for key,label in [('stored','Remaining energy'),('delivered','Electrical output'),('conversionLoss','Conversion loss'),('relaxationLoss','Relaxation loss')]:
    axs[0,1].plot(time,d[key]/3.6e6,label=label)
axs[0,1].set(xlabel='Time (min)',ylabel='Energy (kWh)',title='Reference-case energy accounting');axs[0,1].legend(fontsize=8)
for j in [1,10,20]:axs[1,0].plot(time,d[f'E[{j}]']/d[f'E[{j}]'][0],label=f'Cartridge {j} in each lane')
axs[1,0].set(xlabel='Time (min)',ylabel='Fraction of initial energy',title='Short cartridges released in sequence');axs[1,0].legend(fontsize=8)
vals=[r['active_rope_mass_kg'] for r in results]
axs[1,1].bar(['Lab-density\nupper scenario','50% scale retention\nreference','10% scale retention\nstress test'],vals,color=['#69b8ad','#217a75','#be8d46'])
axs[1,1].set(yscale='log',ylim=(100,50000),ylabel='Active rope mass (kg; log scale)',title='Mass sensitivity: assumptions dominate')
for i,v in enumerate(vals):axs[1,1].text(i,v*1.12,f'{v:,.0f} kg',ha='center')
for ax in axs.flat:ax.grid(alpha=.2)
fig.suptitle('Theoretical CNT torsional storage | 100 kW DC for one hour\nEnergy-flow simulation; ideal switching and unvalidated scale-up',fontsize=15)
fig.savefig(out/'carbon_results.png',dpi=160)
print(json.dumps(results,indent=2))
