"""Compose disjoint proposals into a private, explicitly incomplete manifest."""
from pathlib import Path
import json,hashlib,copy
R=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base=R/'inventory/engine/full-assembly.json';m=json.loads(base.read_text());before=sha(base)
names=['timing-core-integration-patch','timing-corrected-slider-neutral-patch','timing-conditional-drive-integration-patch','timing-front-coordinated-patch','clockwise-linkage-pose-patch','clockwise-linkage-asset-patch']
seen=set();inputs={str(base.relative_to(R)):before};assets={};counts={k:0 for k in ['definitions','assemblies','occurrences']}
for name in names:
 path=R/'inventory/engine'/f'{name}.json';p=json.loads(path.read_text());inputs[str(path.relative_to(R))]=sha(path);assert p['manifest_sha256']==before
 for group in counts:
  lookup={x['id']:x for x in m[group]}
  for row in p.get(group,[]):
   key=(group,row['id']);assert key not in seen,('conflicting proposal',key);seen.add(key)
   assert lookup.get(row['id'])==row['before'],('stale before',key)
   if row['before'] is None:m[group].append(copy.deepcopy(row['after']))
   else:lookup[row['id']].clear();lookup[row['id']].update(copy.deepcopy(row['after']))
   counts[group]+=1
   for kind,asset in row.get('copy_assets',{}).items():
    assert sha(R/asset['from'])==asset['sha256'];inputs[asset['from']]=asset['sha256'];assets[row['id'],kind]=asset['from']
for d in m['definitions']:
 for kind in ['step','glb']:
  if (d['id'],kind) in assets:d[kind]='/'+assets[d['id'],kind]
m['motion_revision']='clockwise-inclined-v1';m['status']='INCOMPLETE INTEGRATION STAGE — known collisions and missing connections; not accepted engine'
m['integration_stage']={'canonical_modified':False,'patches':names,'open':['Inherited rod-bolt/block interference','Shifted pump pickup connection and missing pump gasket/discharge joint','Main cover gasket and terminal sealant dependency','2692 case/elastomer/spring and hub replacement dependency','Full assembly collision/motion and browser acceptance'],'purpose':'Private reproducible composition, never silently substitute for canonical manifest'}
for group in counts:assert len({x['id']for x in m[group]})==len(m[group])
assembly_ids={x['id']for x in m['assemblies']};definition_ids={x['id']for x in m['definitions']}
assert all(o['parent']in assembly_ids and o['definition']in definition_ids for o in m['occurrences'])
assert sha(base)==before
out=R/'inventory/engine/corrected-engine-stage.json';out.write_text(json.dumps(m,indent=2)+'\n')
report={'status':'PASS disjoint proposal composition; incomplete stage','definitions':len(m['definitions']),'occurrences':len(m['occurrences']),'applied_rows':counts,'stage_sha256':sha(out),'canonical_modified':False,'bindings':inputs,'open':m['integration_stage']['open']}
(R/'inventory/engine/corrected-engine-stage-composition.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='bindings'}))
