#!/usr/bin/env python3
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
b.SkipClean.clean=False
from assembly_math import transforms
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
OUT=ROOT/'cad/engine/generated/timing-block-support-machining-candidate';m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in m['definitions']};o=next(o for o in m['occurrences'] if o['id']=='oil-pan');pan=transforms(m)['oil-pan']*b.import_step(ROOT/defs[o['definition']]['step'].lstrip('/'));q=b.import_step(OUT/'block.step');base=b.import_step(ROOT/'cad/engine/generated/block.step');added=b.Compound(children=list(q.cut(base).solids()));hit=added.intersect(pan);rows=[]
for i,s in enumerate(hit.solids()):
 bb=s.bounding_box();p=OUT/f'pan-intersection-{i}.step';b.export_step(s,p);r={'index':i,'valid':s.is_valid,'bounds':[list(bb.min),list(bb.max)],'default_volume':s.volume,'faces':len(s.faces()),'integrations':[]}
 for eps in [1e-5,1e-7,1e-9,1e-11]:
  prop=GProp_GProps();error=BRepGProp.VolumeProperties_s(s.wrapped,prop,eps,True,False);r['integrations'].append({'requested':eps,'error':error,'mass':prop.Mass()})
 rows.append(r)
print(json.dumps(rows,indent=2));(ROOT/'inventory/engine/timing-block-pan-intersection-diagnostic.json').write_text(json.dumps(rows,indent=2)+'\n')
