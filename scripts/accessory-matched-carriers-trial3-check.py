#!/usr/bin/env python3
"""Frozen trial3 matched carrier; actual neighbor and named-seat checks."""
from pathlib import Path
import sys,json,hashlib
import numpy as np,trimesh
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import accessory_matched_carriers_trial3 as src
import accessory_brackets as base
from assembly_clockwise_candidate import transforms,occurrence_shape
from cad_metrics import solid_volume
O=R/'cad/engine/generated/accessory-matched-carriers';O.mkdir(exist_ok=True);rp=R/'inventory/engine/accessory-matched-carriers-trial3-check.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();inputs={str(p.relative_to(R)):sha(p)for p in [Path(__file__),Path(src.__file__),Path(base.__file__),R/'inventory/engine/accessory-constrained-layout-step-check.json',R/'inventory/engine/accessory-constrained-layout-envelopes.json',R/'cad/engine/assembly_clockwise_candidate.py']}
r={'status':'RUNNING','scope':'Conditional trial3 at frozen selected centers; no installation','inputs':inputs,'neighbors':[],'seats':[],'pump_sensitivity':[]}
def save():rp.write_text(json.dumps(r,indent=2)+'\n')
def mesh(shape,path):
 v,f=shape.tessellate(.1,.2);mm=trimesh.Trimesh(vertices=np.array([tuple(x)for x in v]),faces=np.array(f),process=False);mm.export(path);return mm
shape=src.carrier();r['shape']={'valid':shape.is_valid,'solids':len(shape.solids()),'volume_mm3':solid_volume(shape),'bounds':[tuple(shape.bounding_box().min),tuple(shape.bounding_box().max)]};print(r['shape'],flush=True);assert shape.is_valid and len(shape.solids())==1 and shape.bounding_box().min.Y < -340 and shape.bounding_box().max.Z>310,r['shape'];b.export_step(shape,O/'trial3-carrier.step');mesh(shape,O/'trial3-carrier.ply');save()
mp=R/'inventory/engine/corrected-engine-stage-v3.json';inputs[str(mp.relative_to(R))]=sha(mp);m=json.loads(mp.read_text());t=transforms(m,0,0);ds={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};e=json.loads((R/'inventory/engine/accessory-constrained-layout-envelopes.json').read_text());groups={n:g for g,ids in e['moving_occurrence_ownership'].items()for n in ids};pose={};cache={};bounds={};cb=np.array(r['shape']['bounds'])
for n,o in occ.items():
 if n=='alternator-thermactor-common-carrier':continue
 d=ds[o['definition']];p=R/d['glb'].lstrip('/');inputs[str(p.relative_to(R))]=sha(p);vv=np.asarray(trimesh.load(p,force='mesh').vertices)[:,[0,2,1]]*[1,-1,1]*1000;g=groups.get(n);pose[n]=b.Pos(0,*src.SELECT['posedelta_yz_mm'][g])*t[n]if g else t[n];tr=pose[n].wrapped.Transformation();a=np.array([[tr.Value(i,j)for j in range(1,5)]for i in range(1,4)]);vv=vv@a[:,:3].T+a[:,3];bounds[n]=np.array([vv.min(0),vv.max(0)])
def actual(n):
 if n not in cache:
  o=occ[n];p=R/ds[o['definition']]['step'].lstrip('/');inputs[str(p.relative_to(R))]=sha(p);cache[n]=pose[n]*occurrence_shape(o,b.import_step(p),0,0)
 return cache[n]
def overlap(a,z):
 c=a.intersect(z)
 if isinstance(c,b.ShapeList):c=b.Compound(children=list(c))
 return c,solid_volume(c)if c else 0
pairs=[n for n,bb in bounds.items()if np.all(np.minimum(cb[1],bb[1])-np.maximum(cb[0],bb[0])>=-2)]
r['broadphase_pairs']=len(pairs);print('PAIRS',len(pairs),flush=True)
for n in pairs:
 row={'neighbor':n}
 try:
  a=actual(n);c,v=overlap(shape,a);row.update(overlap_mm3=v,distance_mm=float(shape.distance_to(a)))
  if v>.1:
   p=O/f'trial3-overlap__{n}.step';b.export_step(c,p);row['witness']=str(p.relative_to(R))
 except Exception as ex:row['error']=str(ex)
 r['neighbors'].append(row);save();print(n,row,flush=True)
# Seat witnesses straddle no artificial replacement of mate. Engine contact R12,
# actual boss R16 means original flange overhang remains explicitly separate.
seats=[('engine-'+str(i),373,y,z,5.5,12,None)for i,(y,z)in enumerate(src.ENGINE_SEATS)]
seats += [(g+'-'+str(i),src.FACES[g],y,z,5.5,11,'alternator-drive-housing'if g=='ALT'else'thermactor-front-plate')for g in src.EARS for i,(y,z)in enumerate(src.EARS[g])]
for name,x,y,z,ri,ro,owner in seats:
 w=base.boss(x,y,z,ro,ri,width=.02);back=base.boss(x-.02,y,z,ro,ri,width=.02);area=np.pi*(ro*ro-ri*ri);missing=solid_volume(w.cut(shape));owners=[owner]if owner else [n for n in pairs if n in ['engine-block','cylinder-head','block']];mate=back
 for n in owners:mate=mate.cut(actual(n))
 row={'name':name,'axis_world_mm':[x,y,z],'annulus_radii_mm':[ri,ro],'nominal_area_mm2':area,'carrier_missing_mm3':missing,'mate_missing_mm3':solid_volume(mate),'mate_owners':owners};r['seats'].append(row)
# Source inherited clearance holes/bolts retain engagement geometry but no threads.
for label in ['nominal','low-offset','high-offset']:
 p=R/f'cad/engine/generated/waterpump-source-offset-inlet-candidate/{label}-housing.step';inputs[str(p.relative_to(R))]=sha(p);a=b.import_step(p);c,v=overlap(shape,a);row={'hypothesis':label,'overlap_mm3':v,'distance_mm':float(shape.distance_to(a))}
 if v>.1:b.export_step(c,O/f'trial3-pump-{label}-overlap.step')
 r['pump_sensitivity'].append(row);save()
r['status']='COMPLETE trial3; inspect explicit failures, not installed';r['artifacts_sha256']={str(p.relative_to(R)):sha(p)for p in O.glob('*')if p.is_file()};assert all(sha(R/p)==h for p,h in inputs.items());save();print(r['status'],flush=True)
