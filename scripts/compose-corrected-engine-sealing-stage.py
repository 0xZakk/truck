"""Compose sealing dependencies into a new manifest; preserve audited stage v1."""
from pathlib import Path
import json,hashlib,copy
R=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
B=R/'inventory/engine/corrected-engine-stage.json';canonical=R/'inventory/engine/full-assembly.json';m=json.loads(B.read_text());inputs={str(B.relative_to(R)):sha(B),str(canonical.relative_to(R)):sha(canonical),str(Path(__file__).relative_to(R)):sha(Path(__file__))};before=sha(B)
def resolve_records(value):
 if set(value)=={'path','sha256'}:
  assert sha(R/value['path'])==value['sha256'];inputs[value['path']]=value['sha256'];return json.loads((R/value['path']).read_text())
 return value
learning={};new_sources={};aliases={};changed=set();counts={g:0 for g in ['definitions','assemblies','occurrences']}
for name in ['front-seal-2692-composition-patch','timing-front-sealing-patch']:
 path=R/'inventory/engine'/f'{name}.json';p=json.loads(path.read_text());inputs[str(path.relative_to(R))]=sha(path);assert p['manifest_sha256']==sha(canonical)
 for group in counts:
  items={x['id']:x for x in m[group]}
  for row in p.get(group,[]):
   key=(group,row['id']);assert key not in changed;changed.add(key)
   assert items.get(row['id'])==row['before'],key
   after=copy.deepcopy(row['after'])
   if after is None:m[group]=[x for x in m[group]if x['id']!=row['id']]
   else:
    for kind,asset in row.get('copy_assets',{}).items():
     assert sha(R/asset['from'])==asset['sha256'];inputs[asset['from']]=asset['sha256'];after[kind]='/'+asset['from']
    if row['before'] is None:m[group].append(after)
    else:items[row['id']].clear();items[row['id']].update(after)
   counts[group]+=1
 if 'main_screw_source_enrichment'in p:
  row=p['main_screw_source_enrichment'];d=next(d for d in m['definitions']if d['id']==row['id']);compare=copy.deepcopy(d)
  for k in ['step','glb']:compare[k]=row['before'][k]
  assert compare==row['before']
  d['sources']=list(dict.fromkeys(d.get('sources',[])+row['append_sources']))
 for key,value in resolve_records(p.get('learning_additions',p.get('learning',{}))).items():assert key not in learning;learning[key]=value
 for key,value in resolve_records(p.get('source_additions',p.get('sources',{}))).items():
  assert key not in new_sources or new_sources[key]==value;new_sources[key]=value
 aliases.update(p.get('navigation_aliases',{}))
# Preserve original registry layout; source identities may only agree or be new.
assert isinstance(m['sources'],dict)
for key,value in new_sources.items():
 assert key not in m['sources'] or m['sources'][key]==value,key
 m['sources'][key]=value
m['integration_stage']['learning_additions']=learning;m['integration_stage']['navigation_aliases']=aliases
m['integration_stage']['patches']+=['front-seal-2692-composition-patch','timing-front-sealing-patch']
m['integration_stage']['open']=[x for x in m['integration_stage']['open']if x not in ['Main cover gasket and terminal sealant dependency','2692 case/elastomer/spring and hub replacement dependency']]
m['integration_stage']['open']+=['Fresh v1 audit reports cover/water-pump/support/FS10 and shifted ignition-lead conflicts; v2 requires scoped recheck']
for group in counts:assert len({x['id']for x in m[group]})==len(m[group])
D={x['id']for x in m['definitions']};A={x['id']for x in m['assemblies']};O={x['id']for x in m['occurrences']}
assert 'front-seal'not in D|O and aliases['front-seal']=='front-seal-assembly'
assert all(o['parent']in A and o['definition']in D for o in m['occurrences'])
assert all(key in O|A for key in learning)
assert all(src in m['sources']for lesson in learning.values()for src in lesson.get('sources',[]))
assert sha(B)==before
out=R/'inventory/engine/corrected-engine-stage-v2.json';out.write_text(json.dumps(m,indent=2)+'\n')
report={'status':'PASS isolated sealing composition; broad assembly failures remain','definitions':len(D),'occurrences':len(O),'new_lessons':len(learning),'new_sources':len(new_sources),'applied_rows':counts,'bindings':inputs,'stage_sha256':sha(out),'v1_manifest_unchanged':sha(B)==before,'canonical_modified':False,'open':m['integration_stage']['open']}
(R/'inventory/engine/corrected-engine-stage-v2-composition.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items()if k!='bindings'})
