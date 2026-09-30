#!/usr/bin/env python3
"""Local proposed joint checks; explicitly separates unresolved pan integration."""
from pathlib import Path
import sys,json,hashlib,itertools
from dataclasses import asdict,replace
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-cover-shell-candidate';OUT.mkdir(parents=True,exist_ok=True)
if '--render' in sys.argv:
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from mpl_toolkits.mplot3d.art3d import Poly3DCollection
 colors=['#8a9da6','#b88744','#596f6c'];a=np.load(OUT/'preview.npz');fig=plt.figure(figsize=(16,8))
 for view in range(2):
  ax=fig.add_subplot(1,2,view+1,projection='3d')
  for i in range(3):
   key=('c' if view else '')
   t=a[f'{key}v{i}'][a[f'{key}f{i}']].copy()
   if not view:t[:,:,0]+=[25,10,-10][i]
   n=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-10)
   from matplotlib.colors import to_rgb
   shade=.4+.6*np.abs(n@np.array([.5,-.4,.7]));ax.add_collection3d(Poly3DCollection(t,facecolors=shade[:,None]*np.array(to_rgb(colors[i])),edgecolors='none'))
  ax.set(xlim=(350,445),ylim=(-140,245),zlim=(-80,210),xlabel='X mm',ylabel='Y mm',zlabel='Z mm');ax.set_xticks([373,414]);ax.set_box_aspect((95,385,290));ax.view_init(18,155 if view else -30);ax.set_title('Section at Y = 40 mm: seal and rear seating stack' if view else 'Exploded source-shaped shell, gasket and proposed block land')
 fig.suptitle('Isolated estimated timing-cover joint — both gear-axis studies checked\nPan interface is unresolved; this candidate must not be installed');fig.tight_layout();fig.savefig(OUT/'candidate-review.png',dpi=160);raise SystemExit()
sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,trimesh
import timing_cover_shell_candidate as c
import timing_cover_joint_candidate as source
from cad_metrics import solid_volume
vol=lambda s:sum(abs(solid_volume(q)) for q in s.solids()) if s else 0
ov=lambda a,d:vol(a.intersect(d))
p=c.Parameters();parts=c.build(p);shell,gasket,land=parts.values();exports={};preview={};scene=trimesh.Scene()
for i,(k,s) in enumerate(parts.items()):
 print(k,s.is_valid,len(s.solids()),flush=True)
 b.export_step(s,OUT/(k+'.step'));q=b.import_step(OUT/(k+'.step'))
 v,f=s.tessellate(.06,.12);v=np.array([tuple(t) for t in v]);f=np.array(f);preview[f'v{i}']=v;preview[f'f{i}']=f
 m=trimesh.Trimesh(v,f);m.merge_vertices();gm=trimesh.Trimesh(v[:,[0,2,1]]*np.array([1,1,-1])/1000,f);gm.export(OUT/(k+'.glb'));scene.add_geometry(gm,node_name=k)
 loaded=trimesh.load(OUT/(k+'.glb'),force='mesh');bb=s.bounding_box();bounds=np.array([tuple(bb.min),tuple(bb.max)])
 cut=s.intersect(b.Pos(390,-130,60)*b.Box(150,340,350));cv,cf=cut.tessellate(.06,.12);preview[f'cv{i}']=np.array([tuple(t) for t in cv]);preview[f'cf{i}']=np.array(cf)
 exports[k]={'valid':s.is_valid,'solids':len(s.solids()),'mesh_watertight':m.is_watertight,'step_delta_mm3':abs(vol(q)-vol(s)),'cad_mesh_bounds_error_mm':float(np.max(abs(bounds-m.bounds))),'glb_bounds_error_mm':float(np.max(abs(loaded.bounds-gm.bounds))*1000)}
scene.export(OUT/'candidate.glb');np.savez_compressed(OUT/'preview.npz',**preview)
# Full thin probe on each mating side must be supported, not just one point.
face,_,_=c.profiles(p)
probe=c.extrude_x(face,p.block_seat_x,.05)
for pt in source.HOLES_NORMALIZED:
 y,z=c.yz(pt,p);probe-=c.cx(4.2,p.block_seat_x-1,p.block_seat_x+2,y,z)
low=b.Pos(-.05,0,0)*probe;high=b.Pos(p.gasket_thickness,0,0)*probe
seats={'land_uncovered_mm3':vol(low-land),'cover_uncovered_mm3':vol(high-shell),'required_area_mm2':vol(probe)/.05}
shifted=b.Pos(0,5,0)*gasket;faults={'shifted_gasket_outside_land_mm3':vol((b.Pos(-p.gasket_thickness,0,0)*shifted)-land),'removed_gasket_gap_mm':shell.distance_to(land)}
bores=[];walls=[];floors=[];blocked=[]
for pt in source.HOLES_NORMALIZED:
 y,z=c.yz(pt,p);socket=c.cx(3.2,p.block_seat_x-6.9,p.block_seat_x-.1,y,z);bores.append(ov(land,socket));blocked.append(ov(land+socket,socket))
 floor=c.cx(3.3,p.block_seat_x-9.5,p.block_seat_x-7.5,y,z);floors.append(vol(floor-land))
 wall=c.cx(5.3,p.block_seat_x-6.9,p.block_seat_x-.1,y,z)-c.cx(3.4,p.block_seat_x-7,p.block_seat_x,y,z);walls.append(vol(wall-land))
gears={}
for name,cam in [('current_axes',c.CURRENT_CAM),('proposed_axes',p.cam_yz)]:
 es=c.gear_envelopes(replace(p,cam_yz=cam));gears[name]={'cam_yz':cam,'overlap_mm3':[sum(ov(s,e) for s in parts.values()) for e in es],'cover_clearance_mm':[shell.distance_to(e) for e in es]}
seal=c.cx(27,410,418)-c.cx(21,409,419);seal_overlap=ov(shell,seal)
seal_support=c.cx(27.05,410,418)-c.cx(27,409,419)
seal_support_gap=vol(seal_support-shell)
# Exterior support envelope must remain at least 2 mm outside the new relief.
_,outer,_=c.profiles(p);outer_solid=c.extrude_x(outer,378,15)
relief_wall=[]
for cam in (c.CURRENT_CAM,p.cam_yz):
 w=c.cx(c.SOURCE_RADII[1]+p.cam_clearance+2,378.1,392.9,*cam)
 relief_wall.append(vol(w-outer_solid))
# Canonical front pan gasket arc witness, from existing v9 parameters. It is
# deliberately untouched; a conflict is reported as an integration blocker.
pan_arc=(c.cx(61.4,365,381)-c.cx(59.4,364,382)).intersect(b.Pos(373,0,-116)*b.Box(20,400,168))
pan_overlap=ov(shell,pan_arc)
pairs={a+' / '+d:ov(parts[a],parts[d]) for a,d in itertools.combinations(parts,2)}
passed=all(x['valid'] and x['solids']==1 and x['mesh_watertight'] and x['step_delta_mm3']<.01 and x['cad_mesh_bounds_error_mm']<.2 and x['glb_bounds_error_mm']<.2 for x in exports.values()) and max(seats['land_uncovered_mm3'],seats['cover_uncovered_mm3'])<.001 and max(bores+walls+floors+relief_wall)<.001 and min(blocked)>1 and seal_support_gap<.001 and faults['removed_gasket_gap_mm']>.79 and max(pairs.values())<.1 and max(v for g in gears.values() for v in g['overlap_mm3'])<.1 and seal_overlap<.1 and faults['shifted_gasket_outside_land_mm3']>1
r={'local_status':'PASS' if passed else 'FAIL','readiness':'ISOLATED CANDIDATE; NOT FOR INSTALLATION','parameters':asdict(p),'input_sha256':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [Path(__file__),Path(c.__file__),Path(source.__file__)]},'exports':exports,'seat_support':seats,'negative_controls':faults,'blind_socket_obstruction_mm3':bores,'socket_radial_wall_missing_mm3':walls,'socket_bottom_wall_missing_mm3':floors,'blocked_socket_fault_mm3':blocked,'cam_relief_exterior_wall_missing_mm3':relief_wall,'seal_radial_support_missing_mm3':seal_support_gap,'pair_overlap_mm3':pairs,'gear_envelope_tests':gears,'fixed_seal_overlap_mm3':seal_overlap,'pan_joint':{'status':'FAIL' if pan_overlap>.1 else 'NOT RUN','current_front_gasket_arc_overlap_mm3':pan_overlap,'limit':'Only front annulus witness; complete OS34601R and terminal geometry not accepted. Lower bridge does not establish pan seat. Do not install.'},'installed_neighbors':'NOT RUN','browser':'NOT RUN'}
(ROOT/'inventory/engine/timing-cover-shell-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));raise SystemExit(0 if passed else 1)
