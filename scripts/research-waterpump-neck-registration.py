"""Photo landmark correspondence; no metric dimensions inferred from photographs."""
from pathlib import Path
import numpy as np,json,hashlib,itertools,math
R=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
# All point coordinates manually reviewed on unmodified sourcepixels; ±4px mounting,
# ±8px neck-center. Ximage right,Yimage down; convert to image-right/up beforefit.
world=np.array([[7.7,-66.5],[66.3,6.3],[-66.2,5.3],[17,64.9],[-10.9,69.]])
back=np.array([[421,539],[257,584],[362,369],[200,450],[219,408]],float);front=np.array([[268,587],[461,600],[298,378],[499,447]],float)
back_neck=np.array([[552,432],[622,411]],float);front_neck=np.array([[31,476],[109,480]],float)
def fit(pixel,target,parity):
 p=pixel*[1,-1];pc=p.mean(0);tc=target.mean(0);a=p-pc;z=target-tc;u,_,vt=np.linalg.svd(a.T@z);rot=u@vt
 if np.linalg.det(rot)*parity<0:u[:,-1]*=-1;rot=u@vt
 scale=np.sum((a@rot)*z)/np.sum(a*a);pred=(p-pc)@rot*scale+tc;res=np.linalg.norm(pred-target,axis=1)
 def transform(q):return(q*[1,-1]-pc)@rot*scale+tc
 return {'parity':parity,'scale_model_mm_per_pixel_NOT_MEASUREMENT':float(scale),'rotation_matrix_row_convention':rot.tolist(),'rms_model_mm':float(np.sqrt(np.mean(res**2))),'residuals_model_mm':res.tolist(),'predicted_model_yz':pred.tolist()},transform
rows={}
for name,pixel,target,neck in [('rear',back,world,back_neck),('front',front,world[:4],front_neck)]:
 rows[name]={}
 for parity in [-1,1]:
  r,t=fit(pixel,target,parity);nn=t(neck);direction=nn[1]-nn[0]
  # Rear photo uses root→tip; front points run tip→root.
  if name=='front':direction=-direction
  heater=t(np.array([[267,357] if name=='rear' else [440,364]],float))[0];r['heater_root_model_yz_estimate']=heater.tolist();r['heater_root_radial_angle_deg']=float(math.degrees(math.atan2(heater[1],heater[0])));r['neck_model_yz_estimate']=nn.tolist();r['neck_outward_direction_deg']=float(math.degrees(math.atan2(direction[1],direction[0])));unit=direction/np.linalg.norm(direction);normal=np.array([-unit[1],unit[0]]);r['neck_line_signed_offset_model_mm_NOT_MEASUREMENT']=float(np.dot(nn.mean(0),normal));r['neck_center_radial_angle_deg']=float(math.degrees(math.atan2(*nn.mean(0)[::-1])));rows[name][str(parity)]=r
# Preserve fifth-apertureidentity; deliberately scrambleonlyfour smallerholeindices.
perms=[]
for perm in itertools.permutations(range(4)):
 target=np.vstack([world[list(perm)],world[4]])
 r,_=fit(back,target,-1);perms.append({'permutation':list(perm),'rms_model_mm':r['rms_model_mm']})
perms.sort(key=lambda r:r['rms_model_mm'])
wrong_fifth=[]
for perm in itertools.permutations(range(5)):
 if perm[4]==4:continue
 rr,_=fit(back,world[list(perm)],-1);wrong_fifth.append({'permutation':list(perm),'rms_model_mm':rr['rms_model_mm']})
wrong_fifth.sort(key=lambda r:r['rms_model_mm'])
front_alternatives=[]
for perm in itertools.permutations(range(4)):
 rr,_=fit(front,world[list(perm)],1);front_alternatives.append({'permutation':list(perm),'rms_model_mm':rr['rms_model_mm']})
front_alternatives.sort(key=lambda r:r['rms_model_mm'])

# Repeated bounded landmark perturbations quantify pixel sensitivity, not systematicparallax.
rng=np.random.default_rng(44009);angles=[]
for _ in range(1000):
 r,t=fit(back+rng.uniform(-4,4,back.shape),world,-1);n=t(back_neck+rng.uniform(-8,8,back_neck.shape));d=n[1]-n[0];angles.append(math.degrees(math.atan2(d[1],d[0])))
paths=[R/'reference/engine'/n for n in ['gates44009-1.jpg','gates44009-2.jpg','gates44009-3.jpg','felpro-13816.jpg','water-pump-mounting-topology-reviewed.json','water-pump-inlet-v3-topology-reviewed.json']]
j={'scope':'Source landmark registration audit only; modelscale used asreference, not physicalmeasurement','landmarks':{'order':['mount1bottom','mount2right','mount3left','mount4top','larger-fifth-aperture'],'model_relative_yz_mm':world.tolist(),'rear_pixels_xy':back.tolist(),'front_pixels_xy':front.tolist(),'rear_neck_root_tip_pixels':back_neck.tolist(),'front_neck_tip_root_pixels':front_neck.tolist(),'uncertainty_pixels':{'mounts':4,'neck':8}},'fits':rows,'rear_wrong_index_controls':perms,'wrong_fifth_identity_controls':wrong_fifth,'front_index_controls':front_alternatives,'rear_pixel_sensitivity_angle_deg':{'min':min(angles),'max':max(angles),'samples':len(angles),'seed':44009},'limits':['Similarityfit does not correctperspective, lensdistortion oraxialparallax; angleisestimated.','Metriccoordinates inheritprovisionalgasketpattern; no productiondimension inferred.','Frontfourholes usephysicalcorrespondence fromrear/branch/heaterposition; nearfourfoldpatternalone isambiguous.','Forwardneckmustberebuilt withfunctionalpassage andallactualneighbors afterrootcontract; noCADedited.'],'inputs':{str(p.relative_to(R)):sha(p)for p in [Path(__file__),*paths]}};(R/'inventory/engine/waterpump-neck-registration-research.json').write_text(json.dumps(j,indent=2)+'\n');print(json.dumps({'fits':rows,'best_permutations':perms[:4],'sensitivity':j['rear_pixel_sensitivity_angle_deg']},indent=2))
