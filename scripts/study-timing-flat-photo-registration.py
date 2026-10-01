#!/usr/bin/env python3
"""Alternate photo-frame hypothesis, no CAD and no compressor-targeted fit."""
from pathlib import Path
import ast,json,hashlib,math
import numpy as np
from scipy.optimize import least_squares
from matplotlib.path import Path as Poly
R=Path(__file__).resolve().parents[1];src=R/'cad/engine/timing_cover_joint_candidate.py';rp=R/'inventory/engine/timing-cover-registration-validation.json';j=json.loads(rp.read_text())
a={n.targets[0].id:ast.literal_eval(n.value) for n in ast.parse(src.read_text()).body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('OUTLINE_NORMALIZED','HOLES_NORMALIZED')};outline=np.array(a['OUTLINE_NORMALIZED'])*1600;holes=np.array(a['HOLES_NORMALIZED'])*1600;flat=np.array(j['photo_samples']['dorman009_holes_pixels'])
def apply(H,p):
 q=np.c_[p,np.ones(len(p))]@H.T;return q[:,:2]/q[:,2,None]
def homography(s,d):
 A=[]
 for (x,y),(u,v) in zip(s,d):A.extend([[-x,-y,-1,0,0,0,u*x,u*y,u],[0,0,0,-x,-y,-1,v*x,v*y,v]])
 H=np.linalg.svd(A)[2][-1].reshape(3,3);H/=H[2,2];v=least_squares(lambda v:(apply(np.r_[v,1].reshape(3,3),s)-d).ravel(),H.ravel()[:8]).x;return np.r_[v,1].reshape(3,3)
H=homography(holes,flat);mapped=apply(H,outline);origin=apply(H,np.array([j['image_fit']['aperture_circle_source_pixels'][:2]]))[0]
# Terminal line follows original source endpoints after image correspondence.
# New metric assumption: Dorman009 image is nearly planar. It is NOT verified.
ends=outline[(outline[:,1]>1020)&((outline[:,0]<250)|(outline[:,0]>1200))];e=apply(H,ends);u,sv,v=np.linalg.svd(e-e.mean(0));ex=v[0];
if np.dot(flat[6]-flat[0],ex)<0:ex=-ex
ey=np.array([-ex[1],ex[0]])
if np.dot(flat[3]-origin,ey)<0:ey=-ey
basis=np.array([ex,ey]);outer=(mapped-origin)@basis.T;hp=(flat-origin)@basis.T
cam=np.array([95.1098209901611,76.08785679212887]);t=np.linspace(0,math.tau,720,endpoint=False);gear=cam+90.947*np.c_[np.cos(t),np.sin(t)]
def margin(k):
 p=outer[:45]*k;aa=p;bb=np.roll(p,-1,axis=0);v=bb-aa;w=gear[:,None,:]-aa;f=np.clip(np.sum(w*v,axis=2)/np.sum(v*v,axis=1),0,1);ds=np.min(np.linalg.norm(w-f[:,:,None]*v,axis=2),axis=1);return float(np.min(ds*np.where(Poly(p).contains_points(gear),1,-1)))
lo,hi=.1,2
for _ in range(70):
 mid=(lo+hi)/2
 if margin(mid)>=2*mid:hi=mid
 else:lo=mid
k=hi;hnew=hp*k;new=outer*k;term=(e-origin)@basis.T*k
p=j['estimated_coordinated_alternative']['parameters'];ang=math.radians(p[3]);rot=np.array([[math.cos(ang),-math.sin(ang)],[math.sin(ang),math.cos(ang)]]);old=((outline-p[1:3])*[1,-1])*p[0]@rot.T;oldh=((holes-p[1:3])*[1,-1])*p[0]@rot.T
O=R/'cad/engine/generated/timing-flat-photo-registration-study';O.mkdir(exist_ok=True)
r={'status':'ALTERNATE UNVERIFIED PHOTO METRIC HYPOTHESIS; no CAD','method':'Seven-hole homography transfers primary outline/aperture into Dorman009 image only. Assume that separate gasket image near planar, align its terminal line, solve uniform scale solely from actual-axis cam cavity+6mm wall and2px edge reserve. Compressor is not an optimization target.','cautions':['Mapped outline is correspondence-derived, not independently traced009 boundary; hypothesis must be checked against actual009 pixels before adoption.','Aperture is not coplanar with flange in source002; systematic origin error remains unbounded.','Near-planarity of009 is assumed, not calibrated.','Pan terminal coordinates and other protected holes are NOT fixed by this alternative.'], 'scale_mm_per_009_pixel':k,'cam_guard_radius_mm':90.947,'guard_margin_mm':margin(k),'source009_crank_pixel':origin.tolist(),'source009_basis':basis.tolist(),'station_axes': [{'station':i+1,'old_yz_mm':oldh[i].tolist(),'alternate_yz_mm':hnew[i].tolist(),'delta_mm':(hnew[i]-oldh[i]).tolist(),'compressor_axis_distance_mm':float(np.linalg.norm(hnew[i]-[280,100]))} for i in range(7)],'terminal_y_range_mm':[float(term[:,0].min()),float(term[:,0].max())],'terminal_z_range_mm':[float(term[:,1].min()),float(term[:,1].max())],'outline_max_displacement_mm':float(np.max(np.linalg.norm(new-old,axis=1))),'input_sha256':{str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest() for q in [src,rp,Path(__file__)]}}
# Second hypothesis fixes existing pump/main3 axis and terminal seat height,
# rather than transferring an out-of-plane crank aperture.
terminal_base=(e-origin)@basis.T
k2=(oldh[2,1]+24.5)/(hp[2,1]-terminal_base[:,1].mean())
offset=np.array([oldh[2,0]-k2*hp[2,0],-24.5-k2*terminal_base[:,1].mean()])
alternative=outer*k2+offset;alternative_holes=hp*k2+offset
pp=alternative[:45];aa=pp;vv=np.roll(pp,-1,axis=0)-pp;ww=gear[:,None,:]-aa;ff=np.clip(np.sum(ww*vv,axis=2)/np.sum(vv*vv,axis=1),0,1);dist=np.min(np.linalg.norm(ww-ff[:,:,None]*vv,axis=2),axis=1);signed=dist*np.where(Poly(pp).contains_points(gear),1,-1)
r['pump_and_terminal_anchored_hypothesis']={'method':'Fix main3 YZ and mean terminalZ−24.5 using uniform scale/translation in independently aligned009 frame; aperture datum allowed to disagree; compressor not fitted','scale':float(k2),'crank_aperture_axis_error_mm':offset.tolist(),'cam_guard_minimum_margin_mm':float(signed.min()),'actual_tip_envelope_exclusion_lower_bound_mm':float(max(0,-signed.min()-7.0)),'station_axes_yz_mm':alternative_holes.tolist(),'terminal_y_range_mm':[float((terminal_base*k2+offset)[:,0].min()),float((terminal_base*k2+offset)[:,0].max())],'terminal_z_range_mm':[float((terminal_base*k2+offset)[:,1].min()),float((terminal_base*k2+offset)[:,1].max())],'status':'REJECTED: negative cam guard and protected terminal mismatch; no replacement geometry'}
(R/'inventory/engine/timing-flat-photo-registration-study.json').write_text(json.dumps(r,indent=2)+'\n')
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(10,7));ax.plot(*old.T,color='#ac5146',label='Frozen original registration');ax.plot(*new.T,color='#397aa4',label='Unverified Dorman009 metric hypothesis');ax.scatter(*hnew.T,c='#397aa4');ax.plot(*alternative.T,color='#985ca4',label='009 fixed main3 / terminal-plane hypothesis')
for i,q in enumerate(hnew):ax.annotate(str(i+1),q)
ax.plot(*gear.T,color='#658255',label='Actual-axis cam guard R90.947');ax.plot(280+65*np.cos(t),100+65*np.sin(t),color='black',label='Existing compressor barrel R65');ax.set_aspect('equal');ax.grid(alpha=.2);ax.legend(fontsize=8);ax.set(xlabel='Y mm',ylabel='Z mm',title='Independent photo-frame scale hypothesis — no replacement geometry\nNot fitted to compressor; terminal/other-axis deviations remain disqualifying');fig.tight_layout();fig.savefig(O/'photo-hypothesis-review.png',dpi=160)
