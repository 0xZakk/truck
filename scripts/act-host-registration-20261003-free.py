#!/usr/bin/env python3
"""Bounded free-upper-station follow-up; equal-pitch results remain immutable inputs."""
import importlib.util,json,hashlib
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
ROOT=Path(__file__).resolve().parents[1];PREFIX='act-host-registration-20261003'
spec=importlib.util.spec_from_file_location('equal',ROOT/'scripts'/f'{PREFIX}-fit.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
p=ROOT/'reference/engine'/f'{PREFIX}-fit.json';data=json.loads(p.read_text());seed=json.loads(m.LEDGER.read_text())['landmark_seeds']['views'];views=[1,5,6];runs=[]
for old in data['runs']:
 cs=old['contours'];xy=np.array([h['xy_mm'] for h in old['upper_hole_planarity']]).ravel()
 def residual(x):
  result=[];rad=np.exp(x[21]);holes=x[22:36].reshape(7,2);stations=np.r_[0,x[36:],5*m.PITCH]
  for k,v in enumerate(views):
   cam=x[k*7:k*7+7]
   for j,pts in enumerate(cs[str(v)]):result.append(m.conic_residual(np.array(pts),cam,stations[j],rad))
   for j in range(7):
    if v==5 and j==6:continue
    result.append(3*(m.project(np.array([[*holes[j],0]]),cam)[0]-m.HOLES[v][j]))
  return np.concatenate(result)
 lo=np.r_[np.tile(np.r_[[-6]*3,[-10000]*2,[200,np.log(300)]],3),np.log(10),[-1000]*14,[50,160,280,400]]
 hi=np.r_[np.tile(np.r_[[6]*3,[10000]*3,[np.log(15000)]],3),np.log(45),[1000]*14,[160,280,400,520]]
 trials=[]
 for camset in old['joint_multistarts']:
  init=np.r_[np.array(camset['camera_parameters']).ravel(),np.log(old['joint_common_radius_mm']),xy,np.arange(1,5)*m.PITCH]
  trials.append(least_squares(residual,np.clip(init,lo+1e-8,hi-1e-8),bounds=(lo,hi),loss='soft_l1',f_scale=2,max_nfev=400))
 trials.sort(key=lambda f:np.mean(f.fun**2));fit=trials[0];cameras={v:fit.x[k*7:k*7+7] for k,v in enumerate(views)};points={}
 for key in ['sensor_base','connector_center']:
  coords={v:np.array(seed[str(v)][key]) for v in views};f=m.fit_point(coords,cameras,[-30,100,0]);points[key]={'point_mm':f.x.tolist(),'residual_px':f.fun.reshape(-1,2).tolist(),'rms_px':float(np.sqrt(np.mean(f.fun**2)))}
 B=np.array(points['sensor_base']['point_mm']);C=np.array(points['connector_center']['point_mm']);axis=(C-B)/np.linalg.norm(C-B)
 heads=[]
 for j in range(6):
  co={v:np.array(seed[str(v)]['head_ports'][j]) for v in views};f=m.fit_point(co,cameras,[j*m.PITCH,90,80]);heads.append({'point_mm':f.x.tolist(),'residual_px':f.fun.reshape(-1,2).tolist(),'rms_px':float(np.sqrt(np.mean(f.fun**2)))})
 run={'threshold':old['threshold'],'parameter_count':40,'joint_success':bool(fit.success),'joint_common_radius_mm':float(np.exp(fit.x[21])),'joint_rms_weighted_px':float(np.sqrt(np.mean(fit.fun**2))),'upper_stations_mm':np.r_[0,fit.x[36:],5*m.PITCH].tolist(),'cameras':{v:c.tolist() for v,c in cameras.items()},'contours':cs,'sensor_points':points,'axis_base_to_connector':axis.tolist(),'head_points':heads,'joint_multistarts':[{'success':bool(t.success),'weighted_rms_px':float(np.sqrt(np.mean(t.fun**2))),'camera_parameters':t.x[:21].reshape(3,7).tolist(),'upper_stations_mm':np.r_[0,t.x[36:],5*m.PITCH].tolist()} for t in trials],'heldout_view5_hole6_residual_px':(m.project(np.array([[*fit.x[22:36].reshape(7,2)[6],0]]),cameras[5])[0]-m.HOLES[5][6]).tolist()}
 runs.append(run);print(old['threshold'],run['upper_stations_mm'],run['joint_rms_weighted_px'],points,flush=True)
report={'schema':1,'equal_fit_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'views':views,'runs':runs,'scale':'temporary first-to-last upper row length568.96; not physical pitch; head-row normalization requires held-out fit','status':'EXPLORATORY NOT ACCEPTED','no_neighbor_geometry_used':True}
(ROOT/'reference/engine'/f'{PREFIX}-free.json').write_text(json.dumps(report,indent=2)+'\n')
