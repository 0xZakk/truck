#!/usr/bin/env python3
"""Photo registration versus physical similarity feasibility, no CAD mutation."""
from pathlib import Path
import ast,json,hashlib
import numpy as np
from scipy.optimize import least_squares, minimize_scalar, differential_evolution
from matplotlib.path import Path as Polygon
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-cover-registration-study';OUT.mkdir(parents=True,exist_ok=True)
source=ROOT/'cad/engine/timing_cover_joint_candidate.py'
mod=ast.parse(source.read_text());a={n.targets[0].id:ast.literal_eval(n.value) for n in mod.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ['OUTLINE_NORMALIZED','HOLES_NORMALIZED']}
outline=np.array(a['OUTLINE_NORMALIZED'])*1600;holes=np.array(a['HOLES_NORMALIZED'])*1600
back=np.array([(52,318),(156,281),(319,305),(560,296),(621,139),(542,45),(418,14)],float)
flat=np.array([(592,329),(492,292),(333,319),(87,304),(21,137),(99,43),(227,12)],float)
# White-aperture connected boundary at grayscale160,24 angle samples;
# seed(205,198), source002 hash recorded in review. ±4 pixel model covers edge choice.
aperture=np.array([[164, 203], [168, 193], [174, 185], [182, 179], [189, 176], [197, 174], [205, 172], [213, 172], [222, 174], [231, 177], [240, 183], [247, 192], [248, 203], [244, 214], [237, 222], [230, 227], [221, 231], [213, 233], [205, 234], [197, 234], [188, 232], [180, 228], [172, 222], [166, 213]],float)
def apply(H,p):
 q=np.c_[p,np.ones(len(p))]@H.T;return q[:,:2]/q[:,2,None]
def homography(src,dst):
 A=[]
 for (x,y),(u,v) in zip(src,dst):A.extend([[-x,-y,-1,0,0,0,u*x,u*y,u],[0,0,0,-x,-y,-1,v*x,v*y,v]])
 H=np.linalg.svd(A)[2][-1].reshape(3,3);H/=H[2,2]
 q=least_squares(lambda a:(apply(np.r_[a,1].reshape(3,3),src)-dst).ravel(),H.ravel()[:8],max_nfev=150).x
 return np.r_[q,1].reshape(3,3)
def similarity(src,dst):
 s=src-src.mean(0);d=dst-dst.mean(0);u,_,v=np.linalg.svd(s.T@d);r=u@v;k=np.sum((s@r)*d)/np.sum(s*s);return k*s@r+dst.mean(0),np.linalg.det(r)
def circle(points):
 r=least_squares(lambda a:np.linalg.norm(points-a[:2],axis=1)-a[2],[590,940,100]);return r.x,float(np.sqrt(np.mean(r.fun**2)))
H=homography(holes,back);q=apply(np.linalg.inv(H),aperture);cf,cr=circle(q)
sim,det=similarity(holes,back);flatH=homography(holes,flat);flatSim,flatDet=similarity(holes,flat)
rng=np.random.default_rng(32094);draws=[]
for i in range(120):
 src=holes+rng.uniform(-3,3,holes.shape);dst=back+rng.uniform(-5,5,back.shape);ap=aperture+rng.uniform(-4,4,aperture.shape)
 try: draws.append(circle(apply(np.linalg.inv(homography(src,dst)),ap))[0])
 except Exception:pass
bounds=np.percentile(draws,[2.5,97.5],axis=0)
# Flat terminal band in primary source has small hand-trace waviness.
left=outline[(outline[:,0]<250)&(outline[:,1]>1020)];right=outline[(outline[:,0]>1200)&(outline[:,1]>1020)]
ends=np.concatenate([left,right]);line=np.polyfit(ends[:,0],ends[:,1],1);rot0=np.degrees(np.arctan(line[0]))
cam=np.array([[90.,72.],[95.1098209901611,76.08785679212887]])
theta=np.linspace(0,2*np.pi,360,endpoint=False);ring=np.concatenate([c+86.947*np.c_[np.cos(theta),np.sin(theta)] for c in cam])
def trans(points,param,mirror=1):
 scale,cx,cy,angle=param;t=np.radians(angle);R=np.array([[np.cos(t),-np.sin(t)],[np.sin(t),np.cos(t)]]);return ((points-[cx,cy])*[mirror,-1])*scale@R.T
def signed_distance(points,poly):
 a=poly;b=np.roll(poly,-1,axis=0);v=b-a;w=points[:,None,:]-a;frac=np.clip(np.sum(w*v,axis=2)/np.sum(v*v,axis=1),0,1);dist=np.min(np.linalg.norm(w-frac[:,:,None]*v,axis=2),axis=1);return dist*np.where(Polygon(poly).contains_points(points),1,-1)
# Outer arch closes along its two lowest tips. Cam disks lie above this closure;
# crank lower bridge is deliberately omitted and must be designed separately.
def gear_margin(param,mirror=1):return float(np.min(signed_distance(ring,trans(outline[:45],param,mirror))))
def terminal_error(param,mirror=1):
 p=trans(ends,param,mirror);dy=np.maximum(np.maximum(-140-p[:,0],p[:,0]-116.6),0);return float(np.max(np.hypot(dy,p[:,1]+32)))
# Conservative full-band seating test: all source terminal-edge samples must fit
# current pan rail corridor. The cropped front gasket is narrower at round corners.
def loss(param,mirror=1):return max(terminal_error(param,mirror),max(0,-gear_margin(param,mirror)))
photo_bounds=[(.16,.34),(float(bounds[0,0]),float(bounds[1,0])),(float(bounds[0,1]),float(bounds[1,1])),(-30,30)]
fits=[]
for mirror in [1,-1]:
 result=differential_evolution(lambda p:loss(p,mirror),photo_bounds,seed=32,popsize=12,maxiter=110,tol=.0001,polish=True)
 fits.append({'mirror_y':mirror,'parameters':result.x.tolist(),'max_constraint_violation_mm':float(result.fun),'terminal_band_error_mm':terminal_error(result.x,mirror),'gear_wall_margin_mm':gear_margin(result.x,mirror)})
# Extended registration freedoms illustrate missing depth-plane information.
free=differential_evolution(loss,[(.16,.38),(450,800),(750,1100),(-30,30)],seed=32,popsize=14,maxiter=160,tol=.0001,polish=True)
# Coherent estimated alternative: retain aperture-centered similarity and a flat
# terminal plane; solve only minimum scale needed by both protected cam disks.
lo,hi=.16,.4
for i in range(40):
 mid=(lo+hi)/2
 if gear_margin([mid,*cf[:2],rot0])>=0:hi=mid
 else:lo=mid
nominal_minimum_scale=hi
lo,hi=.16,.4
for i in range(40):
 mid=(lo+hi)/2
 if gear_margin([mid,*cf[:2],rot0])>=8*mid:hi=mid
 else:lo=mid
proposed=[hi,*cf[:2],rot0];te=trans(ends,proposed);poly=trans(outline,proposed)
sensitivity=[]
for cx in bounds[:,0]:
 for cy in bounds[:,1]:
  low,high=.16,.4
  for _ in range(36):
   mid=(low+high)/2
   if gear_margin([mid,cx,cy,rot0])>=8*mid:high=mid
   else:low=mid
  points=trans(ends,[high,cx,cy,rot0])
  sensitivity.append({'crank_source_pixel':[cx,cy],'scale':high,'terminal_y_range_mm':[float(points[:,0].min()),float(points[:,0].max())],'terminal_z_range_mm':[float(points[:,1].min()),float(points[:,1].max())]})
r={'scope':'Feasibility study; no factory dimensions or installed acceptance','input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),source]},'photo_samples':{'source_holes_pixels':holes.tolist(),'dorman002_holes_pixels':back.tolist(),'dorman009_holes_pixels':flat.tolist(),'dorman002_aperture_boundary_pixels':aperture.tolist(),'uncertainty_pixels':{'source_holes':3,'back_holes':5,'aperture':4}},'image_fit':{'homography_source_to_back002':H.tolist(),'seven_hole_residual_pixels':np.linalg.norm(apply(H,holes)-back,axis=1).tolist(),'similarity_rms_pixels':float(np.sqrt(np.mean(np.sum((sim-back)**2,axis=1)))),'similarity_determinant':float(det),'flat009_similarity_rms_pixels':float(np.sqrt(np.mean(np.sum((flatSim-flat)**2,axis=1)))),'flat009_homography_rms_pixels':float(np.sqrt(np.mean(np.sum((apply(flatH,holes)-flat)**2,axis=1)))),'aperture_circle_source_pixels':cf.tolist(),'circle_rms_pixels':cr,'pixel_only_95percent_interval':bounds.tolist(),'monte_carlo_seed':32094,'trials':120,'current_seal_ID_scale_comparison':{'current_model_inner_radius_mm':21,'implied_scale_from_aperture':float(21/cf[2]),'limit':'Not a dimensional constraint: current radius is provisional and aperture is not coplanar.'},'depth_parallax':'NOT BOUNDED by this pixel interval. Aperture lies forward of flange; images lack depth/calibration. Circle is only a coplanar approximation.'},'physical_registration':{'method':'Rigid in-plane rotation/reflection plus uniform scale about estimated crank point. No homography applied to CAD.','flat_terminal_rotation_deg':float(rot0),'current_pan_corridor_y_mm':[-140,116.6],'current_pan_rail_z_mm':-32,'gear_protection_radius_mm':86.947,'gear_radius_definition':'83.947 source tip radius +1 estimated clearance +2 estimated wall','photo_constrained_fits':fits,'expanded_unknown_datum_fit':{'parameters':free.x.tolist(),'max_constraint_violation_mm':float(free.fun),'terminal_band_error_mm':terminal_error(free.x),'gear_wall_margin_mm':gear_margin(free.x),'limit':'Expanded crank-image coordinates are hypothetical depth/registration freedom, not observed aperture location.'}},'estimated_coordinated_alternative':{'parameters':proposed,'pixel_interval_corner_sensitivity':sensitivity,'nominal_minimum_scale':nominal_minimum_scale,'trace_uncertainty_reserve_mm':8*hi,'terminal_y_range_mm':[float(te[:,0].min()),float(te[:,0].max())],'terminal_z_range_mm':[float(te[:,1].min()),float(te[:,1].max())],'gear_wall_margin_mm':gear_margin(proposed),'required_pan_change':'Local front seat/terminal corridor must reach these ranges; current pan stations are not moved. This is a proposed coordinated envelope only, not a sealed joint or clamp-load design.'},'status':'NO INSTALLED JOINT; review photo constraints and coordinated alternative','pan_station_count':25,'fixed_crank_yz':[0,0],'fixed_seal_x_mm':414,'browser':'NOT RUN','learning':'NOT RUN'}
(ROOT/'inventory/engine/timing-cover-registration-validation.json').write_text(json.dumps(r,indent=2)+'\n');np.savez_compressed(OUT/'registration-preview.npz',outline=outline,aperture=q,fit=cf,holes=holes,back=back,H=H,proposed_outline=poly,ring=ring,ends=te);print(json.dumps(r,indent=2))
