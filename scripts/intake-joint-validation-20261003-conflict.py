#!/usr/bin/env python3
"""Preserve exact new fuel-return interference and baseline comparison for review."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,numpy as np
from assembly_math import transforms
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
OUT=ROOT/'cad/engine/generated/intake-joint-validation-20261003';manifest=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in manifest['definitions']};occ={o['id']:o for o in manifest['occurrences']};poses=transforms(manifest)
def load(i):return poses[i]*b.import_step(ROOT/defs[occ[i]['definition']]['step'].lstrip('/'))
old=load('efi-upper-intake');tube=load('fuel-return-tube');new=b.import_step(ROOT/'cad/engine/generated/intake-joint-candidate-20261003/efi-upper-intake.step');report={}
for label,s in [('installed_upper',old),('candidate_upper',new)]:
 op=BRepAlgoAPI_Common(s.wrapped,tube.wrapped);op.Build();shape=op.Shape();props=GProp_GProps();BRepGProp.VolumeProperties_s(shape,props);report[label]={'IsDone':op.IsDone(),'null':shape.IsNull(),'valid':BRepCheck_Analyzer(shape).IsValid(),'overlap_mm3':props.Mass()}
 if label=='candidate_upper':
  hit=b.Compound(shape);box=hit.bounding_box();report['intersection_bounds_mm']=[list(box.min),list(box.max)];b.export_step(hit,OUT/'fuel-return-intersection.step')
for label,s in [('candidate-upper',new),('fuel-return-tube',tube),('intersection',hit)]:
 vertices,faces=s.tessellate(.07,.08);np.savez_compressed(OUT/(label+'.npz'),vertices=np.array([tuple(v) for v in vertices]),faces=faces)
report['manifest_sha256']=hashlib.sha256((ROOT/'inventory/engine/full-assembly.json').read_bytes()).hexdigest();report['limits']='Current full upper versus installed tube; no relocation or repair performed. Tube route and upper runner section are both provisional geometry.';(OUT/'fuel-return-conflict.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
