"""Independent coverage/provenance audit; not a repeat of CAD collision Booleans."""
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
P=R/'reference/engine/valve-spring-reconciliation-20261003'
f=Path(str(P)+'-v4-context.json');d=json.loads(f.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name,h in d['input_sha256'].items():
    assert sha(R/name)==h,name
m=json.loads((R/'inventory/engine/corrected-engine-stage-v4.json').read_text())
neighbor_defs={'cylinder-head','valve-cover','rocker-arm','rocker-fulcrum','rocker-bolt','spring-retainer','valve-keeper','valve-seal','intake-valve','exhaust-valve'}
expected_neighbors={o['id'] for o in m['occurrences'] if o['definition'] in neighbor_defs}
expected_springs={f'c{i}-{k}-spring' for i in range(1,7) for k in ('intake','exhaust')}
expected_states={(s,state) for s in expected_springs for state in ('closed','peak')}
actual=[(r['target'],r['state']) for r in d['states']]
assert len(actual)==24 and len(set(actual))==24 and set(actual)==expected_states
assert not d['conflicts'] and not d['errors']
rows=[]
for r in d['states']:
    exact=r['exact_neighbors']; separated=r['bounds_separated']
    ids=[x['id'] for x in exact+separated]
    assert len(ids)==len(set(ids)) and set(ids)==expected_neighbors,(r['target'],r['state'])
    assert all(x['positive_axis_gap_mm']>1e-5 for x in separated)
    assert all(0<=x['overlap_mm3']<=.1 for x in exact)
    assert set(r['other_spring_box_separation_mm'])==expected_springs-{r['target']}
    assert min(r['other_spring_box_separation_mm'].values())>0
    assert abs(r['retainer_bottom_relative_z_mm']-r['spring_height_mm'])<1e-8
    rows.append({'target':r['target'],'state':r['state'],'neighbors_accounted':len(ids),'exact_or_equivalent':len(exact),'bounds_separated':len(separated)})
assert d['negative_control']['detected'] and d['negative_control']['overlap_mm3']>.1
out={'status':'PASS coverage and current recorded input hashes','report_sha256':sha(f),'input_hash_count':len(d['input_sha256']),'states':rows,'negative_control':d['negative_control'],'limits':['No independent collision Boolean replay in this coverage audit.','Endpoints only, not complete crank-cycle neighbor sweep.','Worker must bind audit.json and preserve checkpoint checker provenance.','No canonical installation or browser acceptance.']}
Path(str(P)+'-root-context-review.json').write_text(json.dumps(out,indent=2)+'\n')
print(out['status'],len(rows),'states;',len(expected_neighbors),'neighbors per state')
