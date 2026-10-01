#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from timing_coupled_core_candidate import AXIS
import oil_drive_layout as d
from cad_metrics import solid_volume
O=R/'cad/engine/generated/crossed-oil-drive-corrected-pair';cp=O/'cam-drive-gear-local.step';dp=O/'distributor-drive-gear-local.step';cam=b.Pos(d.DRIVE_X,*AXIS)*b.import_step(cp);df=b.Pos(0,AXIS[0]-90,AXIS[1]-72)*d.GEAR_FRAME;dist=b.import_step(dp);rows=[]
for angle in [-1,-.75,-.5,.5,.75,1]:
 p=df*b.Rot(0,0,angle)*dist;distance=cam.distance_to(p);common=cam.intersect(p) if distance<1e-7 else None
 try:vol=solid_volume(common) if common is not None else 0;err=None
 except Exception as e:vol=None;err=str(e)
 row={'fixed_cam_degrees':0,'distributor_phase_error_degrees':angle,'distance_mm':distance,'overlap_mm3':vol,'metric_error':err};rows.append(row);print(row,flush=True)
r={'scope':'Local geometric phase/backlash bracket at rest; not torque contact or production backlash specification','rows':rows,'input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [Path(__file__),cp,dp,R/'cad/engine/oil_drive_layout.py',R/'cad/engine/timing_coupled_core_candidate.py']}}
(R/'inventory/engine/crossed-oil-drive-backlash-review.json').write_text(json.dumps(r,indent=2)+'\n')
