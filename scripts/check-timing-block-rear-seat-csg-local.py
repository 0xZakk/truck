#!/usr/bin/env python3
"""Compare explicit source-operand construction orders on valid incoming stock."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import full_engine as f
import timing_block_rear_seat_csg_candidate as c
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-block-rear-seat-csg-candidate';OUT.mkdir(exist_ok=True)
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q is not None and getattr(q,'wrapped',True) is not None else 0.
prefix=ROOT/'cad/engine/generated/timing-block-fixed-stock-candidate/block_interface_shape-after.step';q=b.import_step(prefix);move=b.Pos(*c.DELTA);back=b.Pos(*[-v for v in c.DELTA]);q=f.machine_block_bolts(back*q);assert q.is_valid
boss,tunnel,seat=c.operands(f.CAM_BORE_R)
variants={}
for name,fn in [('original',lambda:(q+boss)-tunnel-seat),('skip-empty-tunnel',lambda:c.machine_block_seat(q,f.CAM_BORE_R)),('fused-cutters',lambda:(q+boss).cut(tunnel.fuse(seat)))]:
 shape=fn();p=OUT/(name+'.step');b.export_step(move*shape,p);variants[name]={'valid':shape.is_valid,'solids':len(shape.solids()),'volume_mm3':vol(shape),'step_sha256':hashlib.sha256(p.read_bytes()).hexdigest()};print(name,variants[name],flush=True)
 # Compare only valid originals against the separately imported original STEP.
 if shape.is_valid:
  reference=back*b.import_step(OUT/'original.step');variants[name]['difference_from_original_step_readback_mm3']=vol(shape.cut(reference))+vol(reference.cut(shape))
r={'status':'LOCAL construction comparison; no final-machining changes','variants':variants,'source_operand_policy':'Exact source boss/tunnel/seat expressions, dimensions, frame retained; distributive set identity','input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [prefix,Path(__file__),Path(c.__file__),ROOT/'cad/engine/expansion_plugs.py',ROOT/'cad/engine/cam_retention.py']}}
(ROOT/'inventory/engine/timing-block-rear-seat-csg-local.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
