"""Check inlet delta against actual installed pump/outlet/valve geometry."""
from pathlib import Path
import sys,json,hashlib,tempfile,argparse
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
from valve_layout_integration import occurrence_shape
from cad_metrics import solid_volume
import water_pump_inlet_v3_candidate as inlet
ap=argparse.ArgumentParser();ap.add_argument('--installed',action='store_true');args=ap.parse_args()
raw=(ROOT/'inventory/engine/full-assembly.json').read_bytes();m=json.loads(raw);ds={d['id']:d for d in m['definitions']};poses=transforms(m);cache={};hashes={}
module=Path(inlet.__file__);module_hash=hashlib.sha256(module.read_bytes()).hexdigest()
def load(key):
 if key not in cache:
  path=ROOT/ds[key]['step'].lstrip('/');hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest();cache[key]=b.import_step(path)
 return cache[key]
def vol(s):return sum(solid_volume(q,'adaptive') for q in s.solids()) if s else 0
old=load('water-pump-housing');shape=inlet.housing_interface(old);repeat=inlet.housing_interface(shape)
repeat_delta=vol(repeat-shape)+vol(shape-repeat);assert repeat_delta<.01,repeat_delta
if args.installed:
 delta=vol(old-shape)+vol(shape-old);assert delta<.01,delta
 shape=old
assert shape.is_valid and len(shape.solids())==1
with tempfile.TemporaryDirectory() as td:
 path=Path(td)/'housing.step';b.export_step(shape,path);restored=b.import_step(path)
 delta=vol(shape-restored)+vol(restored-shape);assert delta<.01,delta
frame=poses['water-pump-housing'];subject=frame*shape;bb=subject.bounding_box();checks=0;hits=[]
for o in m['occurrences']:
 if o['id']=='water-pump-housing':continue
 other=poses[o['id']]*occurrence_shape(o,load(o['definition']));ob=other.bounding_box()
 if any(min(getattr(bb.max,k),getattr(ob.max,k))-max(getattr(bb.min,k),getattr(ob.min,k))<=.01 for k in 'XYZ'):continue
 checks+=1;v=vol(subject&other)
 if v>.01:hits.append({'part':o['id'],'volume_mm3':v})
flow=vol(shape&inlet.open_probe());assert flow<1e-6,flow
neck=inlet.cy(23.5,126,127)-inlet.cy(20.5,125,128);missing=vol(neck-shape);assert missing<1e-6,missing
# Prove the geometry checks can detect a blocked inlet.
negative=vol(inlet.open_probe()&inlet.cy(21,125,126));assert negative>1,negative
assert raw==(ROOT/'inventory/engine/full-assembly.json').read_bytes()
assert module_hash==hashlib.sha256(module.read_bytes()).hexdigest()
assert all(hashlib.sha256((ROOT/k).read_bytes()).hexdigest()==h for k,h in hashes.items())
report={'status':'rejected' if hits else 'PASS','installed':args.installed,'manifest_sha256':hashlib.sha256(raw).hexdigest(),'module_sha256':module_hash,'neighbor_checks':checks,'collisions':hits,'roundtrip_symmetric_difference_mm3':delta,'adapter_idempotence_mm3':repeat_delta,'flow_obstruction_mm3':flow,'missing_neck_wall_mm3':missing,'blocked_flow_negative_mm3':negative,'input_step_sha256':hashes,'limits':inlet.GAPS}
name='water-pump-inlet-desktop-installed.json' if args.installed else 'water-pump-inlet-desktop-candidate.json'
(ROOT/'inventory/engine'/name).write_text(json.dumps(report,indent=2)+'\n');print(report['status'],'inlet delta',checks,'checks',hits,flush=True);assert not hits,hits
