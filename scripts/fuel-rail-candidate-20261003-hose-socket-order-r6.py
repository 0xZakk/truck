from pathlib import Path
import json,build123d as b
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003/r6';r={}
for label,sign in [('plus',1),('minus',-1)]:
 outer=b.import_step(OUT/label/'failed-hose-outer.step');inner=b.import_step(OUT/label/'failed-hose-inner.step');socket=b.Pos(174.136,-163+24*sign,424.5)*b.Cylinder(4.15,11)
 union=inner+socket;result=outer-union
 row={'bore_union_volume':union.volume,'bore_union_valid':union.is_valid,'result_volume':result.volume,'result_valid':result.is_valid,'result_solids':len(result.solids())};r[label]=row
 b.export_step(result,OUT/label/'diagnostic-bore-union-order.step');(OUT/'hose-socket-order.json').write_text(json.dumps(r,indent=2)+'\n');print(label,row,flush=True)
