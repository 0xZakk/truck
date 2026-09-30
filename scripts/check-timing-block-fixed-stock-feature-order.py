#!/usr/bin/env python3
"""Instrument the unchanged ordered direct features; no exports or geometry edits."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import full_engine as f
import timing_block_fixed_stock_candidate as c
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-block-fixed-stock-candidate'
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q is not None and getattr(q,'wrapped',True) is not None else 0.
tunnel=b.Pos(0,90+c.DELTA[1],72+c.DELTA[2])*f.cx(f.CAM_BORE_R,f.LENGTH+2)
rows=[];saved={}
def observe(name,feature):
 def run(shape,*args):
  q=feature(shape,*args);move=b.Pos(*c.DELTA) if name in ['machine_block_bolts','machine_block_seat','oil_drive_block_interface'] else b.Pos(0,0,0)
  before=move*shape;after=move*q;row={'feature':name,'before_valid':shape.is_valid,'after_valid':q.is_valid,'tunnel_before_mm3':vol(before.intersect(tunnel)),'tunnel_after_mm3':vol(after.intersect(tunnel))};rows.append(row);print(row,flush=True);return q
 return run
for name in ['block_interface_shape','machine_block_bolts','machine_block_seat','oil_drive_block_interface','accessory_block_interface','thermactor_block_interface','filter_block_interface']:
 saved[name]=getattr(f,name);setattr(f,name,observe(name,saved[name]))
try:q,edits=c.regenerate()
finally:
 for name,fn in saved.items():setattr(f,name,fn)
original=b.import_step(OUT/'block.step');difference=vol(q.cut(original))+vol(original.cut(q))
r={'status':'DIAGNOSTIC feature-order tracing, no geometry policy change','feature_order':rows,'repeated_candidate_symmetric_difference_mm3':difference,'final_valid':q.is_valid,'source_edit_counts':edits,'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'limits':['Invalid geometry is retained; intersections serve failure localization only','Per-function runtime wrappers do not change operands or outputs; conjugated functions reported in new world frame']}
(ROOT/'inventory/engine/timing-block-fixed-stock-feature-order.json').write_text(json.dumps(r,indent=2)+'\n')
