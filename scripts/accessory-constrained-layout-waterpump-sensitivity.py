#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib
import numpy as np,trimesh
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_clockwise_candidate import transforms
from cad_metrics import solid_volume
mp=R/'inventory/engine/corrected-engine-stage-v3.json';rp=R/'inventory/engine/accessory-constrained-layout-step-check.json';j=json.loads(rp.read_text());m=json.loads(mp.read_text());t=transforms(m,0,0);d={x['id']:x for x in m['definitions']};occ={x['id']:x for x in m['occurrences']};e=json.loads((R/'inventory/engine/accessory-constrained-layout-envelopes.json').read_text());groups={n:g for g,ids in e['moving_occurrence_ownership'].items()for n in ids};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();inputs={str(p.relative_to(R)):sha(p)for p in [mp,rp,Path(__file__),R/'cad/engine/assembly_clockwise_candidate.py']};bounds={};pose={}
for n,g in groups.items():
 o=occ[n];dd=d[o['definition']];p=R/dd['glb'].lstrip('/');inputs[str(p.relative_to(R))]=sha(p);v=np.asarray(trimesh.load(p,force='mesh').vertices)[:,[0,2,1]]*[1,-1,1]*1000;pose[n]=b.Pos(0,*j['posedelta_yz_mm'][g])*t[n];tr=pose[n].wrapped.Transformation();mat=np.array([[tr.Value(k,l)for l in range(1,5)]for k in range(1,4)]);v=v@mat[:,:3].T+mat[:,3];bounds[n]=[v.min(0),v.max(0)]
rows=[];cache={};O=R/'cad/engine/generated/accessory-constrained-layout'
for label in ['nominal','low-offset','high-offset']:
 p=R/f'cad/engine/generated/waterpump-source-offset-inlet-candidate/{label}-housing.step';inputs[str(p.relative_to(R))]=sha(p);pump=b.import_step(p);bb=pump.bounding_box();pb=[np.array(tuple(bb.min)),np.array(tuple(bb.max))]
 for n,nb in bounds.items():
  if np.any(np.minimum(pb[1],nb[1])-np.maximum(pb[0],nb[0]) < -2):continue
  if n not in cache:
   q=R/d[occ[n]['definition']]['step'].lstrip('/');inputs[str(q.relative_to(R))]=sha(q);cache[n]=pose[n]*b.import_step(q)
  row={'pump_hypothesis':label,'neighbor':n}
  try:
   c=pump.intersect(cache[n]);v=solid_volume(c)if c else 0;row.update(overlap_mm3=v,distance_mm=float(pump.distance_to(cache[n])))
   if v>.1:
    w=O/f'waterpump-{label}__{n}-overlap.step';b.export_step(c,w);row['witness']=str(w.relative_to(R));row['sha256']=sha(w)
  except Exception as ex:row['error']=str(ex)
  rows.append(row)
r={'status':'COMPLETE sensitivity only; neither pump hypothesis nor accessory layout installed','world_frame_confirmed_by_owner':True,'scope':'New inlet nominal/offset bounds versus moved rigid branch geometry only; replacement carriers absent and must include inlet/uncertainty interface','rows':rows,'input_sha256':inputs};(R/'inventory/engine/accessory-constrained-layout-waterpump-sensitivity.json').write_text(json.dumps(r,indent=2)+'\n')
