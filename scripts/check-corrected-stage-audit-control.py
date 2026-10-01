#!/usr/bin/env python3
"""Actual staged geometry fault control for the static intersection detector."""
from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_clockwise_candidate import transforms
from cad_metrics import solid_volume
mp=R/'inventory/engine/corrected-engine-stage.json';m=json.loads(mp.read_text());defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};poses=transforms(m,0,0)
paths={key:R/defs[occ[key]['definition']]['step'].lstrip('/')for key in ['block','crankshaft']};sh={key:poses[key]*b.import_step(p)for key,p in paths.items()};bad=b.Pos(0,0,100)*sh['crankshaft'];common=bad.intersect(sh['block']);volume=solid_volume(common);assert volume>100
witness=None
for s in common.solids():
 p=tuple(s.center())
 if bad.is_inside(p,tolerance=1e-7)and sh['block'].is_inside(p,tolerance=1e-7):witness=p;break
assert witness is not None
r={'scope':'Artificial raised-crank fault, not actual staged collision','fault_translation_mm':[0,0,100],'detected_overlap_mm3':volume,'strict_interior_witness':witness,'input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [Path(__file__),mp,*paths.values(),R/'cad/engine/assembly_clockwise_candidate.py',R/'cad/engine/assembly_math.py',R/'cad/engine/cad_metrics.py']}}
(R/'inventory/engine/corrected-stage-audit-negative-control.json').write_text(json.dumps(r,indent=2)+'\n');print(volume,witness)
