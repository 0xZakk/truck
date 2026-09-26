"""Reproduce CAD/JS kinematic fixtures without writing installed assets."""
from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from valve_layout_integration import state,annotate_manifest
from valve_layout_candidate import BASE,OUT
angles=[0,111,150,180,210,246,282,333,342,360,372,420,468,516,540,564,603,720]
rows=[{'crank_deg':a,'cylinder':c,'kind':k,'state':state(a,c,k)} for a in angles for c in range(1,7) for k in ['intake','exhaust']]
(OUT/'motion-api-fixtures.json').write_text(json.dumps(rows,indent=2)+'\n')
m=json.loads((BASE/'manifest.json').read_text());n=annotate_manifest(m)
assert annotate_manifest(n)==n
assert [o['id'] for o in m['occurrences']]==[o['id'] for o in n['occurrences']]
print(len(rows),'fixtures; annotation idempotent; occurrence identities preserved')
