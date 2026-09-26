"""Check actual installed solids against a conservative full-rotation impeller envelope."""
from pathlib import Path
import sys,json,hashlib
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import water_pump_joint_candidate as p
import water_pump_thermactor_foot_candidate as t
from assembly_math import transforms
from valve_layout_integration import occurrence_shape
from cad_metrics import solid_volume
paths=[Path(__file__),Path(p.__file__),Path(t.__file__),ROOT/'cad/engine/assembly_math.py',ROOT/'cad/engine/valve_layout_integration.py',ROOT/'cad/engine/valve_layout_candidate.py',ROOT/'inventory/engine/full-assembly.json']
hashes={str(q.relative_to(ROOT)):hashlib.sha256(q.read_bytes()).hexdigest() for q in paths};steps={};cache={}
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in m['definitions']};poses=transforms(m);frame=b.Pos(*p.PUMP_POSITION)
def load(key):
 if key not in cache:
  path=ROOT/defs[key]['step'].lstrip('/');steps[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest();cache[key]=b.import_step(path)
 return cache[key]
def vol(s):return sum(solid_volume(q,'adaptive') for q in s.solids()) if s else 0
envelope=frame*(p.cx(51,-71,-56)-p.cx(8.05,-72,-55))
impeller=poses['water-pump-impeller']*load('water-pump-impeller')
excess=vol(impeller-envelope);assert excess<1e-6,excess
bounds=envelope.bounding_box(optimal=False)

checks=0;failures=[]
for o in m['occurrences']:
 if o['id']=='water-pump-impeller':continue
 s=poses[o['id']]*occurrence_shape(o,load(o['definition']))
 bb=s.bounding_box(optimal=False)
 if not all(min(getattr(bounds.max,k),getattr(bb.max,k))-max(getattr(bounds.min,k),getattr(bb.min,k))>.001 for k in 'XYZ'):continue
 checks+=1;v=vol(envelope&s)
 if v>.1:failures.append({'part':o['id'],'mm3':v})
assert all(hashlib.sha256((ROOT/q).read_bytes()).hexdigest()==h for q,h in dict(hashes,**steps).items())
result={'input_hashes':hashes,'step_hashes':steps,'inputs_unchanged':True,'impeller_outside_sweep_envelope_mm3':excess,'neighbor_checks':checks,'collisions':failures,'scope':'Annular solid contains every angle of the modeled impeller around its Xaxis. This certifies geometric rotation clearance only; vane profile, rotation direction, speed and pumping performance remain unverified.'}
(ROOT/'inventory/engine/water-pump-installed-sweep-desktop-validation.json').write_text(json.dumps(result,indent=2)+'\n');assert not failures,failures;print('PASS fullrotation impeller envelope')
