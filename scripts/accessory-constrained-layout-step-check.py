#!/usr/bin/env python3
"""Actual STEP check of inferred centers; old carriers remain replacement obligations."""
from pathlib import Path
import sys,json,hashlib,itertools
import numpy as np,trimesh
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_clockwise_candidate import transforms,occurrence_shape
from cad_metrics import solid_volume
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();mp=R/'inventory/engine/corrected-engine-stage-v3.json';ep=R/'inventory/engine/accessory-constrained-layout-envelopes.json';sp=R/'inventory/engine/accessory-constrained-layout-order-sensitivity.json';e=json.loads(ep.read_text());sr=json.loads(sp.read_text());selected=min([x for x in sr['rows']if x['gap_mm']==30 and x['feasible']],key=lambda x:x['objective']);m=json.loads(mp.read_text());assert sha(mp)==e['stage_sha256'];t=transforms(m,0,0);defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};groups={n:g for g,ids in e['moving_occurrence_ownership'].items()for n in ids};skip=set(e['declared_replacement_carriers']);delta={g:np.array(selected['centers_yz_mm'][g])-e['current_centers_yz_mm'][g]for g in e['current_centers_yz_mm']};inputs={str(p.relative_to(R)):sha(p)for p in [Path(__file__),mp,ep,sp,R/'cad/engine/assembly_clockwise_candidate.py',R/'cad/engine/assembly_math.py',R/'cad/engine/cad_metrics.py']};meshes={};bounds={};pose={}
for n,o in occ.items():
 if n in skip:continue
 d=defs[o['definition']];p=R/d['glb'].lstrip('/');inputs[str(p.relative_to(R))]=sha(p)
 if d['id']not in meshes:meshes[d['id']]=np.asarray(trimesh.load(p,force='mesh').vertices)[:,[0,2,1]]*[1,-1,1]*1000
 v=meshes[d['id']];dd=delta[groups[n]] if n in groups else np.zeros(2);pose[n]=b.Pos(0,*dd)*t[n];tr=pose[n].wrapped.Transformation();a=np.array([[tr.Value(k,j)for j in range(1,5)]for k in range(1,4)]);v=v@a[:,:3].T+a[:,3];bounds[n]=np.array([v.min(0),v.max(0)])
pairs=[];separated=0
for n,k in itertools.combinations(bounds,2):
 if n not in groups and k not in groups:continue
 if n in groups and k in groups and groups[n]==groups[k]:continue
 if np.any(np.minimum(bounds[n][1],bounds[k][1])-np.maximum(bounds[n][0],bounds[k][0]) < -2.):separated+=1;continue
 pairs.append((n,k))
cache={};placed={}
def shape(n,original=False):
 o=occ[n];d=defs[o['definition']];p=R/d['step'].lstrip('/');inputs[str(p.relative_to(R))]=sha(p)
 if d['id']not in cache:cache[d['id']]=b.import_step(p)
 if original:return t[n]*occurrence_shape(o,cache[d['id']],0,0)
 if n not in placed:placed[n]=pose[n]*occurrence_shape(o,cache[d['id']],0,0)
 return placed[n]
O=R/'cad/engine/generated/accessory-constrained-layout';out=R/'inventory/engine/accessory-constrained-layout-step-check.json';r={'status':'RUNNING','selection':selected,'replacement_carriers_not_accepted':list(skip),'posedelta_yz_mm':{g:v.tolist()for g,v in delta.items()},'mesh_bounds_pad_mm':2,'broadphase_pairs':len(pairs),'bounds_separated_pairs':separated,'exact_checks':[],'failures':[],'input_sha256':inputs}
def save():out.write_text(json.dumps(r,indent=2)+'\n')
save();print('PAIRS',len(pairs),flush=True)
for i,(n,k)in enumerate(pairs):
 a,z=shape(n),shape(k);row={'a':n,'b':k}
 try:
  c=a.intersect(z)
  if isinstance(c,b.ShapeList):c=b.Compound(children=list(c))
  v=solid_volume(c)if c else 0.;row['overlap_mm3']=v;row['distance_mm']=float(a.distance_to(z))
  if v>.1:
   row['adaptive_overlap_mm3']=sum(abs(solid_volume(s,'adaptive'))for s in c.solids());w=O/(n+'__'+k+'-trial-overlap.step');b.export_step(c,w);row['witness']=str(w.relative_to(R));row['witness_sha256']=sha(w);r['failures'].append(row)
 except Exception as ex:row['error']=str(ex);r['failures'].append(row)
 r['exact_checks'].append(row)
 if i%20==0:save();print(i,n,k,flush=True)
# Relevant deliberately wrong pose: old compressor front case against v3cover.
a=shape('ac-compressor-front-cylinder',True);z=shape('timing-cover');c=a.intersect(z);r['wrong_pose_control_overlap_mm3']=solid_volume(c);assert r['wrong_pose_control_overlap_mm3']>.1
r['status']='FAIL exact changed-neighbor scope'if r['failures']else'PASS changed rigid branches q0 only; carriers/belt/hoses still unbuilt';assert all(sha(R/p)==h for p,h in inputs.items());save();print(r['status'],flush=True)
