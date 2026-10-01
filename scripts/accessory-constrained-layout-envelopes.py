#!/usr/bin/env python3
"""Actual v3 mesh slab hulls -> conservative 2D translation obstacles."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
from scipy.spatial import ConvexHull
import trimesh
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
from assembly_clockwise_candidate import transforms,occurrence_shape
import build123d as b
mp=R/'inventory/engine/corrected-engine-stage-v3.json';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(mp)=='f512d6024ed4d3d0d86c45c39492b4ab525e039a9c50fb71b67940633b8a2055'
m=json.loads(mp.read_text());t=transforms(m,0,0);defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};assemblies={a['id']:a for a in m['assemblies']}
roots={'ALT':['alternator-assembly'],'AP':['thermactor-pump-assembly'],'PS':['power-steering-pump-assembly'],'AC':['ac-compressor'],'TENS':['tensioner-pulley-assembly','tensioner-support-assembly']};centers={'ALT':[-325,320],'AP':[-280,100],'PS':[280,410],'AC':[280,100],'TENS':[167,350]}
replace=['ps-ac-support-bracket','alternator-thermactor-common-carrier'];fixed_anchor_prefixes=('carrier-','alt-engine-bracket-bolt-')
def owner(o):
 n=o['id']
 if n.startswith('thermactor-engine-bolt-'):return None
 for prefix,g in [('ps-bracket-bolt-','PS'),('ac-bracket-bolt-','AC'),('alt-bracket-bolt-','ALT')]:
  if n.startswith(prefix):return g
 p=o['parent']
 while p:
  for g,rr in roots.items():
   if p in rr:return g
  p=assemblies.get(p,{}).get('parent')
 return None
ownership={n:owner(o) for n,o in occ.items()};inputs={str(p.relative_to(R)):sha(p) for p in [mp,Path(__file__),R/'cad/engine/assembly_clockwise_candidate.py',R/'cad/engine/assembly_math.py',R/'cad/engine/valve_spring_seating_candidate.py']}
O=R/'cad/engine/generated/accessory-constrained-layout';O.mkdir(exist_ok=True)
# Small axial slabs limit false projected overlap. All facets crossing a slab
# boundary contribute exact linear edge intersections, not just in-slab vertices.
breaks=np.arange(250,551,25.);cache={};world={};bounds={}
for i,(n,o) in enumerate(occ.items()):
 if n in replace:continue
 d=defs[o['definition']];p=R/d['glb'].lstrip('/');inputs[str(p.relative_to(R))]=sha(p)
 if d['id'] not in cache:
  mm=trimesh.load(p,force='mesh');cache[d['id']]=(np.asarray(mm.vertices)[:,[0,2,1]]*[1,-1,1]*1000,np.asarray(mm.edges_unique))
 v,edges=cache[d['id']];tr=t[n].wrapped.Transformation();mat=np.array([[tr.Value(k,j) for j in range(1,5)] for k in range(1,4)]);v=v@mat[:,:3].T+mat[:,3]
 if v[:,0].max()<breaks[0] or v[:,0].min()>breaks[-1]:continue
 if o.get('valvetrain',{}).get('role')=='spring':
  sp=R/d['step'].lstrip('/');inputs[str(sp.relative_to(R))]=sha(sp);shape=t[n]*occurrence_shape(o,b.import_step(sp),0,0);vv,ff=shape.tessellate(.1,.2);v=np.array([tuple(q) for q in vv]);ff=np.array(ff);edges=np.unique(np.sort(np.concatenate([ff[:,[0,1]],ff[:,[1,2]],ff[:,[2,0]]]),axis=1),axis=0)
 
 if ownership[n]:assert v[:,0].min()>=breaks[0] and v[:,0].max()<=breaks[-1],('moving axial scope',n,v[:,0].min(),v[:,0].max())
 world[n]=(v,edges);bounds[n]=[v.min(0).tolist(),v.max(0).tolist()]
 if i%150==0:print('read',i,'included',len(world),flush=True)

def hull(v):
 v=np.unique(np.round(v,7),axis=0)
 if len(v)<3:return None
 try:return v[ConvexHull(v).vertices]
 except Exception:return None

def slab(v,e,lo,hi):
 if v[:,0].max()<lo or v[:,0].min()>hi:return None
 ps=[v[(v[:,0]>=lo)&(v[:,0]<=hi),1:]];a=v[e[:,0]];z=v[e[:,1]]
 for x in [lo,hi]:
  valid=((a[:,0]<x)&(z[:,0]>x))|((z[:,0]<x)&(a[:,0]>x));aa=a[valid];zz=z[valid]
  if len(aa):ps.append((aa+(x-aa[:,0,None])/(zz-aa)[:,0,None]*(zz-aa))[:,1:])
 return hull(np.concatenate(ps))
slabs=[]
for lo,hi in zip(breaks[:-1],breaks[1:]):
 moving={g:[] for g in roots};stationary=[]
 for n,(v,e) in world.items():
  h=slab(v,e,lo,hi)
  if h is None:continue
  g=ownership[n]
  if g:moving[g].append(h-np.array(centers[g]))
  else:stationary.append((n,h))
 mh={g:hull(np.concatenate(v)) for g,v in moving.items() if v};slabs.append((float(lo),float(hi),mh,stationary));print('slab',lo,len(stationary),flush=True)
obstacles=[]
for lo,hi,moving,static in slabs:
 for g,a in moving.items():
  for n,z in static:
   p=hull((z[:,None,:]-a[None,:,:]).reshape(-1,2))
   obstacles.append({'group':g,'neighbor':n,'x_slab':[lo,hi],'polygon':p.tolist()})
 # Relative-center obstacle for every moving pair in the same axial slab.
 for gi,g in enumerate(roots):
  if g not in moving:continue
  for k in list(roots)[gi+1:]:
   if k not in moving:continue
   p=hull((moving[k][:,None,:]-moving[g][None,:,:]).reshape(-1,2));obstacles.append({'group':g,'other_group':k,'x_slab':[lo,hi],'polygon':p.tolist()})
# Remove duplicate convex obstacles (thin layer repetitions remain separately).
assert all(sha(R/p)==h for p,h in inputs.items())
r={'status':'COMPLETE conservative numerical obstacles; no layout acceptance','stage_sha256':sha(mp),'axial_breaks_mm':breaks.tolist(),'moving_occurrence_ownership':{g:[n for n in occ if ownership[n]==g] for g in roots},'declared_replacement_carriers':replace,'current_centers_yz_mm':centers,'actual_loaded_front_occurrences':len(world),'obstacles':obstacles,'scope':'Actual transformed v3 GLB facets, actual q0 spring CAD where in front slab. Per-slab convex hulls conservative; tessellation pad required. Final exact STEP check required. All rear-only geometry outsideX250..550 omitted by axial bounds.','input_sha256':inputs};payload=O/'obstacles.json';payload.write_text(json.dumps(obstacles,separators=(',',':'))+'\n');r.pop('obstacles');r.update(obstacle_file=str(payload.relative_to(R)),obstacle_sha256=sha(payload),obstacle_count=len(obstacles));(R/'inventory/engine/accessory-constrained-layout-envelopes.json').write_text(json.dumps(r,indent=2)+'\n');print('obstacles',len(obstacles),flush=True)
