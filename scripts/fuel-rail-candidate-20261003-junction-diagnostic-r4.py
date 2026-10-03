from pathlib import Path
import sys,json,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from assembly_math import transforms
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};poses=transforms(m);OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003/r4';r={}
i='regulator-vacuum-fitting';fit=poses[i]*b.import_step(ROOT/defs[occ[i]['definition']]['step'].lstrip('/'))
for label in ['plus','minus']:
 hose=b.import_step(OUT/label/'regulator-vacuum-hose.step');hit=hose&fit;bb=hit.bounding_box() if hit else None;r[label]={'overlap_bounds_mm':[list(bb.min),list(bb.max)] if bb else None,'sections':[]}
 for y in [-65,-62,-60,-58,-56,-55,-54,-52]:
  points=[(0,y,460),(3.9,y,460),(4.11,y,460),(4.5,y,460),(5.9,y,460)]
  r[label]['sections'].append({'y':y,'x_offsets_mm':[p[0] for p in points],'hose_material':[hose.is_inside(p,1e-6) for p in points],'fitting_material':[fit.is_inside(p,1e-6) for p in points]})
(OUT/'vacuum-junction-diagnostic.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
