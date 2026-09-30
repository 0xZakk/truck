#!/usr/bin/env python3
"""Locate protected-region failure using actual fixed cover and casting sections."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import pushrod_cover as cover
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-block-fixed-stock-candidate'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q is not None and getattr(q,'wrapped',True) is not None else 0.
paths={'baseline':ROOT/'cad/engine/generated/block.step','candidate':OUT/'block.step','gasket':ROOT/'cad/engine/generated/pushrod-cover-gasket.step','cover':ROOT/'cad/engine/generated/pushrod-cover.step'}
inputs={str(p.relative_to(ROOT)):sha(p) for p in paths.values()};inputs[str(Path(__file__).relative_to(ROOT))]=sha(Path(__file__));inputs['cad/engine/pushrod_cover.py']=sha(ROOT/'cad/engine/pushrod_cover.py')
parts={k:b.import_step(p) for k,p in paths.items()};parts['gasket']=cover.MOUNT*parts['gasket'];parts['cover']=cover.MOUNT*parts['cover']
extra=b.Compound(children=list(parts['candidate'].cut(parts['baseline']).solids()));missing=b.Compound(children=list(parts['baseline'].cut(parts['candidate']).solids()))
profile=b.RectangleRounded(cover.LENGTH,cover.HEIGHT,10)-b.RectangleRounded(cover.LENGTH-18,cover.HEIGHT-18,8)
rail=cover.MOUNT*(b.Pos(0,0,-14)*b.extrude(profile,amount=12.5))
regions={'existing-rail-solid':rail}
for i,x in enumerate(cover.STATIONS,1):regions[f'existing-fastener-web-{i}']=cover.MOUNT*(b.Pos(x,0,-20.75)*b.Box(16,cover.HEIGHT-16,38.5))
changes=[{'name':name,'added_mm3':vol(extra.intersect(mask)),'removed_mm3':vol(missing.intersect(mask))} for name,mask in regions.items()]
contacts=[]
for state in ['baseline','candidate']:
 for other in ['gasket','cover']:
  contacts.append({'state':state,'part':other,'overlap_mm3':vol(parts[state].intersect(parts[other]))})
sections=[]
for z in [135,140,185]:
 contours={}
 for name,q in parts.items():
  section=b.section(q,section_by=b.Plane.XY.offset(z));contours[name]=[[list(edge.position_at(i/60))[:2] for i in range(61)] for edge in section.edges()]
 sections.append({'z_mm':z,'contours_xy':contours})
assert inputs=={p:sha(ROOT/p) for p in inputs}
r={'status':'DIAGNOSTIC only; original protected failure retained','input_sha256':inputs,'original_protected_bounds_mm':[[-337,103,129],[337,122,241]],'fixed_feature_material_comparison':changes,'actual_fixed_neighbor_overlaps':contacts,'sections':sections,'limits':['Supplementary feature localization, never a replacement or relaxation of the original guard','Casting and cover are provisional geometry; no factory fidelity claim']}
(ROOT/'inventory/engine/timing-block-fixed-stock-side-cover.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k!='sections'},indent=2))
