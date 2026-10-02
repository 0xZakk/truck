from pathlib import Path
import json,hashlib
import numpy as np
from scipy.spatial.transform import Rotation
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];p=R/'reference/engine/pump-metric-20261002-fit.json';r=json.loads(p.read_text());old=json.loads((R/'reference/engine/online-heater-radial-registration.json').read_text());names=list(old['views']);names=['rear','front','oblique','side'];w=np.array(old['model_pattern_yz_mm_inherited']);reviews=[]
for q in r['results']:
 minima=[]
 for c in q['cameras']:
  pts=np.vstack([np.c_[np.zeros(5),w*np.array(q['pattern_scale_yz'])],q['root_xyz_mm'],q['tip_xyz_mm'],[q['height_mm'],0,0]])
  minima.append(float((pts@Rotation.from_rotvec(c[:3]).as_matrix().T+np.array(c[3:6]))[:,2].min()))
 reviews.append({'label':q['label'],'minimum_fitted_feature_camera_depth_mm':minima,'positive_depth':min(minima)>0,'weighted_rms':q['weighted_rms'],'heldout_px':q.get('held_out_rear_fifth_error_px',q.get('held_out_side_tip_error_px')),'active_bound_indices':q['active_bounds']})
fig,axs=plt.subplots(2,2,figsize=(10,10));q=r['results'][-1]
for ax,n,c in zip(axs.flat,names,q['cameras']):
 v=old['views'][n];pts=np.vstack([np.c_[np.zeros(len(v['indices'])),w[v['indices']]*np.array(q['pattern_scale_yz'])],q['root_xyz_mm'],q['tip_xyz_mm']]);obs=np.vstack([np.array(v['mounts']).reshape(-1,2),v['root'],v['tip']]);t=pts@Rotation.from_rotvec(c[:3]).as_matrix().T+np.array(c[3:6]);pred=300+np.exp(c[6])*t[:,:2]/t[:,2,None]
 ax.scatter(*obs.T,c='black',marker='x',label='observed pixels');ax.scatter(*pred.T,facecolors='none',edgecolors='red',label='pinhole hypothesis')
 for a,b in zip(obs,pred):ax.plot([a[0],b[0]],[a[1],b[1]],color='red',lw=.7)
 ax.set(xlim=(0,600),ylim=(600,0),title=n,aspect='equal');ax.legend(fontsize=7)
fig.suptitle('H98.43 / D70 conditional perspective fit\nAll tube views fit; rear fifth hole held out. No dimensional acceptance.');fig.tight_layout();out=R/'reference/engine/pump-metric-20261002-fit.png';fig.savefig(out,dpi=130)
(R/'reference/engine/pump-metric-20261002-review.json').write_text(json.dumps({'fits':reviews,'visual':str(out.relative_to(R)),'visual_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'inputs':{str(x.relative_to(R)):hashlib.sha256(x.read_bytes()).hexdigest()for x in[p,Path(__file__)]},'conclusion':'Low training residual does not establish a unique pump. H98.43 with D70 and D115 remain distinct conditional hypotheses; free diameter hits its declared bound. Side held-out failures and imperfect fifth-hole prediction retained.'},indent=2)+'\n')
