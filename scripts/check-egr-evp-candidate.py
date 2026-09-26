"""Check current EGR/EVP candidate solids before publishing them in the atlas."""
import sys,json,itertools,hashlib
from pathlib import Path
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
import egr,evp_sensor
from assembly_math import transforms
raw=(ROOT/'inventory/engine/full-assembly.json').read_bytes();m=json.loads(raw)
defs={d['id']:d for d in m['definitions']};poses=transforms(m)
parts={};definitions={}
def define(id,s,*a):
 assert s.is_valid and len(s.solids())==1,id
 p=Path('/tmp')/('truck-candidate-'+id+'.step');b.export_step(s,p);r=b.import_step(p)
 assert r.is_valid and len(r.solids())==1,id
 definitions[id]=s
 print('Valid STEP:',id,flush=True)
def add(id,d,parent,pos=(0,0,0),explode=(0,0,0),rotation=(0,0,0),**kw):parts[id]=definitions[d].moved(b.Pos(*pos)*b.Rot(*rotation))
egr.build((define,add,lambda *a:None))
for id,(s,*_) in evp_sensor.parts().items():define(id,s);parts[id]=s.moved(egr.MOUNT)
upper=egr.intake_interface(b.import_step(ROOT/'cad/engine/generated/efi-upper-intake.step'))
assert upper.is_valid and len(upper.solids())==1
parts['efi-upper-intake']=upper
old={};cache={}
for o in m['occurrences']:
 if o['id'] in parts:continue
 d=o['definition']
 if d not in cache:cache[d]=b.import_step(ROOT/defs[d]['step'].lstrip('/'))
 old[o['id']]=cache[d].moved(poses[o['id']])
print('Caching bounds',flush=True)
allparts={**old,**parts};bounds={id:s.bounding_box() for id,s in allparts.items()}
checks=0;collisions=[]
for a,c in itertools.combinations(allparts,2):
 if a not in parts and c not in parts:continue
 ba,bc=bounds[a],bounds[c]
 if any(min(getattr(ba.max,k),getattr(bc.max,k))-max(getattr(ba.min,k),getattr(bc.min,k))<=.01 for k in ['X','Y','Z']):continue
 checks+=1;print('Check',a,c,flush=True)
 v=allparts[a].intersect(allparts[c]);vol=sum(t.volume for t in v.solids()) if v else 0
 if vol>.01:collisions.append({'a':a,'b':c,'volume_mm3':vol})
assert (ROOT/'inventory/engine/full-assembly.json').read_bytes()==raw,'Installed manifest changed'
report={'installed':False,'verified_production_fit':False,'existing_manifest_sha256':hashlib.sha256(raw).hexdigest(),'candidate_source_hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'cad/engine/egr.py',ROOT/'cad/engine/evp_sensor.py']},'new_definitions':len(definitions),'new_occurrences':len(parts)-1,'checks':checks,'collisions':collisions,'limits':'Static fit study. EGR dimensions and location and EVP internal construction remain provisional; no calibrated motion, leakage or electrical performance simulation.'}
(ROOT/'inventory/engine/egr-evp-candidate-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2),flush=True);assert not collisions
