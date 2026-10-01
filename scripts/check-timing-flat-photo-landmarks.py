#!/usr/bin/env python3
"""Independent image pixels and all cyclic/reversed seven-hole correspondences."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import label,binary_fill_holes,binary_erosion,distance_transform_edt
from scipy.optimize import least_squares
R=Path(__file__).resolve().parents[1];p=R/'cad/engine/generated/timing-cover-joint-candidate/reference/dorman-635109-009.jpg';rp=R/'inventory/engine/timing-cover-registration-validation.json';j=json.loads(rp.read_text());src=np.array(j['photo_samples']['source_holes_pixels']);target=np.array(j['photo_samples']['dorman009_holes_pixels']);im=np.asarray(Image.open(p).convert('L'));rows=[]
for threshold in (70,100,130):
 lab,n=label(im<threshold);count=np.bincount(lab.ravel());count[0]=0;mask=lab==count.argmax();holes=binary_fill_holes(mask)&~mask;h,n=label(holes);centers=[]
 for i in range(1,n+1):
  yy,xx=np.where(h==i)
  if len(xx)>=40:centers.append({'center_xy':[float(xx.mean()),float(yy.mean())],'area_pixels':len(xx)})
 assigned=[]
 for k,q in enumerate(target):
  v=min(centers,key=lambda v:np.linalg.norm(np.array(v['center_xy'])-q));assigned.append({'station':k+1,**v,'distance_from_authored_center_px':float(np.linalg.norm(np.array(v['center_xy'])-q))})
 rows.append({'threshold':threshold,'large_enclosed_holes':len(centers),'authored_matches':assigned})
def apply(H,p):
 q=np.c_[p,np.ones(len(p))]@H.T;return q[:,:2]/q[:,2,None]
def fit(s,d):
 A=[]
 for (x,y),(u,v) in zip(s,d):A.extend([[-x,-y,-1,0,0,0,u*x,u*y,u],[0,0,0,-x,-y,-1,v*x,v*y,v]])
 H=np.linalg.svd(A)[2][-1].reshape(3,3);H/=H[2,2];v=least_squares(lambda v:(apply(np.r_[v,1].reshape(3,3),s)-d).ravel(),H.ravel()[:8]).x;H=np.r_[v,1].reshape(3,3);return H,float(np.sqrt(np.mean(np.sum((apply(H,s)-d)**2,axis=1))))
actual=np.array([v['center_xy'] for v in rows[1]['authored_matches']]);fits=[]
for reverse in (False,True):
 for shift in range(7):
  indexes=np.roll(np.arange(7)[::-1] if reverse else np.arange(7),shift);H,rms=fit(src,actual[indexes]);fits.append({'reverse':reverse,'cyclic_shift':shift,'rms_px':rms,'mapping':indexes.tolist(),'homography':H.tolist()})
fits.sort(key=lambda v:v['rms_px']);assert fits[0]['mapping']==list(range(7))
r={'status':'Independent009 pixels support existing hole ordering; no sourceindex repair found','pixel_hole_checks':rows,'all14_order_preserving_or_reversing_hypotheses':fits,'best_to_second_rms_ratio':fits[1]['rms_px']/fits[0]['rms_px'],'limits':'Only cyclic and reversed contour ordering checked; homography is image correspondence, not CAD metric calibration. Does not bound aperture depth parallax or make009 orthographic. No source pixels redistributed.','input_sha256':{str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest() for q in [p,rp,Path(__file__)]}}
import ast
sp=R/'cad/engine/timing_cover_joint_candidate.py'
a={n.targets[0].id:ast.literal_eval(n.value) for n in ast.parse(sp.read_text()).body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='OUTLINE_NORMALIZED'}
outline=np.array(a['OUTLINE_NORMALIZED'])*1600
samples=np.concatenate([q+(v-q)*np.linspace(0,1,21)[:,None] for q,v in zip(outline,np.roll(outline,-1,axis=0))]);mapped=apply(np.array(fits[0]['homography']),samples)
lab,n=label(im<100);count=np.bincount(lab.ravel());count[0]=0;mask=binary_fill_holes(lab==count.argmax());boundary=mask&~binary_erosion(mask);distance=distance_transform_edt(~boundary);ix=np.rint(mapped).astype(int);inside=(ix[:,0]>=0)&(ix[:,0]<im.shape[1])&(ix[:,1]>=0)&(ix[:,1]<im.shape[0]);errors=distance[ix[inside,1],ix[inside,0]]
r['transferred_outline_vs_independent009_boundary']={'samples':len(ix),'in_image':int(inside.sum()),'distance_px_percentiles_50_90_95_100':np.percentile(errors,[50,90,95,100]).tolist(),'meaning':'Nearest actual gasket boundary, holes filled; compares source silhouettes without editing either. Quantization about1px; product specimens/trace differences remain.'}
r['input_sha256'][str(sp.relative_to(R))]=hashlib.sha256(sp.read_bytes()).hexdigest()
(R/'inventory/engine/timing-flat-photo-landmarks.json').write_text(json.dumps(r,indent=2)+'\n')
