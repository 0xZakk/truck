#!/usr/bin/env python3
"""Export exact missing material within four declared journal support shells."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import full_engine as f
from timing_block_fixed_stock_candidate import DELTA
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-block-fixed-stock-candidate';path=OUT/'block.step';q=b.import_step(path);rows=[]
for i,x in enumerate([-334,-110,110,360.5],1):
 shell=b.Pos(x,90+DELTA[1],72+DELTA[2])*(f.cx(f.CAM_BORE_R+.05,22)-f.cx(f.CAM_BORE_R+.001,22));missing=b.Compound(children=list(shell.cut(q).solids()));p=OUT/f'journal-{i}-missing-support.step';b.export_step(missing,p);bb=missing.bounding_box();rows.append({'bearing':i,'missing_volume_mm3':sum(abs(solid_volume(s,'adaptive')) for s in missing.solids()),'bounds_mm':[list(bb.min),list(bb.max)],'step':str(p.relative_to(ROOT)),'step_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
r={'status':'DIAGNOSTIC exact support-shell deficits, no material added','block_step_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'missing_support_regions':rows,'limits':['Exact only within the declared thin support-shell witness; not required casting boss geometry','Based on valid STEP readback; original builder topology remains failed']}
(ROOT/'inventory/engine/timing-block-fixed-stock-support-regions.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
