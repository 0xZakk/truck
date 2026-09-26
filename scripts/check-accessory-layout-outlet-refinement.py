"""Exact local obstacle refinement; does not certify full candidate assembly.
The monkeypatch is process-local and never changes candidate source files.
"""
import sys,json,hashlib
from pathlib import Path
import build123d as cad
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'));import accessory_layout_evidence as c
from assembly_math import transforms
m=json.load(open(ROOT/'inventory/engine/full-assembly.json'));poses=transforms(m);d=next(x for x in m['definitions'] if x['id']=='coolant-outlet-housing');obstacle=cad.import_step(ROOT/d['step'].lstrip('/')).moved(poses['coolant-outlet-housing'])
original=c.shifts;results=[]
for dz in [-60,-40,-20,0,2,4]:
 def shift(height,dz=dz):
  v=original(height);v['ALT']=(0,dz);return v
 c.shifts=shift
 shape=c.belt_shape();hit=shape.intersect(obstacle);volume=sum(s.volume for s in hit.solids()) if hit else 0
 result={'alt_dz_mm':dz,'outlet_overlap_mm3':volume,'length_mm':c.base.solve(c.stations(60),False)['length']};results.append(result);print(result,flush=True)
(ROOT/'inventory/engine/accessory-layout-outlet-refinement.json').write_text(json.dumps(results,indent=2))
