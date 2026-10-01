#!/usr/bin/env python3
"""Bind completed candidate reports to current sources and transitive CAD imports."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import timing_rocker_crest_candidate
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
reports=[ROOT/'inventory/engine'/name for name in ['timing-rocker-crest-candidate-validation.json','timing-rocker-crest-neighbors-validation.json','timing-rocker-crest-render-validation.json','timing-rocker-crest-springs-validation.json']]
rows={}
for p in reports:
 r=json.loads(p.read_text());status=r.get('status','')
 assert status not in ['RUNNING'] and not status.startswith('FAIL'),(p,status)
 for key in ['inputs','input_sha256']:
  for name,h in r.get(key,{}).items():assert sha(ROOT/name)==h,(p,name)
 rows[str(p.relative_to(ROOT))]={'sha256':sha(p),'status':status}
sources={}
for module in tuple(sys.modules.values()):
 if not getattr(module,'__file__',None):continue
 p=Path(module.__file__).resolve()
 if p.is_relative_to(ROOT/'cad/engine') and p.is_file():sources[str(p.relative_to(ROOT))]=sha(p)
files=list((ROOT/'cad/engine/generated/timing-rocker-crest-candidate').glob('*.step'))+list((ROOT/'cad/engine/generated/timing-rocker-crest-candidate').glob('*.glb'))+list((ROOT/'cad/engine/generated/timing-rocker-crest-candidate').glob('*.png'))
r={'status':'PASS completed scoped evidence binding; UNINSTALLED CANDIDATE','reports':rows,'transitive_local_cad_source_sha256':sources,'artifact_sha256':{str(p.relative_to(ROOT)):sha(p) for p in files},'checker_sha256':sha(Path(__file__)),'source_review_sha256':sha(ROOT/'reference/engine/timing-rocker-crest-source-review.json'),'remaining':['120 target-branch poses and60 spring seat levels pass; continuous full-neighbor motion and staged disassembly NOT RUN.','6mm rocker crest is an estimated solid-profile hypothesis; production shape, structural capacity and true thread engagement unresolved.','Cover and all previous inclined candidate parts remain frozen; only rocker crest changed.','Browser acceptance NOT RUN; no installation or Done claim.']}
(ROOT/'inventory/engine/timing-rocker-crest-delivery-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
