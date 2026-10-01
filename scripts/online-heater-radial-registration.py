"""Four-view landmark audit; no geometry edits or engine-clearance fitting."""
from pathlib import Path
import json,hashlib,itertools,math
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'reference/engine/online-heater-radial-registration';O.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Estimated pump-axis-relative YZ pattern, inherited; not a measured GMB pattern.
w=np.array([[7.7,-66.5],[66.3,6.3],[-66.2,5.3],[17,64.9],[-10.9,69.]])
views={
 'rear':{'file':'gmb-1251810-view2.jpeg','indices':[0,1,2,3,4],'mounts':[[451,365],[363,427],[371,277],[297,362],[294,330]],'root':[303,296],'tip':[78,142],'hub_center':None,'correspondence':'Four small holes plus distinct larger fifth; all five visible. Body pattern determines affine map with residual degrees of freedom.'},
 'front':{'file':'gmb-1251810-front.jpeg','indices':[3,0,2],'mounts':[[315,199],[466,219],[381,273]],'root':[307,252],'tip':[40,387],'hub_center':[400,140],'correspondence':'Provisional three visible small-hole identities from tube/inlet adjacency; rearward fourth is occluded. Three points interpolate affine map exactly and cannot validate it.'},
 'oblique':{'file':'gmb-1251810-view4.jpeg','indices':[3,0,2],'mounts':[[350,201],[502,263],[388,320]],'root':[328,276],'tip':[47,330],'hub_center':None,'pilot_center':[443,194],'correspondence':'Three visible small holes; tentative identities follow front-view inlet/tube adjacency. Fourth and larger fifth opening obscured. Pilot center is visible but is not the pulley seating-plane center; no hub-plane metric anchor assigned.'},
 'side':{'file':'gmb-1251810-view3.jpeg','indices':[],'mounts':[],'root':[380,360],'tip':[558,438],'hub_center':[262,228],'correspondence':'Mounting holes are foreshortened/occluded; no false correspondence is assigned. Visible hub rim ellipse and mounting-plane silhouette provide a separate ratio test.','mount_plane_y':404,'pulley_plane_y':224,'hub_major_px':140,'hub_minor_px':22}}
def affine(pixel,target):
 p=np.array(pixel,float);fit=np.linalg.lstsq(np.c_[target,np.ones(len(target))],p,rcond=None)[0];C=fit[:2].T;offset=fit[2];res=np.linalg.norm(np.c_[target,np.ones(len(target))]@fit-p,axis=1)
 eig,V=np.linalg.eigh(C@C.T);axis=V[:,0]*np.sqrt(max(0,eig[1]-eig[0]))
 return C,offset,axis,float(np.sqrt(np.mean(res*res))),res
fits={}
for name,v in views.items():
 if not v['indices']:continue
 C,o,axis,rms,res=affine(v['mounts'],w[v['indices']]);signs=[]
 for sign in[-1,1]:
  root=np.linalg.solve(C,np.array(v['root'])-o-sign*35*axis)
  tip=np.linalg.solve(C,np.array(v['tip'])-o-sign*(-26.9666666667)*axis)
  signs.append({'axis_sign':sign,'root_yz_estimate_mm':root.tolist(),'tip_yz_estimate_mm':tip.tolist(),'root_to_tip_radial_mm':float(np.linalg.norm(tip-root)),'root_difference_from_inherited_mm':float(np.linalg.norm(root-[-48,60.3]))})
 fits[name]={'affine_yz_columns_px_per_estimated_mm':C.tolist(),'offset_px':o.tolist(),'weak_perspective_axial_column_up_to_sign':axis.tolist(),'mount_rms_px':rms,'mount_residuals_px':res.tolist(),'depth_assumptions_mm':{'root':35,'tip':-26.9666666667},'conditional_sign_solutions':signs,'warning':'Zero residual with three anchors is interpolation, not validation. Axial column assumes scaled orthographic camera and source pattern fidelity.'}
C,o,axis,rms,res=affine(views['rear']['mounts'],w)
rng=np.random.default_rng(440091810);samples=[]
for _ in range(2048):
 pix=np.array(views['rear']['mounts'])+rng.uniform(-4,4,(5,2));c,t,a,_,_=affine(pix,w)
 # Preserve sign branch oriented nearest inherited root, without asserting it true.
 rootpx=np.array(views['rear']['root'])+rng.uniform(-8,8,2);tippx=np.array(views['rear']['tip'])+rng.uniform(-8,8,2)
 sign=min([-1,1],key=lambda s:np.linalg.norm(np.linalg.solve(c,rootpx-t-s*35*a)-[-48,60.3]))
 root=np.linalg.solve(c,rootpx-t-sign*35*a);tip=np.linalg.solve(c,tippx-t-sign*rng.uniform(-34.875,-19.402174)*a)
 samples.append([*root,*tip,np.linalg.norm(tip-root),math.degrees(math.atan2(*(tip-root)[::-1]))])
samples=np.array(samples)
# Same observed rear pixels, different unknown tube depth: exact projection equality.
alternatives=[]
for tipx in[-100.,-26.9666666667,60.]:
 sign=-1;root=np.linalg.solve(C,np.array(views['rear']['root'])-o-sign*35*axis);tip=np.linalg.solve(C,np.array(views['rear']['tip'])-o-sign*tipx*axis)
 predicted=C@tip+o+sign*tipx*axis
 alternatives.append({'tip_axial_mm':tipx,'tip_yz_estimated_mm':tip.tolist(),'root_to_tip_radial_mm':float(np.linalg.norm(tip-root)),'same_rear_tip_reprojection_error_px':float(np.linalg.norm(predicted-views['rear']['tip'])),'scope':'Rear-camera ambiguity witness only; not claimed compatible with all four images or engine.'})
# Independent side-view circle geometry: projected axis length=sH*sqrt(1-q²).
ratios=[]
for Hpx in[172,180,188]:
 for Dpx in[134,140,146]:
  for minor in[16,22,28]:ratios.append(Hpx/Dpx/math.sqrt(1-(minor/Dpx)**2))
side={'camera_model':'Scaled orthographic; circular hub rim normal aligned with shaft. H/D independent of image scale. Perspective/noncircular rim errors remain possible.','observed_nominal_H_over_D':180/140/math.sqrt(1-(22/140)**2),'landmark_box_H_over_D':[min(ratios),max(ratios)],'inherited_H_over_D':143/70,'predicted_axial_span_with_inherited_ratio_px':140*(143/70)*math.sqrt(1-(22/140)**2),'observed_axial_span_px':180,'result':'FAIL common inherited143mm height/70mm hub-diameter scaled-orthographic side model; do not assign all radial discrepancy to camera azimuth.'}
perms=[]
for perm in itertools.permutations(range(4)):
 pix=np.array(views['rear']['mounts'])[[*perm,4]];_,_,_,e,_=affine(pix,w);perms.append({'small_hole_permutation':perm,'rms_px':e})
perms.sort(key=lambda x:x['rms_px'])
inputs=[Path(__file__),R/'cad/engine/water_pump.py',R/'cad/engine/water_pump_joint_candidate.py',R/'cad/engine/water_pump_gasket_topology_candidate.py',R/'reference/engine/online-heater-research.json',*[R/'reference/engine/online-heater-captures'/v['file']for v in views.values()]]
r={'status':'PARTIAL radial constraint; inherited camera/scale conflict prevents all-four metric registration','scope':'Source pixels only, no engine clearance or CAD fitting','views':views,'model_pattern_yz_mm_inherited':w.tolist(),'fits':fits,'rear_sensitivity':{'seed':440091810,'samples':2048,'mount_pixel_box':4,'tube_pixel_box':8,'columns':['rootY','rootZ','tipY','tipZ','radial_length','radial_azimuth_deg'],'min':samples.min(0).tolist(),'max':samples.max(0).tolist(),'meaning':'Finite perturbation spread conditional on inherited pattern, fixedrootdepth and prior axialrange; not manufacturing tolerance or physical guaranteed bound'},'rear_depth_ambiguity_witnesses':alternatives,'side_circle_ratio_test':side,'rear_index_controls':perms[:6],'wrong_index_example':next(x for x in perms if tuple(x['small_hole_permutation'])==(1,0,2,3)),'conclusions':['Rear five-hole correspondence supports a long radial route under inherited scale, rather than a141mm radial route obtained by treating side horizontal length as unforeshortened.','Front/oblique visible-anchor maps are underconstrained interpolation; inconsistent root estimates flag perspective, uncertain correspondence or differing estimated geometry. They cannot be combined as independent metric truth.','Side ellipse/axis ratio rejects the simultaneous inherited143mm height and70mm hub diameter in a scaled-orthographic camera. Either estimated proportions or camera model must change before jointfit.','Do not shorten/reclock frozen candidate from this study. Next bounded fit needs verified hub-diameter/height datum or a perspective joint model allowing explicit pump-proportion uncertainty.'],'input_sha256':{str(p.relative_to(R)):sha(p)for p in inputs},'canonical_modified':False}
(R/'reference/engine/online-heater-radial-registration.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'side':side,'rear_sensitivity':r['rear_sensitivity'],'ambiguity':alternatives},indent=2))
