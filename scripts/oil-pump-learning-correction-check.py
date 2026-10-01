"""Validate an in-memory lesson patch; never write installed learning or viewer files."""
from pathlib import Path
import copy,hashlib,json
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=R/'inventory/engine/oil-pump-learning-correction-candidate.json';c=json.loads(p.read_text());src=R/c['target'];assert sha(src)==c['target_sha256'],'Stale installed lesson input'
old=json.loads(src.read_text());new=copy.deepcopy(old)
for op in c['changes']:
 cursor=new
 for key in op['path'][:-1]:cursor=cursor[key]
 assert cursor[op['path'][-1]]==op['before'],op['path']
 cursor[op['path'][-1]]=op['after']
m=json.loads((R/'inventory/engine/full-assembly.json').read_text());ids={x['id']for k in ['definitions','assemblies','occurrences']for x in m[k]};sources=m['sources'];changed=sorted({x['path'][0]for x in c['changes']});checks={}
for k in changed:
 a,b=old[k],new[k];assert a.keys()==b.keys()
 oldtargets=[x.get('part')for group in ['steps','troubleshooting']for x in a[group]];newtargets=[x.get('part')for group in ['steps','troubleshooting']for x in b[group]];assert oldtargets==newtargets
 for target in newtargets:
  if target is not None:assert target in ids,target
 for sid in b['sources']:assert sid in sources,sid
 checks[k]={'stable_part_targets':True,'all_source_ids_resolve':True,'part_targets':newtargets,'sources':b['sources']}
for sid in ['ford-industrial-parts','ford-industrial-csg649']:
 record=sources[sid];assert sha(R/record['path'])==record['sha256'],sid
assert old['oil-pump-assembly']['steps'][0]==new['oil-pump-assembly']['steps'][0],'Gerotor explanation changed'
assert old['oil-pump-assembly']['troubleshooting']==new['oil-pump-assembly']['troubleshooting'],'Service limits changed'
inputs=[src,p,R/'inventory/engine/full-assembly.json',Path(__file__),*[R/q for q in c['evidence_files']]]
r={'status':'PASS scoped textual patch; integration/browser NOT RUN','changes':len(c['changes']),'lesson_checks':checks,'gerotor_profile_and_speed_limits_preserved':True,'service_clearance_and_relief_calibration_limits_preserved':True,'all_other_lessons_unchanged':all(new[k]==v for k,v in old.items()if k not in changed),'inputs':{str(q.relative_to(R)):sha(q)for q in inputs},'rendering':'NOT RUN; no canonical/viewer edits','source_links':'Existing stable source IDs resolved against canonical registry; no live URL availability claim'}
(R/'inventory/engine/oil-pump-learning-correction-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items()if k not in ['inputs','lesson_checks']},indent=2))
