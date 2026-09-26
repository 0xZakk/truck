"""Independent support contact and negative-control checks on saved engine solids."""
import argparse,hashlib,json,sys
from pathlib import Path
import build123d as cad
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import alternator_carrier_1994_candidate as candidate
from assembly_math import transforms
p=argparse.ArgumentParser();p.add_argument('--assembly-root',type=Path,required=True);p.add_argument('--installed',action='store_true');a=p.parse_args()
mp=a.assembly_root/'inventory/engine/full-assembly.json';raw=mp.read_bytes();m=json.loads(raw);poses=transforms(m)
defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']}
bracket=candidate.bracket();checks=[]
if a.installed:
 identifier='alternator-support-bracket';d=defs[occ[identifier]['definition']]
 bracket=cad.import_step(a.assembly_root/d['step'].lstrip('/')).moved(poses[identifier])
for identifier in ('block','cylinder-head'):
 d=defs[occ[identifier]['definition']];shape=cad.import_step(a.assembly_root/d['step'].lstrip('/')).moved(poses[identifier])
 seated=bracket.distance_to(shape);withdrawn=(cad.Pos(2,0,0)*bracket).distance_to(shape)
 inter=(cad.Pos(-.2,0,0)*bracket).intersect(shape);penetrated=sum(s.volume for s in inter.solids()) if inter else 0
 assert seated<1e-6,(identifier,seated)
 assert withdrawn>1,(identifier,withdrawn)
 assert penetrated>.01,(identifier,penetrated)
 checks.append({'part':identifier,'seated_distance_mm':seated,'withdrawn_2mm_distance_mm':withdrawn,'penetrated_point2mm_volume_mm3':penetrated})
assert mp.read_bytes()==raw
out=(a.assembly_root if a.installed else ROOT)/('inventory/engine/alternator-carrier-1994-installed-joint-validation.json' if a.installed else 'inventory/engine/alternator-carrier-1994-joint-validation.json')
out.write_text(json.dumps({'passed':True,'manifest_sha256':hashlib.sha256(raw).hexdigest(),'candidate_sha256':hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest(),'checks':checks},indent=2)+'\n')
print(json.dumps(checks,indent=2))
