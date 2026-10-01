"""Correct tube-entry correspondence; do not rewrite frozen registration audit."""
from pathlib import Path
import json,hashlib,math,numpy as np
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=R/'inventory/engine/waterpump-neck-registration-research.json';j=json.loads(p.read_text());w=np.array(j['landmarks']['model_relative_yz_mm']);rows={}
points={'front':[[414,343],[410,244],[450,172],[609,22]],'rear':[[260,353],[246,275],[178,213],[21,18]]}
for name,parity in [('front','1'),('rear','-1')]:
 f=j['fits'][name][parity];mounts=np.array(j['landmarks'][name+'_pixels_xy']);xy=np.array(points[name]);q=(xy*[1,-1]-(mounts*[1,-1]).mean(0))@np.array(f['rotation_matrix_row_convention'])*f['scale_model_mm_per_pixel_NOT_MEASUREMENT']+w[:len(mounts)].mean(0);delta=q[1]-q[0]
 rows[name]={'correct_parity':int(parity),'pixels_root_firstbend_secondbend_tip':points[name],'model_yz_NOT_MEASURED':q.tolist(),'root_radial_deg':math.degrees(math.atan2(q[0,1],q[0,0])),'initial_stem_angle_deg':math.degrees(math.atan2(delta[1],delta[0])),'fit_rms_model_mm':f['rms_model_mm'],'wrong_mirror_rms_model_mm':j['fits'][name][str(-int(parity))]['rms_model_mm']}
# Side image shaft axis points approximately up. Pixel axial coordinates are
# explicitly approximate projected centers; perspective remains uncorrected.
rear_y,hub_y,root_y,tip_y=307.,65.,249.,543.;rear_x,hub_x=375.,518.
scale=(hub_x-rear_x)/(rear_y-hub_y)
side={'axial_pixels_y':{'rear':rear_y,'hub':hub_y,'root':root_y,'tip':tip_y},'retained_model_x_mm':{'rear':rear_x,'hub':hub_x},'estimated_root_world_x':rear_x+(rear_y-root_y)*scale,'estimated_tip_world_x':rear_x+(rear_y-tip_y)*scale,'note':'Uncalibrated side photo; sign of rearward tube departure clearer than absolute coordinate.'}
nomroot=[side['estimated_root_world_x'],-80.,230.3];oldend=[438.,-132.,270.]
# Test only simple monotonic root-straight/tangentarc/endstraight in the YZ plane.
# This is not a proof that no possible 3D routing exists.
theta=math.radians(145);radius=20.;dy=oldend[1]-nomroot[1];dz=oldend[2]-nomroot[2];arcdy=radius*(math.sin(theta)-1);arcdz=-radius*math.cos(theta);straight=(dy-arcdy)/math.cos(theta);rise=straight*math.sin(theta)+arcdz
r={'status':'SOURCE/DATUM CONTRACT; no geometry edits','source_fits':rows,'corrected_prior_landmark':'Frozen front(440,364) selected adjacent casting feature; actual visible tube entry is(414,343). Rear old(267,357) refinedto(260,353).','side_axial_projection':side,'provisional_root_world_mm':nomroot,'old_boundary_world_mm':oldend,'old_boundary_simple_route_test':{'initial_angle_deg':145,'bend_radius_mm':radius,'required_rise_mm':rise,'available_rise_mm':dz,'vertical_terminal_length_mm':dz-rise,'result':'FAIL negative final straight; does not prove all 3D routes impossible'},'proposed_boundary_scope':'Source shows long formed tube departing toward rear in side view. Old X438/Z270 endpoint would reverse axial departure and shorten source silhouette. Prefer a new source-estimated endpoint with vehicle hose routing gap rather than asserting source fidelity for an arbitrary short S bend.','limits':['All millimeter normalization inherits provisional model pattern and hub/rear spacing.','Front/rear side photographs are uncalibrated; they cannot triangulate production3D coordinates.','No manufacturing tolerance, precise hydraulic flow or routing claim.'],'inputs':{str(q.relative_to(R)):sha(q)for q in [Path(__file__),p,*[R/'reference/engine'/('gates44009-'+str(i)+'.jpg')for i in [1,2,3]]]}}
(R/'inventory/engine/waterpump-heater-source-registration.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
