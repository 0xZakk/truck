"""Check sourced bolt envelope and provisional three-point rail mounting."""
import json,sys,math
from pathlib import Path
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
from fuel_mounts import MOUNT_X
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());d={x['id']:x for x in m['definitions']};loc=transforms(m)
def shape(id):return b.import_step(ROOT/d[id]['step'].lstrip('/'))
bolt=shape('fuel-rail-mount-bolt');box=bolt.bounding_box()
assert abs(box.min.Z+.9*25.4)<.001
shank=bolt.intersect(b.Pos(0,0,-12)*b.Box(10,10,20));sb=shank.bounding_box()
assert abs(sb.size.X-6.35)<.01 and abs(sb.size.Y-6.35)<.01
pitch=25.4/20;states=[]
for i in range(50):
 z=-20+i*.2;a=bolt.is_inside((3,0,z));c=bolt.is_inside((3,0,z+pitch));assert a==c;states.append(a)
assert any(states) and not all(states)
rail=shape('fuel-supply-rail');lower=shape('efi-lower-intake');return_tube=shape('fuel-return-tube');washer=shape('fuel-rail-mount-washer');collisions=[]
for i,x in enumerate(MOUNT_X,1):
 bs=bolt.moved(loc[f'fuel-rail-mount-bolt-{i}']);ws=washer.moved(loc[f'fuel-rail-mount-washer-{i}'])
 for a,c,name in [(bs,rail,'bolt/rail'),(bs,lower,'bolt/intake'),(ws,rail,'washer/rail'),(ws,lower,'washer/intake'),(bs,ws,'bolt/washer'),(bs,return_tube,'bolt/return')]:
  v=a.intersect(c);vol=sum(s.volume for s in v.solids()) if v else 0
  if vol>.01:collisions.append({'station':i,'pair':name,'volume_mm3':vol})
 # A clear path for the nominal shank must reach the blind mounting bore.
 probe=b.Pos(x,-178,354)*b.Cylinder(3,20)
 v=lower.intersect(probe);assert not v or sum(s.volume for s in v.solids())<.01
for a,name in [(rail,'rail/return'),(lower,'intake/return')]:
 v=a.intersect(return_tube);vol=sum(s.volume for s in v.solids()) if v else 0
 if vol>.01:collisions.append({'pair':name,'volume_mm3':vol})
report={'bolt_under_head_length_mm':-box.min.Z,'thread_pitch_mm':pitch,'mounts':3,'collisions':collisions,'verified_production_fit':False,'limits':'Nominal diameter/pitch/length follow Ford image648486791. Head, washers, boss contours and stations remain provisional; female threads and production tolerances not modeled.'}
(ROOT/'inventory/engine/fuel-mount-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert not collisions
