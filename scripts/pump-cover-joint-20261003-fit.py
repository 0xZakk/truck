"""Joint camera + two source-pattern registration. Never fits to clashes."""
from pathlib import Path
import json,hashlib,math
import numpy as np
from scipy.optimize import least_squares
R=Path(__file__).resolve().parents[1];P='pump-cover-joint-20261003';jpath=R/f'reference/engine/{P}-measurements.json';j=json.loads(jpath.read_text());l=j['landmarks'];p=np.array(l['pump_world_candidate_mm'])/150;c=np.array(l['cover_current_world_mm'])/150;pp=np.array(l['pump_order_bottom_right_left_top_pixels']);cc=np.array(l['cover_order_source_gasket_1_to_7_pixels']);f=np.array(l['fifth_candidate_mm'])/150;fp=np.array(l['fifth_pixels']);s=j['proposed_cover_similarity'];H=np.diag([.001,.001,1])@np.array(j['homography_candidate_pump_plane_to_image'])@np.diag([150,150,1]);H/=H[2,2]
x0=np.r_[H.ravel()[:8],np.log(s['scale']),np.radians(s['rotation_deg']),np.array(s['offset_candidate_mm'])/150]
def trans(x,q):
 a=x[9];rot=np.array([[np.cos(a),np.sin(a)],[-np.sin(a),np.cos(a)]])
 return np.exp(x[8])*q@rot+x[10:12]
def image(x,q):
 h=np.r_[x[:8],1].reshape(3,3);v=np.c_[q,np.ones(len(q))]@h.T;return 1000*v[:,:2]/v[:,2,None]
def fit(pp,cc,c=c,mask=np.ones(7,dtype=bool),initial=x0):
 def residual(x):return np.r_[(image(x,p)-pp).ravel(),(image(x,trans(x,c[mask]))-cc[mask]).ravel()]
 return least_squares(residual,initial,max_nfev=120,xtol=1e-11,ftol=1e-11,gtol=1e-11)
b=fit(pp,cc);x=b.x;fitaxes=150*trans(x,c);gap=float(np.linalg.norm(fitaxes[2]-p[0]*150));pred=image(x,np.array([f]))[0]
held=[]
for i in range(7):
 mask=np.arange(7)!=i;q=fit(pp,cc,mask=mask,initial=x);held.append(float(np.linalg.norm(image(q.x,trans(q.x,c[[i]]))[0]-cc[i])))
rng=np.random.default_rng(473204);draws=[]
for i in range(400):
 # Cover source manual picks +/-3 pixels at .262233 model-mm/pixel.
 q=fit(pp+rng.uniform(-2,2,pp.shape),cc+rng.uniform(-2,2,cc.shape),c=c+rng.uniform(-3,3,c.shape)*.26223302269259874/150,initial=x);a=q.x;ax=150*trans(a,c)
 draws.append([np.linalg.norm(ax[2]-150*p[0]),np.exp(a[8]),np.degrees(a[9]),a[10]*150,a[11]*150,np.linalg.norm(image(a,np.array([f]))[0]-fp)])
controls={}
for name,qq,fc in [('swapped_pump_sides',pp[[0,2,1,3]],fp),('fifth_shift20',pp,fp+[20,0])]:
 q=fit(qq,cc,initial=x);controls[name]={'training_rms_px':float(np.sqrt(np.mean(q.fun**2))),'heldout_fifth_error_px':float(np.linalg.norm(image(q.x,np.array([f]))[0]-fc))}
r={'status':'RESEARCH; proposed shared block-face hypothesis, not CAD acceptance','method':'Joint projective camera (8DOF) and proper planar cover similarity (4DOF) fitted to four pump and seven cover hole centers (22scalarobservations); fifth aperture withheld. Pump pattern fixes metric gauge only by prior estimate. No clearance or neighbor inputs in objective.','camera_normalization':{'model_units':150,'image_units':1000},'parameters':x.tolist(),'cover_similarity':{'scale':float(np.exp(x[8])),'rotation_deg':float(np.degrees(x[9])),'offset_candidate_mm':(150*x[10:12]).tolist(),'axes_candidate_mm':fitaxes.tolist(),'axis_gap_mm':gap,'head_R8_75_plus_boss_R11_5_nominal_margin':gap-20.25,'tool_R10_5_plus_boss_R11_5_nominal_margin':gap-22},'fit':{'success':bool(b.success),'nfev':b.nfev,'pump_residuals_px':np.linalg.norm(image(x,p)-pp,axis=1).tolist(),'cover_residuals_px':np.linalg.norm(image(x,trans(x,c))-cc,axis=1).tolist(),'radius_rms_px':float(np.sqrt(np.mean(b.fun.reshape(-1,2)**2)*2)),'heldout_fifth_prediction_px':pred.tolist(),'heldout_fifth_error_px':float(np.linalg.norm(pred-fp)),'leave_one_cover_out_errors_px':held},'controls':controls,'pixel_selection_sensitivity':{'trials':400,'seed':473204,'columns':['gap_mm','scale','rotation_deg','offset_y','offset_z','heldout_fifth_px'],'p2_5_p50_p97_5':np.percentile(draws,[2.5,50,97.5],axis=0).tolist(),'limit':'Not calibrated confidence; unknown lens, planar distortion and pump scale absent.'},'limits':['Proper source-pattern similarity prevents carving and maintains gasket proportions; camera homography is NOT a CAD deformation.','Forward crank/cam hubs excluded because depth differs; current crank/pump registration remains unverified.','A lower-pump/cover gap can be source-supported proportionally while absolute shaft layout remains unresolved.','No independent millimeter anchor found; Carter axialheight is not a transverse ATK scale.','Do not apply estimated coordinate changes to shared assembly before coordinated crank/seal/gear/pan/accessory review.'],'input_sha256':{str(z.relative_to(R)):hashlib.sha256(z.read_bytes()).hexdigest()for z in [jpath,Path(__file__)]}}
(R/f'reference/engine/{P}-joint-fit.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
