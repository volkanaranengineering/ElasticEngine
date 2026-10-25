"""Run with FreeCADCmd; creates editable CAD and structured FE input decks."""
import json
from pathlib import Path
import FreeCAD as App
import Part

root = Path(__file__).resolve().parents[1]
out = root / 'results' / 'validation'
out.mkdir(parents=True, exist_ok=True)
doc = App.newDocument('ElasticEngineValidation')
rod = doc.addObject('Part::Box', 'Rod')
rod.Length, rod.Width, rod.Height = 100, 10, 10
doc.recompute()
assert abs(rod.Shape.Volume - 10000) < 1e-6
doc.saveAs(str(out / 'rod.FCStd'))
Part.export([rod], str(out / 'rod.step'))
(out / 'cad.json').write_text(json.dumps({'volume_mm3': rod.Shape.Volume,
    'expected_volume_mm3': 10000, 'freecad_version': App.Version()}, indent=2))

for refinement in (1, 2):
    nx, ny, nz = 10*refinement, refinement, refinement
    def node(i,j,k):
        return 1 + i + (nx+1)*(j+(ny+1)*k)
    lines = ['*HEADING', 'ElasticEngine axial validation: mm N MPa', '*NODE']
    for k in range(nz+1):
        for j in range(ny+1):
            for i in range(nx+1):
                lines.append(f'{node(i,j,k)}, {100*i/nx}, {10*j/ny}, {10*k/nz}')
    lines.append('*ELEMENT,TYPE=C3D8,ELSET=ALL')
    eid=0
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                eid+=1
                ids=[node(i,j,k),node(i+1,j,k),node(i+1,j+1,k),node(i,j+1,k),
                     node(i,j,k+1),node(i+1,j,k+1),node(i+1,j+1,k+1),node(i,j+1,k+1)]
                lines.append(','.join(map(str,[eid]+ids)))
    sets = {'LEFT':[node(0,j,k) for k in range(nz+1) for j in range(ny+1)],
            'TIP':[node(nx,j,k) for k in range(nz+1) for j in range(ny+1)],
            'Y0':[node(i,0,k) for k in range(nz+1) for i in range(nx+1)],
            'Z0':[node(i,j,0) for j in range(ny+1) for i in range(nx+1)]}
    for name,ids in sets.items():
        lines.append('*NSET,NSET='+name)
        for start in range(0,len(ids),12): lines.append(','.join(map(str,ids[start:start+12])))
    lines += ['*MATERIAL,NAME=STEEL','*ELASTIC','210000,0.3',
              '*SOLID SECTION,ELSET=ALL,MATERIAL=STEEL','*BOUNDARY',
              'LEFT,1,1,0','Y0,2,2,0','Z0,3,3,0','*STEP','*STATIC',
              '*BOUNDARY','TIP,1,1,0.1','*NODE PRINT,NSET=TIP,TOTALS=YES','RF',
              '*NODE FILE','U','*EL FILE','S,E','*END STEP']
    (out/f'axial_{refinement}.inp').write_text('\n'.join(lines)+'\n')
print('CAD and FE inputs created in', out)
