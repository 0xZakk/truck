#!/usr/bin/env python3
"""Bounded path witness only: does not replace full oil-cavity acceptance."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from timing_cover_attachment_v2 import norm,RELOCATIONS
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-pan-oil-boundary'
inputs={'pan':ROOT/'cad/engine/generated/timing-pan-access-candidate/pan.step','gasket':ROOT/'cad/engine/generated/timing-cover-attachment-v2/pan-gasket.step','roof':OUT/'roof-trial.step','collar':OUT/'roof-gasket-collar.step'}
parts={k:norm(b.import_step(p))for k,p in inputs.items()}
p=RELOCATIONS[20];start=b.Vector(p[0],p[1],p[2]-2.75);end=b.Vector(370,0,-70);delta=end-start
path=b.Solid.make_cylinder(.25,delta.length,b.Plane(origin=start,z_dir=delta))
b.export_step(path,OUT/'station20-head-to-front-neck-path.step')
values={}
for key,shape in parts.items():
 op=BRepAlgoAPI_Common(path.wrapped,shape.wrapped)
 assert op.IsDone()
 hit=norm(b.Compound(op.Shape()))
 values[key]=0 if hit is None else sum(abs(solid_volume(q,'adaptive'))for q in hit.solids())
block=b.Pos(*tuple((start+end)*.5))*b.Box(1,1,1)
control=BRepAlgoAPI_Common(path.wrapped,block.wrapped);assert control.IsDone()
control_volume=volume=abs(solid_volume(norm(b.Compound(control.Shape())),'adaptive'))
result={'negative_control_blocked_path_overlap_mm3':control_volume,'negative_control_detected':control_volume>.01,'scope':'Positive-radius path from actual station20 head center to designated front-neck interior witness; does not establish closed cavity','start_mm':list(start),'end_mm':list(end),'radius_mm':.25,'overlap_mm3':values,'unobstructed':max(values.values())<.01,'classification':'An unobstructed path contradicts dry-side isolation from the intended front-neck region; whole cavity/containment remains unverified.','input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [Path(__file__),*inputs.values()]}}
(OUT/'station20-head-wet-path.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
