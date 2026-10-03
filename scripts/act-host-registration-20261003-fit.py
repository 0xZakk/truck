#!/usr/bin/env python3
"""Fit public casting port silhouettes; no assembly or clearance input."""
from pathlib import Path
import argparse,json,hashlib
import numpy as np
from PIL import Image
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation
from scipy.ndimage import map_coordinates, label, center_of_mass, binary_erosion, binary_fill_holes

ROOT=Path(__file__).resolve().parents[1]
PREFIX='act-host-registration-20261003'
LEDGER=ROOT/'reference/engine/act-host-secondview-20261003-evidence.json'
PITCH=113.792
# Approximate dark aperture centers of the seven staggered flange holes.
HOLES={1:[[230,115],[353,169],[548,162],[757,181],[968,148],[1183,141],[1384,192]],5:[[293,451],[401,487],[586,473],[786,485],[985,448],[1197,435],[1410,463]],6:[[91,341],[292,393],[548,346],[769,326],[1017,242],[1225,200],[1414,237]]}

def project(points,p):
 q=Rotation.from_rotvec(p[:3]).apply(points)+p[3:6]
 return np.exp(p[6])*q[:,:2]/q[:,2,None]+[800,600]

def extract(image,center,threshold):
 gray=np.asarray(image.convert('L'),float);x,y=np.rint(center).astype(int);x0=x-80;y0=y-80
 crop=gray[y0:y+81,x0:x+81];labs,n=label(crop<threshold);choices=[]
 for k in range(1,n+1):
  mask=labs==k;area=mask.sum()
  if area<300 or mask[0].any() or mask[-1].any() or mask[:,0].any() or mask[:,-1].any():continue
  cy,cx=center_of_mass(mask);choices.append(((cx-80)**2+(cy-80)**2,mask))
 if not choices:raise ValueError(f'No aperture component near {center}, threshold{threshold}')
 mask=binary_fill_holes(min(choices,key=lambda t:t[0])[1]);yy,xx=np.where(mask&~binary_erosion(mask));cx=xx.mean();cy=yy.mean();angles=np.arctan2(yy-cy,xx-cx);order=np.argsort(angles)
 order=order[np.linspace(0,len(order)-1,64,dtype=int)]
 return np.column_stack([xx[order]+x0,yy[order]+y0]).astype(float)

def conic_residual(pts,p,cx,radius):
 # Exact projected circle conic; signed Sampson distance in pixel units.
 R=Rotation.from_rotvec(p[:3]).as_matrix();K=np.array([[np.exp(p[6]),0,800],[0,np.exp(p[6]),600],[0,0,1.]])
 H=K@np.column_stack([R[:,0],R[:,1],p[3:6]])
 C=np.array([[1,0,-cx],[0,1,0],[-cx,0,cx*cx-radius*radius]])
 Hi=np.linalg.inv(H);Q=Hi.T@C@Hi;uv=np.column_stack([pts,np.ones(len(pts))]);v=uv@Q
 return np.sum(v*uv,axis=1)/(2*np.linalg.norm(v[:,:2],axis=1)+1e-12)

def fit_view(contours,start,radius_init=25):
 def residual(x):
  return np.concatenate([conic_residual(pts,x[:7],i*PITCH,np.exp(x[7])) for i,pts in enumerate(contours)])
 x=np.r_[start,np.log(radius_init)]
 return least_squares(residual,x,bounds=(np.r_[[-6]*3,[-10000]*2,[200,np.log(300),np.log(10)]],np.r_[[6]*3,[10000]*3,[np.log(15000),np.log(45)]]),loss='soft_l1',f_scale=2,max_nfev=250)

def fit_point(images,cameras,start):
 return least_squares(lambda p:np.concatenate([project(np.array([p]),cameras[v])[0]-images[v] for v in images]),start,max_nfev=250)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--images',type=Path,required=True);ap.add_argument('--output',type=Path,default=ROOT/'reference/engine');a=ap.parse_args()
 ledger=json.loads(LEDGER.read_text());seeds=ledger['landmark_seeds']['views'];views=[1,5,6];data={};results=[]
 for v in views:
  path=a.images/f'act-host-secondview-20261003-view{v}.webp';entry=next(i for i in ledger['images'] if i['gallery_view']==v)
  assert hashlib.sha256(path.read_bytes()).hexdigest()==entry['sha256'];data[v]=Image.open(path)
 for threshold in [120,140,160]:
  cameras={};contour_output={};multi={}
  for v in views:
   contours=[extract(data[v],c,threshold) for c in seeds[str(v)]['upper_ports']];contour_output[v]=[p.tolist() for p in contours]
   # +X image right; +Y towardhead (down); plane normal chosen toward camera.
   starts=[]
   for focal in [900,1800,3600]:
    z=focal*PITCH/210; x=(seeds[str(v)]['upper_ports'][0][0]-800)*z/focal;y=(seeds[str(v)]['upper_ports'][0][1]-600)*z/focal
    for tilt in [-1.0,-0.5,0.5,1.0]:
     starts.append(np.r_[[tilt,0,-0.15 if v==6 else 0],[x,y,z],np.log(focal)])
   fits=[fit_view(contours,s) for s in starts];fits.sort(key=lambda r:np.mean(r.fun**2));best=fits[0];cameras[v]=best.x[:7]
   multi[v]=[{'rms_px':float(np.sqrt(np.mean(f.fun**2))),'camera':f.x[:7].tolist(),'radius_mm':float(np.exp(f.x[7])),'success':bool(f.success)} for f in fits]
  # Common circle radius across views; noncollinear holes share unknown XY.
  cams0=np.concatenate([cameras[v] for v in views]);rad0=np.mean([multi[v][0]['radius_mm'] for v in views])
  xy0=[]
  for j in range(7):
   f=least_squares(lambda xy:np.concatenate([project(np.array([[xy[0],xy[1],0]]),cameras[v])[0]-HOLES[v][j] for v in views]),[j*PITCH-50,0]);xy0.extend(f.x)
  initial=np.r_[cams0,np.log(rad0),xy0]
  def joint_res(x):
   result=[];rad=np.exp(x[21]);xy=x[22:].reshape(7,2)
   for k,v in enumerate(views):
    p=x[k*7:k*7+7]
    result.extend(conic_residual(np.array(pts),p,i*PITCH,rad) for i,pts in enumerate(contour_output[v]))
    # Last hole held out in view5;2D Euclidean residual weight reflects64 contour samples/port.
    for j in range(7):
     if v==5 and j==6:continue
     result.append(3*(project(np.array([[*xy[j],0]]),p)[0]-HOLES[v][j]))
   return np.concatenate(result)
  lo=np.r_[np.tile(np.r_[[-6]*3,[-10000]*2,[200,np.log(300)]],3),np.log(10),[-1000]*14]
  hi=np.r_[np.tile(np.r_[[6]*3,[10000]*3,[np.log(15000)]],3),np.log(45),[1000]*14]
  joint=least_squares(joint_res,np.clip(initial,lo+1e-8,hi-1e-8),bounds=(lo,hi),loss='soft_l1',f_scale=2,max_nfev=400)
  # Repeat joint optimization from camera alternatives having the opposite plane tilt sign.
  joint_trials=[joint]
  for wanted in [-1,1]:
   alt=initial.copy()
   for k,v in enumerate(views):
    options=[f for f in multi[v] if np.sign(f['camera'][0])==wanted]
    if options:alt[k*7:k*7+7]=options[0]['camera']
   joint_trials.append(least_squares(joint_res,np.clip(alt,lo+1e-8,hi-1e-8),bounds=(lo,hi),loss='soft_l1',f_scale=2,max_nfev=400))
  joint_trials.sort(key=lambda f:np.mean(f.fun**2));joint=joint_trials[0]
  cameras={v:joint.x[k*7:k*7+7] for k,v in enumerate(views)}
  points={}
  for key in ['sensor_base','connector_center']:
   coords={v:np.array(seeds[str(v)][key]) for v in views};fit=fit_point(coords,cameras,[-30,100,0]);points[key]={'point_mm':fit.x.tolist(),'residual_px':fit.fun.reshape(-1,2).tolist(),'rms_px':float(np.sqrt(np.mean(fit.fun**2)))}
  B=np.array(points['sensor_base']['point_mm']);C=np.array(points['connector_center']['point_mm']);axis=(C-B)/np.linalg.norm(C-B)
  # Planar holes fit on Z=0, all views; measures consistency, not dimension truth.
  holes=[]
  for j in range(7):
   f=least_squares(lambda xy:np.concatenate([project(np.array([[xy[0],xy[1],0]]),cameras[v])[0]-HOLES[v][j] for v in views]),[j*PITCH-50,0]);holes.append({'xy_mm':f.x.tolist(),'residual_px':f.fun.reshape(-1,2).tolist(),'rms_px':float(np.sqrt(np.mean(f.fun**2)))})
  heads=[]
  for j in range(6):
   co={v:np.array(seeds[str(v)]['head_ports'][j]) for v in views};f=fit_point(co,cameras,[j*PITCH,90,-80]);heads.append({'point_mm':f.x.tolist(),'residual_px':f.fun.reshape(-1,2).tolist(),'rms_px':float(np.sqrt(np.mean(f.fun**2)))})
  results.append({'threshold':threshold,'joint_multistarts':[{'success':bool(j.success),'weighted_rms_px':float(np.sqrt(np.mean(j.fun**2))),'camera_parameters':j.x[:21].reshape(3,7).tolist()} for j in joint_trials],'joint_common_radius_mm':float(np.exp(joint.x[21])),'joint_success':bool(joint.success),'joint_rms_weighted_px':float(np.sqrt(np.mean(joint.fun**2))),'heldout_view5_hole6_residual_px':(project(np.array([[*joint.x[22:].reshape(7,2)[6],0]]),cameras[5])[0]-HOLES[5][6]).tolist(),'cameras':{v:p.tolist() for v,p in cameras.items()},'multistarts':multi,'contours':contour_output,'sensor_points':points,'axis_base_to_connector':axis.tolist(),'upper_hole_planarity':holes,'head_points':heads})
 a.output.mkdir(parents=True,exist_ok=True)
 report={'schema':1,'source_ledger_sha256':hashlib.sha256(LEDGER.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'pitch_mm':PITCH,'pitch_class':'provisional existing model','camera_assumptions':'independent f; square pixels; c=(800,600); zero distortion','views':views,'runs':results,'status':'EXPLORATORY NOT ACCEPTED','no_neighbor_geometry_used':True}
 (a.output/(PREFIX+'-fit.json')).write_text(json.dumps(report,indent=2)+'\n')
 for r in results:print(r['threshold'],{v:round(r['multistarts'][v][0]['rms_px'],2) for v in views},r['sensor_points'],r['axis_base_to_connector'])
if __name__=='__main__':main()
