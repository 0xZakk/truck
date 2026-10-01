#!/usr/bin/env python3
from pathlib import Path
import json,sys,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_math import transforms
p=R/'inventory/engine/full-assembly.json';m=json.loads(p.read_text());t=transforms(m,0);d={x['id']:x for x in m['definitions']};o={x['id']:x for x in m['occurrences']}
ids=['ac-compressor-clutch-pulley','ps-pump-pulley','alternator-pulley','thermactor-pulley','water-pump-pulley','tensioner-pulley-wheel','ac-compressor-manifold-suction-seal','ac-compressor-manifold-discharge-seal','ps-pump-outlet-fitting'];rows=[];paths=[p,Path(__file__),R/'cad/engine/assembly_math.py']
for n in ids:
 q=R/d[o[n]['definition']]['step'].lstrip('/');paths.append(q);shape=t[n]*b.import_step(q);bb=shape.bounding_box();rows.append({'id':n,'parent':o[n]['parent'],'definition':o[n]['definition'],'world_bounds':{'min':list(bb.min),'max':list(bb.max)},'radial_bbox_center_yz_mm':[(bb.min.Y+bb.max.Y)/2,(bb.min.Z+bb.max.Z)/2],'scope':'Radial bounds infer axis only for full circular pulley; fitting bounds are endpoint region, not bore axis'})
assembly={x['id']:x for x in m['assemblies']}
def belongs(row,g):
 q=row['parent']
 while q:
  if q==g:return True
  q=assembly.get(q,{}).get('parent')
 return False
groups=['ac-compressor','power-steering-pump-assembly','alternator-assembly','thermactor-pump-assembly','tensioner-pulley-assembly','tensioner-support-assembly']
report={'status':'COMPLETE actual datum inventory; no movement','canonical_belt_occurrences':[v['id'] for v in m['occurrences'] if 'belt' in v['id']],'canonical_hose_occurrences':[v['id'] for v in m['occurrences'] if 'hose' in v['id']],'rows':rows,'group_ownership':{g:[v['id'] for v in m['occurrences'] if belongs(v,g)] for g in groups},'input_sha256':{str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest() for q in paths}}
(R/'inventory/engine/accessory-common-layout-datums.json').write_text(json.dumps(report,indent=2)+'\n')
