#!/usr/bin/env python3
"""Frozen trial0 matched carrier; actual neighbor and named-seat checks."""
from pathlib import Path
import sys,json,hashlib
import numpy as np,trimesh
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import accessory_psac_carrier_candidate as src
import accessory_brackets as base
from assembly_clockwise_candidate import transforms,occurrence_shape
from cad_metrics import solid_volume
O=R/'cad/engine/generated/accessory-psac-carrier';O.mkdir(exist_ok=True);rp=R/'inventory/engine/accessory-psac-carrier-trial0-check.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();inputs={str(p.relative_to(R)):sha(p)for p in [Path(__file__),Path(src.__file__),Path(base.__file__),R/'inventory/engine/accessory-constrained-layout-step-check.json',R/'inventory/engine/accessory-constrained-layout-envelopes.json',R/'cad/engine/assembly_clockwise_candidate.py']}
r={'status':'RUNNING','scope':'Conditional trial0 at frozen selected centers; no installation','inputs':inputs,'neighbors':[],'seats':[],'pump_sensitivity':[]}
def save():rp.write_text(json.dumps(r,indent=2)+'\n')
def mesh(shape,path):
 v,f=shape.tessellate(.1,.2);mm=trimesh.Trimesh(vertices=np.array([tuple(x)for x in v]),faces=np.array(f),process=False);mm.export(path);return mm
shape=src.carrier();r['shape']={'valid':shape.is_valid,'solids':len(shape.solids()),'volume_mm3':solid_volume(shape),'bounds':[tuple(shape.bounding_box().min),tuple(shape.bounding_box().max)]};print(r['shape'],flush=True);assert shape.is_valid and len(shape.solids())==1 and shape.bounding_box().max.Y>400 and shape.bounding_box().min.X<300 and shape.bounding_box().max.Z>400,r['shape'];b.export_step(shape,O/'trial0-carrier.step');mesh(shape,O/'trial0-carrier.ply');save()
mp=R/'inventory/engine/corrected-engine-stage-v3.json';inputs[str(mp.relative_to(R))]=sha(mp);m=json.loads(mp.read_text());t=transforms(m,0,0);ds={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};e=json.loads((R/'inventory/engine/accessory-constrained-layout-envelopes.json').read_text());groups={n:g for g,ids in e['moving_occurrence_ownership'].items()for n in ids};pose={};cache={};bounds={};cb=np.array(r['shape']['bounds'])
for n,o in occ.items():
 if n=='ps-ac-support-bracket':continue
 d=ds[o['definition']];p=R/d['glb'].lstrip('/');inputs[str(p.relative_to(R))]=sha(p);vv=np.asarray(trimesh.load(p,force='mesh').vertices)[:,[0,2,1]]*[1,-1,1]*1000;g=groups.get(n);pose[n]=b.Pos(0,*src.SELECT['posedelta_yz_mm'][g])*t[n]if g else t[n];tr=pose[n].wrapped.Transformation();a=np.array([[tr.Value(i,j)for j in range(1,5)]for i in range(1,4)]);vv=vv@a[:,:3].T+a[:,3];bounds[n]=np.array([vv.min(0),vv.max(0)])
def actual(n):
 if n not in cache:
  o=occ[n];p=R/ds[o['definition']]['step'].lstrip('/');inputs[str(p.relative_to(R))]=sha(p);cache[n]=pose[n]*occurrence_shape(o,b.import_step(p),0,0)
 return cache[n]
def overlap(a,z):
 c=a.intersect(z)
 if isinstance(c,b.ShapeList):c=b.Compound(children=list(c))
 return c,solid_volume(c)if c else 0
# Frozen proposed ALT/AP replaces its old occurrence for this pair audit.
p=R/'cad/engine/generated/accessory-matched-carriers/trial6-carrier.step';inputs[str(p.relative_to(R))]=sha(p);a=b.import_step(p);cache['alternator-thermactor-common-carrier']=a;bb=a.bounding_box();bounds['alternator-thermactor-common-carrier']=np.array([tuple(bb.min),tuple(bb.max)])
pairs=[n for n,bb in bounds.items()if np.all(np.minimum(cb[1],bb[1])-np.maximum(cb[0],bb[0])>=-2)]
r['broadphase_pairs']=len(pairs);print('PAIRS',len(pairs),flush=True)
for n in pairs:
 row={'neighbor':n}
 try:
  a=actual(n);c,v=overlap(shape,a);row.update(overlap_mm3=v,distance_mm=float(shape.distance_to(a)))
  if v>.1:
   p=O/f'trial0-overlap__{n}.step';b.export_step(c,p);row['witness']=str(p.relative_to(R))
 except Exception as ex:row['error']=str(ex)
 r['neighbors'].append(row);save();print(n,row,flush=True)
# Independent named mating witnesses; face orientation is explicit.
def ann(x,y,z,ri,ro,width=.02):return base.boss(x,y,z,ro,ri,width)
def seat(name,front,back,owner):
 row={'name':name,'owner':owner,'carrier_missing_mm3':solid_volume(front.cut(shape)),'mate_missing_mm3':solid_volume(back.cut(actual(owner))),'witness_mm3':solid_volume(front)};r['seats'].append(row)
seat('front-head',ann(373,90,300,5.5,12),ann(372.98,90,300,5.5,12),'cylinder-head')
for i,(x,z)in enumerate(src.SIDE):
 f=src.old.sideways(14,.02,x,135.01,z).cut(src.old.sideways(5.5,.04,x,135.01,z));back=b.Pos(0,-.02,0)*f;seat('side-'+str(i),f,back,'cylinder-head'if i==2 else'block')
for g,ears,ri,ro,owner in [('PS',src.PS_EARS,4.8,10,'ps-pump-housing'),('AC',src.AC_EARS,5.5,11,'ac-compressor-front-cylinder')]:
 for i,(y,z)in enumerate(ears):seat(g+'-'+str(i),ann(src.FACE,y,z,ri,ro),ann(src.FACE-.02,y,z,ri,ro),owner)
ty,tz=src.PIVOT;front=ann(400.54,ty,tz,8,32).cut(base.axial(6.35,.1,(400.55,ty+20,tz)));seat('tensioner-cartridge',front,b.Pos(.02,0,0)*front,'tensioner-spring-cartridge')
# Separate candidates never silently replace current v3 neighbors.
for label,p in [('pump-'+l,R/f'cad/engine/generated/waterpump-source-offset-inlet-candidate/{l}-housing.step')for l in ['nominal','low-offset','high-offset']]+[('rear-cover',R/'cad/engine/generated/timing-pump-rear-flange-candidate/cover.step')]:
 inputs[str(p.relative_to(R))]=sha(p);a=b.import_step(p);c,v=overlap(shape,a);row={'hypothesis':label,'overlap_mm3':v,'distance_mm':float(shape.distance_to(a))}
 if v>.1:b.export_step(c,O/f'trial0-{label}-overlap.step')
 r['pump_sensitivity'].append(row);save()
r['shaft_beltplane_contract']={'world_delta_X_mm':0,'rotations_unchanged':True,'belt_plane_estimate_X_mm':473.56,'proposed_centers':src.C,'meaning':'Actual rigid branches retain each original shaft axis and axial pulley envelope; production alignment unknown'}
r['status']='COMPLETE trial0 conditional support; inspect failures, not installed';r['artifacts_sha256']={str(p.relative_to(R)):sha(p)for p in O.glob('*')if p.is_file()};assert all(sha(R/p)==h for p,h in inputs.items());save();print(r['status'],flush=True)
