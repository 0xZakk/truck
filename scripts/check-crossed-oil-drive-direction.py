#!/usr/bin/env python3
"""Actual drive datums and source-geometry signed tooth-lead compatibility."""
from pathlib import Path
import sys,json,math,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_math import transforms
import oil_drive_layout as d
from timing_coupled_core_candidate import AXIS
from timing_cover_attachment_v2 import norm
from cad_metrics import solid_volume
O=R/'cad/engine/generated/crossed-oil-drive-direction';O.mkdir(exist_ok=True)
m=json.loads((R/'inventory/engine/full-assembly.json').read_text());poses=transforms(m);occ={q['id']:q for q in m['occurrences']};definitions={q['id']:q for q in m['definitions']};delta=np.array([0,AXIS[0]-90,AXIS[1]-72]);shift=b.Pos(*delta)
cam_path=R/'cad/engine/generated/timing-thrust-land-candidate/camshaft.step';cam=b.import_step(cam_path)
ids=['distributor-drive-gear','distributor-shaft','oil-pump-intermediate-shaft','oil-pump-rotor-shaft','oil-pump-inner-rotor','oil-pump-outer-rotor']
paths={n:R/definitions[occ[n]['definition']]['step'].lstrip('/') for n in ids};parts={n:shift*poses[n]*b.import_step(paths[n])for n in ids}
a=np.array([1.,0,0]);baxis=np.array([0,math.sin(math.radians(d.TILT)),math.cos(math.radians(d.TILT))]);n=np.cross(baxis,a)
cam_origin=np.array([d.DRIVE_X,*AXIS]);old_drive=np.array(tuple(d.GEAR_FRAME.position));new_drive=old_drive+delta;r1=18*n;r2=-18*n
# Source extrude_linear_with_rotation has dtheta/daxial=-1/18 radians/mm.
k=-1/18;tcam=a+k*np.cross(a,r1);tdist=baxis+k*np.cross(baxis,r2);tooth_normal=(a+baxis)/np.sqrt(2)
velcam=np.cross(a,r1);veldist=np.cross(baxis,r2)
r={'source_construction':{'teeth_each':16,'pitch_radius_mm':18,'face_width_mm':12,'signed_twist_deg_across_face':-math.degrees(12/18),'lead_slope_rad_per_mm':k,'factory_hand':'UNKNOWN; geometric signed lead only'},'axes':{'cam':a.tolist(),'distributor':baxis.tolist(),'dot':float(a@baxis),'common_normal_cam_to_distributor':n.tolist(),'shift_mm':delta.tolist(),'old_drive_origin_mm':old_drive.tolist(),'shifted_drive_origin_mm':new_drive.tolist(),'shifted_axis_spacing_mm':float((new_drive-cam_origin)@n),'unshifted_axis_spacing_mm':float((old_drive-cam_origin)@n),'unshifted_axial_registration_error_mm':float((old_drive-cam_origin)@baxis)},'lead_tangent_check':{'cam':tcam.tolist(),'distributor':tdist.tolist(),'parallel_cross_norm':float(np.linalg.norm(np.cross(tcam,tdist))),'normal_velocity_same_signed_rates':float(tooth_normal@(velcam-veldist)),'normal_velocity_opposite_signed_rates':float(tooth_normal@(velcam+veldist)),'units':'mm/s per1rad/s shaft rate','conclusion':'Current two signed leads require equal signed cam/distributor angular rates for this contact side; proposed opposite rates incompatible'},'actual_manifest_motion':{q['id']:q.get('motion')for q in m['assemblies'] if q['id'] in ['cam-motion','distributor-rotation','oil-pump-intermediate-rotation','oil-pump-inner-rotation','oil-pump-outer-rotation']}}
# Actual frozen teeth, shifted distributor branch, bounded quarter-tooth-period fit snapshots.
rows=[]
for angle in [0,5.625,11.25]:
 cf=b.Pos(0,*AXIS)*b.Rot(angle,0,0)*b.Pos(0,-AXIS[0],-AXIS[1]);cw=cf*cam
 for sign in [1,-1]:
  gf=shift*d.GEAR_FRAME*b.Rot(0,0,sign*angle)*d.GEAR_FRAME.inverse()*shift.inverse();gw=gf*parts['distributor-drive-gear'];common=cw.intersect(gw)
  try:vol=solid_volume(common) if common is not None else 0;error=None
  except Exception as exc:vol=None;error=str(exc)
  row={'cam_angle_deg':angle,'distributor_angle_deg':sign*angle,'overlap_mm3':vol,'distance_mm':cw.distance_to(gw),'metric_error':error};rows.append(row);print(row,flush=True)
  if angle==0 and sign==1:
   b.export_step(gw,O/'actual-shifted-distributor-gear.step');b.export_step(norm(common),O/'rest-overlap.step') if common is not None and len(common.solids()) else None
r['actual_tooth_fit_samples']=rows
# Coaxial attachment kinematics are separate from crossed gear compatibility.
points={}
for name in ['distributor-shaft','oil-pump-intermediate-shaft','oil-pump-rotor-shaft']:
 frame=shift*poses[name];tr=frame.wrapped.Transformation();origin=np.array([tr.Value(i,4)for i in range(1,4)]);axis=np.array([tr.Value(i,3)for i in range(1,4)]);points[name]={'origin_mm':origin.tolist(),'axis':axis.tolist(),'distance_from_drive_axis_mm':float(np.linalg.norm(np.cross(origin-new_drive,baxis)))}
r['attachment_axes']=points
r['same_direction_attachment_contacts']={}
for left,right in [('distributor-shaft','oil-pump-intermediate-shaft'),('oil-pump-intermediate-shaft','oil-pump-rotor-shaft')]:
 common=parts[left].intersect(parts[right]);r['same_direction_attachment_contacts'][left+' / '+right]={'rest_distance_mm':parts[left].distance_to(parts[right]),'rest_overlap_mm3':solid_volume(common) if common is not None else 0}
r['limits']=['No factory hand/count/phase assertion','Sampled gear fit only; baseline meshing never accepted','Rigid translation preserves shaft/pump attachment, not surrounding neighbor acceptance','No pump pressure/flow direction or blanket ratio change claim']
r['input_sha256']={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [Path(__file__),R/'inventory/engine/full-assembly.json',R/'cad/engine/oil_drive_layout.py',R/'cad/engine/engine_clockwise_pose_candidate.py',R/'cad/engine/timing_coupled_core_candidate.py',cam_path,*paths.values()]}
(R/'inventory/engine/crossed-oil-drive-direction-review.json').write_text(json.dumps(r,indent=2)+'\n')
