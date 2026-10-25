import csv,json
from pathlib import Path
root=Path(__file__).resolve().parents[1];out=root/'results'/'optimization'
r=json.loads((out/'optimization.json').read_text());c=r['selected_1GPa_refined']
rows=list(csv.DictReader((out/'OptimizedSilicaHydraulic_res.csv').open()))
last=rows[-1]
err=max(abs(float(row['residual'])) for row in rows)
expected=c['module_delivered_J']
assert abs(float(last['delivered'])-expected)/expected<2e-6
assert abs(float(last['x'])-.1*c['rated_stroke_m'])<1e-6
assert err<.5
assert c['delivered_kWh']>=100
assert c['piston_speed_max_m_s']<=.5 and c['discharge_cutoff_bar']>=25
assert c['module_nominal_duration_s']>=60
assert c['charge_bar']<=350 and c['rated_stroke_m']<=6 and c['length_m']<=1000
actual_area=c['fibres_per_module']*3.141592653589793*(c['diameter_um']*1e-6)**2/4
assert abs(actual_area-c['glass_area_m2'])<1e-12
stats={'checks':'passed','expected_module_J':expected,'simulated_module_J':float(last['delivered']),
 'max_energy_error_J':err,'simulation_cutoff_time_s':max(float(row['time']) for row in rows if float(row['shaftPower'])>1)}
(out/'verification.json').write_text(json.dumps(stats,indent=2));print(json.dumps(stats,indent=2))
