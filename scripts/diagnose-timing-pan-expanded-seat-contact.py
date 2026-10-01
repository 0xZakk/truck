#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
from timing_cover_attachment_v2 import norm
OUT=ROOT/'cad/engine/generated/timing-pan-expanded-seat-candidate'
result={}
for label,folder in [('new',OUT),('frozen',ROOT/'cad/engine/generated/timing-cover-attachment-v2')]:
 pan=norm(b.import_step(folder/'pan.step'));gasket=norm(b.import_step(folder/'pan-gasket.step'));bottom=[f for f in gasket.faces()if f.normal_at().Z<-.05]
 q=BRepAlgoAPI_Cut(b.Compound(bottom).wrapped,b.Compound(list(pan.faces())).wrapped);assert q.IsDone();diff=b.Compound(q.Shape());faces=list(diff.faces())
 result[label]={'area_mm2':sum(f.area for f in faces),'faces':[{'area_mm2':f.area,'center':list(f.center()),'normal':list(f.normal_at()),'bounds':[list(f.bounding_box().min),list(f.bounding_box().max)]}for f in faces]}
 b.export_step(diff,OUT/(label+'-gasket-unbacked-faces.step'))
result['input_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [Path(__file__),OUT/'pan.step',OUT/'pan-gasket.step',ROOT/'cad/engine/generated/timing-cover-attachment-v2/pan.step',ROOT/'cad/engine/generated/timing-cover-attachment-v2/pan-gasket.step']}
(OUT/'gasket-contact-diagnostic.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
