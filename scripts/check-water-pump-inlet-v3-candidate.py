"""Candidate pump joint geometry/neighbor audit, no baseline mutation."""
from pathlib import Path
import sys,json,hashlib,itertools,argparse
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import water_pump_joint_candidate as p
import water_pump_inlet_v3_candidate as inlet
import water_pump_thermactor_foot_candidate as support
from assembly_math import transforms
from valve_layout_integration import occurrence_shape
ap=argparse.ArgumentParser();ap.add_argument('--baseline-root',type=Path,default=ROOT);args=ap.parse_args();BASE=args.baseline_root
m_path=BASE/'inventory/engine/full-assembly.json';raw=m_path.read_bytes();m=json.loads(raw);defs={d['id']:d for d in m['definitions']};poses=transforms(p.shifted_manifest(m))
paths=[ROOT/'reference/engine/water-pump-inlet-v3-topology-reviewed.json',Path(__file__),Path(inlet.__file__),ROOT/'cad/engine/valve_layout_integration.py',ROOT/'cad/engine/valve_layout_candidate.py',Path(support.__file__),ROOT/'cad/engine/accessory_brackets.py',ROOT/'cad/engine/cooling_connections.py',Path(p.__file__),ROOT/'cad/engine/water_pump_gasket_topology_candidate.py',ROOT/'reference/engine/water-pump-mounting-topology-reviewed.json']
hashes={str(q.relative_to(ROOT)):hashlib.sha256(q.read_bytes()).hexdigest() for q in paths};step_hashes={};cache={}
def load(key):
 if key not in cache:
  path=BASE/defs[key]['step'].lstrip('/');step_hashes[str(path.relative_to(BASE))]=hashlib.sha256(path.read_bytes()).hexdigest();cache[key]=b.import_step(path)
 return cache[key]
def vol(s):return sum(q.volume for q in s.solids()) if s else 0
def broad(a,c):return all(min(getattr(a.max,k),getattr(c.max,k))-max(getattr(a.min,k),getattr(c.min,k))>.001 for k in 'XYZ')
frame=b.Pos(*p.PUMP_POSITION)
parts={'block':p.block_interface(support.block_interface(load('block'))),'water-pump-housing':frame*inlet.housing_interface(p.housing_interface(load('water-pump-housing'))),'water-pump-gasket':frame*p.gasket_shape(),'water-pump-shaft':frame*p.shaft_shape(),'water-pump-impeller':frame*p.impeller_interface(load('water-pump-impeller'))}
parts['thermactor-support-bracket']=support.support()
parts['thermactor-engine-bolt-2']=support.upper_bolt()
active={'water-pump-assembly','fan-clutch-assembly'}
while True:
 more=active|{a['id'] for a in m['assemblies'] if a['parent'] in active}
 if more==active:break
 active=more
for o in m['occurrences']:
 if (o['parent'] in active or o['id']=='heater-pump-return-elbow') and o['id'] not in parts:parts[o['id']]=poses[o['id']]*occurrence_shape(o,load(o['definition']))
screw=p.screw_shape()
for n,(y,z) in enumerate(p.MOUNTING,1):parts[f'water-pump-mounting-screw-{n}']=frame*b.Pos(-51,y,z)*screw
for key,s in parts.items():assert s.is_valid and len(s.solids())==1,key
print('Valid candidate solids',len(parts),flush=True)
failures=[];checks=0
neighbors={o['id']:poses[o['id']]*occurrence_shape(o,load(o['definition'])) for o in m['occurrences'] if o['id'] not in parts}
bounds={k:s.bounding_box(optimal=False) for k,s in {**neighbors,**parts}.items()}
for a,s in parts.items():
 for c,t in neighbors.items():
  if a=='block':continue # Existing casting mutations separately probe new material below.
  if broad(bounds[a],bounds[c]):
   checks+=1;v=vol(s&t)
   if v>.1:failures.append({'a':a,'b':c,'mm3':v});print('Collision',a,c,v,flush=True)
for (a,s),(c,t) in itertools.combinations(parts.items(),2):
 if broad(bounds[a],bounds[c]):
  checks+=1;v=vol(s&t)
  if v>.1:failures.append({'a':a,'b':c,'mm3':v});print('Collision',a,c,v,flush=True)
added=parts['block']-load('block')
if isinstance(added,b.ShapeList):added=b.Compound(children=list(added))
ab=added.bounding_box(optimal=False)
for c,t in neighbors.items():
 if broad(ab,bounds[c]):
  checks+=1;v=vol(added&t)
  if v>.1:failures.append({'a':'block-added-material','b':c,'mm3':v})
unchanged=raw==m_path.read_bytes() and all(hashlib.sha256((ROOT/q).read_bytes()).hexdigest()==h for q,h in hashes.items()) and all(hashlib.sha256((BASE/q).read_bytes()).hexdigest()==h for q,h in step_hashes.items())
report={'baseline_root':str(BASE),'input_hashes':hashes,'step_hashes':step_hashes,'manifest_sha256':hashlib.sha256(raw).hexdigest(),'inputs_unchanged':unchanged,'candidate_solids':len(parts),'neighbor_checks':checks,'collisions':failures,'scope':'Initial static candidate audit. Sealing areas, socket retention, flow boundary, sampled motion, export comparison and visual review still required.'}
(ROOT/'inventory/engine/water-pump-inlet-v3-candidate-validation.json').write_text(json.dumps(report,indent=2)+'\n')
assert unchanged and not failures,(unchanged,failures)
print('PASS initial pump candidate neighbors')
