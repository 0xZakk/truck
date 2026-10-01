#!/usr/bin/env python3
"""Positive interior witnesses for translated pump-foot/pan collisions."""
from pathlib import Path
import sys,json,hashlib,itertools
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
b.SkipClean.clean=False
import oil_drive_layout as drive
from timing_block_support_machining_candidate import DELTA
from cad_metrics import solid_volume
from assembly_math import transforms
OUT=ROOT/'cad/engine/generated/timing-block-support-machining-candidate'
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q is not None and getattr(q,'wrapped',True) is not None else 0.
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
manifestpath=ROOT/'inventory/engine/full-assembly.json';m=json.loads(manifestpath.read_text());defs={d['id']:d for d in m['definitions']};o=next(o for o in m['occurrences'] if o['id']=='oil-pan');panpath=ROOT/defs[o['definition']]['step'].lstrip('/');pan=transforms(m)['oil-pan']*b.import_step(panpath)
basepath=OUT/'base.step';base=b.import_step(basepath);qpath=OUT/'block.step';q=b.import_step(qpath);supports=[b.Pos(*DELTA)*s for s in drive.pump_mount_supports()];rows=[]
for i in range(2):
 path=OUT/f'pan-intersection-{i}.step';hit=b.import_step(path);bb=hit.bounding_box();witness=None
 for fractions in itertools.product([.5,.35,.65],repeat=3):
  center=[list(bb.min)[j]+fractions[j]*list(bb.size)[j] for j in range(3)];cube=b.Pos(*center)*b.Box(.2,.2,.2)
  if vol(cube.cut(hit))<1e-9:witness=cube;break
 assert witness is not None,'No positive witness found'
 source_errors=[vol(witness.cut(s)) for s in supports];row={'region':i,'cube_center_mm':center,'witness_volume_mm3':vol(witness),'outside_intersection_mm3':vol(witness.cut(hit)),'outside_actual_pan_mm3':vol(witness.cut(pan)),'outside_repaired_base_before_support_machining_mm3':vol(witness.cut(base)),'outside_new_candidate_mm3':vol(witness.cut(q)),'outside_identified_translated_pump_support_mm3':min(source_errors),'source_support_index':source_errors.index(min(source_errors))};assert all(v<1e-9 for k,v in row.items() if k.startswith('outside_'));p=OUT/f'pump-pan-positive-witness-{i}.step';b.export_step(witness,p);row['step_sha256']=sha(p);rows.append(row)
inputs=[Path(__file__),manifestpath,panpath,basepath,qpath,ROOT/'cad/engine/oil_drive_layout.py']
r={'status':'FAIL confirmed pump-support/pan collision, positive witnesses at both feet','input_sha256':{str(p.relative_to(ROOT)):sha(p) for p in inputs},'witnesses':rows,'limits':['Each0.008mm3 cube proves positive overlap; it is not the total overlap volume','Approximate131.526mm3 per region remains unaccepted due adaptive-volume nonconvergence','Collision already exists in repaired translated-drive base before support completion/final machining','No pan or pump-support repair applied']}
(ROOT/'inventory/engine/timing-pump-foot-pan-witnesses.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
