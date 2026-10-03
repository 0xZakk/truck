from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003';report={}
for label in ['plus','minus']:
 folder=OUT/label;a=b.import_step(folder/'fuel-supply-rail.step');c=b.import_step(folder/'fuel-return-tube.step');common=a&c;solids=[]
 for s in common.solids():
  bb=s.bounding_box();solids.append({'valid':s.is_valid,'volume_mm3':s.volume,'center_mm':list(s.center()),'bounds_mm':[list(bb.min),list(bb.max)]})
 report[label]=solids
(OUT/'rail-return-conflict.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
