#!/usr/bin/env python3
"""Isolated runner stage/preflight/check; canonical writes require explicit--apply."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import numpy as np
import trimesh
import intake_runner_exterior_integration as adapter
STAGE=ROOT/'cad/engine/generated/intake-runner-exterior-integration-stage'
CONTEXT=ROOT/'inventory/engine/intake-runner-exterior-context-validation.json'
RECORD=ROOT/'inventory/engine/intake-runner-exterior-installation.json'
HELPER=ROOT/'scripts/install-intake-cap-coordination.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def dump(p,data):p.write_text(json.dumps(data,indent=2)+'\n')
def source_paths():
 return [Path(__file__),Path(adapter.__file__),ROOT/'inventory/engine/intake-runner-exterior-learning.json',ROOT/'reference/engine/intake-runner-exterior-review.json',HELPER]+[ROOT/('inventory/engine/intake-runner-exterior-'+kind+'-validation.json') for kind in ('candidate','context','controls','render')]
def artifacts(stage=STAGE):return {'cad/engine/generated/efi-upper-intake.step':stage/'step/efi-upper-intake.step','models/engine/efi-upper-intake.glb':stage/'models/efi-upper-intake.glb'}
def transaction_helper():
 spec=importlib.util.spec_from_file_location('reviewed_runner_transaction',HELPER);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def stage():
 proof=read(CONTEXT);assert proof['status'].startswith('PASS') and proof['input_guard_pass']
 for name in ('candidate','controls','render'):assert read(ROOT/('inventory/engine/intake-runner-exterior-'+name+'-validation.json'))['status'].startswith('PASS')
 for p,h in proof['input_sha256_after'].items():assert sha(ROOT/p)==h,p
 mp=ROOT/'inventory/engine/full-assembly.json';raw=mp.read_bytes();m=json.loads(raw);assert sha(mp)==proof['manifest_sha256']
 before={str(p.relative_to(ROOT)):sha(p) for p in source_paths()}
 for folder in ('step','models','baseline'): (STAGE/folder).mkdir(parents=True,exist_ok=True)
 baseline_report=ROOT/'inventory/engine/atlas-static-validation.json';(STAGE/'baseline/atlas-static-validation.json').write_bytes(baseline_report.read_bytes())
 old={d['id']:d for d in m['definitions']};shapes={}
 def define(i,s,name,function,system,color,sources,gaps,claims,prepared=False):
  assert prepared
  row=copy.deepcopy(old[i]);row.update(name=name,function=function,system=system,color=color,sources=sources,unresolved=gaps,dimension_claims=claims)
  m['definitions'].append(row);shapes[i]=s;b.export_step(s,STAGE/'step'/(i+'.step'))
 change=adapter.install(define,m['definitions'],m['occurrences'],m['assemblies'],shapes,m.get('mechanism'),STAGE/'models')
 m['sources'].update(adapter.sources());dump(STAGE/'full-assembly.json',m)
 assert mp.read_bytes()==raw and before=={str(p.relative_to(ROOT)):sha(p) for p in source_paths()}
 record=dict(historical_report_sha256={'inventory/engine/atlas-static-validation.json':sha(STAGE/'baseline/atlas-static-validation.json')},status='STAGED runner exterior; not installed',before_manifest_sha256=hashlib.sha256(raw).hexdigest(),staged_manifest_sha256=sha(STAGE/'full-assembly.json'),source_sha256=before,context_report_sha256=sha(CONTEXT),canonical_artifact_sha256={p:sha(v) for p,v in artifacts().items()},staged_artifact_sha256={str(p.relative_to(STAGE)):sha(p) for p in artifacts().values()},baseline_occurrence=next(o for o in json.loads(raw)['occurrences'] if o['id']==adapter.ID),definitions=len(m['definitions']),occurrences=len(m['occurrences']),export_settings=dict(linear_deflection_mm=.07,angular_deflection_rad=.08),**change)
 dump(STAGE/'installation.json',record);result=validate(False);dump(STAGE/'validation.json',result);print(result['status'])

def replay(m,shape,baseline=False):
 data=copy.deepcopy(m);old=next(d for d in data['definitions'] if d['id']==adapter.ID);shapes={adapter.ID:adapter.targets()[0] if baseline else shape}
 def define(i,s,n,f,system,color,sources,gaps,claims,prepared=False):
  row=copy.deepcopy(old);row.update(name=n,function=f,system=system,color=color,sources=sources,unresolved=gaps,dimension_claims=claims);data['definitions'].append(row);shapes[i]=s
 adapter.install(define,data['definitions'],data['occurrences'],data['assemblies'],shapes,data.get('mechanism'))
 assert data==m,'Repeat/partial refresh changed metadata'
 error=adapter.difference(shapes[adapter.ID],shape);assert error<.1
 return error

def validate(installed=False,stage_dir=STAGE):
 stage=Path(stage_dir);record=read(RECORD if installed else stage/'installation.json')
 for p,h in record['source_sha256'].items():assert sha(ROOT/p)==h,'Source/proof changed: '+p
 assert sha(CONTEXT)==record['context_report_sha256'];proof=read(CONTEXT)
 mp=ROOT/'inventory/engine/full-assembly.json' if installed else stage/'full-assembly.json';raw=mp.read_bytes();m=json.loads(raw)
 assert sha(mp)==record['staged_manifest_sha256'],'Manifest changed'
 assert len(m['definitions'])==733 and len(m['occurrences'])==1341
 for p,h in proof['input_sha256_after'].items():
  expected=record['canonical_artifact_sha256'].get(p,h) if installed else h
  if p=='inventory/engine/full-assembly.json':expected=record['staged_manifest_sha256'] if installed else record['before_manifest_sha256']
  bound=stage/'baseline/atlas-static-validation.json' if installed and p in record['historical_report_sha256'] else ROOT/p
  assert sha(bound)==expected,'Bound baseline/context changed: '+p
 for p,h in record['historical_report_sha256'].items():assert sha(stage/'baseline/atlas-static-validation.json')==h,'Historical static proof changed'
 for p,h in record['staged_artifact_sha256'].items():assert sha(stage/p)==h,'Stage artifact changed: '+p
 for p,h in record['canonical_artifact_sha256'].items():
  if installed:assert sha(ROOT/p)==h,'Installed artifact changed: '+p
 watched={ROOT/p for p in proof['input_sha256_after'] if not(installed and p in record['historical_report_sha256'])}|set(source_paths())|{mp,stage/'installation.json',stage/'baseline/atlas-static-validation.json'}|set(artifacts(stage).values())
 initial_hashes={str(p):sha(p) for p in watched}
 d=next(d for d in m['definitions'] if d['id']==adapter.ID);o=next(o for o in m['occurrences'] if o['id']==adapter.ID)
 frame_keys=('parent','position_cad_mm','rotation_cad_deg','explode_cad_mm');assert all(o.get(k)==record['baseline_occurrence'].get(k) for k in frame_keys)
 assert m['sources'][adapter.SOURCE]==adapter.sources()[adapter.SOURCE]
 sp=ROOT/d['step'].lstrip('/') if installed else stage/'step/efi-upper-intake.step';gp=ROOT/d['glb'].lstrip('/') if installed else stage/'models/efi-upper-intake.glb'
 shape=b.import_step(sp);assert shape.is_valid and len(shape.solids())==1
 accepted=b.import_step(adapter.STUDY/'runner-exterior.step');difference=adapter.difference(shape,accepted);assert difference<.1
 mesh=trimesh.load(gp,force='mesh');mesh.merge_vertices(digits_vertex=8);assert mesh.is_watertight and mesh.unique_faces().all() and mesh.nondegenerate_faces().all()
 v=np.asarray(mesh.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000;bb=shape.bounding_box();bounds=float(np.max(abs(np.array([v.min(0),v.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))))
 assert bounds<.15 and len(mesh.faces)==d['triangle_count'] and np.max(abs(np.array(tuple(bb.size))-d['model_bounds_mm']))<.01
 ordinary=replay(m,shape);partial=replay(m,shape,True)
 def reject(data,part,phrase):
  def forbidden(*a,**k):raise AssertionError('Invalid input reached export')
  try:adapter.install(forbidden,data['definitions'],data['occurrences'],data['assemblies'],{adapter.ID:part},data.get('mechanism'))
  except ValueError as error:return phrase in str(error)
  return False
 bad=copy.deepcopy(m);next(o for o in bad['occurrences'] if o['id']==adapter.ID)['position_cad_mm'][0]+=.25
 frame_rejected=reject(bad,shape,'frame');geometry_rejected=reject(copy.deepcopy(m),b.Pos(.25,0,0)*shape,'geometry');assert frame_rejected and geometry_rejected
 lessons=read(ROOT/'inventory/engine/intake-runner-exterior-learning.json');ids={o['id'] for o in m['occurrences']}
 for ident,lesson in lessons.items():
  assert ident in ids and set(lesson['sources'])<=set(m['sources'])
  for section in ('steps','troubleshooting'):
   for item in lesson.get(section,[]):assert 'part' not in item or item['part'] in ids
 final_hashes={str(p):sha(p) for p in watched};assert initial_hashes==final_hashes and mp.read_bytes()==raw
 guard_digest=hashlib.sha256(json.dumps(initial_hashes,sort_keys=True).encode()).hexdigest()
 return dict(input_guard=dict(file_count=len(watched),before_sha256=guard_digest,after_sha256=hashlib.sha256(json.dumps(final_hashes,sort_keys=True).encode()).hexdigest()),status='PASS installed runner exterior; browser pending' if installed else 'PASS staged runner exterior',manifest_sha256=sha(mp),installation_record_sha256=sha(RECORD if installed else stage/'installation.json'),source_sha256=record['source_sha256'],geometry_difference_mm3=difference,exports=dict(triangles=len(mesh.faces),bytes=gp.stat().st_size,watertight=True,bounds_error_mm=bounds,**record['export_settings']),replay=dict(repeat_difference_mm3=ordinary,partial_refresh_difference_mm3=partial,changed_frame_rejected=frame_rejected,changed_geometry_rejected=geometry_rejected),context_report_sha256=sha(CONTEXT),inherited_context_scope=proof['summary'],new_static_or_motion_pairs_rerun_here=0,learning_valid=True,input_guard_pass=True,limits=adapter.GAPS)

def preflight():
 r=read(STAGE/'validation.json');assert r['status'].startswith('PASS')
 record=read(STAGE/'installation.json');assert r['installation_record_sha256']==sha(STAGE/'installation.json')
 assert sha(ROOT/'inventory/engine/full-assembly.json')==record['before_manifest_sha256']
 for p,h in record['source_sha256'].items():assert sha(ROOT/p)==h,p
 for p,h in record['historical_report_sha256'].items():assert sha(STAGE/'baseline/atlas-static-validation.json')==h,p
 for p,h in record['staged_artifact_sha256'].items():assert sha(STAGE/p)==h,p
 assert sha(STAGE/'full-assembly.json')==record['staged_manifest_sha256']
 for p,h in read(CONTEXT)['input_sha256_after'].items():assert sha(ROOT/p)==h,p
 return record

def apply():
 record=preflight();helper=transaction_helper();writes={ROOT/p:s.read_bytes() for p,s in artifacts().items()}
 writes[ROOT/'inventory/engine/full-assembly.json']=(STAGE/'full-assembly.json').read_bytes();writes[RECORD]=(json.dumps(record,indent=2)+'\n').encode()
 result_path=ROOT/'inventory/engine/intake-runner-exterior-installed-validation.json';writes[result_path]=b''
 preflight()
 def postcheck():helper.replace(result_path,(json.dumps(validate(True),indent=2)+'\n').encode())
 helper.promote(writes,postcheck);print('Installed runner exterior; browser acceptance pending')

def transaction_tests():
 helper=transaction_helper();results=[]
 with tempfile.TemporaryDirectory(prefix='runner-transaction-',dir=STAGE) as folder:
  folder=Path(folder);a=folder/'existing';z=folder/'new';a.write_bytes(b'original');writes={a:b'changed',z:b'new'}
  for failure in (1,2,'postcheck'):
   def post():
    if failure=='postcheck':raise RuntimeError('Injected postcheck failure')
   try:helper.promote(writes,post,None if failure=='postcheck' else failure)
   except RuntimeError:pass
   assert a.read_bytes()==b'original' and not z.exists();results.append(failure)
 # Preflight corruption tests are confined to staged artifact copies, never canonical.
 import shutil
 with tempfile.TemporaryDirectory(prefix='runner-corruption-',dir=STAGE) as directory:
  mirror=Path(directory);shutil.copytree(STAGE/'step',mirror/'step');shutil.copytree(STAGE/'models',mirror/'models');shutil.copytree(STAGE/'baseline',mirror/'baseline')
  for name in ('full-assembly.json','installation.json'):shutil.copy2(STAGE/name,mirror/name)
  gp=mirror/'models/efi-upper-intake.glb';original=gp.read_bytes();gp.write_bytes(original+b'corrupt');caught=False
  try:validate(False,mirror)
  except AssertionError as e:caught='Stage artifact changed' in str(e)
  assert caught;gp.write_bytes(original)
  m=read(mirror/'full-assembly.json');next(o for o in m['occurrences'] if o['id']==adapter.ID)['position_cad_mm'][0]=.25;dump(mirror/'full-assembly.json',m);frame_caught=False
  try:validate(False,mirror)
  except AssertionError as e:frame_caught='Manifest changed' in str(e)
  assert frame_caught
 result=dict(status='PASS scoped promotion controls',stage_validation_sha256=sha(STAGE/'validation.json'),source_sha256={str(p.relative_to(ROOT)):sha(p) for p in source_paths()},rollback_failures=results,corrupt_staged_mesh_rejected=True,corrupt_staged_frame_rejected=True)
 dump(ROOT/'inventory/engine/intake-runner-exterior-promotion-validation.json',result);print(result['status'])

def main():
 p=argparse.ArgumentParser(description=__doc__);m=p.add_mutually_exclusive_group();m.add_argument('--stage',action='store_true');m.add_argument('--apply',action='store_true');m.add_argument('--check-installed',action='store_true');m.add_argument('--test-promotion',action='store_true');args=p.parse_args()
 if args.stage:stage()
 elif args.apply:
  test=read(ROOT/'inventory/engine/intake-runner-exterior-promotion-validation.json');assert test['status'].startswith('PASS') and test['stage_validation_sha256']==sha(STAGE/'validation.json');apply()
 elif args.check_installed:
  result=validate(True);dump(ROOT/'inventory/engine/intake-runner-exterior-installed-validation.json',result);print(result['status'])
 elif args.test_promotion:preflight();transaction_tests()
 else:preflight();print('PASS runner promotion preflight; no writes')
if __name__=='__main__':main()
