"""Held-out block/head seam audit. No CAD or clearance fitting; no source redistribution."""
from pathlib import Path
import json,hashlib,ast
import numpy as np
from matplotlib.path import Path as Polygon
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
R=Path(__file__).resolve().parents[1];P='pump-cover-candidate-20261003'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
f=R/'reference/engine/pump-cover-joint-20261003-joint-fit.json';j=json.loads(f.read_text());x=np.array(j['parameters']);H=np.r_[x[:8],1].reshape(3,3);rot=np.array([[np.cos(x[9]),np.sin(x[9])],[-np.sin(x[9]),np.cos(x[9])]]);k=np.exp(x[8]);t=150*x[10:12]
def rect(p):
 p=np.atleast_2d(p);v=np.c_[p/1000,np.ones(len(p))]@np.linalg.inv(H).T
 return (150*v[:,:2]/v[:,2,None]-t)@rot.T/k
# Manual held-out observations on the existing 1200px public replacement photo.
seam=np.array([[470,414],[530,414],[590,415],[660,415],[727,416]])
pan=np.array([[450,977],[950,980]])
# Main outlet aperture approximate extremes; recess/seat identity is NOT established.
port=np.array([[563,320],[620,264],[678,320],[620,375]])
s=rect(seam);p=rect(pan);q=rect(port);deck=254.;pan_z=-24.5
scale=(deck-pan_z)/(np.mean(s[:,1])-np.mean(p[:,1]));shift=pan_z-scale*np.mean(p[:,1])
local=[]
for a in np.vstack([seam,pan,port]):
 J=np.column_stack([(rect(a+np.eye(2)[d])-rect(a-np.eye(2)[d]))[0]/2 for d in range(2)])
 local.append({'pixel':a.tolist(),'singular_values_mm_per_px':np.linalg.svd(J)[1].tolist(),'condition_number':float(np.linalg.cond(J))})
rng=np.random.default_rng(473205);vals=[]
for _ in range(2000):
 ss=rect(seam+rng.uniform(-3,3,seam.shape));pp=rect(pan+rng.uniform(-3,3,pan.shape));sc=(deck-pan_z)/(ss[:,1].mean()-pp[:,1].mean());vals.append([ss[:,1].mean(),sc,pan_z-sc*pp[:,1].mean()])
measure=R/'reference/engine/pump-cover-joint-20261003-measurements.json';lm=json.loads(measure.read_text())['landmarks'];pa=rect(lm['pump_order_bottom_right_left_top_pixels']);ca=rect(lm['cover_order_source_gasket_1_to_7_pixels'])
report={'status':'RESEARCH amendment; no new CAD; prior option B invalid for installed head interfaces','baseline':'5584306a595f87b60b29eca9ea82b527ade5ae98','source':{'url':'https://www.ebay.com/itm/146111774717','image_url':'https://i.ebayimg.com/images/g/bBwAAOSw8FVnEovT/s-l1200.jpg','sha256':'70616ce77f9adbee7ff6415545bdace98b786ba405e20524a8b9b9ce7d87ae45','identity':'Seller ATK DFF8; ATK catalog1987–96 VIN Y family comparison; not owner engine','seam_identification':'Visible horizontal joint between separate head-front face and machined block-front face, above fifth opening and top pump screw. Both mating surfaces and interface depth are not measured.','coplanarity_limit':'Seam projection treated as block front X373 for this diagnostic; head frontage/recess depth unknown. Outlet extrema are qualitative held-out features, not a thermostat flange calibration.'},'primary_deck_source':{'url':'https://www.trackey.ford.com/download/pdfs/EngineDimensions.pdf','download_sha256':'0e81983110834897b86bbb06023f5f1df4381ab9e9174c35a18a425f4430049c','page':1,'row':'300 I-6, 1965–96','column':'DECK HEIGHT','inches':10.0,'mm':254.,'class':'manufacturer nominal reference dimension; no production tolerance or this-casting measurement','visual_review':'PDF page raster reviewed; deck-height column verified; raw PDF excluded'},'observations':{'deck_seam_pixels':seam.tolist(),'pan_pixels':pan.tolist(),'outlet_extrema_pixels':port.tolist(),'manual_selection_uncertainty_px':3,'optionB_deck_yz_mm':s.tolist(),'optionB_pan_yz_mm':p.tolist(),'optionB_outlet_extrema_yz_mm':q.tolist()},'fit_audit':{'original_training_rms_px':j['fit']['radius_rms_px'],'original_heldout_fifth_error_px':j['fit']['heldout_fifth_error_px'],'original_leave_one_cover_out_errors_px':j['fit']['leave_one_cover_out_errors_px'],'normalized_homography_condition_number':float(np.linalg.cond(H)),'local_inverse_Jacobians':local,'new_observations_used_to_refit_homography':False},'conditional_pan_deck_scale_hypothesis':{'method':'Uniform similarity of coupled source footprints constrained to primary deck254 and inherited pan−24.5; no overlap term. NOT approved geometry.','scale_relative_optionB':float(scale),'z_translation_mm':float(shift),'pump_axes_yz_mm':(pa*scale+[0,shift]).tolist(),'cover_axes_yz_mm':(ca*scale+[0,shift]).tolist(),'mapped_optionB_crank_origin_yz_mm':[0,float(shift)],'why_not_installable':'Changes cover scale, source seal-origin registration and all coupled mounts; preserving the real crank/seal/gear interfaces requires independent source calibration. No automatic gear/hardware scaling.','fixed_camera_selection_sensitivity_p2_5_p50_p97_5':np.percentile(vals,[2.5,50,97.5],axis=0).tolist(),'sensitivity_columns':['optionB_mean_deckZ','scale','Ztranslation'],'uncertainty_limit':'Pixel-selection only under frozen homography; excludes camera, pattern, depth, scale and pan-datum uncertainty.'},'negative_controls':{'seam_shift20px_Z_displacement_mm':float(rect(seam+[0,20])[:,1].mean()-s[:,1].mean()),'forbidden_controls':'Forward crank/cam hubs remain excluded from coplanar fit.'},'inputs':{str(z.relative_to(R)):sha(z) for z in [f,measure,Path(__file__)]}}
# Independent trace feasibility screen; never changes gear or source curves.
sourcefile=R/'cad/engine/timing_cover_joint_candidate.py'
outline=next(ast.literal_eval(n.value) for n in ast.parse(sourcefile.read_text()).body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='OUTLINE_NORMALIZED')
a0=np.radians(-.039823552987937626);r0=np.array([[np.cos(a0),np.sin(a0)],[-np.sin(a0),np.cos(a0)]])
trace=((np.array(outline)*1600-[588.5373742452892,930.4751087566926])*[1,-1])*.26223302269259874@r0
angles=np.arange(360)*np.pi/180;ring=np.array([95.1098209901611,76.08785679212887])+86.947*np.c_[np.cos(angles),np.sin(angles)]
def margin(poly):
 a=poly;b=np.roll(poly,-1,axis=0);v=b-a;w=ring[:,None,:]-a;u=np.clip(np.sum(w*v,axis=2)/np.sum(v*v,axis=1),0,1)
 return float(np.min(np.min(np.linalg.norm(w-u[:,:,None]*v,axis=2),axis=1)*np.where(Polygon(poly).contains_points(ring),1,-1)))
report['conditional_pan_deck_scale_hypothesis']['sampled_cam_outer_arch_margin_mm']=margin(trace[:45]*scale+[0,shift])
report['conditional_pan_deck_scale_hypothesis']['sampled_cam_limit']='Same360point R86.947 ring and outer45point trace as prior option study; fails feasibility, not an actual CAD collision test. Never scale gears to force fit.'
report['inputs'][str(sourcefile.relative_to(R))]=sha(sourcefile)
# Separate raster: authored trace data and actual STEP display triangles only.
data=R/f'reference/engine/{P}-display-data.npz';d=np.load(data);report['inputs'][str(data.relative_to(R))]=sha(data)
fig,axes=plt.subplots(1,3,figsize=(16,7))
a=axes[0];a.scatter(*np.array(lm['pump_order_bottom_right_left_top_pixels']).T,label='pump anchors');a.scatter(*np.array(lm['cover_order_source_gasket_1_to_7_pixels']).T,label='cover anchors');a.plot(*seam.T,'r-o',label='held-out head/block seam');a.plot(*pan.T,'k-o',label='pan trace');a.plot(*port.T,'g+',label='outlet aperture extrema');a.set(xlim=(250,1100),ylim=(1050,200),title='Authored source landmarks / pixels');a.legend(fontsize=8);a.set_aspect('equal')
a=axes[1];a.plot(*(trace[:45]*scale+[0,shift]).T,':',color='gray',label='conditional cover arch');a.plot(*ring.T,color='purple',lw=.8,label='fixed cam+wall ring');a.scatter(*pa.T,label='option B pump');a.scatter(*ca.T,label='option B cover');a.plot(*s.T,'r-o',label='source seam under B');a.plot(*p.T,'k-',label='source pan under B');a.axhline(254,color='red',ls='--',label='Ford nominal deck254');a.scatter(*(pa*scale+[0,shift]).T,marker='x',label='conditional deck/pan fit');a.set(title='Conflicting registration hypotheses / mm',xlabel='Y',ylabel='Z',ylim=(-60,350));a.set_aspect('equal');a.legend(fontsize=8)
a=axes[2]
for n,color in [('cylinder-head','#cccccc'),('coolant-outlet-housing','#c38b8b'),('water-pump-housing','#80a7b1'),('water-pump-gasket','#beaa76')]:
 vs=d[n+'__vertices'];fs=d[n+'__faces'];tri=vs[fs][:,:,[1,2]];a.add_collection(PolyCollection(tri,facecolors=color,edgecolors='none',alpha=.65))
a.axhline(254,color='red',ls='--');a.scatter(*pa.T,c='black',s=20);a.set(xlim=(-110,70),ylim=(185,325),xlabel='Y',ylabel='Z',title='Actual STEP surfaces: upper joint conflict');a.set_aspect('equal')
fig.suptitle('Pump / cover option B: deck conflict is a source-registration failure\nFord nominal deck254mm retained; conditional smaller footprint is research only',fontsize=14);fig.tight_layout();out=R/f'reference/engine/{P}-deck-registration.png';fig.savefig(out,dpi=150);plt.close(fig)
report['visual']={'path':str(out.relative_to(R)),'sha256':sha(out),'source_pixels_redistributed':False}
(R/f'reference/engine/{P}-deck-registration.json').write_text(json.dumps(report,indent=2)+'\n')
# Optional local review overlay; never required by the authored-data reproduction.
source=R/'reference/engine/atk-dff8-block-front.jpg'
if source.exists():
 assert sha(source)==report['source']['sha256']
 fig,a=plt.subplots(figsize=(9,9));a.imshow(plt.imread(source));a.plot(*seam.T,'r-o',label='held-out seam');a.plot(*pan.T,'c-o',label='pan');a.plot(*port.T,'g+',ms=10,label='unverified aperture');a.legend();a.axis('off');a.set_title('Source identification overlay / restricted review only')
 out=R/'cad/engine/generated/pump-cover-candidate-20261003/deck-source-overlay.png';fig.savefig(out,dpi=140);plt.close(fig)
print(json.dumps({'optionB_seam_meanZ':float(s[:,1].mean()),'conditional_scale':float(scale),'conditional_Zshift':float(shift),'report':f'reference/engine/{P}-deck-registration.json'}))
