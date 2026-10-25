"""FreeCADCmd: conceptual charged assembly, real involute gear, beam decks."""
import json, math, sys
from pathlib import Path
import FreeCAD as App
import Part
sys.path.append(str(Path(App.getResourceDir())/'Mod'/'PartDesign'))
import InvoluteGearFeature
out=Path(__file__).resolve().parents[1]/'results'/'rack_motor'
out.mkdir(parents=True,exist_ok=True)
doc=App.newDocument('SpringRackMotor')
V=App.Vector
parts=[]
def add(name,shape):
    obj=doc.addObject('PartDesign::Feature',name)
    obj.Shape=shape
    assert shape.isValid(), name
    parts.append(obj)
    return obj
def prism(points,depth,z):
    vv=[V(x,y,z) for x,y in points]
    return Part.Face(Part.Wire(Part.makePolygon(vv+[vv[0]]).Edges)).extrude(V(0,0,depth))
# Beam shown in the charged state: Euler-Bernoulli displacement shape.
ys=[200*i/100 for i in range(101)]
xs=[20*y*y*(600-y)/(2*200**3) for y in ys]
leaf=add('ChargedGlassEpoxyLeaf',prism([(x-2,y) for x,y in zip(xs,ys)]+[(x+2,y) for x,y in reversed(list(zip(xs,ys)))],30,-15))
leaf.addProperty('App::PropertyString','MaterialBasis').MaterialBasis='UD S-2 glass/913 epoxy; E1=45.6 GPa; assumed density 1900 kg/m3'
leaf.addProperty('App::PropertyString','GeometryBasis').GeometryBasis='200 x 30 x 4 mm; 20 mm tip displacement; approximate charged shape'
add('FixedClamp',Part.makeBox(22,20,42,V(-11,-20,-21)))
# Rack pitch line y=207; 20-degree full-depth teeth, 0.10 mm tooth-thickness allowance.
p=2*math.pi
centers=[100+i*p for i in range(-12,13)]
root_half=p/4+2.5*math.tan(math.radians(20))-.05
tip_half=p/4-2*math.tan(math.radians(20))-.05
points=[(20,195),(180,195),(180,204.5)]
for c in reversed(centers):
    points += [(c+root_half,204.5),(c+tip_half,209),(c-tip_half,209),(c-root_half,204.5)]
points += [(20,204.5)]
rack=add('Rack',prism(points,12,-6))
profile=InvoluteGearFeature.makeInvoluteGear('PinionProfile')
profile.NumberOfTeeth=20
profile.Modules=2
profile.PressureAngle=20
doc.recompute()
gear=Part.Face(profile.Shape.Wires[0]).extrude(V(0,0,12))
gear.translate(V(0,0,-6))
gear=gear.cut(Part.makeCylinder(4,12,V(0,0,-6)))
# Gap at bottom aligns with rack tooth centered under the pinion.
gear.rotate(V(0,0,0),V(0,0,1),9)
gear.translate(V(100,227,0))
pinion=add('Pinion',gear)
add('OutputShaft',Part.makeCylinder(4,44,V(100,227,-22)))
# Conceptual rear guides and bearing block, all behind moving parts.
add('ShaftBearing',Part.makeBox(18,18,10,V(91,218,-22)).cut(Part.makeCylinder(4,10,V(100,227,-22))))
for x in [50,150]:
    add('RackGuide'+str(x),Part.makeBox(12,13,10,V(x,192,-16)))
# Tip coupling pin along z; vertical slot allows tip rotation/shortening.
add('TipPin',Part.makeCylinder(1.5,44,V(20,200,-22)))
clevis=Part.makeBox(8,18,4,V(16,191,-22))
slot=Part.makeBox(3.4,10,4,V(18.3,195,-22))
add('SlottedTipCoupler',clevis.cut(slot))
# Test rack/gear interference over the full stroke; conjugate pitch motion.
checks=[]
for i in range(21):
    travel=float(i)
    rs=rack.Shape.copy(); rs.translate(V(-travel,0,0))
    gs=gear.copy(); gs.rotate(V(100,227,0),V(0,0,1),-travel/20*180/math.pi)
    checks.append({'released_mm':travel,'overlap_mm3':rs.common(gs).Volume})
doc.removeObject(profile.Name)
doc.recompute()
doc.saveAs(str(out/'spring_rack_motor.FCStd'))
Part.export(parts,str(out/'spring_rack_motor.step'))
preview=[]
for obj in parts:
    vertices,triangles=obj.Shape.tessellate(.3)
    preview.append({'name':obj.Name,'vertices':[[v.x,v.y,v.z] for v in vertices],'triangles':triangles})
(out/'geometry.json').write_text(json.dumps(preview))
(out/'mesh_checks.json').write_text(json.dumps(checks,indent=2))
for n in (20,40):
    lines=['*HEADING','Longitudinal effective beam mm N MPa; no laminate failure prediction','*NODE']
    lines += [f'{i+1},0,{200*i/n},0' for i in range(n+1)]
    lines += ['*ELEMENT,TYPE=B31,ELSET=BEAM']+[f'{i+1},{i+1},{i+2}' for i in range(n)]
    lines += ['*MATERIAL,NAME=EFFECTIVE','*ELASTIC','45600,0.3','*BEAM SECTION,ELSET=BEAM,MATERIAL=EFFECTIVE,SECTION=RECT','4,30','1,0,0','*NSET,NSET=TIP',str(n+1),'*BOUNDARY','1,1,6','*STEP','*STATIC','*CLOAD',f'{n+1},1,54.72','*NODE PRINT,NSET=TIP','U','*END STEP']
    (out/f'leaf_{n}.inp').write_text('\n'.join(lines)+'\n')
print('CAD built; maximum mesh overlap mm3:',max(c['overlap_mm3'] for c in checks))
