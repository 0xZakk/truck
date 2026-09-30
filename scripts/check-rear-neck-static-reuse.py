"""Bind unchanged static evidence and a fresh changed-part scan; no new global sweep."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads((ROOT/p).read_text())
old='cad/engine/generated/exhaust-timing-checkpoint/'
stage='cad/engine/generated/rear-exhaust-neck-integration-stage/'
paths=[old+'atlas-static-validation.json',old+'combined-step-export.json',stage+'before.json',stage+'full-assembly.json',stage+'installation.json','inventory/engine/rear-exhaust-neck-installed-validation.json','inventory/engine/full-assembly.json']
inputs={p:sha(ROOT/p) for p in paths}
before=read(stage+'before.json');now=read('inventory/engine/full-assembly.json');audit=read(old+'atlas-static-validation.json');combined=read(old+'combined-step-export.json');installed=read('inventory/engine/rear-exhaust-neck-installed-validation.json');record=read(stage+'installation.json')
assert audit['manifest_sha256']==combined['manifest_sha256']==inputs[stage+'before.json']
assert audit['collisions']==[] and audit['checked_poses_deg']==[0]
assert installed['manifest_sha256']==inputs['inventory/engine/full-assembly.json']==inputs[stage+'full-assembly.json']
assert installed['installation_sha256']==inputs[stage+'installation.json']
for key in ['definitions','occurrences']:
 assert {d['id']:d for d in before[key] if d['id']!='exhaust-rear'}=={d['id']:d for d in now[key] if d['id']!='exhaust-rear'}
assert before['assemblies']==now['assemblies'] and before['mechanism']==now['mechanism']
a=next(o for o in before['occurrences'] if o['id']=='exhaust-rear');z=next(o for o in now['occurrences'] if o['id']=='exhaust-rear')
assert {k:v for k,v in a.items() if k not in ['name','function']}=={k:v for k,v in z.items() if k not in ['name','function']}
unchanged={p:h for p,h in combined['part_step_hashes'].items() if p!='cad/engine/generated/exhaust-rear.step'}
assert all(sha(ROOT/p)==h for p,h in unchanged.items())
assert all(sha(ROOT/p)==h for p,h in combined['export_dependency_hashes'].items())
assert all(sha(ROOT/p)==h for p,h in installed['context']['artifact_sha256'].items())
assert all(sha(ROOT/p)==h for p,h in record['input_sha256'].items())
for suffix,directory in [('step','cad/engine/generated'),('glb','models/engine')]:
 key=('step/' if suffix=='step' else 'models/')+'exhaust-rear.'+suffix
 assert sha(ROOT/directory/('exhaust-rear.'+suffix))==record['staged_artifact_sha256'][key]
checks=installed['context']['exact_checks'];assert checks and all(row['overlap_mm3']<=.1 for row in checks)
report=dict(status='PASS unchanged static evidence plus fresh rear-neighbor scan',manifest_sha256=inputs['inventory/engine/full-assembly.json'],input_sha256=inputs,unchanged_step_definitions=len(unchanged),fresh_rear_exact_comparisons=len(checks),fresh_max_overlap_mm3=max(r['overlap_mm3'] for r in checks),prior_global_exact_comparisons=audit['exact_intersection_checks'],scope='Prior static audit is retained for byte-identical unchanged STEP shapes, identical assembly/occurrence/mechanism frames. Fresh installed scan covers every potentially affected rear-manifold neighbor. Not a newly executed whole-engine audit or continuous motion test.',limits=['Browser NOT RUN. Factory fidelity and full clean rebuild unproven.','The historical global report remains keyed to its original manifest; this report documents only justified reuse and changed-part checks.'])
assert all(sha(ROOT/p)==h for p,h in inputs.items())
(ROOT/'inventory/engine/rear-neck-static-reuse.json').write_text(json.dumps(report,indent=2)+'\n')
print(report['status'])
