"""Separate guarded asset/pose proposal; no canonical writes."""
from pathlib import Path
import sys,json,hashlib,copy
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b,trimesh
from assembly_math import transforms
import timing_pan21_lateral_candidate as c
from oil_pan_joint_v9_candidate import STATIONS
O=R/'cad/engine/generated/timing-front-coordinated-stage';O.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def bounds(s):return np.array([tuple(s.bounding_box().min),tuple(s.bounding_box().max)])
def matrix(loc):
 t=loc.wrapped.Transformation();return np.array([[t.Value(i,j)for j in range(1,5)]for i in range(1,4)])
manifest=R/'inventory/engine/full-assembly.json';m=json.loads(manifest.read_text());poses=transforms(m);occ={x['id']:x for x in m['occurrences']};defs={x['id']:x for x in m['definitions']};watched={manifest:sha(manifest),Path(__file__):sha(Path(__file__))}
for n in ['timing-seven-block-delivery-validation','timing-pan21-lateral-delivery-validation','timing-front-stage-contact-delta']:
 p=R/'inventory/engine'/f'{n}.json';watched[p]=sha(p)
limits=['Estimated coordinatedfront candidate, not factoryspecification/strength/installation.','OriginalpumpR85/pan20R12guardFAIL retained; root permits only signed/bound exterior deltas, narrowerfunctionalinterfaces intact.','Rear/uppercontactstudies analysis-only: fullfaceoverhang/rearowner/pressure limitations retained.','Requiresmain-gasket/terminalsealant and2692seal stage; browser/canonicalintegrationnotperformed.']
changes=[];rows=[];staged={};sources={};base=R/'cad/engine/generated/timing-pan21-lateral-candidate'
specs=[('block',c.COVER.with_name('block.step'),poses['block']),('timing-cover',base/'cover.step',poses['timing-cover']),('oil-pan',base/'pan.step',poses['oil-pan']),('oil-pan-molded-gasket',base/'pan-gasket.step',poses['oil-pan-molded-gasket']),('oil-pan-mounting-screw',c.MALE,b.Location()),('timing-cover-mounting-screw',c.COVER.with_name('main-cover-screw-1.step'),c.main.frame(*c.main.AXES[0]))]
for ident,p,frame in specs:
 watched[p]=sha(p);source=b.import_step(p);local=frame.inverse()*source;sp=O/(ident+'.step');b.export_step(local,sp);back=b.import_step(sp);assert back.is_valid and len(back.solids())==1 and len(back.faces())==len(source.faces());err=float(np.max(abs(bounds(frame*back)-bounds(source))));assert err<.01
 v,f=source.tessellate(.08,.12);v=np.array([tuple(x)for x in v]);mat=matrix(frame);vl=(v-mat[:,3])@mat[:,:3];mesh=trimesh.Trimesh(vl,np.array(f));mesh.merge_vertices(digits_vertex=6);assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
 gp=O/(ident+'.glb');trimesh.Trimesh(mesh.vertices[:,[0,2,1]]*[1,1,-1]/1000,mesh.faces).export(gp);gl=trimesh.load(gp,force='mesh');lv=gl.vertices[:,[0,2,1]]*[1,-1,1]*1000;wv=lv@mat[:,:3].T+mat[:,3];meshbounds=float(np.max(abs(np.array([wv.min(0),wv.max(0)])-bounds(source))));assert meshbounds<.025
 row={'id':ident,'source_step':str(p.relative_to(R)),'source_sha256':sha(p),'local_to_source_transform':mat.tolist(),'step_bounds_error_mm':err,'mesh_world_bounds_error_mm':meshbounds,'volume_serialization_error_mm3':abs(back.volume-source.volume),'valid':back.is_valid,'watertight':gl.is_watertight,'solids':len(back.solids()),'faces':len(back.faces()),'triangles':len(gl.faces),'step':str(sp.relative_to(R)),'step_sha256':sha(sp),'glb':str(gp.relative_to(R)),'glb_sha256':sha(gp)};rows.append(row);staged[ident]=back;sources[ident]=source
 before=defs.get(ident);after=copy.deepcopy(before)if before else {'id':ident,'name':'Timing-cover screw ·1986comparison','function':'Clamps the estimated recessed cover seat to a modeled blind female socket; exact1994 hardware remains unverified.','system':'closures','color':'#a3adb3','glb':'/models/engine/'+ident+'.glb','step':'/cad/engine/generated/'+ident+'.step','geometry_status':'candidate','sources':[],'dimension_claims':[],'unresolved':['Ford1986callout51comparison5/16-18×7/8in;1994transfer andheadgeometry unverified.']}
 after.update(volume_mm3=back.volume,solid_count=1,triangle_count=len(gl.faces),model_bounds_mm=(bounds(back)[1]-bounds(back)[0]).tolist());after['unresolved']=after.get('unresolved',[])+limits
 changes.append({'id':ident,'before':before,'after':after,'copy_assets':{'step':{'from':row['step'],'to':after['step'].lstrip('/'),'sha256':row['step_sha256']},'glb':{'from':row['glb'],'to':after['glb'].lstrip('/'),'sha256':row['glb_sha256']}}});print('staged',ident,flush=True)
# Tenexistingpanposes; sevennewmainoccurrences, withexplicitparentframes.
new=copy.deepcopy(m);proposals=[];rel=dict(c.owner.RELOCATIONS);rel[21]=c.NEW
for q in new['occurrences']:
 for n,world in rel.items():
  if q['id'] in [f'oil-pan-mounting-{kind}-{n}'for kind in ['screw','washer']]:
   before=occ[q['id']];oldlocal=b.Pos(*before['position_cad_mm'])*b.Rot(*before['rotation_cad_deg']);parent=poses[q['id']]*oldlocal.inverse();target=parent.inverse()*b.Pos(*world);mt=matrix(target);assert np.max(abs(mt[:,:3]-np.eye(3)))<1e-10;q['position_cad_mm']=mt[:,3].tolist();q['rotation_cad_deg']=[0,0,0];proposals.append({'id':q['id'],'before':before,'after':copy.deepcopy(q),'world_target_mm':list(world)})
cover_occ=occ['timing-cover'];parent=poses['timing-cover']*(b.Pos(*cover_occ['position_cad_mm'])*b.Rot(*cover_occ['rotation_cad_deg'])).inverse()
for n,axis in enumerate(c.main.AXES,1):
 world=c.main.frame(*axis);target=parent.inverse()*world;position,rotation=target.to_tuple();q={'id':f'timing-cover-mounting-screw-{n}','definition':'timing-cover-mounting-screw','parent':'closures','name':f'Timing-cover screw{n} ·comparison','function':'Clamps estimatedrecessedseat; productionhardware unknown.','position_cad_mm':list(position),'rotation_cad_deg':list(rotation),'explode_cad_mm':[280,0,0]};assert q['id']not in occ;new['occurrences'].append(q);proposals.append({'id':q['id'],'before':None,'after':q,'world_target_transform':matrix(world).tolist()})
newposes=transforms(new);poserows=[]
for n,orig in enumerate(STATIONS,1):
 target=rel.get(n,orig)
 for kind in ['screw','washer']:
  oid=f'oil-pan-mounting-{kind}-{n}';mt=matrix(newposes[oid]);assert np.max(abs(mt[:,3]-target))<1e-8;assert np.max(abs(mt[:,:3]-np.eye(3)))<1e-8
  poserows.append({'id':oid,'world_xyz_mm':mt[:,3].tolist(),'unchanged':next(q for q in new['occurrences']if q['id']==oid)==occ[oid]})
for n,axis in enumerate(c.main.AXES,1):
 oid=f'timing-cover-mounting-screw-{n}';p=c.COVER.with_name(f'main-cover-screw-{n}.step');watched[p]=sha(p);expected=b.import_step(p);placed=newposes[oid]*staged['timing-cover-mounting-screw'];assert np.max(abs(bounds(placed)-bounds(expected)))<.01
 poserows.append({'id':oid,'world_transform':matrix(newposes[oid]).tolist(),'actual_source_bounds_error_mm':float(np.max(abs(bounds(placed)-bounds(expected))))})
# Signedexactdeltaassets arepartofthisscopeapproval,notgeometryrepairs.
old=b.import_step(c.main.BLOCK);q=b.import_step(c.COVER.with_name('block.step'));watched[c.main.BLOCK]=sha(c.main.BLOCK);signed=[]
for name,shape,sign in [('block-added',q.cut(old),1),('block-removed',old.cut(q),-1)]:
 p=O/(name+'.step');b.export_step(c.norm(shape),p);signed.append({'sign':sign,'path':str(p.relative_to(R)),'sha256':sha(p),'bounds_mm':bounds(c.norm(shape)).tolist()})
broad=[]
for p in sorted((R/'cad/engine/generated/timing-seven-block-guard-study').glob('*.step')):broad.append({'path':str(p.relative_to(R)),'sha256':sha(p),'sign':1 if p.stem.endswith('added')else-1});watched[p]=sha(p)
scope={'authorization':'Root expressly permits only recorded exterior deltas in originalpumpR85/pan20R12 guards for integrationcandidate; originalguardFAIL permanent.','parent_block_sha256':sha(c.main.BLOCK),'new_block_sha256':sha(c.COVER.with_name('block.step')),'whole_signed_deltas':signed,'broad_guard_signed_witnesses':broad,'seven_supports':[{'station':n,'x_mm':[c.main.SUPPORT_BACK,373],'radius_mm':8,'axis_yz_mm':list(axis)}for n,axis in enumerate(c.main.AXES,1)],'functional_guard_report':'inventory/engine/timing-seven-block-functional-guards.json'}
patch={'schema':'truck-guarded-integration-proposal-v2','scope':'Uninstalled coordinatedfront assets andhardwareposes; requiredseal/gasketdependenciesexplicit','manifest_sha256':sha(manifest),'definitions':changes,'occurrences':proposals,'scope_approval':scope,'dependencies':['Main cover gasket andterminalsealant fromfrozenattachment-v2 requireseparatedefinitions/occurrences; notfusedintoassets.','Frontseal2692stage supplieshub/case/elastomer/garterspringandoldfront-sealalias.','Correctedcrank/cam/core integration remainsroot-owned.'],'requirements':['Rejectstale manifest/beforeobjects/assets.','Applyfivepanpairposes andsevenmainhardwareoccurrences togetherwithfrontassets.','Do notpromote thispartialdependencyproposal alone.','PreserveallunpatchedIDs/parents/metadata.'],'limits':limits};pp=R/'inventory/engine/timing-front-coordinated-patch.json';pp.write_text(json.dumps(patch,indent=2)+'\n')
r={'status':'PASS assetandpose stage; dependencycomposition/browserpending','parts':rows,'poses':poserows,'scope_approval':scope,'inputs':{str(p.relative_to(R)):h for p,h in watched.items()},'patch':str(pp.relative_to(R)),'patch_sha256':sha(pp),'canonical_modified':False,'contact_studies':'Bothanalysis-only; noadditionalpanrepairasset. Changedcontact/routeproof separatelybound.'};(R/'inventory/engine/timing-front-coordinated-stage-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],flush=True)
