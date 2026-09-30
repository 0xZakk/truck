#!/usr/bin/env python3
"""Rebuild isolated candidate and explicit limited geometry/flow tests."""
from pathlib import Path
import sys,json,hashlib,itertools,platform
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'cad/engine/generated/air-cleaner-candidate';OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'cad/engine'))
if '--render' in sys.argv:
 preview=np.load(OUT/'preview.npz')
 colors=['#555d65','#39424a','#d9bf83','#b57853']
 # Deterministic actual tessellated geometry views; no protected source pixels embedded.
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from mpl_toolkits.mplot3d.art3d import Poly3DCollection
 from matplotlib.colors import to_rgb
 fig=plt.figure(figsize=(15,7))
 for view in range(2):
  ax=fig.add_subplot(1,2,view+1,projection='3d')
  for i in range(4):
   t=preview[f'v{i}'][preview[f'f{i}']].copy()
   if view: t[:,:,2]+=[0,120,65,95][i]
   n=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-10)
   shade=.45+.55*np.abs(n@np.array([.3,-.6,.74]));ax.add_collection3d(Poly3DCollection(t,facecolors=shade[:,None]*np.array(to_rgb(colors[i])),edgecolor='none'))
  ax.set(xlim=(-215,185),ylim=(-95,95),zlim=(-105,190 if view else 65),xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.set_box_aspect((400,190,295 if view else 170));ax.view_init(25,-140);ax.set_title('Exploded: estimated paper pleats / seal' if view else 'Assembled estimated candidate')
 fig.suptitle('Air cleaner — comparison envelope, body placement and hardware unresolved');fig.tight_layout();fig.savefig(OUT/'candidate-review.png',dpi=150)
 raise SystemExit()
import build123d as b,trimesh
import air_cleaner_candidate as c
from cad_metrics import solid_volume
vol=lambda s:sum(abs(solid_volume(q)) for q in s.solids()) if s else 0
ov=lambda a,d:vol(a.intersect(d))
parts=c.build();tray,lid,paper,seal=parts.values()
exports={};scene=trimesh.Scene();meshes=[]
colors=['#555d65','#39424a','#d9bf83','#b57853']
for i,(k,s) in enumerate(parts.items()):
    print(k,'valid',s.is_valid,'solids',len(s.solids()),flush=True)
    sp=OUT/(k+'.step');b.export_step(s,sp);q=b.import_step(sp)
    v,f=s.tessellate(.08,.15);v=np.array([tuple(x) for x in v]);f=np.array(f)
    mesh=trimesh.Trimesh(v,f);mesh.merge_vertices();meshes.append(mesh)
    gm=trimesh.Trimesh(v[:,[0,2,1]]*np.array([1,1,-1])/1000,f);gm.visual.face_colors=trimesh.visual.color.hex_to_rgba(colors[i]);gm.export(OUT/(k+'.glb'));scene.add_geometry(gm,node_name=k)
    loaded=trimesh.load(OUT/(k+'.glb'),force='mesh')
    glb_error=float(np.max(np.abs(loaded.bounds-gm.bounds))*1000)
    bb=s.bounding_box();bounds=np.array([tuple(bb.min),tuple(bb.max)])
    exports[k]={'valid':s.is_valid,'solids':len(s.solids()),'mesh_watertight':mesh.is_watertight,'glb_roundtrip_bounds_error_mm':glb_error,'step_volume_delta_mm3':abs(vol(q)-vol(s)),'mesh_bounds_error_mm':float(np.max(np.abs(bounds-mesh.bounds)))}
scene.export(OUT/'candidate.glb')
# Air must pass through porous media. These open witnesses separately certify
# inlet-to-dirty chamber and clean chamber-to-each-outlet, not pore permeability.
witnesses={'dirty_inlet':c.cylx(2,-203,200,0,-70),'clean_outlet_a':c.cylx(2,-205,205,-37,30),'clean_outlet_b':c.cylx(2,-205,205,37,30)}
flow={k:sum(ov(w,s) for s in parts.values()) for k,w in witnesses.items()}
blocked={k:ov(w,b.Pos(-180,0,-20)*b.Box(3,160,180)) for k,w in witnesses.items()}
# Continuous rectangular seal coverage at its mid-plane; missing/shifted seal controls.
required=c.box(326.7,148.7,.5,-2.25)-c.box(304,126,1,-2.5)
bypass=vol(required-seal);missing=vol(required);shifted=vol(required-b.Pos(3,0,0)*seal)
collisions={a+' / '+d:ov(parts[a],parts[d]) for a,d in itertools.combinations(parts,2)}
# Contact coverage uses complete annular seating footprint, not only minimum distance.
seat=c.box(326.7,148.7,.1,-4.05)-c.box(304,126,.2,-4.1)
lower_contact=ov(seat,tray);upper_contact=ov(b.Pos(0,0,4)*seat,lid)
passed=all(e['valid'] and e['solids']==1 and e['mesh_watertight'] and e['step_volume_delta_mm3']<.01 and e['mesh_bounds_error_mm']<.2 and e['glb_roundtrip_bounds_error_mm']<.2 for e in exports.values()) and max(flow.values())<.001 and min(blocked.values())>1 and bypass<.001 and min(missing,shifted)>1 and max(collisions.values())<.1 and min(lower_contact,upper_contact)>1
r={'status':'PASS' if passed else 'FAIL','scope':'Isolated candidate; no OEM dimensions, installed fit, media permeability or retained cover claim','input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(c.__file__)]},'environment':{'python':platform.python_version(),'platform':platform.platform(),'build123d':b.__version__,'trimesh':trimesh.__version__},'exports':exports,'collisions_mm3':collisions,'flow_obstruction_mm3':flow,'blocked_flow_fault_mm3':blocked,'perimeter_uncovered_mm3':bypass,'faults':{'missing_seal_mm3':missing,'shifted_seal_mm3':shifted},'seat_probe_overlap_mm3':{'lower':lower_contact,'upper':upper_contact},'limits':['Media modeled as paper pleats, not pore scale','Cover screw retention unknown, NOT RUN','Body mounting and engine motion NOT RUN','Browser integration NOT RUN']}
(ROOT/'inventory/engine/air-cleaner-candidate-validation.json').write_text(json.dumps(r,indent=2)+'\n')
np.savez_compressed(OUT/'preview.npz',**{key:val for i,m in enumerate(meshes) for key,val in [(f'v{i}',m.vertices),(f'f{i}',m.faces)]})
print(json.dumps(r,indent=2));raise SystemExit(0 if passed else 1)
