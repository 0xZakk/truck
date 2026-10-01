#!/usr/bin/env python3
import json,hashlib,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
reportnames=['build-validation','mesh-validation','neighbor-validation','render'];reports={n:json.loads((ROOT/f'inventory/engine/shifted-ignition-lead-{n}.json').read_text()) for n in reportnames};bindings={}
for n,r in reports.items():
 p=ROOT/f'inventory/engine/shifted-ignition-lead-{n}.json';bindings[str(p.relative_to(ROOT))]=sha(p)
 for path,h in r['inputs'].items():assert sha(ROOT/path)==h,path
assert len(reports['mesh-validation']['parts'])==28
assert not reports['neighbor-validation']['conflicts']
mp=ROOT/'inventory/engine/corrected-engine-stage-v2.json';assert sha(mp)=='9b8253b318e800e18b999a0a74caa749d9525978f2c19bc7286c07bb79a7c100';m=json.loads(mp.read_text());defs={x['id']:x for x in m['definitions']};occ={x['id']:x for x in m['occurrences']};proposal={'manifest_sha256':sha(mp),'definitions':[],'occurrences':[],'limits':['Uninstalled candidate. World-aligned original definition frames, millimetre STEP and metre GLTF with existing axis conversion. All occurrence transforms unchanged; connector shift is baked in assets.','Routes and connector dimensions remain estimated. Static q0/axial0 neighbor audit only. Coplanar Boolean replay and fixed-tail subtraction are untrusted; separately scoped source/curve identity and actual boundary probes retained.']}
for row in reports['mesh-validation']['parts']:
 ident=row['id'];old=defs[ident];new=copy.deepcopy(old);sp='cad/engine/generated/shifted-ignition-lead-candidate/'+ident+'.step';gp=row['artifact'];assert sha(ROOT/gp)==row['sha256'];new['step']='/'+sp;new['glb']='/'+gp;new['triangle_count']=row['triangles'];new['unresolved']=old.get('unresolved',[])+proposal['limits'];new.pop('volume_mm3',None);new.pop('model_bounds_mm',None)
 proposal['definitions'].append({'id':ident,'before':old,'after':new,'copy_assets':{'step':{'from':sp,'sha256':sha(ROOT/sp)},'glb':{'from':gp,'sha256':sha(ROOT/gp)}}});proposal['occurrences'].append({'id':ident,'before':occ[ident],'after':occ[ident]});bindings[sp]=sha(ROOT/sp);bindings[gp]=sha(ROOT/gp)
p=ROOT/'inventory/engine/shifted-ignition-lead-integration-proposal.json';p.write_text(json.dumps(proposal,indent=2)+'\n');bindings[str(p.relative_to(ROOT))]=sha(p)
for pattern in ['scripts/*shifted-ignition-lead*.py','cad/engine/shifted_ignition_lead_candidate.py','docs/components/shifted-ignition-lead-candidate.md','inventory/engine/shifted-ignition-lead-*failure.json','inventory/engine/shifted-ignition-lead-source-replay-diagnostic.json']:
 for p in ROOT.glob(pattern):bindings[str(p.relative_to(ROOT))]=sha(p)
r=reports['render'];assert sha(ROOT/r['image'])==r['sha256'];bindings[r['image']]=r['sha256'];n=reports['neighbor-validation'];out={'status':'PASS scoped uninstalled candidate; root replay and browser pending','bindings':bindings,'scope':{'definitions':28,'stable_occurrences_unchanged':28,'fixed_opposite_end_definitions_unchanged':14,'exact_static_pairs':len(n['exact_checks']),'bounds_separated_pairs':n['bounds_separated'],'positive_overlap_pairs':len(n['conflicts']),'meshes_watertight_winding_positive':28},'limitations':proposal['limits']};p=ROOT/'inventory/engine/shifted-ignition-lead-delivery.json';p.write_text(json.dumps(out,indent=2)+'\n');print(sha(p))
