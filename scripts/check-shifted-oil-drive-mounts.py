#!/usr/bin/env python3
"""Bind unchanged actual pump-foot supports and mechanical shaft passage only."""
import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import oil_drive_layout as d
from timing_block_axis_feature_candidate import DELTA
files=['scripts/check-shifted-oil-drive-mounts.py','cad/engine/oil_drive_layout.py','cad/engine/timing_block_axis_feature_candidate.py','inventory/engine/timing-pump-foot-faceted-validation.json','cad/engine/generated/timing-front-block-expanded-seat-v3-candidate/block.step']
block=b.import_step(ROOT/files[-1]);v=lambda s:sum(x.volume for x in s.solids()) if s else 0.
rows=[]
for i in [0,1]:
 p=f'cad/engine/generated/timing-pump-foot-faceted-candidate/support-{i}.step';files.append(p);s=b.import_step(ROOT/p);missing=v(s.cut(block));rows.append({'support':i,'missing_from_current_block_mm3':missing});print(rows[-1],flush=True)
probe=b.Pos(*DELTA)*d.GEAR_FRAME*d.axial_cylinder(7.1,d.INTERMEDIATE_BOTTOM-1,d.INTERMEDIATE_TOP-12)
normal=v(probe.intersect(block));fault=v((b.Pos(2,0,0)*probe).intersect(block));assert normal<1e-5 and fault>.1 and all(r['missing_from_current_block_mm3']<1e-5 for r in rows)
r={'status':'PASS retained mechanical support and shaft passage; fluid joint NOT MODELED','inputs':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files},'actual_support_containment':rows,'shaft_probe_overlap_mm3':normal,'shaft_probe_shift_2mm_control_overlap_mm3':fault,'reuse_scope':'Frozen support report positive pump seats and bolt seats apply only to unchanged rigid pump/bolts and these retained supports; static mechanical topology','limits':['Shaft bore is not a pump discharge passage','Source-supported pump gasket missing','Pump outlet/block sealing face and gallery are unmodeled','No pressure/strength/production or whole oil-system acceptance']}
(ROOT/'inventory/engine/shifted-oil-drive-mount-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],flush=True)
