"""Actual nominal STEP candidate vs frozen v4; reused baseline bounds by hashes/frames."""
from pathlib import Path
import sys,json,hashlib,itertools,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_clockwise_candidate import transforms,occurrence_shape
from cad_metrics import solid_volume
import pump_functional_20261003 as c
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
oldp=R/'inventory/engine/accessory-stage-v4-solids.json';old=json.loads(oldp.read_text());mp=c.core.MP;m=json.loads(mp.read_text());poses=transforms(m,0,0);occ={o['id']:o for o in m['occurrences']};defs={d['id']:d for d in m['definitions']};exportp=R/'reference/engine/pump-functional-20261003-build.json';ex=json.loads(exportp.read_text());changed=ex['parts'];paths={n:R/d['step'].lstrip('/')for n,d in defs.items()};bounds={};placed={};inputs={str(p.relative_to(R)):sha(p)for p in[Path(__file__),mp,oldp,exportp,Path(c.__file__),R/'cad/engine/assembly_clockwise_candidate.py']}
assert sha(mp)==old['stage_sha256']
for n,o in occ.items():
 p=paths[o['definition']];g=old['occurrence_geometry'][n];assert sha(p)==g['sha256'],n
 tr=poses[n].wrapped.Transformation();mat=np.array([[tr.Value(i,j)for j in range(1,5)]for i in range(1,4)]+[[0,0,0,1]])
 assert np.max(abs(mat-np.array(g['matrix'])))<1e-8,n
 inputs[str(p.relative_to(R))]=sha(p);bounds[n]=np.array(old['bounds'][n])
for n,v in changed.items():
 p=R/v['path'];assert sha(p)==v['sha256'];s=b.import_step(p);placed[n]=s;bounds[n]=np.array([list(s.bounding_box().min),list(s.bounding_box().max)]);inputs[str(p.relative_to(R))]=sha(p)
rebuilt={'water-pump-housing','water-pump-shaft','water-pump-pulley','heater-pump-return-elbow'}
pairs=[];reused=[]
for a,z in itertools.combinations(occ,2):
 if not set([a,z])&set(changed):continue
 if np.any(np.minimum(bounds[a][1],bounds[z][1])-np.maximum(bounds[a][0],bounds[z][0])< -2):continue
 if a in changed and z in changed and not(set([a,z])&rebuilt):reused.append([a,z]);continue
 pairs.append((a,z))
r={'status':'RUNNING','scope':'nominal98.43mm q0 only; conditional pump ports/frontstack vs actual v4 incl both proposed carriers. No canonical mutation','threshold_mm3':.1,'broadphase_padding_mm':2,'bounds_provenance':'Prior actual STEP bounds reused only after all occurrence STEP hashes and q0 matrices match','pairs_total':len(pairs),'unchanged_translated_internal_relations':reused,'reuse_is_not_acceptance':True,'checks':[],'conflicts':[],'errors':[],'inputs':inputs};rp=R/'reference/engine/pump-functional-20261003-neighbors.json';O=c.O

def save():rp.write_text(json.dumps(r,indent=2)+'\n')
def get(n):
 if n not in placed:
  o=occ[n];placed[n]=poses[n]*occurrence_shape(o,b.import_step(paths[o['definition']]),0,0)
 return placed[n]
save();print('PAIRS',len(pairs),'INHERITED',len(reused),flush=True)
for i,(a,z)in enumerate(pairs,1):
 row={'a':a,'b':z}
 try:
  hit=c.core.norm(get(a).intersect(get(z)));v=sum(abs(solid_volume(q,'adaptive'))for q in hit.solids())if hit else 0
  row['overlap_mm3']=v
  if v>.1:
   p=O/('overlap-'+str(i)+'.step');b.export_step(hit,p);row.update(witness=str(p.relative_to(R)),sha256=sha(p),bounds=[list(hit.bounding_box().min),list(hit.bounding_box().max)]);r['conflicts'].append(row);print('CONFLICT',a,z,v,flush=True)
 except Exception as e:row['error']=repr(e);r['errors'].append(row)
 r['checks'].append(row)
 if i%20==0:print('CHECKED',i,flush=True);save()
r['status']='FAIL'if r['conflicts']else'INCONCLUSIVE'if r['errors']else'PASS scoped nominal q0 only';save();print(r['status'],len(r['conflicts']),len(r['errors']),flush=True)
