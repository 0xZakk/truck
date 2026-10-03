from pathlib import Path
import itertools,json,hashlib,math
import numpy as np
from scipy import ndimage, stats
from PIL import Image
R=Path(__file__).resolve().parents[1];lp=R/'reference/engine/pump-source-registration-20261003-landmarks.json';L=json.loads(lp.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();ip=R/L['image_path'];assert sha(ip)==L['sha256']
im=np.array(Image.open(ip).convert('RGB'));white=np.min(im,axis=2)>L['white_hole_threshold'];lab,num=ndimage.label(white);holes=[]
for i,sl in enumerate(ndimage.find_objects(lab),1):
 if sl is None:continue
 sy,sx=sl;area=int(np.sum(lab[sl]==i))
 if 1000<area<6000 and sy.start>1100 and sx.start>300 and sx.stop<1300:
  cy,cx=ndimage.center_of_mass(white,lab,i);holes.append({'xy':[float(cx),float(cy)],'area_px2':area,'bbox':[sx.start,sy.start,sx.stop,sy.stop]})
assert len(holes)==4
def darkcenter(box,threshold):
 x0,y0,x1,y1=box;mask=im[y0:y1,x0:x1].mean(2)<threshold;lab,num=ndimage.label(mask);sizes=np.bincount(lab.ravel());sizes[0]=0;n=sizes.argmax();cy,cx=ndimage.center_of_mass(mask,lab,n);return np.array([cx+x0,cy+y0])
fifth=darkcenter(L['fifth_dark_roi_xyxy'],60);shaft=darkcenter(L['shaft_dark_roi_xyxy'],60)
# These are the frozen source-module estimates, not new measured millimeters.
M=np.array([[7.7,-66.5],[66.3,6.3],[-66.2,5.3],[17.,64.9]])*[-1,1]
E=np.array([10.9,69.]);S=np.array([x['xy']for x in holes])*[1,-1]
def fit(M,B,det=1):
 a=M-M.mean(0);z=B-B.mean(0);U,sv,Vt=np.linalg.svd(a.T@z);D=np.diag([1,det*np.linalg.det(U@Vt)]);rot=U@D@Vt;scale=np.sum(sv*np.diag(D))/np.sum(a*a);trans=B.mean(0)-scale*M.mean(0)@rot;pred=scale*M@rot+trans
 return scale,rot,trans,float(np.sqrt(np.mean(np.sum((pred-B)**2,axis=1))))
candidates=[]
for perm in itertools.permutations(range(4)):
 for det in [1,-1]:
  scale,rot,trans,rms=fit(M,S[list(perm)],det)
  candidates.append({'permutation':list(perm),'handedness':det,'scale_px_per_candidate_mm':float(scale),'rotation':rot.tolist(),'translation_math_px':trans.tolist(),'bolt_rms_px':rms,'fifth_error_px':float(np.linalg.norm(scale*E@rot+trans-fifth*[1,-1])),'shaft_error_px':float(np.linalg.norm(trans-shaft*[1,-1]))})
# Rank by bolt residual only; held-out landmarks independently disambiguate.
candidates.sort(key=lambda q:q['bolt_rms_px']);best=candidates[0];scale=best['scale_px_per_candidate_mm'];rot=np.array(best['rotation']);trans=np.array(best['translation_math_px']);perm=best['permutation']
def project(yz):return (scale*(np.asarray(yz)*[-1,1])@rot+trans)*[1,-1]
def angle(vec):return float(np.degrees(np.arctan2(vec[1],vec[0])))
def anglediff(a,z):return float((a-z+180)%360-180)
angle_roll=angle(np.array([1.,0.])@rot)
# The fixed azimuths below are read-only candidate parameters.
idir=np.array([math.cos(math.radians(-130)),math.sin(math.radians(-130))])
hdir=np.array([math.cos(math.radians(145)),math.sin(math.radians(145))])
candidate_points={'heater_visible_root_cuff_axis':project([-48.,60.3]),'heater_terminal_opening_center':project([-139.,245.]),'inlet_terminal_rim_center':project(np.array([[math.cos(math.radians(-130)),-math.sin(math.radians(-130))],[math.sin(math.radians(-130)),math.cos(math.radians(-130))]])@np.array([145.,6.]))}
mask=np.min(im,axis=2)<220
inletaxis=[]
for x in L['inlet_straight_axis_columns']:
 low,high=L['inlet_axis_y_roi'];ys=np.where(mask[low:high,x])[0]+low;inletaxis.append([x,float((ys.min()+ys.max())/2)])
heateraxis=[]
for y in L['heater_straight_axis_rows']:
 low,high=L['heater_axis_x_roi'];xs=np.where(mask[y,low:high])[0]+low;heateraxis.append([float((xs.min()+xs.max())/2),y])
slope_i=np.polyfit(np.array(inletaxis)[:,0],np.array(inletaxis)[:,1],1)[0]
slope_h_ols=np.polyfit(np.array(heateraxis)[:,1],np.array(heateraxis)[:,0],1)[0]
slope_h=float(stats.theilslopes(np.array(heateraxis)[:,0],np.array(heateraxis)[:,1]).slope)
src_ia=angle([1,-slope_i]);src_ha=angle([-slope_h,1])
mod_ia=angle((idir*[-1,1])@rot);mod_ha=angle((hdir*[-1,1])@rot)
features={}
radius=float(np.sqrt(np.mean(np.sum((S-trans)**2,axis=1))))
for name,v in L['manual_points'].items():
 source=np.array(v['xy']);model=candidate_points[name];sv=(source*[1,-1])-trans;mv=(model*[1,-1])-trans
 features[name]={'source_xy':source.tolist(),'candidate_registered_xy':model.tolist(),'source_uncertainty_px':v['uncertainty_px'],'residual_px':float(np.linalg.norm(model-source)),'source_radial_angle_deg':angle(sv),'candidate_radial_angle_deg':angle(mv),'radial_angle_difference_deg':anglediff(angle(mv),angle(sv)),'source_radius_normalized_bolt_rms_radius':float(np.linalg.norm(sv)/radius),'candidate_radius_normalized_bolt_rms_radius':float(np.linalg.norm(mv)/radius),'source_over_candidate_projected_radius':float(np.linalg.norm(sv)/np.linalg.norm(mv))}
# Affine fit is diagnostic; do not interpret a flexible planar map as evidence of factory dimensions.
aff=np.linalg.lstsq(np.c_[M,np.ones(4)],S[perm],rcond=None)[0];ares=np.c_[M,np.ones(4)]@aff-S[perm];sv=np.linalg.svd(aff[:2],compute_uv=False)
affine={'bolt_rms_px':float(np.sqrt(np.mean(np.sum(ares**2,axis=1)))),'axis_scale_ratio':float(max(sv)/min(sv)),'fifth_error_px':float(np.linalg.norm(np.r_[E,1]@aff-fifth*[1,-1]))}
# Perturb image landmarks only; this does not cover lens/perspective or unknown model error.
rng=np.random.default_rng(20261003);runs=[]
for _ in range(2000):
 noisy=S[perm]+rng.uniform(-2,2,(4,2));sc,rr,tt,err=fit(M,noisy)
 ia=np.array(inletaxis)+rng.uniform(-2,2,(len(inletaxis),2));ha=np.array(heateraxis)+rng.uniform(-2,2,(len(heateraxis),2))
 si=np.polyfit(ia[:,0],ia[:,1],1)[0];sh=float(stats.theilslopes(ha[:,0],ha[:,1]).slope)
 ai=angle([1,-si]);ah=angle([-sh,1]);runs.append([angle(np.array([1.,0])@rr),sc,anglediff(ah,ai)])
runs=np.array(runs);sensitivity={n:{'min':float(runs[:,i].min()),'max':float(runs[:,i].max()),'p2_5':float(np.percentile(runs[:,i],2.5)),'p97_5':float(np.percentile(runs[:,i],97.5))}for i,n in enumerate(['roll_deg','scale_px_per_candidate_mm','source_heater_minus_inlet_angle_deg'])}
# Read-only actual housing mesh outline projected with the fitted rear similarity.
gp=R/'cad/engine/generated/pump-functional-20261003/water-pump-housing.glb';npz=R/'reference/engine/pump-source-registration-20261003-candidate-projection.npz';md=json.loads((R/'reference/engine/pump-source-registration-20261003-mesh-data.json').read_text());assert sha(gp)==md['source_sha256']and sha(npz)==md['npz_sha256'];mesh=np.load(npz);v=mesh['vertices'];projected=project(v[:,1:]-[-32,170]);tris=projected[mesh['faces']];outline=[]
for x in L['outline_columns']:
 src=[]
 for threshold in L['outline_threshold_sensitivity']:
  low,high=L['outline_y_roi'];ys=np.where(im[low:high,x].min(1)<threshold)[0]+low;src.append([float(ys.min()),float(ys.max())])
 near=tris[(tris[:,:,0].min(1)<=x)&(tris[:,:,0].max(1)>=x)];hits=[]
 for i,j in [(0,1),(1,2),(2,0)]:
  a,z=near[:,i],near[:,j];ok=(a[:,0]-x)*(z[:,0]-x)<=0;delta=z[ok,0]-a[ok,0];good=abs(delta)>1e-9;aa=a[ok][good];zz=z[ok][good];hits.extend((aa[:,1]+(x-aa[:,0])/(zz[:,0]-aa[:,0])*(zz[:,1]-aa[:,1])).tolist())
 model=[float(min(hits)),float(max(hits))]if hits else None
 outline.append({'x_px':x,'source_threshold_y_bounds':src,'candidate_y_bounds':model,'source_width_px_at220':src[2][1]-src[2][0],'candidate_width_px':None if model is None else model[1]-model[0]})
r={'status':'RESEARCH only; no CAD changes; conditional near-rear similarity','source_holes':holes,'source_fifth_xy':fifth.tolist(),'source_shaft_xy':shaft.tolist(),'all_correspondences':candidates,'best_by_bolts':best,'roll_deg':angle_roll,'bolt_rms_radius_px':radius,'affine_diagnostic':affine,'axes':{'source_inlet_deg':src_ia,'source_heater_near_root_deg':src_ha,'source_heater_OLS_deg':angle([-slope_h_ols,1]),'heater_fit_method':'Theil-Sen robust line; row1170 encounters collar flare; all samples retained, OLS result also reported.','candidate_registered_inlet_deg':mod_ia,'candidate_registered_heater_deg':mod_ha,'source_heater_minus_inlet_deg':anglediff(src_ha,src_ia),'candidate_heater_minus_inlet_deg':anglediff(mod_ha,mod_ia),'inlet_samples_xy':inletaxis,'heater_samples_xy':heateraxis},'manual_features':features,'outline_samples':outline,'pixel_sensitivity_2000_trials':sensitivity,'caveats':['Scale uses candidate assumed bolt coordinates, NOT source-measured millimeters.','Near-similarity fit does not calibrate axial parallax, lens or unknown camera perspective.','Manual end/root/rim coordinates are projected silhouettes and carry declared uncertainty.','Affine/homography cannot establish3D shape; no perfect4-point homography claimed.','Existing bolt pattern derives from approximate Fel-Pro13816 photo ratios scaled to estimated centralR59, not known independent dimensional survey.'],'inputs':{str(p.relative_to(R)):sha(p)for p in[lp,ip,gp,npz,Path(__file__),R/'cad/engine/water_pump_gasket_topology_candidate.py',R/'cad/engine/pump_functional_20261003.py',R/'reference/engine/pump-functional-20261003-delivery.json']}}
(R/'reference/engine/pump-source-registration-20261003-measurements.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'best':best,'roll':angle_roll,'axes':r['axes'],'features':features,'affine':affine,'outline':outline,'sensitivity':sensitivity},indent=2))

opening={'hole_white_equivalent_radii_px':[math.sqrt(q['area_px2']/math.pi)for q in holes],'candidate_housing_bore_radius_projected_px':4.3*scale,'candidate_gasket_hole_radius_projected_px':5.2*scale,'classification':'Conditional opening-size comparison only: white aperture threshold is image area; obliquity and rear lip distinction unresolved. Does not authorize a bore diameter change.','scope':'Supplementary source proportions, not an independent dimensional survey'}
(R/'reference/engine/pump-source-registration-20261003-opening-proportions.json').write_text(json.dumps(opening,indent=2)+'\n')
