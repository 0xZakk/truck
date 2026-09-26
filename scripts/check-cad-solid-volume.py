#!/usr/bin/env python3
"""Check nested STEP compound measurement without weakening export tolerances."""
from pathlib import Path
import hashlib,json,sys,tempfile
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
box=b.Box(4,5,6);nested=b.Compound(children=[b.Compound(children=[box])])
assert abs(solid_volume(box)-120)<1e-9
assert abs(solid_volume(nested)-120)<1e-9
with tempfile.TemporaryDirectory() as temp:
 p=Path(temp)/'nested.step';b.export_step(nested,p);restored=b.import_step(p)
 assert restored.is_valid and len(restored.solids())==1
 assert abs(solid_volume(restored)-120)<1e-8
 cut=box-b.Box(2,2,8)
 assert abs(solid_volume(cut)-96)<1e-8
 assert abs(solid_volume(cut)-solid_volume(restored))>max(1e-5,120*1e-5),'Removed material escaped original tolerance'
record=dict(status='PASS nested compound STEP and removed-material negative control',expected_volume_mm3=120,removed_material_mm3=24,threshold_unchanged=True,source_sha256=hashlib.sha256((ROOT/'cad/engine/cad_metrics.py').read_bytes()).hexdigest(),checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
(ROOT/'inventory/engine/cad-solid-volume-validation.json').write_text(json.dumps(record,indent=2)+'\n');print(record['status'])
