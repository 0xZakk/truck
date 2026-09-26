"""Common casting candidate, saved-engine neighbors, joint continuity and controls."""
import argparse,hashlib,json,sys,tempfile
from pathlib import Path
import build123d as cad
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import alt_thermactor_cast_surface_candidate as c
p=argparse.ArgumentParser();p.add_argument('--assembly-root',type=Path,required=True);p.add_argument('--installed',action='store_true');a=p.parse_args()
sys.path.insert(0,str(a.assembly_root/'cad/engine'))
from assembly_math import transforms
from valve_layout_integration import occurrence_shape
mp=a.assembly_root/'inventory/engine/full-assembly.json';raw=mp.read_bytes();m=json.loads(raw);poses=transforms(m);defs={d['id']:d for d in m['definitions']};cache={};hashes={};neighbors={}
if a.installed:
 assert not set(c.REMOVE_IDS).intersection(o['id'] for o in m['occurrences']),'Obsolete separate brackets remain installed'
shape=c.carrier();assert shape.is_valid and len(shape.solids())==1
installed_difference=None
for module in (c,c.alt,c.ap,c.base):
 path=Path(module.__file__);hashes[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
def vol(s):return sum(v.volume for v in s.solids()) if s else 0
def broad(b1,b2):return all(min(getattr(b1.max,k),getattr(b2.max,k))-max(getattr(b1.min,k),getattr(b2.min,k))>.001 for k in 'XYZ')
for o in m['occurrences']:
 if o['id'] in c.REMOVE_IDS or (o['id']==c.NEW_ID and not a.installed):continue
 d=o['definition']
 if d not in cache:
  path=a.assembly_root/defs[d]['step'].lstrip('/');hashes[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest();cache[d]=cad.import_step(path)
 placed=occurrence_shape(o,cache[d]).moved(poses[o['id']])
 if o['id']==c.NEW_ID:
  installed_difference=vol(placed-shape)+vol(shape-placed);assert installed_difference<.01,installed_difference
  shape=placed
 else:neighbors[o['id']]=placed
if a.installed:assert installed_difference is not None,'Installed occurrence absent'
print('Loaded',len(neighbors),'neighbors',flush=True)
checks=[];failures=[];bounds=shape.bounding_box()
for identifier,s in neighbors.items():
 if not broad(bounds,s.bounding_box()):continue
 v=vol(shape.intersect(s));checks.append({'id':identifier,'volume_mm3':v})
 if v>.01:failures.append(checks[-1]);print('COLLISION',checks[-1],flush=True)
joints=[]
for identifier in ['block','cylinder-head','alternator-drive-housing','thermactor-front-plate','alt-bracket-bolt-1','alt-bracket-bolt-2','alt-engine-bracket-bolt-1','alt-engine-bracket-bolt-2','thermactor-mount-bolt-1','thermactor-mount-bolt-2','thermactor-engine-bolt-1','thermactor-engine-bolt-2']:
 distance=shape.distance_to(neighbors[identifier]);joints.append({'id':identifier,'gap_mm':distance})
 if distance>1e-6:failures.append({'joint':identifier,'gap_mm':distance})
# Preserve individual old interface collars exactly, not merely nearest distance.
interface_checks=[]
for y,z in [(-100,220),(-100,310),(-100,90),(-125,140)]:
 probe=c.base.axial(16,12,(379,y,z));old=c.alt.bracket() if z in (220,310) else c.ap.support()
 expected=old.intersect(probe);actual=shape.intersect(probe);delta=vol(expected-actual)+vol(actual-expected)
 interface_checks.append({'seat_yz':[y,z],'symmetric_difference_mm3':delta})
 if delta>.01:failures.append(interface_checks[-1])
with tempfile.TemporaryDirectory(prefix='truck-common-carrier-') as tmp:
 path=Path(tmp)/'carrier.step';cad.export_step(shape,path);saved=cad.import_step(path)
 assert saved.is_valid and len(saved.solids())==1
 delta=vol(saved-shape)+vol(shape-saved)
 if delta>.01:failures.append({'STEP_difference_mm3':delta})
controls=[]
for key in ['block','cylinder-head']:
 s=neighbors[key];withdrawal=(cad.Pos(2,0,0)*shape).distance_to(s);penetration=vol((cad.Pos(-.2,0,0)*shape).intersect(s))
 controls.append({'id':key,'withdrawal_gap_mm':withdrawal,'penetration_mm3':penetration})
 if withdrawal<=1 or penetration<=.01:failures.append({'negative_control':controls[-1]})
assert mp.read_bytes()==raw
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in hashes.items())
report={'status':'rejected' if failures else 'candidate-static-pass','installed':a.installed,'installed_difference_mm3':installed_difference,'production_fidelity':False,'candidate_solids':len(shape.solids()),'manifest_sha256':hashlib.sha256(raw).hexdigest(),'candidate_sha256':hashes[c.__file__],'exact_checks':len(checks),'checks':checks,'joints':joints,'four_seat_preservation_checks':interface_checks,'roundtrip_symmetric_difference_mm3':delta,'controls':controls,'failures':failures,'input_sha256':hashes,'limits':c.GAPS}
((a.assembly_root if a.installed else ROOT)/('inventory/engine/alt-thermactor-cast-surface-installed-validation.json' if a.installed else 'inventory/engine/alt-thermactor-cast-surface-validation.json')).write_text(json.dumps(report,indent=2)+'\n')
print(report['status'],len(checks),'checks',len(failures),'failures',flush=True)
assert not failures,failures
