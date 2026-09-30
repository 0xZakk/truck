#!/usr/bin/env python3
"""Isolated estimated vent geometry: no installed or calibrated EVR claim."""
from pathlib import Path
import sys,json,hashlib,itertools
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/evr-detail-candidate'
if '--render' in sys.argv:
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from mpl_toolkits.mplot3d.art3d import Poly3DCollection
 from matplotlib.colors import to_rgb
 a=np.load(OUT/'preview.npz');fig=plt.figure(figsize=(10,8));ax=fig.add_subplot(projection='3d');tris=[];colors=[]
 for i,color in enumerate(['#727c81','#9dabb4','#d5b674']):
  t=a[f'cv{i}'][a[f'cf{i}']]
  n=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-12);shade=.4+.6*np.abs(n@np.array([.3,-.8,.5]));tris.extend(t);colors.extend(shade[:,None]*np.array(to_rgb(color)))
 ax.add_collection3d(Poly3DCollection(tris,facecolors=colors,edgecolor='none'))
 ax.set(xlim=(-20,34),ylim=(-5,35),zlim=(-9,60),xlabel='Local X mm',ylabel='Y',zlabel='Z');ax.set_box_aspect((54,40,69));ax.view_init(18,-65)
 ax.set_title('EVR estimated vent/filter section\nLower source port remains unfinished; no regulating valve');fig.tight_layout();fig.savefig(OUT/'candidate-review.png',dpi=160);raise SystemExit
sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,trimesh
import evr,evr_detail_candidate as c
from cad_metrics import solid_volume
vol=lambda s:sum(abs(solid_volume(q)) for q in s.solids()) if s else 0
ov=lambda a,d:vol(a.intersect(d))
ledger=json.loads((ROOT/'reference/engine/evr-detail-review.json').read_text())
for row in ledger['local_sources']:assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256'], row['path']
parts=c.build();body,cap,filt=parts.values();base=evr.body()
# Exact face-area contact and protected outer functional regions.
def contact(a,d):
 return sum((q.area if q else 0) for f in a.faces() for g in d.faces() if f.geom_type==g.geom_type==b.GeomType.PLANE and f.distance_to(g)<1e-7 for q in [f.intersect(g)])
protected={'ears':b.Pos(0,0,27)*b.Box(8,70,14)-b.Pos(0,0,27)*b.Box(10,31,16),'connector':b.Pos(26,0,31)*b.Box(24,22,20),'nipple_ends':b.Pos(23,0,8)*b.Box(18,12,28)}
diff=b.Compound(children=list((body-base).solids())+list((base-body).solids()));preserved={k:ov(diff,s) for k,s in protected.items()}
# A connected volume witness from upper nipple through well, pore and side inlet.
w=(c.cx(.2,0,31,15)+c.cz(.2,40,15)+c.cx(.2,-19,38,54))
# Connections overlap and pore at origin guarantees a real passage through filter.
flow=sum(ov(w,s) for s in parts.values());blocked=ov(w,b.Pos(0,0,49)*b.Box(3,3,.5))
contacts={'lower':contact(body,filt),'upper':contact(cap,filt)}
collisions={a+' / '+d:ov(parts[a],parts[d]) for a,d in itertools.combinations(parts,2)}
# Missing/oversize filter and closed-inlet controls are intentionally invalid.
oversize=ov(c.cz(13.5,2,48),cap);seat_missing_gap=(b.Pos(0,0,.5)*filt).distance_to(body)
OUT.mkdir(parents=True,exist_ok=True);preview={};exports={};scene=trimesh.Scene()
for i,(k,s) in enumerate(parts.items()):
 from OCP.BRepTools import BRepTools
 BRepTools.Clean_s(s.wrapped)
 v,f=s.tessellate(.015,.08);v=np.array([tuple(p) for p in v]);f=np.array(f);preview[f'v{i}']=v;preview[f'f{i}']=f
 cut=s.intersect(b.Pos(0,50,25)*b.Box(100,100,100));cv,cf=cut.tessellate(.04,.12);preview[f'cv{i}']=np.array([tuple(p) for p in cv]);preview[f'cf{i}']=np.array(cf)
 sp=OUT/(k+'.step');b.export_step(s,sp);q=b.import_step(sp);mesh=trimesh.Trimesh(v[:,[0,2,1]]*np.array([1,1,-1])/1000,f);mesh.merge_vertices(digits_vertex=8);mesh.update_faces(mesh.unique_faces());mesh.update_faces(mesh.nondegenerate_faces());mesh.export(OUT/(k+'.glb'));scene.add_geometry(mesh,node_name=k)
 exports[k]={'valid':s.is_valid,'solids':len(s.solids()),'watertight':mesh.is_watertight,'step_volume_delta':abs(vol(q)-vol(s))}
np.savez_compressed(OUT/'preview.npz',**preview);scene.export(OUT/'candidate.glb')
paths=[Path(__file__),Path(c.__file__),Path(evr.__file__),ROOT/'reference/engine/evr-detail-review.json'];hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
passed=max(preserved.values())<1e-5 and max(collisions.values())<1e-5 and min(contacts.values())>100 and flow<1e-5 and blocked>.01 and oversize>1 and seat_missing_gap>.4 and all(e['valid'] and e['solids']==1 and e['watertight'] and e['step_volume_delta']<.001 for e in exports.values())
r={'status':'PASS' if passed else 'FAIL','scope':'Isolated illustrative vent/filter only; source port and regulating mechanism unfinished; not integration ready','input_sha256':hashes,'protected_region_change_mm3':preserved,'contact_mm2':contacts,'collision_mm3':collisions,'flow_witness_obstruction_mm3':flow,'faults':{'blocked_witness_mm3':blocked,'oversize_overlap_mm3':oversize,'unseated_gap_mm':seat_missing_gap},'exports':exports,'installed_neighbors':'NOT RUN: isolated candidate only; no promotion permitted'}
(ROOT/'inventory/engine/evr-detail-candidate-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));raise SystemExit(0 if passed else 1)
