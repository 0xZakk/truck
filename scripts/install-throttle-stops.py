#!/usr/bin/env python3
"""Scoped stop stage, validation and explicit transactional promotion."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import numpy as np
import trimesh
import throttle_stop_integration as adapter
from assembly_math import transforms
from cad_metrics import solid_volume
STAGE=ROOT/'cad/engine/generated/throttle-stop-integration-stage'
PROOF=ROOT/'inventory/engine/throttle-stop-candidate-validation.json'
BASE=ROOT/'cad/engine/generated/throttle-cable-integration-stage/full-assembly.json'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def dump(p,v):Path(p).write_text(json.dumps(v,indent=2)+'\n')
def deps():return [Path(__file__),Path(adapter.__file__),PROOF,ROOT/'cad/engine/throttle_stop_candidate.py',ROOT/'cad/engine/assembly_math.py',ROOT/'cad/engine/cad_metrics.py',ROOT/'cad/engine/full_engine.py',ROOT/'scripts/install-intake-cap-coordination.py',ROOT/'reference/engine/throttle-stop-review.json',ROOT/'inventory/engine/throttle-stop-learning.json',ROOT/'inventory/engine/completion-plan.json']
def watch():return {str(p.relative_to(ROOT)):sha(p) for p in deps()}
def evidence():
 r=read(PROOF);assert r['status']=='PASS' and r['full_sweep'] and r['thread_retention_status']=='PASS'
 assert sha(BASE)==r['input_hashes']['inventory/engine/full-assembly.json']
 for p,h in r['input_hashes'].items():
  if p.endswith('.py'):assert sha(ROOT/p)==h,p
 for p,h in r['output_hashes'].items():assert sha(ROOT/p)==h,p
 adapter.fixtures();return r

def metadata(m):
 m['coverage'].update(modeled_definitions=len(m['definitions']),modeled_occurrences=len(m['occurrences']))
 m['omissions']=[item['system']+': '+', '.join(item['items']) for item in read(ROOT/'inventory/engine/completion-plan.json')['remaining']]

def scope(before,after):
 expected=copy.deepcopy(after);metadata(expected);assert after['coverage']==expected['coverage'] and after['omissions']==expected['omissions'],'Coverage/omissions stale'
 assert after['coverage'].get('verified_complete') is False
 for key,allowed in [('definitions',adapter.CHANGED_IDS),('occurrences',adapter.CHANGED_IDS),('assemblies',set())]:
  assert {x['id']:x for x in before[key] if x['id'] not in allowed}=={x['id']:x for x in after[key] if x['id'] not in allowed},key
  assert len(after[key])==len({x['id'] for x in after[key]})
 old={x['id']:x for x in before['occurrences']};new={x['id']:x for x in after['occurrences']}
 for ident in adapter.REPLACED:
  for k in ['definition','parent','position_cad_mm','rotation_cad_deg','explode_cad_mm']:assert old[ident].get(k)==new[ident].get(k)
 assert len(after['definitions'])==len(before['definitions'])+1 and len(after['occurrences'])==len(before['occurrences'])+1

def stage():
 import full_engine as engine
 proof=evidence();initial=watch();mp=ROOT/'inventory/engine/full-assembly.json';raw=mp.read_bytes();before=json.loads(raw);m=copy.deepcopy(before)
 assert adapter.SCREW not in {x['id'] for x in m['definitions']},'Already installed; use --check-installed'
 for folder in ('step','models'): (STAGE/folder).mkdir(parents=True,exist_ok=True)
 engine.STEP=STAGE/'step';engine.OUT=STAGE/'models';engine.defs[:]=m['definitions'];engine.occurrences[:]=m['occurrences'];engine.assemblies[:]=m['assemblies'];engine.shapes.clear()
 change=adapter.install(engine.define,engine.add,engine.defs,engine.occurrences,engine.assemblies,engine.shapes)
 m.update(definitions=engine.defs,occurrences=engine.occurrences,assemblies=engine.assemblies);m['sources'].update(adapter.source());metadata(m);scope(before,m)
 dump(STAGE/'full-assembly.json',m);(STAGE/'before.json').write_bytes(raw)
 record=dict(status='STAGED illustrative throttle stops',before_manifest_sha256=sha(mp),staged_manifest_sha256=sha(STAGE/'full-assembly.json'),input_sha256=initial,staged_artifact_sha256={str(p.relative_to(STAGE)):sha(p) for folder in ('step','models') for p in (STAGE/folder).iterdir()},**change)
 dump(STAGE/'installation.json',record);assert mp.read_bytes()==raw and initial==watch()
 result=validate();dump(STAGE/'validation.json',result);print(result['status'],flush=True)

def context(m,proof):
 baseline=read(BASE);bd={x['id']:x for x in baseline['definitions']};bo={x['id']:x for x in baseline['occurrences']};d={x['id']:x for x in m['definitions']};o={x['id']:x for x in m['occurrences']}
 angles=[x['angle_deg'] for x in proof['contacts']];assert len(angles)==47
 changed=set();poses_by_angle={}
 for angle in angles:
  oldposes=transforms(baseline,throttle_degrees=angle);poses=transforms(m,throttle_degrees=angle);poses_by_angle[angle]=poses
  for ident in adapter.REPLACED:assert str(poses[ident])==str(oldposes[ident]),'Stop inherited world frame changed: '+ident
  for ident,row in o.items():
   if ident in adapter.CHANGED_IDS:continue
   if ident not in bo or row!=bo[ident] or d[row['definition']]!=bd.get(row['definition']) or str(poses[ident])!=str(oldposes.get(ident)):changed.add(ident)
 assert not {i for i in changed if i.startswith('throttle-cable-') or i=='throttle-return-spring-illustrative'},'Changed dynamic neighbor requires new full sweep'
 # The exact-neighbor STEP hashes from the frozen proof must still match unless
 # explicitly treated as changed. Bind every current mesh used in broadphase.
 hashes={};meshes={}
 for ident,row in o.items():
  if ident in adapter.CHANGED_IDS:continue
  definition=d[row['definition']];sp=definition['step'].lstrip('/');gp=definition['glb'].lstrip('/');hashes[gp]=sha(ROOT/gp)
  if sp in proof['input_hashes'] and sha(ROOT/sp)!=proof['input_hashes'][sp]:changed.add(ident)
  mesh=trimesh.load(ROOT/gp,force='mesh');v=np.asarray(mesh.vertices)[:,[0,2,1]]*[1,-1,1]*1000;meshes[ident]=(v.min(0)-.15,v.max(0)+.15)
 base,target=adapter.fixtures();delta={i:b.Compound(children=list(target[i].cut(base[i]).solids())) for i in adapter.REPLACED};delta[adapter.SCREW]=target[adapter.SCREW]
 exact=0;hits=[];cache={};tested=[];inherited_pairs=0
 def box(q):bb=q.bounding_box();return np.array([tuple(bb.min),tuple(bb.max)])
 def overlap(a,z):return np.all(a[0]<=z[1]+1e-6) and np.all(z[0]<=a[1]+1e-6)
 import itertools
 for angle,poses in poses_by_angle.items():
  parts={i:q.moved(poses[i]) for i,q in delta.items()};part_bounds={i:box(q) for i,q in parts.items()}
  for ident in sorted(meshes):
   corners=np.array([tuple(b.Vertex(*p).moved(poses[ident]).center()) for p in itertools.product(*zip(*meshes[ident]))]);bounds=np.array([corners.min(0),corners.max(0)])
   if not any(overlap(bounds_q,bounds) for bounds_q in part_bounds.values()):continue
   sp=d[o[ident]['definition']]['step'].lstrip('/');hashes[sp]=sha(ROOT/sp)
   if ident not in changed and hashes[sp]==proof['input_hashes'].get(sp):
    inherited_pairs+=1;continue
   # Deforming cable/spring geometry is evaluated by the frozen source-bound
   # candidate proof; its inputs and frames must remain unchanged.
   if ident.startswith('throttle-cable-') or ident=='throttle-return-spring-illustrative':
    assert ident not in changed,'Changed dynamic neighbor requires new full sweep';inherited_pairs+=1;continue
   if sp not in cache:cache[sp]=b.import_step(ROOT/sp)
   q=cache[sp].moved(poses[ident])
   for key,p in parts.items():
    if overlap(box(p),box(q)):
     inter=p.intersect(q);v=sum(abs(solid_volume(s,'adaptive')) for s in inter.solids()) if inter else 0.;exact+=1;tested.append([angle,key,ident,v])
     if v>1e-5:hits.append(tested[-1])
 assert not hits,hits
 assert all(sha(ROOT/p)==h for p,h in hashes.items())
 return dict(angles=angles,changed_or_new_neighbors=sorted(changed),exact_pairs=exact,inherited_bound_neighbor_pose_hits=inherited_pairs,pairs=tested,collisions=hits,artifact_sha256=hashes,scope='Frozen 47-pose exact proof plus fresh all-occurrence broadphase and exact checks for changed/new/unbound overlapping neighbors. Historical broadphase GLBs and helper modules were not hash-bound by the original candidate report; current files are now bound, not retrospectively certified.')

def validate(installed=False):
 record=read(STAGE/'installation.json');assert watch()==record['input_sha256'];proof=evidence()
 mp=ROOT/'inventory/engine/full-assembly.json' if installed else STAGE/'full-assembly.json';assert sha(mp)==record['staged_manifest_sha256'];m=read(mp);before=read(STAGE/'before.json');assert sha(STAGE/'before.json')==record['before_manifest_sha256'];scope(before,m)
 for p,h in record['staged_artifact_sha256'].items():assert sha(STAGE/p)==h,p
 base,target=adapter.fixtures();exports={};shapes={}
 for ident in adapter.CHANGED_IDS:
  sp=(ROOT/'cad/engine/generated' if installed else STAGE/'step')/(ident+'.step');gp=(ROOT/'models/engine' if installed else STAGE/'models')/(ident+'.glb')
  if installed:
   assert sha(sp)==record['staged_artifact_sha256']['step/'+ident+'.step'];assert sha(gp)==record['staged_artifact_sha256']['models/'+ident+'.glb']
  q=b.import_step(sp);assert q.is_valid and len(q.solids())==1;error=adapter.difference(q,target[ident]);assert error<1e-5;shapes[ident]=q
  mesh=trimesh.load(gp,force='mesh');mesh.merge_vertices(digits_vertex=8);assert mesh.is_watertight and mesh.nondegenerate_faces().all() and mesh.unique_faces().all()
  assert len(mesh.faces)==next(d['triangle_count'] for d in m['definitions'] if d['id']==ident),'Triangle metadata differs'
  v=np.asarray(mesh.vertices)[:,[0,2,1]]*[1,-1,1]*1000;bb=q.bounding_box();bounds=float(np.max(abs(np.array([v.min(0),v.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))));assert bounds<.15
  exports[ident]=dict(difference_mm3=error,watertight=True,bounds_error_mm=bounds)
 # Replay mutates in-memory metadata only; geometry must equal the frozen target.
 replay=[]
 for replacements in ({},base,{'throttle-housing':base['throttle-housing']},{'throttle-lever-estimated':base['throttle-lever-estimated']}):
  data=copy.deepcopy(m);ss=shapes|replacements;old={d['id']:d for d in m['definitions']}
  def define(i,q,*args,**kwargs):data['definitions'].append(copy.deepcopy(old[i]));ss[i]=q
  def add(i,d,parent,pos,explode,name=None):data['occurrences'].append(copy.deepcopy(next(o for o in m['occurrences'] if o['id']==i)))
  adapter.install(define,add,data['definitions'],data['occurrences'],data['assemblies'],ss);assert data==m
  assert all(adapter.difference(ss[i],target[i])<1e-5 for i in adapter.CHANGED_IDS);replay.append(sorted(replacements))
 controls={}
 bad=copy.deepcopy(m);next(o for o in bad['occurrences'] if o['id']=='throttle-housing')['position_cad_mm'][0]=.25
 try:adapter.local_bindings(bad['occurrences'])
 except ValueError:controls['shifted_frame_rejected']=True
 assert controls.get('shifted_frame_rejected')
 badshapes=shapes|{'throttle-lever-estimated':b.Pos(.25,0,0)*shapes['throttle-lever-estimated']}
 try:adapter.install(define,add,copy.deepcopy(m['definitions']),copy.deepcopy(m['occurrences']),copy.deepcopy(m['assemblies']),badshapes)
 except ValueError:controls['shifted_geometry_rejected']=True
 assert controls.get('shifted_geometry_rejected')
 lesson=read(ROOT/'inventory/engine/throttle-stop-learning.json');ids={x['id'] for k in ['occurrences','assemblies'] for x in m[k]}
 for key,row in lesson.items():
  assert key in ids and set(row['sources'])<=set(m['sources'])
  for section in ('steps','troubleshooting'):
   for item in row.get(section,[]):assert item.get('part',key) in ids
 ctx=context(m,proof);assert watch()==record['input_sha256']
 return dict(status='PASS installed throttle stops; browser pending' if installed else 'PASS staged throttle stops',manifest_sha256=sha(mp),installation_sha256=sha(STAGE/'installation.json'),inherited_proof_sha256=sha(PROOF),inherited_exact_pairs=proof['exact_pairs'],exports=exports,replay=replay,negative_controls=controls,transaction_rollback_controls=transaction_controls(),context=ctx,learning_valid=True,coverage_and_omissions_current=True,limits=adapter.GAPS)

def transaction_controls():
 spec=importlib.util.spec_from_file_location('stop_transaction_test',ROOT/'scripts/install-intake-cap-coordination.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
 passed=[]
 with tempfile.TemporaryDirectory(prefix='stop-promotion-',dir=STAGE) as path:
  folder=Path(path);a=folder/'existing';z=folder/'new';a.write_bytes(b'original')
  for failure in (1,2,'postcheck'):
   def post():
    if failure=='postcheck':raise RuntimeError('Injected stop postcheck failure')
   try:helper.promote({a:b'changed',z:b'new'},post,None if failure=='postcheck' else failure)
   except RuntimeError:pass
   assert a.read_bytes()==b'original' and not z.exists();passed.append(failure)
 return passed

def apply():
 r=read(STAGE/'validation.json');record=read(STAGE/'installation.json');assert r['status'].startswith('PASS') and r['installation_sha256']==sha(STAGE/'installation.json');assert watch()==record['input_sha256'];assert sha(ROOT/'inventory/engine/full-assembly.json')==record['before_manifest_sha256']
 for p,h in r['context']['artifact_sha256'].items():assert sha(ROOT/p)==h,p
 for p,h in record['staged_artifact_sha256'].items():assert sha(STAGE/p)==h,p
 assert sha(STAGE/'full-assembly.json')==record['staged_manifest_sha256']
 spec=importlib.util.spec_from_file_location('stop_transaction',ROOT/'scripts/install-intake-cap-coordination.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
 writes={ROOT/'inventory/engine/full-assembly.json':(STAGE/'full-assembly.json').read_bytes(),ROOT/'inventory/engine/throttle-stop-installation.json':(STAGE/'installation.json').read_bytes()}
 for ident in adapter.CHANGED_IDS:
  writes[ROOT/'cad/engine/generated'/(ident+'.step')]=(STAGE/'step'/(ident+'.step')).read_bytes();writes[ROOT/'models/engine'/(ident+'.glb')]=(STAGE/'models'/(ident+'.glb')).read_bytes()
 result_path=ROOT/'inventory/engine/throttle-stop-installed-validation.json';writes[result_path]=b''
 def postcheck():helper.replace(result_path,(json.dumps(validate(True),indent=2)+'\n').encode())
 helper.promote(writes,postcheck);print('Installed guarded throttle stops; browser acceptance NOT RUN')
if __name__=='__main__':
 p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group();g.add_argument('--stage',action='store_true');g.add_argument('--apply',action='store_true');g.add_argument('--check-installed',action='store_true');a=p.parse_args()
 if a.stage:stage()
 elif a.apply:apply()
 elif a.check_installed:dump(ROOT/'inventory/engine/throttle-stop-installed-validation.json',validate(True))
 else:print('Plan: replace housing/lever and add one illustrative stationary screw; --stage validates isolated outputs; --apply promotes checked outputs.')
