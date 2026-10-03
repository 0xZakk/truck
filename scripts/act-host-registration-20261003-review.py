#!/usr/bin/env python3
"""Create source-free fit plots and numerical held-out review; optional local original overlay."""
import argparse,json,hashlib
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares
from scipy.spatial.transform import Rotation
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
PREFIX='act-host-registration-20261003'

def project(points,p):
 q=Rotation.from_rotvec(p[:3]).apply(points)+p[3:6]
 return np.exp(p[6])*q[:,:2]/q[:,2,None]+[800,600]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path,required=True);ap.add_argument('--images',type=Path);ap.add_argument('--local-overlay',type=Path);a=ap.parse_args()
 data=json.loads(a.report.read_text());summary=[]
 for run in data['runs']:
  cams={int(k):np.array(v) for k,v in run['cameras'].items()};pts=np.array([p['point_mm'] for p in run['head_points']]);ids=np.arange(6)
  # Best independent equally spaced row; headpoints were never in camera fit.
  coef=np.linalg.lstsq(np.column_stack([np.ones(6),ids]),pts,rcond=None)[0];line=coef[0]+ids[:,None]*coef[1];step=np.linalg.norm(coef[1]);scale=113.792/step
  ledger=json.loads((ROOT/'reference/engine/act-host-secondview-20261003-evidence.json').read_text());seeds=ledger['landmark_seeds']['views']
  headfit=least_squares(lambda x:np.concatenate([(project(x[:3]+ids[:,None]*x[3:],p)-seeds[str(v)]['head_ports']).ravel() for v,p in cams.items()]),coef.ravel(),max_nfev=500)
  line=headfit.x[:3]+ids[:,None]*headfit.x[3:];step=np.linalg.norm(headfit.x[3:]);scale=113.792/step
  errors={v:(project(line,p)-seeds[str(v)]['head_ports']).tolist() for v,p in cams.items()}
  summary.append({'threshold':run['threshold'],'joint_success':run['joint_success'],'common_radius_temporary_gauge':run['joint_common_radius_mm'],'heldout_hole_euclidean_px':float(np.linalg.norm(run['heldout_view5_hole6_residual_px'])),'heldout_hole_plus20px_x_negative_control_error_px':float(np.linalg.norm(np.array(run['heldout_view5_hole6_residual_px'])-[20,0])),'sensor_max_euclidean_px':{k:float(np.linalg.norm(run['sensor_points'][k]['residual_px'],axis=1).max()) for k in ['sensor_base','connector_center']},'head_row_step_temporary_gauge':float(step),'head_row_scale_to_provisional_pitch':float(scale),'head_row_point_deviation_temporary_gauge':np.linalg.norm(pts-line,axis=1).tolist(),'head_equal_row_projection_errors_px':errors,'head_equal_row_max_euclidean_px':float(max(np.linalg.norm(e,axis=1).max() for e in map(np.array,errors.values()))),'sensor_base_rms_coordinate_px':run['sensor_points']['sensor_base']['rms_px'],'sensor_connector_rms_coordinate_px':run['sensor_points']['connector_center']['rms_px'],'axis_base_to_connector':run['axis_base_to_connector'],'upper_station_intervals_temporary_gauge':np.diff(run.get('upper_stations_mm',[i*113.792 for i in range(6)])).tolist(),'camera_focal_lengths_px':{v:float(np.exp(p[6])) for v,p in cams.items()}})
 out=a.report.with_name(a.report.stem+'-review.json');out.write_text(json.dumps({'input_sha256':hashlib.sha256(a.report.read_bytes()).hexdigest(),'review_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'runs':summary,'status':'NOT ACCEPTED; inspect actual residuals and parameter spread'},indent=2)+'\n')
 run=data['runs'][1];fig,axes=plt.subplots(3,1,figsize=(14,13));t=np.linspace(0,2*np.pi,128)
 for ax,v in zip(axes,data['views']):
  if a.local_overlay and a.images:ax.imshow(Image.open(a.images/f'act-host-secondview-20261003-view{v}.webp'))
  p=np.array(run['cameras'][str(v)]);radius=run['joint_common_radius_mm'];stations=run.get('upper_stations_mm',[i*113.792 for i in range(6)])
  for j,(pts,cx) in enumerate(zip(run['contours'][str(v)],stations)):
   pts=np.array(pts);ax.plot(pts[:,0],pts[:,1],'.',color='#536d9e',ms=2,label='Observed aperture boundary' if j==0 else None)
   circle=np.column_stack([cx+radius*np.cos(t),radius*np.sin(t),np.zeros(len(t))]);pred=project(circle,p);ax.plot(*pred.T,color='#e49b1f',label='Shared-circle fit' if j==0 else None)
  for name,color in [('sensor_base','#c5233d'),('connector_center','#751b8c')]:
   point=np.array(run['sensor_points'][name]['point_mm']);pred=project(point[None,:],p)[0];obs=np.array(seeds[str(v)][name]);ax.plot([obs[0],pred[0]],[obs[1],pred[1]],color=color);ax.plot(*obs,'o',color=color);ax.plot(*pred,'x',color=color)
  ax.set_xlim(0,1600);ax.set_ylim(1000,0);ax.set_aspect('equal');ax.set_title(f'View{v}, threshold140: observed contours / fitted circles; sensor observed o → predicted x');ax.legend(loc='lower right')
 fig.tight_layout();target=a.local_overlay if a.local_overlay else a.report.with_suffix('.png');fig.savefig(target,dpi=130)
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
