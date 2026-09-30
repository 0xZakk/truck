#!/usr/bin/env python3
"""Guarded isolated rear stage; explicit export rebind and transactional install."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,sys,tempfile,itertools,struct,inspect
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import numpy as np
import trimesh
import rear_exhaust_neck_integration as adapter
from assembly_math import transforms
from cad_metrics import solid_volume,support_bounds
STAGE=ROOT/'cad/engine/generated/rear-exhaust-neck-integration-stage'
PROOF=adapter.PROOF;ID=adapter.ID
sha=adapter.sha
read=lambda p:json.loads(Path(p).read_text())
def dump(p,v):Path(p).write_text(json.dumps(v,indent=2)+'\n')
def watch():
 files=[Path(__file__),Path(adapter.__file__),PROOF,ROOT/'reference/engine/rear-exhaust-port-topology.json',ROOT/'inventory/engine/rear-exhaust-neck-learning.json',ROOT/'scripts/check-rear-exhaust-neck-installed.py',ROOT/'cad/engine/full_engine.py',ROOT/'scripts/check-rear-exhaust-neck-promotion-controls.py',ROOT/'viewer/engine-learning-modules.js',ROOT/'cad/engine/assembly_math.py',ROOT/'cad/engine/cad_metrics.py',ROOT/'scripts/install-intake-cap-coordination.py']
 return {str(p.relative_to(ROOT)):sha(p) for p in files}
def evidence():
 r=read(PROOF);assert r['status']=='PASS isolated candidate; root review pending'
 # Original source/CAD proof remains frozen. Canonical target bytes may
 # legitimately change on apply; all other historical inputs remain bound.
 for p,h in r['input_sha256'].items():
  if p!='cad/engine/generated/exhaust-rear.step':assert sha(ROOT/p)==h,p
 for ext,h in r['exports'].items():assert sha(adapter.OUT/('candidate.'+ext))==h
 for p in ['front','back','three-quarter']:
  source=ROOT/('reference/engine/dorman-674186-'+p+'.jpg')
  assert sha(source)==r['input_sha256'][str(source.relative_to(ROOT))]
 adapter.fixtures();return r

def canonical_artifacts(manifest):
 d=next(d for d in manifest['definitions'] if d['id']==ID)
 return {d[k].lstrip('/'):sha(ROOT/d[k].lstrip('/')) for k in ('step','glb')}

def check_artifacts(expected,root=ROOT):
 for p,h in expected.items():assert sha(root/p)==h,'Canonical rear artifact changed: '+p

def metadata_preserved(before,after):
 old=next(d for d in before['definitions'] if d['id']==ID);new=next(d for d in after['definitions'] if d['id']==ID)
 assert set(old)<=set(new),'Rear definition metadata dropped'
 assert not any('This incremental entry correction retains the old collector' in gap for gap in new['unresolved']),'Obsolete collector limitation retained'
 assert adapter.SUPERSEDED not in new['unresolved'],'Obsolete neck limitation retained'
 assert new['name']=='Rear exhaust manifold','Implementation-heavy rear name'
 assert len(new['model_bounds_mm'])==3 and all(np.isfinite(x) and x>0 for x in new['model_bounds_mm']),'Invalid rear model bounds'
 for key in set(old)-{'id','name','function','system','color','glb','step','geometry_status','sources','dimension_claims','unresolved','volume_mm3','volume_method','solid_count','triangle_count','model_bounds_mm'}:
  assert old[key]==new[key],'Rear extension metadata changed: '+key

def scope(before,after):
 for key in ('definitions','occurrences','assemblies'):
  assert len(before[key])==len(after[key])==len({x['id'] for x in after[key]})
  assert {x['id']:x for x in before[key] if x['id']!=ID}=={x['id']:x for x in after[key] if x['id']!=ID},key
 adapter.frame(before);adapter.frame(after);metadata_preserved(before,after)
 for key in before:
  if key not in ('definitions','occurrences','sources'):assert before[key]==after[key],key
 expected=copy.deepcopy(before['sources']);expected.update(adapter.source());assert after['sources']==expected
 assert after['coverage']['modeled_definitions']==len(after['definitions']) and after['coverage']['modeled_occurrences']==len(after['occurrences'])
 assert after['coverage']['verified_complete'] is False

def isolated_mesh_export(engine):
 # Explicit test-only exporter shim, never accepted by --apply. Root's later
 # shared hook must independently pass stage without this flag.
 original=engine.define
 def define(*args,**kwargs):
  original(*args,**kwargs);ident=args[0]
  if ident!=ID:return
  from OCP.BRepTools import BRepTools
  s=b.import_step(engine.STEP/(ID+'.step'));BRepTools.Clean_s(s.wrapped);v,f=s.tessellate(.05,.1)
  mesh=trimesh.Trimesh(np.array([tuple(q) for q in v])[:,[0,2,1]]*[1,1,-1]/1000,np.array(f),process=False)
  mesh.merge_vertices();mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices()
  mesh.visual=trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(baseColorFactor=[124,110,99,255],metallicFactor=.65,roughnessFactor=.38))
  (engine.OUT/(ID+'.glb')).write_bytes(trimesh.Scene(mesh).export(file_type='glb'))
  next(d for d in engine.defs if d['id']==ID)['triangle_count']=len(mesh.faces)
 return define

def context(m,shape):
 poses=transforms(m);frame=poses[ID].inverse();defs={d['id']:d for d in m['definitions']};bb=support_bounds(shape);low=np.array(tuple(bb.min))-.2;high=np.array(tuple(bb.max))+.2
 hashes={};cache={};checks=[];spatial=[]
 for o in m['occurrences']:
  if o['id']==ID:continue
  d=defs[o['definition']];gp=ROOT/d['glb'].lstrip('/');sp=ROOT/d['step'].lstrip('/')
  if o['definition'] not in cache:
   hashes[str(gp.relative_to(ROOT))]=sha(gp)
   with gp.open('rb') as f:
    magic,version,total,length,kind=struct.unpack('<5I',f.read(20));j=json.loads(f.read(length))
   assert magic==0x46546c67 and version==2 and kind==0x4e4f534a
   if any(any(k in n for k in ('matrix','translation','rotation','scale')) for n in j.get('nodes',[])):v=np.asarray(trimesh.load(gp,force='mesh').vertices)
   else:
    rows=[j['accessors'][p['attributes']['POSITION']] for mesh in j['meshes'] for p in mesh['primitives']];v=np.array([a[k] for a in rows for k in ['min','max']])
   v=v[:,[0,2,1]]*[1,-1,1]*1000;cache[o['definition']]=(v.min(0),v.max(0))
  lo,hi=cache[o['definition']];local=frame*poses[o['id']];v=np.array([tuple(b.Vertex(*p).moved(local).center()) for p in itertools.product(*zip(lo,hi))])
  if not(np.all(v.min(0)<=high) and np.all(low<=v.max(0))):continue
  spatial.append(o['id']);hashes[str(sp.relative_to(ROOT))]=sha(sp);s=b.import_step(sp).moved(local);sb=s.bounding_box()
  if not all(min(tuple(bb.max)[i],tuple(sb.max)[i])-max(tuple(bb.min)[i],tuple(sb.min)[i])>1e-7 for i in range(3)):continue
  inter=shape.intersect(s);volume=sum(abs(solid_volume(q,'adaptive')) for q in inter.solids()) if inter else 0.;assert volume<=.1,(o['id'],volume);checks.append(dict(neighbor=o['id'],overlap_mm3=volume))
 assert all(sha(ROOT/p)==h for p,h in hashes.items())
 return dict(artifact_sha256=hashes,spatial_neighbors=spatial,exact_checks=checks,scope='Fresh all-current-occurrence broadphase, exact STEP checks for overlapping bounds; threshold unchanged at0.1mm3. No historical neighbor pass reused.')

def transaction_helper():
 spec=importlib.util.spec_from_file_location('rear_transaction',ROOT/'scripts/install-intake-cap-coordination.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def rollback_controls():
 helper=transaction_helper();passed=[]
 with tempfile.TemporaryDirectory(prefix='rollback-',dir=STAGE) as p:
  a=Path(p)/'existing';z=Path(p)/'new';a.write_bytes(b'original')
  for failure in [1,2,'postcheck']:
   def post():
    if failure=='postcheck':raise RuntimeError('Injected rear postcheck failure')
   try:helper.promote({a:b'changed',z:b'new'},post,None if failure=='postcheck' else failure)
   except RuntimeError:pass
   assert a.read_bytes()==b'original' and not z.exists();passed.append(failure)
 return passed

def guard(record,installed=False):
 assert record['input_sha256']==watch(),'Changed stage dependency'
 assert record['candidate_proof_sha256']==sha(PROOF),'Changed candidate proof';evidence()
 assert sha(STAGE/'before.json')==record['before_manifest_sha256'],'Changed baseline manifest'
 assert sha(STAGE/'full-assembly.json')==record['staged_manifest_sha256'],'Changed staged manifest'
 for p,h in record['staged_artifact_sha256'].items():assert sha(STAGE/p)==h,'Changed staged export: '+p
 if 'context' in record:
  for p,h in record['context']['artifact_sha256'].items():assert sha(ROOT/p)==h,'Changed neighbor: '+p
 canonical=ROOT/'inventory/engine/full-assembly.json'
 assert sha(canonical)==record['staged_manifest_sha256' if installed else 'before_manifest_sha256'],'Canonical manifest changed'
 before=read(STAGE/'before.json');d=next(d for d in before['definitions'] if d['id']==ID)
 assert set(record['before_artifact_sha256'])=={d[k].lstrip('/') for k in ('step','glb')},'Rear baseline artifact bindings missing'
 if not installed:check_artifacts(record['before_artifact_sha256'])
 else:
  check_artifacts({d['step'].lstrip('/'):record['staged_artifact_sha256']['step/'+ID+'.step'],d['glb'].lstrip('/'):record['staged_artifact_sha256']['models/'+ID+'.glb']})
 scope(read(STAGE/'before.json'),read(STAGE/'full-assembly.json'))

def validate(installed=False):
 rec=read(STAGE/'installation.json');guard(rec,installed);m=read(ROOT/'inventory/engine/full-assembly.json' if installed else STAGE/'full-assembly.json')
 sp=(ROOT/'cad/engine/generated' if installed else STAGE/'step')/(ID+'.step');gp=(ROOT/'models/engine' if installed else STAGE/'models')/(ID+'.glb')
 if installed:
  assert sha(sp)==rec['staged_artifact_sha256']['step/'+ID+'.step'];assert sha(gp)==rec['staged_artifact_sha256']['models/'+ID+'.glb']
 base,target=adapter.fixtures();shape=b.import_step(sp);assert shape.is_valid and len(shape.solids())==1;error=adapter.difference(shape,target);assert error<.001
 mesh=trimesh.load(gp,force='mesh');mesh.merge_vertices(digits_vertex=8);assert mesh.is_watertight and mesh.nondegenerate_faces().all() and mesh.unique_faces().all()
 d=next(d for d in m['definitions'] if d['id']==ID);assert len(mesh.faces)==d['triangle_count'];assert adapter.SOURCE_ID in d['sources']
 v=mesh.vertices[:,[0,2,1]]*[1,-1,1]*1000;bb=support_bounds(shape);bounds=float(np.max(abs(np.array([v.min(0),v.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))));assert bounds<.1
 expected_size=np.array(tuple(bb.size));assert np.max(abs(np.array(d['model_bounds_mm'])-expected_size))<1e-5,'Stale model bounds metadata'
 assert d['solid_count']==1 and abs(d['volume_mm3']-solid_volume(shape,d.get('volume_method','default')))<max(1e-5,d['volume_mm3']*1e-5),'Stale CAD metadata'
 replay=[]
 for label,current in [('baseline',base),('target',target)]:
  data=copy.deepcopy(m);shapes={ID:current}
  def define(i,q,*args,**kwargs):data['definitions'].append(copy.deepcopy(d));shapes[i]=q
  adapter.install(define,None,data['definitions'],data['occurrences'],data['assemblies'],shapes);assert data==m and adapter.difference(shapes[ID],target)<.001;replay.append(label)
 controls={};bad=copy.deepcopy(m);next(o for o in bad['occurrences'] if o['id']==ID)['position_cad_mm'][0]+=.5
 try:adapter.frame(bad)
 except ValueError:controls['local_frame_rejected']=True
 assert controls.get('local_frame_rejected')
 bad=copy.deepcopy(m);parent=next(o for o in bad['occurrences'] if o['id']==ID)['parent'];next(a for a in bad['assemblies'] if a['id']==parent)['position_cad_mm'][0]+=.5
 try:adapter.frame(bad)
 except ValueError:controls['ancestor_frame_rejected']=True
 assert controls.get('ancestor_frame_rejected')
 bad=copy.deepcopy(m)
 try:adapter.install(define,None,bad['definitions'],bad['occurrences'],bad['assemblies'],{ID:b.Pos(.5,0,0)*target})
 except ValueError:controls['unknown_geometry_rejected']=True
 assert controls.get('unknown_geometry_rejected')
 lesson=read(ROOT/'inventory/engine/rear-exhaust-neck-learning.json');ids={x['id'] for k in ('assemblies','occurrences') for x in m[k]}
 for k,row in lesson.items():
  assert k in ids and set(row['sources'])<=set(m['sources'])
  for source_id in row['sources']:
   source=m['sources'][source_id];assert sha(ROOT/source['path'].lstrip('/'))==source['sha256'],'Changed learning source: '+source_id
  for section in ('steps','troubleshooting'):
   assert all(item.get('part',k) in ids and item.get('source',row['sources'][0]) in row['sources'] for item in row.get(section,[]))
 ctx=context(m,shape);guard(rec,installed)
 return dict(status='PASS installed rear neck; browser pending' if installed else 'PASS staged rear neck',installation_sha256=sha(STAGE/'installation.json'),manifest_sha256=sha(STAGE/'full-assembly.json'),candidate_proof_sha256=sha(PROOF),fresh_export_rebind=rec['export_rebind'],exports=dict(difference_mm3=error,watertight=True,triangles=len(mesh.faces),bounds_error_mm=bounds),replay=replay,negative_controls=controls,rollback_controls=rollback_controls(),context=ctx,learning_valid=True,definition_metadata_preserved=True,scope='Frozen source-bound candidate CAD/flow/wall proof plus fresh target STEP binding, actual exporter mesh check, idempotence and current neighbors. No whole-candidate rebuild or silent exporter hash waiver.',limits=adapter.GAPS)

def full_build_contract():
 # Read-only wiring audit; no whole-engine rebuild. The previous rear hook
 # creates the recognized baseline, then this adapter replaces it in order.
 text=(ROOT/'cad/engine/full_engine.py').read_text()
 assert text.index('rear_collector.install(')<text.index('rear_neck.install('),'Neck must follow rear collector'
 assert "import rear_exhaust_neck_integration as rear_neck" in text
 assert 'sources.update(rear_neck.source())' in text
 assert text.index("rear-exhaust-neck-learning.json")>text.index("exhaust-rear-collector-learning.json")
 # Both adapters have the same changed ID. Existing final exact-bounds branch
 # already covers exhaust-rear through rear_collector.CHANGED_IDS.
 assert "rear_collector.CHANGED_IDS" in text and adapter.CHANGED_IDS=={'exhaust-rear'}
 viewer=(ROOT/'viewer/engine-learning-modules.js').read_text()
 assert viewer.index("'rear-exhaust-neck'")>viewer.index("'exhaust-rear-collector'")
 return dict(hook_order='rear_collector then rear_neck',final_bounds='Existing rear_collector.CHANGED_IDS covers same exhaust-rear ID',learning_override=True,scope='Static wiring audit plus scoped exporter stage, not a full engine rebuild')

def stage(isolated=False,rebind=False):
 import full_engine as engine
 proof=evidence();wiring=full_build_contract();initial=watch();raw=(ROOT/'inventory/engine/full-assembly.json').read_bytes();before=json.loads(raw);m=copy.deepcopy(before)
 baseline_artifacts=canonical_artifacts(before)
 current_exporter=hashlib.sha256(inspect.getsource(engine.define).encode()).hexdigest()
 if not rebind:raise ValueError('Neck candidate used isolated fine export; use --rebind-exporter for actual shared exporter proof')
 for name in ['step','models']:(STAGE/name).mkdir(parents=True,exist_ok=True)
 engine.STEP=STAGE/'step';engine.OUT=STAGE/'models';engine.defs[:]=m['definitions'];engine.occurrences[:]=m['occurrences'];engine.assemblies[:]=m['assemblies'];engine.shapes.clear()
 change=adapter.install(isolated_mesh_export(engine) if isolated else engine.define,engine.add,engine.defs,engine.occurrences,engine.assemblies,engine.shapes)
 m.update(definitions=engine.defs,occurrences=engine.occurrences,assemblies=engine.assemblies);m['sources'].update(adapter.source());scope(before,m)
 (STAGE/'before.json').write_bytes(raw);dump(STAGE/'full-assembly.json',m)
 rec=dict(status='STAGED rear neck',full_build_contract=wiring,isolated_export_test_only=isolated,before_manifest_sha256=sha(STAGE/'before.json'),before_artifact_sha256=baseline_artifacts,staged_manifest_sha256=sha(STAGE/'full-assembly.json'),candidate_proof_sha256=sha(PROOF),input_sha256=initial,staged_artifact_sha256={str(p.relative_to(STAGE)):sha(p) for p in [STAGE/'step'/(ID+'.step'),STAGE/'models'/(ID+'.glb')]},export_rebind=dict(historical_candidate_exporter_define_sha256=None,historical_export_profile=proof['isolated_export'],current_exporter_define_sha256=current_exporter,explicit_rebind=rebind,method='Retain original candidate report; rerun actual current define on frozen target, verify exact STEP/mesh/metadata/current neighbors. Isolated test shim is explicitly marked and cannot be promoted.'),**change)
 dump(STAGE/'installation.json',rec);result=validate();rec['context']=result['context'];dump(STAGE/'installation.json',rec);result['installation_sha256']=sha(STAGE/'installation.json');dump(STAGE/'validation.json',result)
 assert initial==watch() and (ROOT/'inventory/engine/full-assembly.json').read_bytes()==raw;print(result['status'])

def apply():
 rec=read(STAGE/'installation.json');r=read(STAGE/'validation.json');assert not rec['isolated_export_test_only'],'Isolated exporter shim cannot be promoted';assert r['status']=='PASS staged rear neck' and r['installation_sha256']==sha(STAGE/'installation.json');guard(rec)
 helper=transaction_helper();dest=ROOT/'inventory/engine/rear-exhaust-neck-installed-validation.json';writes={ROOT/'inventory/engine/full-assembly.json':(STAGE/'full-assembly.json').read_bytes(),ROOT/'inventory/engine/rear-exhaust-neck-installation.json':(STAGE/'installation.json').read_bytes(),dest:b''}
 for folder,target in [('step','cad/engine/generated'),('models','models/engine')]:
  ext='step' if folder=='step' else 'glb';writes[ROOT/target/(ID+'.'+ext)]=(STAGE/folder/(ID+'.'+ext)).read_bytes()
 def postcheck():helper.replace(dest,(json.dumps(validate(True),indent=2)+'\n').encode())
 helper.promote(writes,postcheck);print('Installed rear neck; browser checks pending')
if __name__=='__main__':
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group();g.add_argument('--stage',action='store_true');g.add_argument('--apply',action='store_true');g.add_argument('--check-installed',action='store_true');p.add_argument('--isolated-export',action='store_true');p.add_argument('--rebind-exporter',action='store_true');a=p.parse_args()
 if a.stage:stage(a.isolated_export,a.rebind_exporter)
 elif a.apply:apply()
 elif a.check_installed:dump(ROOT/'inventory/engine/rear-exhaust-neck-installed-validation.json',validate(True))
 else:print('Use --stage; --isolated-export tests before shared hook and cannot promote. Use --stage --rebind-exporter after shared exporter changes. --apply is explicit.')
