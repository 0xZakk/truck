#!/usr/bin/env python3
"""Reproduce only the first invalid operation; retain in-memory topology diagnostics."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import full_engine as f
from timing_block_fixed_stock_candidate import DELTA
from OCP.BRepCheck import BRepCheck_Analyzer
OUT=ROOT/'cad/engine/generated/timing-block-fixed-stock-candidate'
path=OUT/'block_interface_shape-after.step';q=b.import_step(path);move=b.Pos(*DELTA);back=b.Pos(*[-v for v in DELTA]);q=move*f.machine_block_bolts(back*q);before=q.is_valid;q=move*f.machine_block_seat(back*q,f.CAM_BORE_R);an=BRepCheck_Analyzer(q.wrapped);bad=[]
for kind,items in [('solid',q.solids()),('shell',q.shells()),('face',q.faces()),('wire',q.wires()),('edge',q.edges())]:
 for i,item in enumerate(items):
  result=an.Result(item.wrapped)
  if result is None:continue
  statuses=[str(s) for s in result.Status()]
  if any('NoError' not in s for s in statuses):
   bb=item.bounding_box();bad.append({'kind':kind,'index':i,'status':statuses,'bounds_mm':[list(bb.min),list(bb.max)]})
r={'status':'DIAGNOSTIC first invalid operation','before_valid':before,'after_valid':q.is_valid,'invalid_subshapes':bad,'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [path,Path(__file__),ROOT/'cad/engine/expansion_plugs.py',ROOT/'cad/engine/cam_retention.py']},'limits':['No repair or healing applied; imported prefix is valid STEP readback','This is a local reconstruction, not a replacement candidate']}
(ROOT/'inventory/engine/timing-block-fixed-stock-rear-seat.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
