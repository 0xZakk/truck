#!/usr/bin/env python3
"""Baseline equivalence prerequisite only. Never writes canonical artifacts."""
from pathlib import Path
import sys,json,hashlib,time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import timing_block_migration_candidate as c
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-block-migration-candidate';OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
mp=ROOT/'inventory/engine/full-assembly.json';raw=mp.read_bytes();m=json.loads(raw);record=next(x for x in m['definitions'] if x['id']=='block');installed=ROOT/record['step'].lstrip('/')
protected={str(mp.relative_to(ROOT)):sha(mp),str(installed.relative_to(ROOT)):sha(installed)}
initial={str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'cad/engine').glob('*.py')}
initial['inventory/engine/dimensions.json']=sha(ROOT/'inventory/engine/dimensions.json');initial[str(Path(__file__).relative_to(ROOT))]=sha(Path(__file__))
stages=[]
def stage(name,q):
 print(name,'valid',q.is_valid,'solids',len(q.solids()),flush=True)
 sp=OUT/(name+'.step');b.export_step(q,sp)
 stages.append({'stage':name,'valid':q.is_valid,'solids':len(q.solids()),'step':str(sp.relative_to(ROOT)),'sha256':sha(sp)})
 (OUT/'baseline-progress.json').write_text(json.dumps(stages,indent=2)+'\n')
print('Regenerating only block definition and ordered block hooks',flush=True)
start=time.monotonic();regenerated=c.baseline(stage);base=b.import_step(installed)
print('Computing exact symmetric differences',flush=True)
extra=regenerated.cut(base);missing=base.cut(regenerated)
errors={'regenerated_extra_mm3':vol(extra),'regenerated_missing_mm3':vol(missing)}
for name,shape in [('extra',extra),('missing',missing)]:
 if shape and shape.solids():b.export_step(b.Compound(children=list(shape.solids())),OUT/('baseline-'+name+'.step'))
loaded={}
for module in list(sys.modules.values()):
 path=getattr(module,'__file__',None)
 if path:
  path=Path(path).resolve()
  if path.suffix=='.py' and path.parent==ROOT/'cad/engine':
   rel=str(path.relative_to(ROOT));assert sha(path)==initial[rel],rel;loaded[rel]=initial[rel]
assert protected=={p:sha(ROOT/p) for p in protected},'Canonical inputs changed during baseline check'
r={'status':'PASS exact baseline regeneration' if max(errors.values())<1e-5 else 'MISMATCH baseline regeneration; migration prohibited pending explanation','baseline_commit':'705c4683c199d8c5e28addba018bc8d1bdd399b1','manifest_sha256':hashlib.sha256(raw).hexdigest(),'canonical_inputs_sha256':protected,'source_modules_sha256':loaded,'checker_sha256':sha(Path(__file__)),'dimensions_sha256':initial['inventory/engine/dimensions.json'],'stages':stages,'symmetric_difference':errors,'valid':regenerated.is_valid,'solids':len(regenerated.solids()),'elapsed_seconds':time.monotonic()-start,'limits':['Baseline reconstruction prerequisite only; no migrated block built','No old tunnel filling, no canonical writes','Source hashes include imported builder dependencies, not a claim that every imported feature changes the block']}
(ROOT/'inventory/engine/timing-block-baseline-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:r[k] for k in ['status','symmetric_difference','elapsed_seconds']},indent=2),flush=True)
