"""Small probes of saved fuel/idle/exhaust mating interfaces; no flow simulation."""
from pathlib import Path
import sys,json,hashlib
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
raw=(ROOT/'inventory/engine/full-assembly.json').read_bytes();m=json.loads(raw)
poses=transforms(m);defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};cache={}
def shape(id):
 d=occ[id]['definition']
 if d not in cache:cache[d]=b.import_step(ROOT/defs[d]['step'].lstrip('/'))
 return cache[d].moved(poses[id])
checks=[]
def clear(label,probe,ids):
 for id in ids:
  overlap=shape(id).intersect(probe);volume=sum(s.volume for s in overlap.solids()) if overlap else 0
  assert volume<.01,(label,id,volume)
 checks.append(label)
for i in range(1,7):
 x=(3.5-i)*m['mechanism']['bore_pitch_mm']
 clear(f'Injector {i} lower socket',b.Pos(x-25,-163,302)*b.Cylinder(1,20),['efi-lower-intake'])
 clear(f'Injector {i} rail inlet',b.Pos(x-25,-163,365)*b.Cylinder(1,6),['fuel-supply-rail',f'injector-{i}-metal-body',f'injector-{i}-inlet-filter'])
 exhaust='exhaust-front' if i<=3 else 'exhaust-rear'
 clear(f'Cylinder {i} exhaust/head connection',b.Pos(x+25,-134,277.5)*b.Rot(90,0,0)*b.Cylinder(2,20),['cylinder-head',exhaust])
for x in [385,409]:
 clear(f'IAC mounting port at {x}',b.Pos(x,25,526)*b.Cylinder(1,8),['throttle-housing','iac-gasket','iac-valve-body'])
 clear(f'IAC bypass bore at {x}',b.Pos(x,10,506)*b.Rot(90,0,0)*b.Cylinder(1,30),['throttle-housing'])
clear('Regulator return inlet',b.Pos(0,-163,380)*b.Cylinder(1,6),['fuel-supply-rail','fuel-return-tube','regulator-valve-seat'])
for name,station in [('front',1.5),('rear',-1.5)]:
 clear(f'{name} exhaust collector',b.Pos(station*m['mechanism']['bore_pitch_mm']+25,-180,150)*b.Cylinder(2,20),['exhaust-'+name])
report={'status':'pass','manifest_sha256':hashlib.sha256(raw).hexdigest(),'interfaces':checks,'scope':'Small local clearance probes of provisional passages. Not a connected-volume, leak-tightness, fuel-flow or OEM-geometry certificate.'}
(ROOT/'inventory/engine/flow-interface-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'{len(checks)} fuel, idle-air and exhaust interface probes passed.')
