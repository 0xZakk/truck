#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import trimesh
from OCP.BRepTools import BRepTools
import cam_composed_drive_candidate as c
from timing_coupled_core_candidate import AXIS
from cad_metrics import solid_volume
O=R/'cad/engine/generated/cam-composed-drive-candidate';O.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return solid_volume(s) if s is not None else 0
def diff(a,z):return vol(a.cut(z))+vol(z.cut(a))
base=b.import_step(c.CAM);gear=b.Pos(c.X,0,0)*b.import_step(c.GEAR);new=c.build();print('Built single valid solid',flush=True)
b.export_step(new,O/'camshaft-local.step');new=b.import_step(O/'camshaft-local.step');assert new.is_valid and len(new.solids())==1
# Exact shared boundaries, no relaxed mask or material metric.
mask=c.mask();outside=diff(base.cut(mask),new.cut(mask));print('Outside',outside,flush=True);assert outside<1e-5
window=b.Pos(c.X,0,0)*b.Box(12,100,100);actualgear=new.intersect(window);gear_error=diff(actualgear,gear);print('Gear window',gear_error,flush=True);assert gear_error<1e-5
core=c.cylinder(c.CORE);core_error=vol(core.cut(new));assert core_error<1e-5
fault=new.cut(b.Pos(0,0,0)*b.Sphere(.5));fault_error=diff(new.cut(mask),fault.cut(mask));assert fault_error>.4
# Wrong signed gear is detected by actual edge pitch rather than unreliable changed volume.
slopes=[]
for edge in actualgear.edges():
 p=np.array([tuple(edge.position_at(t))for t in np.linspace(0,1,17)])
 if np.ptp(p[:,0])<11.9:continue
 slope=float(np.polyfit(p[:,0],np.unwrap(np.arctan2(p[:,2],p[:,1])),1)[0])
 if abs(slope)>1e-3:slopes.append(slope)
assert len(slopes)==304 and max(abs(x-1/18)for x in slopes)<1e-6
world=b.Pos(0,*AXIS)*new;b.export_step(world,O/'camshaft.step');w=b.import_step(O/'camshaft.step');world_error=diff(b.Pos(0,-AXIS[0],-AXIS[1])*w,new);assert world_error<.001
BRepTools.Clean_s(new.wrapped);v,f=new.tessellate(.05,.1)
mesh=trimesh.Trimesh(np.array([tuple(x)for x in v])[:,[0,2,1]]*[1,1,-1]/1000,np.array(f));mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();mesh.export(O/'camshaft-local.glb')
mesh=trimesh.load(O/'camshaft-local.glb',force='mesh');mesh.merge_vertices(digits_vertex=8);assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
v=mesh.vertices[:,[0,2,1]]*[1,-1,1]*1000;bb=new.bounding_box();bounds=float(np.max(abs(np.array([v.min(0),v.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))));assert bounds<.15
wb=w.bounding_box();wbounds=float(np.max(abs(np.array([v.min(0),v.max(0)])+[0,*AXIS]-np.array([tuple(wb.min),tuple(wb.max)]))));assert wbounds<.15
r={'status':'PASS bounded composed fullcam','outside_exact_mask_difference_mm3':outside,'actual_gear_window_difference_mm3':gear_error,'R15_core_missing_mm3':core_error,'protected_notch_control_mm3':fault_error,'positive_helix_edge_count':len(slopes),'lead_range_rad_per_mm':[min(slopes),max(slopes)],'local_world_roundtrip_difference_mm3':world_error,'mesh':{'watertight':True,'winding_consistent':True,'positive_volume':True,'triangles':len(mesh.faces),'local_bounds_error_mm':bounds,'world_bounds_error_mm':wbounds},'input_sha256':{str(p.relative_to(R)):sha(p)for p in [Path(__file__),Path(c.__file__),c.CAM,c.GEAR,R/'cad/engine/timing_coupled_core_candidate.py']},'output_sha256':{str(p.relative_to(R)):sha(p)for p in O.glob('*')if p.suffix in ['.step','.glb']}}
(R/'inventory/engine/cam-composed-drive-build-review.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2),flush=True)
