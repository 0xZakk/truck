#!/usr/bin/env python3
"""Only isolated topology/export checks; never installed-joint acceptance."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-cover-joint-candidate';OUT.mkdir(parents=True,exist_ok=True)
if '--render' in sys.argv:
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from mpl_toolkits.mplot3d.art3d import Poly3DCollection
 a=np.load(OUT/'preview.npz');v=a['v'];f=a['f'];t=v[f]
 fig=plt.figure(figsize=(12,6));ax=fig.add_subplot(121)
 from matplotlib.collections import PolyCollection
 ax.add_collection(PolyCollection(t[:,:,[1,2]],facecolors='#687d72',edgecolors='none'));ax.autoscale();ax.set_aspect('equal');ax.set(xlabel='Source-view Y (mm)',ylabel='Source-view Z (mm)',title='Seven holes; bottom intentionally open')
 ax=fig.add_subplot(122,projection='3d');ax.add_collection3d(Poly3DCollection(t,facecolors='#687d72',edgecolors='none'));ax.set(xlim=(-1,1),ylim=(-155,160),zlim=(-5,185),xlabel='X',ylabel='Y',zlabel='Z');ax.set_box_aspect((12,315,190));ax.view_init(18,15);ax.set_title('0.8 mm estimated sheet; no engine transform')
 fig.suptitle('Timing-cover main gasket topology candidate\nManufacturer outline comparison; arbitrary mm display scale, installed joint unresolved');fig.tight_layout();fig.savefig(OUT/'candidate-review.png',dpi=160);raise SystemExit()
sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,trimesh
import timing_cover_joint_candidate as c
from cad_metrics import solid_volume
vol=lambda s:sum(abs(solid_volume(q)) for q in s.solids()) if s else 0
shape=next(iter(c.build().values()));b.export_step(shape,OUT/'main-gasket.step');q=b.import_step(OUT/'main-gasket.step')
v,f=shape.tessellate(.035,.12);v=np.array([tuple(x) for x in v]);f=np.array(f);mesh=trimesh.Trimesh(v,f);mesh.merge_vertices()
glb=trimesh.Trimesh(v[:,[0,2,1]]*np.array([1,1,-1])/1000,f);glb.export(OUT/'main-gasket.glb');reimport=trimesh.load(OUT/'main-gasket.glb',force='mesh')
np.savez_compressed(OUT/'preview.npz',v=v,f=f)
obstructions=[];faults=[]
for p in c.HOLES_NORMALIZED:
 y,z=c.yz(p);w=c.axial_cylinder(3.5,y,z);obstructions.append(vol(shape.intersect(w)));faults.append(vol((shape+c.axial_cylinder(4.2,y,z,0,.8)).intersect(w)))
# Main opening and lower gap are geometrically open, not a claim of oil sealing.
w=b.Pos(.4,0,45)*b.Box(.5,60,95);opened=vol(shape.intersect(w));bridge=b.Pos(.4,0,0)*b.Box(.8,80,5);bridge_fault=vol(bridge.intersect(w))
err=float(np.max(np.abs(reimport.bounds-glb.bounds))*1000);delta=abs(vol(shape)-vol(q))
passed=shape.is_valid and len(shape.solids())==1 and mesh.is_watertight and delta<.01 and err<.2 and max(obstructions)<.001 and min(faults)>1 and opened<.001 and bridge_fault>1
r={'status':'PASS' if passed else 'FAIL','scope':'Source-proportioned isolated topology only; coordinated sealing joint NOT RUN','input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(c.__file__)]},'valid':shape.is_valid,'solid_count':len(shape.solids()),'mesh_watertight':mesh.is_watertight,'step_roundtrip_volume_delta_mm3':delta,'glb_roundtrip_bounds_error_mm':err,'seven_hole_obstructions_mm3':obstructions,'seven_plug_faults_mm3':faults,'opening_obstruction_mm3':opened,'bottom_bridge_fault_mm3':bridge_fault,'installed_gates':{'continuous_seating':'NOT RUN; mating flanges and registration unresolved','pan_junction':'NOT RUN; lower strip function/terminal contact unresolved','shaft_gear_clearance':'NOT RUN; no engine transform','browser':'NOT RUN; isolated study'}}
(ROOT/'inventory/engine/timing-cover-joint-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));raise SystemExit(0 if passed else 1)
