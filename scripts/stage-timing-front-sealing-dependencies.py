"""Stage existing physical seals and source-qualified screw lessons; no canonical writes."""
from pathlib import Path
import sys,json,hashlib,copy
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b,trimesh
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from assembly_math import transforms
O=R/'cad/engine/generated/timing-front-sealing-stage';O.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def bounds(s):return np.array([tuple(s.bounding_box().min),tuple(s.bounding_box().max)])
def contact(a,c):
 op=BRepAlgoAPI_Common(b.Compound(list(a.faces())).wrapped,b.Compound(list(c.faces())).wrapped);op.Build();assert op.IsDone();return sum(f.area for f in b.Compound(op.Shape()).faces())
def dump(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
manifest=R/'inventory/engine/full-assembly.json';front=R/'inventory/engine/timing-front-coordinated-patch.json';m=json.loads(manifest.read_text());fp=json.loads(front.read_text());pose=transforms(m);co=next(q for q in m['occurrences']if q['id']=='timing-cover');parent=pose['timing-cover']*(b.Pos(*co['position_cad_mm'])*b.Rot(*co['rotation_cad_deg'])).inverse();frame=pose['timing-cover'];localpose=parent.inverse()*frame
F=R/'cad/engine/generated/timing-cover-attachment-v2';paths={'main':F/'main-gasket.step','terminal':F/'front-terminal-sealant.step','block':R/'cad/engine/generated/timing-cover-seven-fastener-candidate/block.step','cover':R/'cad/engine/generated/timing-pan21-lateral-candidate/cover.step','pan':R/'cad/engine/generated/timing-pan21-lateral-candidate/pan.step','pan-gasket':R/'cad/engine/generated/timing-pan21-lateral-candidate/pan-gasket.step'}
parts={k:b.import_step(p)for k,p in paths.items()};solids=sorted(parts['terminal'].solids(),key=lambda x:x.center().Y);assert len(solids)==2
specs=[('timing-cover-main-gasket',parts['main'],'Main timing-cover gasket'),*[(f'timing-cover-terminal-sealant-{n}',s,f'Timing-cover terminal sealant {n}')for n,s in enumerate(solids,1)]]
changes=[];occ=[];rows=[];meshes={};checks={}
for ident,s,name in specs:
 assert ident not in {q['id']for q in m['definitions']+m['occurrences']}
 local=frame.inverse()*s;sp=O/(ident+'.step');b.export_step(local,sp);back=b.import_step(sp);assert back.is_valid and len(back.solids())==1
 err=float(np.max(abs(bounds(frame*back)-bounds(s))));assert err<.025
 v,f=local.tessellate(.025,.08);v=np.array([tuple(x)for x in v]);mesh=trimesh.Trimesh(v,np.array(f));mesh.merge_vertices(digits_vertex=6);assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
 gp=O/(ident+'.glb');trimesh.Trimesh(mesh.vertices[:,[0,2,1]]*[1,1,-1]/1000,mesh.faces).export(gp);gl=trimesh.load(gp,force='mesh');gv=gl.vertices[:,[0,2,1]]*[1,-1,1]*1000;gb=np.array([gv.min(0),gv.max(0)]);ge=float(np.max(abs(gb-bounds(local))));assert ge<.025
 after={'id':ident,'name':name,'function':'Closes a static boundary at the front cover joint.','system':'closures','color':'#586b5e','glb':'/models/engine/'+ident+'.glb','step':'/cad/engine/generated/'+ident+'.step','geometry_status':'candidate','sources':['timing-front-joint-review'],'dimension_claims':[],'unresolved':['Inherited estimated registration and section; no pressure or factory material specification.'],'volume_mm3':back.volume,'solid_count':1,'triangle_count':len(gl.faces),'model_bounds_mm':(bounds(local)[1]-bounds(local)[0]).tolist()}
 changes.append({'id':ident,'before':None,'after':after,'copy_assets':{k:{'from':str(p.relative_to(R)),'to':after[k].lstrip('/'),'sha256':sha(p)}for k,p in [('step',sp),('glb',gp)]}})
 pos,rot=localpose.to_tuple();q={'id':ident,'definition':ident,'parent':'closures','name':name,'function':after['function'],'position_cad_mm':list(pos),'rotation_cad_deg':list(rot),'explode_cad_mm':[180,0,0]};occ.append({'id':ident,'before':None,'after':q})
 rows.append({'id':ident,'world_bounds_mm':bounds(s).tolist(),'step_bounds_error_mm':err,'mesh_bounds_error_mm':ge,'watertight':gl.is_watertight,'valid':back.is_valid,'solids':1})
 meshes[ident+'_vertices']=mesh.vertices+np.array([403,0,0]);meshes[ident+'_faces']=mesh.faces
 contacts={k:contact(s,parts[k])for k in ['block','cover','pan','pan-gasket']};overlaps={k:abs(q.volume) if (q:=s.intersect(parts[k])) is not None else 0.0 for k in ['block','cover','pan','pan-gasket']}
 if ident.endswith('main-gasket'):
  assert contacts['block']>0 and contacts['cover']>0
  shifted=contact(b.Pos(.2,0,0)*s,parts['block']);assert shifted<1e-5
 else:
  contacts['main-gasket']=contact(s,parts['main']);assert all(contacts[k]>0 for k in ['block','cover','pan-gasket','main-gasket'])
 assert max(overlaps.values())<.1
 checks[ident]={'contact_area_mm2':contacts,'overlap_mm3':overlaps};print(ident,checks[ident],flush=True)
hardware={}
for n in range(1,8):
 p=paths['block'].with_name(f'main-cover-screw-{n}.step');paths[f'main-screw-{n}']=p;male=b.import_step(p)
 hardware[str(n)]={ident:abs(q.volume)if(q:=male.intersect(s))is not None else 0.0 for ident,s,name in specs}
 assert max(hardware[str(n)].values())<.1
placed=copy.deepcopy(m)
placed['occurrences'] += [q['after']for q in occ]
posed=transforms(placed)
pose_errors={ident:float(np.max(abs(bounds(posed[ident]*b.import_step(O/(ident+'.step')))-bounds(s))))for ident,s,name in specs}
assert max(pose_errors.values())<.025
np.savez_compressed(O/'review-data.npz',**meshes)
ledger=R/'reference/engine/ford-1986-main-cover-fastener-comparison.json';review=R/'reference/engine/timing-cover-joint-review.json';sources={'timing-main-screw-1986-comparison':{'title':'Ford1986 4.9L cover screw comparison — authored source review','path':str(ledger.relative_to(R)),'sha256':sha(ledger),'url':json.loads(ledger.read_text())['source_url'],'capture_kind':'Authored review ledger, not original PDF','original_pdf_sha256':json.loads(ledger.read_text())['pdf_sha256'],'pdf_pages':[62,63],'printed_pages':['21-11-9','21-11-10']},'timing-front-joint-review':{'title':'Timing cover joint source review and estimation limits','path':str(review.relative_to(R)),'sha256':sha(review),'capture_kind':'Authored review ledger'}}
lessons={}
for n in range(1,8):
 ident=f'timing-cover-mounting-screw-{n}';lessons[ident]={'summary':f'Cover screw {n} clamps a recessed cover seat toward the block across the main gasket.','limits':'The 1986 Ford 4.9L manual identifies a 5/16-18 × 7/8 inch washer-head cover bolt. Applying that comparison to all seven modeled positions is unverified for this 1994 truck. Head dimensions, seat depth, blind socket and support stock are estimates; no torque or production thread class is specified.','steps':[{'title':'Follow the clamp path','text':'The head bears on the cover. The shank passes through clearance openings and the modeled male thread meets the blind block socket. The gasket lies between the mating faces.','part':'timing-cover'},{'title':'Separate source size from placement','text':'The comparison length is 22.225 mm and the nominal thread is 5/16-18. The historical illustration does not establish the seven-hole quantity, every station assignment or the recessed seat depths on this truck.','part':ident,'source':'timing-main-screw-1986-comparison'},{'title':'Inspect the static seal','text':'The main gasket and the separate terminal sealant deposits have different physical roles. Geometric face contact shows their modeled arrangement; it does not calculate sealing pressure.','part':'timing-cover-main-gasket'}],'troubleshooting':[{'title':'Inspect the complete joint','text':'A loose or damaged attachment can reduce clamping. Oil near the cover can also come from another joint; visible oil alone does not identify a failed screw or justify a torque value.','part':'timing-cover'}],'sources':['timing-main-screw-1986-comparison','timing-front-joint-review']}
for ident,s,name in specs:
 lessons[ident]={'summary':('The main gasket lies between the block and cover mating faces.' if ident.endswith('main-gasket') else 'This separate sealant deposit bridges one lower end of the main cover gasket to the molded pan gasket.'),'limits':'The contact geometry is an estimated reconstruction. Material, applied bead size, compression and sealing pressure are not production specifications. Existing rear pan contact limitations remain open.','steps':[{'title':'Find the mating surfaces','text':'Shared faces show where this stationary sealing part meets its neighbors. A clear gap or overlap would indicate an assembly problem, while contact alone does not prove leak resistance.','part':'timing-cover'},{'title':'Keep the joint parts distinct','text':'The molded pan gasket remains a separate part below this joint. The crankshaft lip seal has a different job at the rotating shaft.','part':'oil-pan-molded-gasket'}],'troubleshooting':[{'title':'Locate the leak path','text':'Oil near the front joint is a clue rather than a diagnosis. Inspect the adjoining boundaries and follow applicable service guidance before choosing a repair.','part':'timing-cover'}],'sources':['timing-front-joint-review']}
lp=R/'inventory/engine/timing-front-sealing-learning.json';sr=R/'inventory/engine/timing-front-sealing-sources.json';dump(lp,lessons);dump(sr,sources)
known={q['id']for q in m['occurrences']}|{q['id']for q in fp['occurrences']}|{q['id']for q in occ}
assert all(step['part']in known for l in lessons.values()for step in l['steps']+l['troubleshooting'])
assert all(sha(R/s['path'])==s['sha256']for s in sources.values())
patch={'schema':'truck-guarded-integration-proposal-v2','scope':'Existing main gasket and two separate terminal deposits; seven screw lessons','manifest_sha256':sha(manifest),'front_patch_sha256':sha(front),'definitions':changes,'occurrences':occ,'learning':{'path':str(lp.relative_to(R)),'sha256':sha(lp)},'sources':{'path':str(sr.relative_to(R)),'sha256':sha(sr)},'main_screw_source_enrichment':{'id':'timing-cover-mounting-screw','before':next(q['after']for q in fp['definitions']if q['id']=='timing-cover-mounting-screw'),'append_sources':['timing-main-screw-1986-comparison']},'requirements':['Compose only with bound coordinated front proposal.','Reject duplicate IDs, stale assets, stale before objects and stale source hashes.','No geometry repair; preserve existing pan gasket and2692 physical definitions.'],'limits':['Candidate geometry only; inherited rear/upper contact gaps unchanged.','No factory material, torque, strength, pressure or installation claim.','Browser integration NOT RUN.']}
pp=R/'inventory/engine/timing-front-sealing-patch.json';dump(pp,patch)
r={'status':'PASS scoped exports and actual contact; integration pending','parts':rows,'contacts':checks,'negative_control_shifted_main_gasket_block_area_mm2':shifted,'serialized_world_bounds_errors_mm':pose_errors,'main_screw_overlap_mm3':hardware,'learning_occurrences':list(lessons),'canonical_modified':False,'inputs':{str(p.relative_to(R)):sha(p)for p in [manifest,front,Path(__file__),*paths.values(),ledger,review]},'patch_sha256':sha(pp),'limits':patch['limits']};dump(R/'inventory/engine/timing-front-sealing-validation.json',r)
