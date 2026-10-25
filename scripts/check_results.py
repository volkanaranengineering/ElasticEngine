"""Check solver results with Python's standard library."""
import csv
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
checks = []
for refinement in (1, 2):
    path = root / 'results' / 'validation' / f'axial_{refinement}.dat'
    text = path.read_text()
    match = re.search(r'total force[^\n]*\n\s*\n?\s*([+\-\d.Ee]+)', text, re.I)
    if not match:
        raise RuntimeError(f'Cannot find total reaction force in {path}')
    force = abs(float(match.group(1)))
    error = abs(force-21000)/21000
    assert error < 0.001, (force,error)
    checks.append({'check': f'axial_mesh_{refinement}', 'force_N': force,
        'expected_force_N':21000, 'strain_energy_J':0.5*force*0.1/1000,
        'relative_error':error, 'passed':True})

path = root / 'results' / 'modelica' / 'SpringDischarge_res.csv'
with path.open(newline='') as stream:
    rows = list(csv.DictReader(stream))
max_error=max(abs(float(row['residual'])) for row in rows)
final=rows[-1]
assert abs(float(final['time'])-20) < 1e-6
assert max_error < 1e-5, max_error
assert float(final['delivered']) > 4.99
checks.append({'check':'spring_discharge', 'initial_energy_J':5,
    'delivered_to_damping_load_J':float(final['delivered']),
    'max_energy_balance_error_J':max_error,'passed':True})
(root/'results'/'validation_report.json').write_text(json.dumps(checks,indent=2))
print(json.dumps(checks,indent=2))
