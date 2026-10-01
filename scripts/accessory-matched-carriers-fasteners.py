#!/usr/bin/env python3
"""Trial4 independent holes and estimated forward tool approaches; no preload claim."""
from pathlib import Path
import sys,json,hashlib
import numpy as np,trimesh
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import accessory_matched_carriers_trial4 as src
import accessory_brackets as base
from assembly_clockwise_candidate import transforms,occurrence_shape
from cad_metrics import solid_volume
O=R/'cad/engine/generated/accessory-matched-carriers';cp=O/'trial4-carrier.step';mp=R/'inventory/engine/corrected-engine-stage-v3.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();inputs={str(p.relative_to(R)):sha(p)for p in [cp,mp,Path(__file__),Path(src.__file__),Path(base.__file__)]};carrier=b.import_step(cp);m=json.loads(mp.read_text());t=transforms(m,0,0);ds={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};e=json.loads((R/'inventory/engine/accessory-constrained-layout-envelopes.json').read_text());groups={n:g for g,ids in e['moving_occurrence_ownership'].items()for n in ids};bounds={};pose={};cache={}
for n,o in occ.items():
 if n=='alternator-thermactor-common-carrier':continue
 d=ds[o['definition']];p=R/d['glb'].lstrip('/');inputs[str(p.relative_to(R))]=sha(p);v=np.asarray(trimesh.load(p,force='mesh').vertices)[:,[0,2,1]]*[1,-1,1]*1000;g=groups.get(n);pose[n]=b.Pos(0,*src.SELECT['posedelta_yz_mm'][g])*t[n]if g else t[n];tr=pose[n].wrapped.Transformation();a=np.array([[tr.Value(i,j)for j in range(1,5)]for i in range(1,4)]);v=v@a[:,:3].T+a[:,3];bounds[n]=np.array([v.min(0),v.max(0)])
def actual(n):
 if n not in cache:
  o=occ[n];p=R/ds[o['definition']]['step'].lstrip('/');inputs[str(p.relative_to(R))]=sha(p);cache[n]=pose[n]*occurrence_shape(o,b.import_step(p),0,0)
 return cache[n]
def vol(a,z):
 c=a.intersect(z)
 if isinstance(c,b.ShapeList):c=b.Compound(children=list(c))
 return c,solid_volume(c)if c else 0
seats=[('engine-'+str(i),373,12,y,z,14)for i,(y,z)in enumerate(src.ENGINE_SEATS)]+[(g+'-'+str(i),src.FACES[g],10,y,z,19.8 if g=='ALT'else 7.8)for g in src.EARS for i,(y,z)in enumerate(src.EARS[g])]
r={'status':'RUNNING','tool_contract':'Estimated R11 solid40mm axial approach begins at bolt head front; no actual socket source identity','retention':'Smooth inherited bolt/clearance-hole geometry only; nuts/thread identity/preload remain missing or unverified','holes':[],'tools':[],'inputs':inputs};out=R/'inventory/engine/accessory-matched-carriers-fasteners.json'
def save():out.write_text(json.dumps(r,indent=2)+'\n')
for name,x,width,y,z,engagement in seats:
 _,v=vol(base.axial(5.4,width,(x+width/2,y,z)),carrier);r['holes'].append({'seat':name,'R5_4_probe_overlap_mm3':v,'modeled_engagement_or_ear_insertion_mm':engagement})
 tool=base.axial(11,40,(x+width+6+20,y,z));bb=tool.bounding_box();tb=np.array([tuple(bb.min),tuple(bb.max)]);pairs=[n for n,nb in bounds.items()if np.all(np.minimum(tb[1],nb[1])-np.maximum(tb[0],nb[0])>=-1)];row={'seat':name,'tested_neighbors':len(pairs),'faults':[]};c,v=vol(tool,carrier);row['carrier_overlap_mm3']=v
 for n in pairs:
  try:
   c,v=vol(tool,actual(n))
   if v>.1:row['faults'].append({'neighbor':n,'overlap_mm3':v})
  except Exception as ex:row['faults'].append({'neighbor':n,'error':str(ex)})
 for label in ['nominal','low-offset','high-offset']:
  p=R/f'cad/engine/generated/waterpump-source-offset-inlet-candidate/{label}-housing.step';inputs[str(p.relative_to(R))]=sha(p);c,v=vol(tool,b.import_step(p))
  if v>.1:row['faults'].append({'separate_pump_hypothesis':label,'overlap_mm3':v})
 r['tools'].append(row);save();print(name,row,flush=True)
w=base.boss(373,-100,220,12,5.5,width=.02);r['wrong_seat_gap_control_missing_mm3']=solid_volume(w.cut(b.Pos(1,0,0)*carrier));r['expected_witness_mm3']=solid_volume(w);assert r['wrong_seat_gap_control_missing_mm3']>.1
r['status']='COMPLETE bounded holes/tool study; explicit faults retained; no thread/load acceptance';save()
