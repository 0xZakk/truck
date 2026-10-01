#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib,math
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import trimesh
import crossed_oil_drive_corrected_pair as c
import oil_drive_layout as old
from timing_coupled_core_candidate import AXIS
from timing_cover_attachment_v2 import norm
from cad_metrics import solid_volume
O=R/'cad/engine/generated/crossed-oil-drive-corrected-pair-reproduction';O.mkdir(exist_ok=False)
cam,dist=c.pair();shift=b.Pos(0,AXIS[0]-90,AXIS[1]-72);camframe=b.Pos(old.DRIVE_X,*AXIS);distframe=shift*old.GEAR_FRAME
parts={'cam-drive-gear-local':cam,'distributor-drive-gear-local':dist};exports={}
for n,s in parts.items():
 assert s.is_valid and len(s.solids())==1;b.export_step(s,O/(n+'.step'));v,f=s.tessellate(.04,.12);mesh=trimesh.Trimesh(np.array([tuple(p)for p in v]),np.array(f));mesh.merge_vertices(digits_vertex=6);assert mesh.is_watertight;trimesh.Trimesh(mesh.vertices[:,[0,2,1]]*[1,1,-1]/1000,mesh.faces).export(O/(n+'.glb'));exports[n]={'valid':s.is_valid,'solids':len(s.solids()),'watertight':mesh.is_watertight,'volume_mm3':s.volume}
rows=[]
for a in np.linspace(0,22.5,17):
 p=camframe*b.Rot(float(a),0,0)*cam;q=distframe*b.Rot(0,0,-float(a))*dist;distance=p.distance_to(q);common=p.intersect(q) if distance<1e-7 else None
 try:volume=solid_volume(common) if common is not None else 0;error=None
 except Exception as e:volume=None;error=str(e)
 row={'cam_degrees':float(a),'distributor_degrees':-float(a),'overlap_mm3':volume,'distance_mm':distance,'metric_error':error,'overlap_method':'exact positive separation' if distance>=1e-7 else 'strict intersection volume'};rows.append(row);print(row,flush=True)
# Connection guards compare actual retained distributor STEP in gear-centered local frame.
actual=b.Pos(0,0,85)*b.import_step(R/'cad/engine/generated/distributor-drive-gear.step');guard=b.Pos(0,0,17)*b.Box(60,60,22)
conn={'removed_mm3':solid_volume(actual.intersect(guard).cut(dist)),'added_mm3':solid_volume(dist.intersect(guard).cut(actual))}
# Old ratio is now an adversarial control at the previously hidden quarter tooth.
p=camframe*b.Rot(5.625,0,0)*cam;q=distframe*b.Rot(0,0,5.625)*dist;wrong=p.intersect(q);wrong_volume=solid_volume(wrong) if wrong is not None else 0
r={'scope':'Estimated positive-lead pair, bounded tooth-period snapshots only','exports':exports,'poses':rows,'distributor_connection_guard':conn,'wrong_same_signed_ratio_overlap_mm3':wrong_volume,'source_phase_deg':{'cam':c.CAM_PHASE,'distributor':c.DISTRIBUTOR_PHASE},'input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [Path(__file__),Path(c.__file__),Path(old.__file__),R/'cad/engine/generated/distributor-drive-gear.step']},'output_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [*O.glob('*.step'),*O.glob('*.glb')]}}
(O/'fresh-review.json').write_text(json.dumps(r,indent=2)+'\n')
