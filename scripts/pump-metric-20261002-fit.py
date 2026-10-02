"""Bounded pinhole-camera/proportion study. No engine geometry/clearance input."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation
R=Path(__file__).resolve().parents[1];old=R/'reference/engine/online-heater-radial-registration.json';a=json.loads(old.read_text());names=['rear','front','oblique','side'];w=np.array(a['model_pattern_yz_mm_inherited'])
# Visible metal rim bounds, ±6px: edge thickness/occlusion make these soft observations.
rims={'front':[[338,139],[400,103],[460,143],[401,179]],'oblique':[[370,203],[426,146],[505,211],[451,263]],'side':[[192,230],[331,230]],'rear':[]}
def camera_init(name):
 if name=='side':M=np.array([[0,1,0],[-1,0,0],[0,0,1.]]);s=1.8;o=np.array([262,404])
 else:
  fit=a['fits'][name];C=np.array(fit['affine_yz_columns_px_per_estimated_mm']);x=np.array(fit['weak_perspective_axial_column_up_to_sign']);s=np.linalg.svd(C)[1][0];o=np.array(fit['offset_px']);rows=np.c_[x,C]/s;M=np.vstack([rows,np.cross(*rows)])
  if (M[2,0]>0)==(name!='rear'):rows=np.c_[-x,C]/s;M=np.vstack([rows,np.cross(*rows)])
  u,_,v=np.linalg.svd(M);M=u@v
 return np.r_[Rotation.from_matrix(M).as_rotvec(),(o-300)/s,1000/s,np.log(1000)]
def project(P,c):
 M=Rotation.from_rotvec(c[:3]).as_matrix();Q=np.atleast_2d(P)@M.T+c[3:6];return 300+np.exp(c[6])*Q[:,:2]/Q[:,2,None]
def residual(x,H,fixedD=None,details=False,holdout="side-tip"):
 D=x[0] if fixedD is None else fixedD;sy,sz=x[1:3];root=x[3:6];tip=x[6:9];holes=np.c_[np.zeros(5),w*np.array([sy,sz])];errs=[];info={}
 for i,n in enumerate(names):
  c=x[9+7*i:16+7*i];v=a['views'][n];obs=np.array(v['mounts']);items={}
  if len(obs):e=project(holes[v['indices']],c)-obs;errs.extend((e[:-1]/4 if n=='rear' and holdout=='rear-fifth' else e/4).ravel());items['mount_errors_px']=e.tolist()
  e=project(root,c)[0]-v['root'];errs.extend(e/8);items['root_error_px']=e.tolist()
  e=project(tip,c)[0]-v['tip'];items['tip_error_px']=e.tolist()
  if n!='side' or holdout!='side-tip':errs.extend(e/8) # held-out side tube terminal
  if rims[n]:
   M=Rotation.from_rotvec(c[:3]).as_matrix();K=np.array([[np.exp(c[6]),0,300],[0,np.exp(c[6]),300],[0,0,1]])
   hom=K@np.c_[M[:,1],M[:,2],M[:,0]*H+c[3:6]];q=np.c_[rims[n],np.ones(len(rims[n]))]@np.linalg.inv(hom).T;q=q[:,:2]/q[:,2,None]
   e=(np.linalg.norm(q,axis=1)-D/2)*np.exp(c[6])/np.linalg.norm(M[:,0]*H+c[3:6]);errs.extend(e/6);items['rim_radial_residual_px_equivalent']=e.tolist()
  if n=='side':e=project([0,0,0],c)[0]-[262,404];errs.extend(e/12);items['inferred_mount_origin_error_px']=e.tolist()
  info[n]=items
 return info if details else np.array(errs)
base=np.r_[76,1,1,25,-48,60,-20,-150,240,*np.concatenate([camera_init(n)for n in names])]
lo=np.r_[50,.6,.6,-60,-100,0,-150,-300,100,*np.tile([-8,-8,-8,-1500,-1500,250,np.log(400)],4)]
hi=np.r_[115,1.3,1.3,100,20,140,120,0,400,*np.tile([8,8,8,1500,1500,5000,np.log(5000)],4)]
results=[]
for label,H,D in [('primary-height-free-diameter',98.43,None),('primary-height-70mm',98.43,70),('inherited143-70',143,70),('inch-conversion-free-diameter',98.552,None)]:
 fit=least_squares(residual,base,bounds=(lo,hi),args=(H,D),max_nfev=450,ftol=1e-7,xtol=1e-7,gtol=1e-7)
 d=residual(fit.x,H,D,True);r={'label':label,'height_mm':H,'diameter_mm':float(fit.x[0]if D is None else D),'pattern_scale_yz':fit.x[1:3].tolist(),'root_xyz_mm':fit.x[3:6].tolist(),'tip_xyz_mm':fit.x[6:9].tolist(),'cameras':[fit.x[9+7*i:16+7*i].tolist()for i in range(4)],'weighted_rms':float(np.sqrt(np.mean(fit.fun**2))),'nfev':fit.nfev,'solver_success':bool(fit.success),'held_out_side_tip_error_px':float(np.linalg.norm(d['side']['tip_error_px'])),'views':d,'active_bounds':np.where((abs(fit.x-lo)<.01)|(abs(fit.x-hi)<.01))[0].tolist()};results.append(r);print(label,r['weighted_rms'],r['diameter_mm'],r['held_out_side_tip_error_px'],flush=True)

# Complementary holdout: include all four tube views, exclude distinct rear fifth opening.
for prior in list(results)[:2]:
 H=prior['height_mm'];D=None if prior['label'].endswith('free-diameter') else 70
 x=np.r_[prior['diameter_mm'],prior['pattern_scale_yz'],prior['root_xyz_mm'],prior['tip_xyz_mm'],np.array(prior['cameras']).ravel()]
 fit=least_squares(lambda z:residual(z,H,D,False,'rear-fifth'),x,bounds=(lo,hi),max_nfev=600,ftol=1e-7,xtol=1e-7,gtol=1e-7)
 d=residual(fit.x,H,D,True,'rear-fifth');outrow={'label':prior['label']+'-all-tube-views','height_mm':H,'diameter_mm':float(fit.x[0]if D is None else D),'pattern_scale_yz':fit.x[1:3].tolist(),'root_xyz_mm':fit.x[3:6].tolist(),'tip_xyz_mm':fit.x[6:9].tolist(),'cameras':[fit.x[9+7*i:16+7*i].tolist()for i in range(4)],'weighted_rms':float(np.sqrt(np.mean(fit.fun**2))),'nfev':fit.nfev,'solver_success':bool(fit.success),'held_out_rear_fifth_error_px':float(np.linalg.norm(d['rear']['mount_errors_px'][-1])),'views':d,'active_bounds':np.where((abs(fit.x-lo)<.01)|(abs(fit.x-hi)<.01))[0].tolist()};results.append(outrow);print(outrow['label'],outrow['weighted_rms'],outrow['diameter_mm'],outrow['held_out_rear_fifth_error_px'],flush=True)
paths=[old,Path(__file__),*[R/'reference/engine/online-heater-captures'/v['file']for v in a['views'].values()]]
out={'status':'Research only; bounded local optimizations, not unique or global calibration','camera_model':'Pinhole, independent poses/focal400..5000px, principal point300,300 fixed; no lens distortion. PlaneX0, rimXH. Original hole pattern allowed shared Y/Z scales0.6..1.3. No metric truth attributed to those bounds.','rims_px':rims,'uncertainties_px':{'mount':4,'root_tip':8,'rim':6,'side_inferred_mount_origin':12},'held_out':'First four fits exclude side tube terminal; final two include all tube views but exclude rear fifth opening. All errors retained, including held-out. Rim thickness/visible face selection remain approximate.','results':results,'input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths}}
(R/'reference/engine/pump-metric-20261002-fit.json').write_text(json.dumps(out,indent=2)+'\n')
