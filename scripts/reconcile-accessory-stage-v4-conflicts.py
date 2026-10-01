"""Reclassify known v3 static conflicts against the scoped v4 audit, not full acceptance."""
import hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=['inventory/engine/corrected-stage-v3-remaining-conflicts.json','inventory/engine/accessory-stage-v4-solids.json','inventory/engine/accessory-stage-v4-composition.json','inventory/engine/corrected-engine-stage-v3.json','inventory/engine/corrected-engine-stage-v4.json']
old,audit,composition,v3,v4=[json.loads((R/p).read_text()) for p in paths]
assert audit['status']=='PASS bounded affected-solid q0 only'
assert audit['stage_sha256']==composition['stage_sha256']==sha(R/paths[-1])
for p,h in audit['input_sha256'].items():assert sha(R/p)==h,p
ids=set(audit['affected_occurrences']);checks={frozenset([r['a'],r['b']]):r for r in audit['exact_checks']}
resolved=[];inherited=[]
for row in old['remaining_known_pairs']:
 pair=frozenset([row['a'],row['b']])
 if pair&ids:
  if pair in checks:
   result=checks[pair];assert result['overlap_mm3']<=.1 and 'error' not in result
   proof={'kind':'fresh exact pair','overlap_mm3':result['overlap_mm3']}
  else:
   x,y=[audit['bounds'][n] for n in [row['a'],row['b']]]
   gaps=[max(x[0][i]-y[1][i],y[0][i]-x[1][i]) for i in range(3)]
   assert max(gaps)>2
   proof={'kind':'actual posed STEP AABB separation','axis_gaps_mm':gaps}
  resolved.append({'prior':row,'v4_evidence':proof})
 else:
  for n in pair:
   o3=next(x for x in v3['occurrences'] if x['id']==n);o4=next(x for x in v4['occurrences'] if x['id']==n)
   assert o3==o4
   assert next(x for x in v3['definitions'] if x['id']==o3['definition'])==next(x for x in v4['definitions'] if x['id']==o4['definition'])
  inherited.append(row)
report={'status':'Known static baseline reconciled; not whole-engine acceptance','superseded_known_pairs':resolved,'remaining_known_pairs':inherited,'remaining_count':len(inherited),'input_sha256':{p:sha(R/p) for p in paths}|{str(Path(__file__).relative_to(R)):sha(Path(__file__))},'limits':['Four unchanged baseline pairs are inherited findings, not new Boolean measurements','Only q0 affected-pair coverage; rod motion and tool-access failures remain','Source fidelity, complete BOM, belt/hoses and browser acceptance unresolved']}
(R/'inventory/engine/accessory-stage-v4-remaining-conflicts.json').write_text(json.dumps(report,indent=2)+'\n')
print('Superseded',len(resolved),'known q0 conflicts; inherited',len(inherited),inherited)
