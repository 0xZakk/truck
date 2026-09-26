#!/usr/bin/env python3
"""Stage/preflight rotor-only detail; canonical writes require explicit --apply."""
from pathlib import Path
import argparse,copy,hashlib,importlib.util,json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,numpy as np,trimesh
import distributor_center_contact_integration as adapter
from assembly_math import transforms
STAGE=ROOT/'cad/engine/generated/distributor-center-contact-integration-stage'
RECORD=ROOT/'inventory/engine/distributor-center-contact-installation.json'
PROOF=ROOT/'inventory/engine/distributor-center-contact-candidate-validation.json'
CHECKER=ROOT/'scripts/check-distributor-center-contact-installed.py'
HELPER=ROOT/'scripts/install-intake-cap-coordination.py'
SOURCES=[Path(__file__),CHECKER,ROOT/'cad/engine/distributor_center_contact_candidate.py',ROOT/'cad/engine/distributor_center_contact_integration.py',ROOT/'reference/engine/distributor-center-contact-review.json',ROOT/'inventory/engine/distributor-center-contact-learning.json',ROOT/'cad/engine/assembly_math.py',ROOT/'scripts/check-distributor-center-contact-candidate.py']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def load_module(path,name):
 spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def scope(m):
 occ=[o for o in m['occurrences'] if o['parent'] in ('distributor-assembly','distributor-rotation')]
 ids={o['definition'] for o in occ};groups={a['id']:a for a in m['assemblies']};parents={o['parent'] for o in occ}
 for parent in list(parents):
  while parent in groups:
   parents.add(parent);parent=groups[parent].get('parent')
 return dict(definitions={d['id']:d for d in m['definitions'] if d['id'] in ids},occurrences={o['id']:o for o in occ},assemblies={k:groups[k] for k in parents if k in groups},source=m['sources'].get(adapter.SOURCE))
def scene_frames(m):
 return dict(assemblies=m['assemblies'],mechanism=m['mechanism'],occurrences={o['id']:{k:o.get(k) for k in ('definition','parent','position_cad_mm','rotation_cad_deg','motion','valvetrain')} for o in m['occurrences']})
def artifacts():
 return {str(Path('cad/engine/generated')/(i+'.step')):STAGE/'step'/(i+'.step') for i in adapter.IDS}|{str(Path('models/engine')/(i+'.glb')):STAGE/'models'/(i+'.glb') for i in adapter.IDS}
def stage():
 import full_engine as engine
 source_before={str(p.relative_to(ROOT)):sha(p) for p in SOURCES};proof_hash=sha(PROOF)
 proof=read(PROOF);assert proof['status'].startswith('PASS') and proof['input_guard_pass']
 for p,h in proof['input_sha256_after'].items():assert sha(ROOT/p)==h,'Candidate context changed: '+p
 path=ROOT/'inventory/engine/full-assembly.json';raw=path.read_bytes();m=json.loads(raw);before=copy.deepcopy(m);defs={d['id']:d for d in m['definitions']}
 STAGE.mkdir(exist_ok=True);engine.STEP=STAGE/'step';engine.OUT=STAGE/'models';engine.STEP.mkdir(exist_ok=True);engine.OUT.mkdir(exist_ok=True)
 engine.defs[:]=m['definitions'];engine.occurrences[:]=m['occurrences'];engine.assemblies[:]=m['assemblies'];engine.shapes.clear()
 change=adapter.install(engine.define,engine.add,engine.group,engine.defs,engine.occurrences,engine.assemblies,engine.shapes)
 m.update(definitions=engine.defs,occurrences=engine.occurrences,assemblies=engine.assemblies);m['sources'].update(adapter.sources())
 for kind in ('definitions','occurrences'):
  assert {r['id']:r for r in before[kind] if r['id'] not in adapter.IDS}=={r['id']:r for r in m[kind] if r['id'] not in adapter.IDS}
 assert before['assemblies']==m['assemblies']
 for oid in adapter.REPLACED:
  a=next(o for o in before['occurrences'] if o['id']==oid);z=next(o for o in m['occurrences'] if o['id']==oid)
  for key in ('id','definition','parent','position_cad_mm','rotation_cad_deg','explode_cad_mm'):assert a[key]==z[key]
 # Current whole-assembly static audit; native/posed shapes are STEP baked
 # before boolean contact tests. Small added leaf stays inside unchanged cap.
 poses=transforms(m);bounds={};tracked={};pairs=[];excluded=0
 def track(p):
  rel=str(p.relative_to(ROOT));tracked.setdefault(rel,sha(p));return p
 def baked(shape,ident):
  folder=STAGE/'baked';folder.mkdir(exist_ok=True);p=folder/(ident+'.step');b.export_step(shape,p);return b.import_step(p)
 changed={i:baked(poses[i]*b.import_step(engine.STEP/(i+'.step')),i) for i in adapter.IDS}
 old={i:baked(poses[i]*b.import_step(track(ROOT/defs[i]['step'].lstrip('/'))),'baseline-'+i) for i in adapter.REPLACED}
 for o in m['occurrences']:
  if o['id'] in adapter.IDS:continue
  d=defs[o['definition']];gp=track(ROOT/d['glb'].lstrip('/'))
  if d['id'] not in bounds:
   a=np.asarray(trimesh.load(gp,force='mesh').vertices);xyz=a[:,[0,2,1]]*np.array([1,-1,1])*1000;bounds[d['id']]=(xyz.min(0)-.2,xyz.max(0)+.2)
  lo,hi=bounds[d['id']];corners=np.array([tuple(b.Vertex(x,y,z).moved(poses[o['id']]).center()) for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])]);lo,hi=corners.min(0),corners.max(0)
  neighbor=None
  for i,a in changed.items():
   box=a.bounding_box();alo=np.array(tuple(box.min));ahi=np.array(tuple(box.max))
   if np.any(ahi<lo) or np.any(hi<alo):excluded+=1;continue
   if neighbor is None:neighbor=baked(poses[o['id']]*b.import_step(track(ROOT/d['step'].lstrip('/'))),o['id'])
   v=adapter.volume(a&neighbor);prior=adapter.volume(old[i]&neighbor) if i in old and v>.1 else 0.
   pairs.append(dict(actor=i,neighbor=o['id'],overlap_mm3=v,baseline_overlap_mm3=prior,new_or_worsened=v>prior+.1))
 assert not any(p['new_or_worsened'] for p in pairs),[p for p in pairs if p['new_or_worsened']]
 assert path.read_bytes()==raw and all(sha(ROOT/p)==h for p,h in tracked.items()),'Canonical inputs changed'
 assert source_before=={str(p.relative_to(ROOT)):sha(p) for p in SOURCES} and sha(PROOF)==proof_hash,'Stage source changed during audit'
 (STAGE/'full-assembly.json').write_text(json.dumps(m,indent=2)+'\n')
 record=dict(status='STAGED rotor-only detail; not installed',before_manifest_sha256=hashlib.sha256(raw).hexdigest(),staged_manifest_sha256=sha(STAGE/'full-assembly.json'),candidate_report_sha256=sha(PROOF),source_sha256=source_before,transaction_helper_sha256=sha(HELPER),exporter_at_stage_sha256=sha(ROOT/'cad/engine/full_engine.py'),installed_scope=scope(m),scene_frames=scene_frames(m),before_scope=scope(before),neighbor_sha256=tracked,staged_artifact_sha256={str(p.relative_to(STAGE)):sha(p) for p in artifacts().values()},canonical_artifact_sha256={p:sha(v) for p,v in artifacts().items()},static=dict(exact_pairs=len(pairs),aabb_excluded=excluded,pairs=pairs),**change)
 (STAGE/'installation.json').write_text(json.dumps(record,indent=2)+'\n')
 result=load_module(CHECKER,'rotor_stage_checker').validate(False,STAGE)
 (STAGE/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'static':record['static'],'replay':result['replay']},indent=2))

def preflight():
 record=read(STAGE/'installation.json');validation=read(STAGE/'validation.json');assert validation['status'].startswith('PASS')
 assert sha(ROOT/'inventory/engine/full-assembly.json')==record['before_manifest_sha256'],'Canonical manifest changed since stage'
 assert sha(PROOF)==record['candidate_report_sha256'] and sha(HELPER)==record['transaction_helper_sha256']
 for p,h in record['source_sha256'].items():assert sha(ROOT/p)==h,'Stage source changed: '+p
 for p,h in record['neighbor_sha256'].items():assert sha(ROOT/p)==h,'Stage neighbor changed: '+p
 for p,h in record['staged_artifact_sha256'].items():assert sha(STAGE/p)==h,'Stage artifact changed: '+p
 assert sha(STAGE/'full-assembly.json')==record['staged_manifest_sha256']
 assert validation['installation_record_sha256']==sha(STAGE/'installation.json')
 return record

def main():
 p=argparse.ArgumentParser(description=__doc__);g=p.add_mutually_exclusive_group();g.add_argument('--stage',action='store_true');g.add_argument('--apply',action='store_true');g.add_argument('--check-installed',action='store_true');args=p.parse_args()
 if args.stage:stage();return
 if args.check_installed:
  result=load_module(CHECKER,'rotor_installed_checker').validate(True,STAGE);(ROOT/'inventory/engine/distributor-center-contact-installed-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));return
 record=preflight()
 if not args.apply:print('PASS rotor-only promotion preflight; no writes');return
 writes={ROOT/k:v.read_bytes() for k,v in artifacts().items()};writes[ROOT/'inventory/engine/full-assembly.json']=(STAGE/'full-assembly.json').read_bytes();writes[RECORD]=(STAGE/'installation.json').read_bytes()
 output=ROOT/'inventory/engine/distributor-center-contact-installed-validation.json';writes[output]=b'';result={}
 helper=load_module(HELPER,'rotor_transaction_helper')
 def postcheck():
  result.update(load_module(CHECKER,'rotor_applied_checker').validate(True,STAGE));helper.replace(output,(json.dumps(result,indent=2)+'\n').encode())
 preflight();helper.promote(writes,postcheck);print(result['status'])
if __name__=='__main__':main()
