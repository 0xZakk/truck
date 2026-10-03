"""Reproduce the pre-CAD ACT registration sensitivity; no CAD mutations."""
from pathlib import Path
import hashlib,itertools,json,math,subprocess
import numpy as np
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'cad/engine/generated/act-host-estimate-20261002-registration'
OUT.mkdir(parents=True,exist_ok=True)
IMAGE='manuals/factory-service-manual/1994 Ford F 150 2WD Pickup L6-300 4.9L/images/DM05Q313/ford10/147826554.png'
PATHS=[IMAGE,'cad/engine/generated/efi-lower-intake.step','cad/engine/efi_intake.py','inventory/engine/full-assembly.json','inventory/engine/corrected-engine-stage-v4.json','reference/engine/act-online-20261002-delivery.json','reference/engine/act-host-online-20261002-evidence.json','docs/components/act-host-estimate-20261002-contract.md']
sha=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
inputs={p:sha(p) for p in PATHS}
assert inputs['inventory/engine/corrected-engine-stage-v4.json']=='9da33ca507e31cf6d906d4ee2c92b87a64ba01db7abea8f14b72f244631f9fe9'
pts=np.array([[49,127],[147,196],[267,241],[420,156],[478,103]],dtype=float)
def properties(a):
 A,B,P,T,C=a;v=B-A;D=np.dot(v,v)
 rel=P-B
 projected=np.array([np.dot(rel,v),np.linalg.det(np.array([v,rel]))])/D
 u=T-P;w=C-T
 ang=math.degrees(math.atan2(np.linalg.det(np.array([u,w])),np.dot(u,w)))
 return projected,ang
nom,ang=properties(pts)
values=[]
for signs in itertools.product((-1,1),repeat=10):
 values.append((*properties(pts+4*np.array(signs).reshape(5,2))[0],properties(pts+4*np.array(signs).reshape(5,2))[1]))
values=np.array(values)
# Abstract camera coordinates only: imageU,imageV,viewDepth. NOT truck axes.
axis2=pts[4]-pts[3];axis2=axis2/np.linalg.norm(axis2)
family=[]
for beta in (-60,-30,0,30,60):
 a=np.array([*(axis2*math.cos(math.radians(beta))),math.sin(math.radians(beta))])
 projection=a[:2]/np.linalg.norm(a[:2])
 family.append({'out_of_image_plane_angle_deg':beta,'unit_axis_camera_coordinates':a.tolist(),'normalized_projection_error':float(np.linalg.norm(projection-axis2))})
separation=math.degrees(math.acos(float(np.clip(np.dot(family[0]['unit_axis_camera_coordinates'],family[-1]['unit_axis_camera_coordinates']),-1,1))))
shape=b.import_step(ROOT/'cad/engine/generated/efi-lower-intake.step');bb=shape.bounding_box()
# All points with arbitrary depth have the exact same pixel projection.
centers=[{'camera_coordinates':[267,241,d],'pixel_projection':[267,241]} for d in (-40,-20,0,20,40)]
report={'scope':'Pre-CAD registration sensitivity, NOT installed candidate','baseline':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'inputs':inputs,'pixel_landmarks':dict(zip(('A_previous_upper_port','B_terminal_upper_port','P_boss','T_depicted_probe_end','C_connector_center'),pts.tolist())),'pixel_pick_sensitivity_each_coordinate':4,'consecutive_runner_correspondence':'Assumption, not measured dimension;113.792mm projectpitch is provisional','projected_basis_result':{'boss_relative_to_B_in_projected_pitch_units':nom.tolist(),'nominal_pitch_scaled_values_NOT_world_mm':(nom*113.792).tolist(),'all1024_corner_min':values.min(axis=0).tolist(),'all1024_corner_max':values.max(axis=0).tolist(),'correspondence_line_vs_depicted_axis_nominal_deg':ang,'quantity_order':['longitudinal_pitch_units','perpendicular_pitch_units','axis_line_angle_deg']},'camera_nullspace':{'frame':'Abstract imageU,imageV,viewDepth; no world-camera calibration','axis_family':family,'first_last_axis_separation_deg':separation,'center_family_NOT_depth_bounds':centers,'interpretation':'Identical projected positions/directions permit different depths/axes; sampled angles and depths are mathematical demonstrations, not Ford uncertaintybounds'},'controls':{'all_axis_normalized_projection_errors_below_1e_12':all(v['normalized_projection_error']<1e-12 for v in family),'image_plane_shift_10px_detected':bool(np.linalg.norm((np.array([267.,241.,0.])+np.array([10.,0.,0.]))[:2]-pts[2])>4),'negative_control_pixel_residual':float(np.linalg.norm((np.array([267.,241.,0.])+np.array([10.,0.,0.]))[:2]-pts[2]))},'actual_host':{'bounds_min_mm':list(bb.min),'bounds_max_mm':list(bb.max),'valid':shape.is_valid,'solid_count':len(shape.solids()),'existing_front_runner_center_x_mm':284.48,'receiver_present_in_declared_source_module':False,'no_geometry_changed':True},'verdict':{'topological_station':'supported front terminal lower runner','metric_port_pose':'NOT VERIFIED; no independent camera/depth datum','registration_sensitivity':'PASS reproducible ambiguity demonstration','CAD_export':'NOT RUN: no justified numeric pose constructed','host_wall_guard_air_exposure':'NOT RUN','thread_fit_seal':'NOT VERIFIED','wrench_removal':'NOT RUN','actual_neighbor_collisions':'NOT RUN; canonical/v4 hashes bound only, no arbitrary positioned object','readiness':'Research sensitivity; root may explicitly authorize a separate axis/depth design assumption, but it would not be photo-derived metric evidence'}}
(ROOT/'reference/engine/act-host-estimate-20261002-registration.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'projected':report['projected_basis_result'],'family_separation_deg':separation,'host':report['actual_host']},indent=2))
