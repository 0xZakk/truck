#!/usr/bin/env python3
import sys,json,hashlib,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import shifted_oil_pickup_candidate as c
from assembly_math import transforms
OUT=ROOT/'cad/engine/generated/shifted-oil-pickup-candidate';OUT.mkdir(exist_ok=True)
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());poses=transforms(m);defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']}
inputs={}
def bind(p):
 p=str(p);inputs[p]=hashlib.sha256((ROOT/p).read_bytes()).hexdigest();return ROOT/p
def vol(s):return sum(v.volume for v in s.solids()) if s else 0.
def get(i,shift=False):
 p=defs[occ[i]['definition']]['step'].lstrip('/');return (b.Pos(*c.DELTA) if shift else b.Pos())*poses[i]*b.import_step(bind(p))
for p in ['scripts/check-shifted-oil-pickup-candidate.py','cad/engine/shifted_oil_pickup_candidate.py','cad/engine/oil_drive_layout.py','cad/engine/timing_block_axis_feature_candidate.py','inventory/engine/full-assembly.json']:bind(p)
old=get('oil-pickup-tube');q,data=c.build(old)
print('built',q.is_valid,len(q.solids()),flush=True)
mask=b.Pos(sum(c.MASK_X)/2,0,0)*b.Box(c.MASK_X[1]-c.MASK_X[0],2000,2000)
a=old.cut(mask);z=q.cut(mask);outside=vol(a.cut(z))+vol(z.cut(a));print('outside',outside,flush=True)
rows=[]
for i in ['oil-pump-housing','oil-pump-inner-rotor','oil-pump-outer-rotor','oil-pump-cover','oil-pickup-bell','oil-pickup-screen']:
 s=get(i,i.startswith('oil-pump-'));rows.append({'neighbor':i,'overlap_mm3':vol(q.intersect(s)),'distance_mm':q.distance_to(s)});print(rows[-1],flush=True)
for name,p in [('block','cad/engine/generated/timing-front-block-expanded-seat-v3-candidate/block.step'),('pan','cad/engine/generated/timing-pan-expanded-seat-v2-candidate/pan.step')]:
 s=b.import_step(bind(p));rows.append({'neighbor':name,'overlap_mm3':vol(q.intersect(s)),'distance_mm':q.distance_to(s)});print(rows[-1],flush=True)
p=OUT/'oil-pickup-tube-world.step';b.export_step(q,p)
local=poses['oil-pickup-tube'].inverse()*q;lp=OUT/'oil-pickup-tube.step';b.export_step(local,lp)
rt=b.import_step(lp);print('export',flush=True)
import numpy as np,trimesh
v,t=rt.tessellate(.12,.12);verts=np.array([tuple(x) for x in v]);mesh=trimesh.Trimesh(verts[:,[0,2,1]]*[1,1,-1]/1000,np.array(t),process=True);mesh.fix_normals();gp=OUT/'oil-pickup-tube.glb';mesh.export(gp)
mm=trimesh.load(gp,force='mesh');mm.merge_vertices(digits_vertex=8);vv=mm.vertices[:,[0,2,1]]*[1,-1,1]*1000;bb=rt.bounding_box();err=float(np.max(np.abs(np.array([vv.min(0),vv.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))))
report={'status':'CANDIDATE built; contact/passage and visual gates pending','inputs':inputs,'valid':q.is_valid,'solid_count':len(q.solids()),'change_mask_world_x_mm':c.MASK_X,'outside_mask_difference_mm3':outside,'splice_mm':list(data['splice']),'inlet_mm':list(data['start']),'insertion_estimate_mm':c.INSERTION_MM,'neighbors':rows,'roundtrip_volume_error_mm3':abs(vol(local)-vol(rt)),'mesh':{'watertight':bool(mm.is_watertight),'winding_consistent':bool(mm.is_winding_consistent),'positive_volume':bool(mm.volume>0),'bounds_error_mm':err,'triangles':len(mm.faces)},'artifacts':{str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in [p,lp,gp]},'limits':['Incomplete pump discharge/gasket/block gallery unchanged','No fluid performance or factory dimensions','Contact and passage acceptance pending independent actual probes']}
(ROOT/'inventory/engine/shifted-oil-pickup-candidate-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],flush=True)
