#!/usr/bin/env python3
"""Bind isolated cam reports, exact artifacts and transitive local source snapshot."""
from pathlib import Path
import ast,json,hashlib,subprocess
ROOT=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
reports={};artifacts={};watched={}
for kind in ['build','contact','section','linkage']:
 p=ROOT/f'inventory/engine/cam-clockwise-candidate-{kind}-validation.json';r=json.loads(p.read_text());assert r['status'].startswith('PASS')
 reports[str(p.relative_to(ROOT))]=sha(p)
 for name,h in r['inputs'].items():assert sha(ROOT/name)==h,name;watched[name]=h
 if kind=='build':
  for name,h in r['exports'].items():assert sha(ROOT/name)==h,name;artifacts[name]=h
 if kind=='contact':
  assert r['build_report_sha256']==sha(ROOT/'inventory/engine/cam-clockwise-candidate-build-validation.json')
  m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());d=next(d for d in m['definitions'] if d['id']=='lifter-body');p=ROOT/d['step'].lstrip('/');assert sha(p)==r['lifter_sha256'];artifacts[str(p.relative_to(ROOT))]=sha(p)
prior=json.loads((ROOT/'inventory/engine/timing-coupled-core-candidate-validation.json').read_text())
p=ROOT/'cad/engine/generated/timing-coupled-core-candidate/camshaft.step';assert sha(p)==prior['exports']['camshaft']['step_sha256'];artifacts[str(p.relative_to(ROOT))]=sha(p)
# Discover transitive CAD imports without executing them. Dependencies omitted from
# the build watch must still be byte-identical to the pre-task baseline commit.
queue=['cam_clockwise_candidate'];seen=set();transitive={};baseline_checks={}
while queue:
 n=queue.pop();p=ROOT/'cad/engine'/(n+'.py')
 if n in seen or not p.exists():continue
 seen.add(n);name=str(p.relative_to(ROOT));transitive[name]=sha(p)
 if name not in watched:
  content=subprocess.check_output(['git','show','dafb817:'+name],cwd=ROOT)
  h=hashlib.sha256(content).hexdigest();assert h==sha(p),name;baseline_checks[name]=h
 for item in ast.walk(ast.parse(p.read_text())):
  if isinstance(item,ast.Import):queue.extend(a.name.split('.')[0] for a in item.names)
  elif isinstance(item,ast.ImportFrom) and item.module:queue.append(item.module.split('.')[0])
for name in ['cad/engine/generated/cam-clockwise-candidate/cam-clockwise-mesh-section.png','cad/engine/generated/cam-clockwise-candidate/cam-clockwise-review.png','scripts/render-cam-clockwise-candidate.py','docs/components/cam-clockwise-candidate.md','inventory/engine/cam-clockwise-coplanar-probe-diagnostic.json']:
 artifacts[name]=sha(ROOT/name)
r=dict(status='PASS bounded cam candidate binding; uninstalled',baseline='dafb817',reports=reports,artifacts=artifacts,transitive_source_sha256=transitive,unwatched_dependencies_verified_unchanged_from_baseline=baseline_checks,checker_sha256=sha(Path(__file__)),limits=['No continuous angular whole-neighbor collision proof','Crossed distributor/oil-drive geometry preserved but compatible corrected handedness unsupported','Actual source replay and lobe phase sections are sampled boundary comparisons; unreliable changed-volume metric retained untrusted','Root owns integration, corrected crank pairing and browser acceptance'])
(ROOT/'inventory/engine/cam-clockwise-candidate-delivery-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
