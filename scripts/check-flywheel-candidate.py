"""Validate unpublished flywheel against the installed assembly."""
import sys,json,hashlib,itertools
from pathlib import Path
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
import flywheel as hose
from assembly_math import transforms
raw=(ROOT/'inventory/engine/full-assembly.json').read_bytes();m=json.loads(raw)
poses=transforms(m);defs={d['id']:d for d in m['definitions']}
parts={'flywheel-body':hose.MOUNT*hose.body(),'flywheel-ring-gear':hose.MOUNT*hose.ring_gear()}
for i,(x,y) in enumerate(hose.HOLES):parts[f'flywheel-crank-bolt-{i+1}']=hose.MOUNT*b.Pos(x,y,0)*hose.bolt()
parts['crankshaft']=hose.crank_interface(b.import_step(ROOT/defs['crankshaft']['step'].lstrip('/')))
for k,s in parts.items():
 assert s.is_valid and len(s.solids())==1,k
 p=Path('/tmp')/(k+'-candidate.step');b.export_step(s,p)
 r=b.import_step(p);assert r.is_valid and len(r.solids())==1,k
 print('STEP valid',k,flush=True)
bounds={k:s.bounding_box() for k,s in parts.items()};cache={};checks=0;collisions=[]
for o in m['occurrences']:
 if o['id'] in parts:continue
 d=o['definition']
 if d not in cache:cache[d]=b.import_step(ROOT/defs[d]['step'].lstrip('/'))
 s=cache[d].moved(poses[o['id']]);bb=s.bounding_box()
 for k,c in parts.items():
  cb=bounds[k]
  if any(min(getattr(bb.max,a),getattr(cb.max,a))-max(getattr(bb.min,a),getattr(cb.min,a))<=.01 for a in 'XYZ'):continue
  checks+=1;print('Check',k,o['id'],flush=True)
  v=s.intersect(c);volume=sum(x.volume for x in v.solids()) if v else 0
  if volume>.01:collisions.append({'a':k,'b':o['id'],'volume_mm3':volume})
for (ka,a),(kc,c) in itertools.combinations(parts.items(),2):
 v=a.intersect(c);volume=sum(x.volume for x in v.solids()) if v else 0
 if volume>.01:collisions.append({'a':ka,'b':kc,'volume_mm3':volume})
assert (ROOT/'inventory/engine/full-assembly.json').read_bytes()==raw
report={'installed':False,'verified_production_fit':False,'manifest_sha256':hashlib.sha256(raw).hexdigest(),'source_sha256':hashlib.sha256((ROOT/'cad/engine/flywheel.py').read_bytes()).hexdigest(),'checks':checks,'collisions':collisions,'limits':hose.GAPS}
(ROOT/'inventory/engine/flywheel-candidate-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2),flush=True)
assert not collisions
