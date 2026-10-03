"""Coplanar landmark study. No manufacturer pixels emitted; no CAD mutations."""
from pathlib import Path
import ast,hashlib,json,math
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];PREFIX='pump-cover-joint-20261003'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# Original ATK1200x1200 pixels; manual hole-center picks +/-2px per coordinate.
# Cover1 was found on enlarged view, not an accessory lug at(268,762).
pump=np.array([[-24.3,103.5],[34.3,176.3],[-98.2,175.3],[-15,234.9]])
pump_px=np.array([[532.,716.],[658.,590.],[405.,567.],[576.,470.]])
fifth=np.array([-42.9,239.]);fifth_px=np.array([522.,457.])
cover_px=np.array([[359.,946.],[462.,901.],[557.,758.],[745.,581.],[969.,654.],[1017.,806.],[953.,951.]])
# Forward gear hubs are explicitly NOT block-face coplanar landmarks.
forward_px=np.array([[596.,990.],[802.,800.]])
source=R/'cad/engine/timing_cover_joint_candidate.py'
a={n.targets[0].id:ast.literal_eval(n.value) for n in ast.parse(source.read_text()).body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ['OUTLINE_NORMALIZED','HOLES_NORMALIZED']}
theta=math.radians(-.039823552987937626)
rot=np.array([[math.cos(theta),math.sin(theta)],[-math.sin(theta),math.cos(theta)]])
def oldreg(p):return ((np.array(p)*1600-[588.5373742452892,930.4751087566926])*[1,-1])*.26223302269259874@rot
cover=oldreg(a['HOLES_NORMALIZED']);outline=oldreg(a['OUTLINE_NORMALIZED'])
def project(h,p):
 p=np.atleast_2d(p);q=np.c_[p,np.ones(len(p))]@h.T;return q[:,:2]/q[:,2,None]
def homography(s,d):
 # Four explicit anchors only; zero fit residual is tautological, not acceptance.
 A=[];v=[]
 for(x,y),(u,w)in zip(s,d):A.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-w*x,-w*y]]);v.extend([u,w])
 return np.r_[np.linalg.solve(A,v),1].reshape(3,3)
def similarity(s,d):
 ss=s-s.mean(0);dd=d-d.mean(0);u,_,v=np.linalg.svd(ss.T@dd);r=u@v
 if np.linalg.det(r)<0:u[:,-1]*=-1;r=u@v
 k=np.sum((ss@r)*dd)/np.sum(ss*ss);t=d.mean(0)-k*s.mean(0)@r
 return k,r,t,k*s@r+t
h=homography(pump,pump_px);hi=np.linalg.inv(h);rect=project(hi,cover_px)
k,r,t,fit=similarity(cover,rect);resid=np.linalg.norm(rect-fit,axis=1)
span=float(np.linalg.norm(pump[1]-pump[2]));gap=float(np.linalg.norm(rect[2]-pump[0]));fitgap=float(np.linalg.norm(fit[2]-pump[0]))
# Perturb every selected image hole; also perturb cover source picks +/-3/1600.
rng=np.random.default_rng(473203);draws=[]
for i in range(2000):
 hp=homography(pump,pump_px+rng.uniform(-2,2,pump_px.shape));ri=project(np.linalg.inv(hp),cover_px+rng.uniform(-2,2,cover_px.shape))
 cp=oldreg(np.array(a['HOLES_NORMALIZED'])+rng.uniform(-3/1600,3/1600,cover.shape))
 ki,rr,tt,ff=similarity(cp,ri)
 draws.append([np.linalg.norm(ri[2]-pump[0]),np.linalg.norm(ff[2]-pump[0]),ki,math.degrees(math.atan2(rr[0,1],rr[0,0])),*tt,np.sqrt(np.mean(np.sum((ri-ff)**2,axis=1)))])
# Controls for held-out aperture/correspondence detection, no acceptance of fit to training anchors.
bad=homography(pump,pump_px[[0,2,1,3]])
controls={'normal_fifth_residual_px':float(np.linalg.norm(project(h,fifth)[0]-fifth_px)),'swapped_side_holes_fifth_residual_px':float(np.linalg.norm(project(bad,fifth)[0]-fifth_px)),'fifth_shift_20px_residual_px':float(np.linalg.norm(project(h,fifth)[0]-(fifth_px+[20,0])))}
# Seven leave-one-out similarities in rectified plane, independent heldout station.
held=[]
for i in range(7):
 mask=np.arange(7)!=i;kk,rr,tt,_=similarity(cover[mask],rect[mask]);held.append(float(np.linalg.norm(kk*cover[i]@rr+tt-rect[i])))
inputs=[source,R/'cad/engine/timing_cover_front_joint_candidate.py',R/'cad/engine/timing_cover_seven_fastener_candidate.py',R/'cad/engine/water_pump_gasket_topology_candidate.py',R/'cad/engine/water_pump_joint_candidate.py',R/'cad/engine/pump_functional_20261003.py',R/'inventory/engine/corrected-engine-stage-v4.json',R/'reference/engine/atk-dff8-block-front.jpg',R/'reference/engine/felpro-13816.jpg',R/'cad/engine/generated/timing-cover-joint-candidate/reference/tcs45829-manufacturer.jpg',R/'cad/engine/generated/timing-cover-joint-candidate/reference/dorman-635109-002.jpg',R/'cad/engine/generated/timing-cover-joint-candidate/reference/dorman-635109-009.jpg',R/'reference/engine/pump-functional-20261003-delivery.json',R/'reference/engine/pump-source-registration-20261003-delivery.json',Path(__file__)]
out={'status':'RESEARCH; source-led proposed layout only, not installed or factory measured','coordinate_class':'Rectified units inherit existing estimated pump pattern; no independent metric anchor','source':{'url':'https://www.ebay.com/itm/146111774717','image_url':'https://i.ebayimg.com/images/g/bBwAAOSw8FVnEovT/s-l1200.jpg','part':'ATK DFF8; seller Titan Engines; remanufactured Ford300/4.9L1987-1996 listing','view':'Oblique engine front; pump and timing cover absent; gear hubs forward of block face','pixel_dimensions':[1200,1200],'source_pixels_excluded':True},'landmarks':{'pump_order_bottom_right_left_top_pixels':pump_px.tolist(),'pump_world_candidate_mm':pump.tolist(),'fifth_pixels':fifth_px.tolist(),'fifth_candidate_mm':fifth.tolist(),'cover_order_source_gasket_1_to_7_pixels':cover_px.tolist(),'cover_current_world_mm':cover.tolist(),'forward_crank_cam_hub_pixels_NOT_COPLANAR':forward_px.tolist(),'selection_uncertainty_px_each_coordinate':2,'forward_hub_selection_uncertainty_px':4},'homography_candidate_pump_plane_to_image':h.tolist(),'held_out_fifth':controls,'common_face':{'cover_rectified_candidate_mm':rect.tolist(),'normalized_cover_relative_pump_center_over_side_bolt_span':((rect-[-32,170])/span).tolist(),'normalizing_side_bolt_span_candidate_mm':span,'current_axis_gap_mm':float(np.linalg.norm(cover[2]-pump[0])),'source_conditional_axis_gap_candidate_mm':gap,'source_gap_over_pump_side_span':gap/span},'proposed_cover_similarity':{'scale':float(k),'rotation_deg':math.degrees(math.atan2(r[0,1],r[0,0])),'row_vector_rotation_matrix':r.tolist(),'offset_candidate_mm':t.tolist(),'axes_candidate_mm':fit.tolist(),'residuals_candidate_mm':resid.tolist(),'rms_candidate_mm':float(np.sqrt(np.mean(resid**2))),'rms_reprojected_pixels':float(np.sqrt(np.mean(np.sum((project(h,fit)-cover_px)**2,axis=1)))),'leave_one_out_residuals_candidate_mm':held,'gap_candidate_mm':fitgap,'nominal_radial_margin_to_R11_5_pump_R8_75_cover_head_mm':fitgap-20.25,'nominal_radial_margin_to_R11_5_pump_R10_5_tool_mm':fitgap-22.,'method':'Proper similarity fitted to seven source holes in the pump-rectified block face. No overlap witness or clearance term in fit.'},'sensitivity':{'seed':473203,'trials':2000,'columns':['raw_gap','similarity_gap','scale','rotation_deg','offset_y','offset_z','fit_rms'],'p2_5_p50_p97_5':np.percentile(draws,[2.5,50,97.5],axis=0).tolist(),'limits':'Pixel selection only, not statistical confidence, no lens/flatness/pump-pattern calibration uncertainty.'},'noncoplanar_diagnostic_NOT_METRIC':{'forward_hubs_pseudo_rectified':project(hi,forward_px).tolist(),'old_crank_marker_reprojected_pixels':project(h,[0,0])[0].tolist(),'forbidden_inference':'Do not translate crank/pump from hub pixel displacement. Forward hub depth and camera calibration unknown.'},'caveats':['Pump anchor geometry inherits Fel-Pro photo ratios and estimated R59 scale.','Four anchor perfect fit is not independent evidence. Fifth aperture is held out.','Seven cover holes may carry source-photo perspective; similarity residual and leave-one-out retained.','No seal mounting bore is exposed in this block photograph; visible shaft bore, gear OD and pump ellipse are not interchangeable dimensional references.','Carter98.43mm axial mounting height is not a scale for transverse ATK block face.','Proposed smaller/rotated cover gasket registration is not a shell/gear/pan feasibility PASS.','Earlier preliminary identification omitted coverhole1(359,946); final seven-hole correspondence excludes accessory lugs(268,762),(313,644).'],'inputs_sha256':{str(p.relative_to(R)):sha(p)for p in inputs}}
(R/f'reference/engine/{PREFIX}-measurements.json').write_text(json.dumps(out,indent=2)+'\n')
fig,axs=plt.subplots(1,2,figsize=(14,7));ax=axs[0]
ax.plot(*pump_px.T,'o',label='Pump anchors');ax.scatter(*fifth_px,marker='*',s=110,label='Withheld fifth');ax.plot(*cover_px.T,'o-',label='Observed cover holes');ax.plot(*project(h,cover).T,'x--',label='Current cover projected');ax.plot(*project(h,fit).T,'+--',label='Source-fit cover')
for i,(x,y)in enumerate(cover_px,1):ax.annotate(f'C{i}',(x,y),xytext=(5,5),textcoords='offset points')
ax.set_aspect('equal');ax.invert_yaxis();ax.set_title('ATK front face: authored landmark comparison');ax.set_xlabel('Original image x / px');ax.set_ylabel('Original image y / px');ax.legend(fontsize=8)
ax=axs[1];ax.plot(*outline.T,'--',alpha=.5,label='Current gasket outline');ax.plot(*(k*outline@r+t).T,label='Source-fit gasket hypothesis');ax.plot(*pump.T,'o',label='Pump anchors');ax.plot(*rect.T,'+',label='Rectified cover observations');
for rad,color,name in [(11.5,'tab:blue','Protected pump boss'),(8.75,'tab:orange','Cover head envelope')]:
 center=pump[0] if rad==11.5 else fit[2];ax.add_patch(plt.Circle(center,rad,fill=False,color=color,label=name))
ax.plot(*np.array([pump[0],fit[2]]).T,':',color='black');ax.set_aspect('equal');ax.set_xlabel('Y / conditional candidate-mm');ax.set_ylabel('Z / conditional candidate-mm');ax.set_title('Common face hypothesis; no independent metric scale');ax.legend(fontsize=8)
fig.suptitle('Pump / cover joint: registration study only — geometry feasibility NOT RUN');fig.tight_layout();fig.savefig(R/f'reference/engine/{PREFIX}-review.png',dpi=160);plt.close(fig)
print(json.dumps({k:out[k]for k in ['held_out_fifth','common_face','proposed_cover_similarity','sensitivity']},indent=2))
