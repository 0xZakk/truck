#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib,math
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
from timing_coupled_core_candidate import AXIS
O=R/'cad/engine/generated/crossed-oil-drive-corrected-pair';cp=O/'cam-drive-gear-local.step';dp=O/'distributor-drive-gear-local.step';oldp=R/'cad/engine/generated/distributor-drive-gear.step'
cam=b.import_step(cp);dist=b.import_step(dp);old=b.Pos(0,0,85)*b.import_step(oldp)
lead={}
for name,shape in [('cam',b.Rot(0,-90,0)*cam),('distributor',dist)]:
 slopes=[]
 for edge in shape.edges():
  p=edge.position_at(0);q=edge.position_at(1)
  if abs(abs(p.Z-q.Z)-12)>1e-5 or min(math.hypot(p.X,p.Y),math.hypot(q.X,q.Y))<15:continue
  pts=np.array([tuple(edge.position_at(t))for t in np.linspace(0,1,17)]);theta=np.unwrap(np.arctan2(pts[:,1],pts[:,0]));slope=float(np.polyfit(pts[:,2],theta,1)[0]);slopes.append(slope)
 assert slopes and max(abs(x-1/18) for x in slopes)<1e-6
 lead[name]={'actual_helical_edges':len(slopes),'minimum_slope_rad_per_mm':min(slopes),'maximum_slope_rad_per_mm':max(slopes)}
# Inner distributor material and voids contain bore/cross-pin/collar connection.
guard=b.Pos(0,0,9)*b.Cylinder(9,32)
r={'actual_step_lead':lead,'distributor_inner_connection_removed_mm3':solid_volume(old.intersect(guard).cut(dist)),'distributor_inner_connection_added_mm3':solid_volume(dist.intersect(guard).cut(old))}
actualcam=b.import_step(R/'cad/engine/generated/timing-thrust-land-candidate/camshaft.step');sections=[]
for x in [220.584,234.584]:
 sec=b.section(actualcam,b.Plane.YZ.offset(x));bb=sec.bounding_box();sections.append({'x_mm':x,'y_bounds': [bb.min.Y,bb.max.Y],'z_bounds':[bb.min.Z,bb.max.Z]})
r['actual_cam_adjacent_shaft_sections']=sections
core=b.Rot(0,90,0)*b.Cylinder(15,12)
r['candidate_cam_R15_core_missing_mm3']=solid_volume(core.cut(cam))
r['actual_cam_R15_core_missing_mm3']=solid_volume((b.Pos(227.584,*AXIS)*core).cut(actualcam))
r['scope']='Actual STEP helix slope and distributor connection material/void preservation; full camshaft integration remains caller-owned'
r['input_sha256']={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [Path(__file__),cp,dp,oldp,R/'cad/engine/generated/timing-thrust-land-candidate/camshaft.step']}
(R/'inventory/engine/crossed-oil-drive-connection-lead-review.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
