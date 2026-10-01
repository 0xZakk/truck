"""Preserve remaining known static failures after the bound ignition correction."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((ROOT/p).read_text())
sha=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
files=['inventory/engine/corrected-stage-v2-sealing-summary.json','inventory/engine/corrected-stage-v2-sealing-neighbors.json','inventory/engine/shifted-ignition-lead-neighbor-validation.json','inventory/engine/shifted-ignition-lead-integration-proposal.json','inventory/engine/corrected-stage-v3-ignition-replay.json','inventory/engine/corrected-engine-stage-v3.json','inventory/engine/engine-stage-v3-navigation-validation.json']
summary,delta,audit,patch,replay,stage,nav=map(load,files)
for record,key in [(summary,'bindings'),(audit,'inputs'),(replay,'bindings'),(nav,'bindings')]:
 for path,digest in record[key].items():assert sha(path)==digest,path
assert not audit['conflicts'] and audit['status'].startswith('PASS')
assert replay['status'].startswith('PASS') and nav['status'].startswith('PASS')
known=summary['retained_v1_conflicts']+[{'a':r['a'],'b':r['b'],'overlap_mm3':r['adaptive_overlap_mm3']}for r in delta['conflicts']]
affected={r['id']for r in patch['occurrences']}
remaining=[r for r in known if not {r['a'],r['b']}&affected]
superseded=[r for r in known if {r['a'],r['b']}&affected]
assert len(known)==82 and len(superseded)==56 and len(remaining)==26
assert len(audit['exact_checks'])==365
report={'status':'FAIL remaining v3 static interfaces; ignition correction passes scoped replay','remaining_known_pairs':remaining,'remaining_count':len(remaining),'superseded_ignition_pairs':len(superseded),'fresh_ignition_pairs':len(audit['exact_checks']),'bindings':{p:sha(p) for p in files+['scripts/summarize-corrected-stage-v3-ignition.py']},'limits':['Known static pairs only, not a complete production BOM or motion-clearance acceptance','Inherited rod-bolt motion conflicts remain','Pump architecture, dimensional/source gaps and browser acceptance remain','No canonical installation']}
(ROOT/'inventory/engine/corrected-stage-v3-remaining-conflicts.json').write_text(json.dumps(report,indent=2)+'\n')
print(report['status'],report['remaining_count'])
