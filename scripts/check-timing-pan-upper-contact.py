#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common,BRepAlgoAPI_Cut
from timing_cover_attachment_v2 import norm
O=R/'cad/engine/generated/timing-pan-upper-contact';F=R/'cad/engine/generated/timing-cover-attachment-v2'
paths={'gasket':R/'cad/engine/generated/timing-pan-expanded-seat-v2-candidate/pan-gasket.step','block-v3':R/'cad/engine/generated/timing-front-block-expanded-seat-v3-candidate/block.step','cover-2692':R/'cad/engine/generated/front-seal-2692-candidate/cover.step','main-gasket':F/'main-gasket.step','terminal-sealant':F/'front-terminal-sealant.step','rear-main-cap':R/'cad/engine/generated/main-cap.step','rear-crank-seal':R/'cad/engine/generated/rear-seal.step'}
parts={n:norm(b.import_step(p)) for n,p in paths.items()};j=json.loads((R/'inventory/engine/full-assembly.json').read_text());placements={}
for name,occ in [('rear-main-cap','main-cap-7'),('rear-crank-seal','rear-seal')]:
 q=next(x for x in j['occurrences'] if x['id']==occ);parts[name]=b.Pos(*q['position_cad_mm'])*b.Rot(*q['rotation_cad_deg'])*parts[name];placements[name]=q
upper=b.Compound([f for f in parts['gasket'].faces() if f.normal_at().Z>.05]);remaining=upper
owners={};meshes={}
def faces(shape):return b.Compound(list(shape.faces()))
def operate(kind,a,other):
 op=kind(a.wrapped,other.wrapped);op.Build();assert op.IsDone();return b.Compound(op.Shape())
def info(f):return {'area_mm2':f.area,'center_mm':list(f.center()),'bounds_mm':[list(f.bounding_box().min),list(f.bounding_box().max)]}
for name,shape in parts.items():
 if name=='gasket':continue
 contact=operate(BRepAlgoAPI_Common,upper,faces(shape));owned=list(contact.faces());owners[name]={'area_mm2':sum(f.area for f in owned),'faces':[info(f) for f in owned],'gasket_distance_mm':parts['gasket'].distance_to(shape)}
 if owned:
  b.export_step(contact,O/(name+'-contact.step'));v,f=contact.tessellate(.025,.08);meshes[name]={'vertices':np.array([tuple(q) for q in v]),'faces':np.array(f)}
 remaining=operate(BRepAlgoAPI_Cut,remaining,faces(shape))
 print(name,owners[name]['area_mm2'],flush=True)
gaps=list(remaining.faces());b.export_step(remaining,O/'unsupported-upper-faces.step') if gaps else None
v,f=upper.tessellate(.025,.08);meshes['upper']={'vertices':np.array([tuple(q)for q in v]),'faces':np.array(f)}
if gaps:
 v,f=remaining.tessellate(.025,.08);meshes['unsupported']={'vertices':np.array([tuple(q)for q in v]),'faces':np.array(f)}
np.savez_compressed(O/'contact-preview.npz',**{n+'_'+k:a for n,d in meshes.items() for k,a in d.items()})
report={'scope':'Actual upward gasket faces by component owner; no pressure/containment claim','upper_face_area_mm2':upper.area,'owners':owners,'unsupported_area_mm2':sum(f.area for f in gaps),'unsupported_faces':[info(f)for f in gaps],'retained_placements':placements,'input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),R/'inventory/engine/full-assembly.json',*paths.values()]}}
(R/'inventory/engine/timing-pan-upper-contact-review.json').write_text(json.dumps(report,indent=2)+'\n');print('UNSUPPORTED',report['unsupported_area_mm2'],report['unsupported_faces'],flush=True)
