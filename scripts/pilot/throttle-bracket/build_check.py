from pathlib import Path
import sys,json,hashlib,importlib.util
import build123d as b
import numpy as np
import trimesh
R=Path(__file__).resolve().parents[3]; C=R/'cad/engine/pilot/throttle-bracket'; I=R/'inventory/engine/pilot/throttle-bracket'; REF=R/'reference/engine/pilot/throttle-bracket'
spec=importlib.util.spec_from_file_location('candidate',C/'candidate.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
s=m.shape(); b.export_step(s,C/'accelerator-cable-bracket.step')
v,f=s.tessellate(.12,.15);mesh=trimesh.Trimesh(np.array([tuple(x) for x in v]),np.array(f));mesh.visual.face_colors=[135,146,151,255];mesh.export(C/'accelerator-cable-bracket.glb')
BASE=Path('/private/tmp/truck-desktop-integration-20260925'); M=BASE/'cad/engine/generated'
checks=[];context={}
def pair(id,n):
 common=s.intersect(n); vol=common.volume if common else 0
 checks.append(dict(id=id,distance_mm=s.distance_to(n),overlap_mm3=vol));context[id]=n
for name in ['throttle-housing','throttle-gasket','iac-valve-body','tps-housing','efi-upper-intake']:
 p=M/(name+'.step')
 if p.exists():
  pose={'iac-valve-body':(397,25,540),'tps-housing':(394,-44,490)}.get(name,(0,0,0));pair(name,b.Pos(*pose)*b.import_step(p))
for z in m.PARAMS['mount_z']:
 pair('stud-'+str(z),b.Pos(371,74,z)*b.import_step(M/'throttle-mount-stud.step'))
 pair('baseline-nut-'+str(z),b.Pos(381.5,74,z)*b.import_step(M/'throttle-mount-nut.step'))
 pair('candidate-shifted-nut-'+str(z),b.Pos(383.5,74,z)*b.import_step(M/'throttle-mount-nut.step'))
for angle in [0,45,90]:
 for y in [-27,27]:
  pair(f'plate-{y}-angle-{angle}',b.Pos(394,25,490)*b.Rot(0,angle,0)*b.Pos(0,y,0)*b.import_step(M/'throttle-plate.step'))
pair('throttle-shaft',b.Pos(394,25,490)*b.import_step(M/'throttle-shaft.step'))
# Real face contact area, not only zero minimum distance.
housing=context['throttle-housing']; contact=[]
for a in s.faces():
 for c in housing.faces():
  common=a.intersect(c)
  if common:contact.append(sum(q.area for q in common))
arrays={};meta=[]
for name,obj in {'bracket':s,**context}.items():
 vv,ff=obj.tessellate(.3,.25);i=len(meta);arrays[f'v{i}']=np.array([tuple(v) for v in vv]);arrays[f'f{i}']=np.array(ff);meta.append(name)
arrays['metadata']=np.array(json.dumps(meta));np.savez_compressed(REF/'preview.npz',**arrays)
report=dict(status='candidate-not-production-accepted',valid=s.is_valid,solids=len(s.solids()),volume_mm3=s.volume,bounds_mm=[list(s.bounding_box().min),list(s.bounding_box().max)],mesh_watertight=mesh.is_watertight,checks=checks,housing_coplanar_contact_area_mm2=sum(contact),params=m.PARAMS,source_dimension_count=0,baseline_datum_count=5,limitations=m.GAPS,input_hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [C/'candidate.py',Path(__file__),REF/'salvage-photo.jpg',BASE/'inventory/engine/full-assembly.json']})
(I/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
