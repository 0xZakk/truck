from pathlib import Path
import json,build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut,BRepAlgoAPI_Common
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003/r6';r={}
for label,sign in [('plus',1),('minus',-1)]:
 shell=b.import_step(OUT/label/'failed-hose-shell.step');socket=b.Pos(174.136,-163+24*sign,424.5)*b.Cylinder(4.15,11);row=[]
 for fuzzy in [0,1e-7,1e-6,1e-5]:
  vals={}
  for name,cls in [('cut',BRepAlgoAPI_Cut),('common',BRepAlgoAPI_Common)]:
   op=cls(shell.wrapped,socket.wrapped);op.SetFuzzyValue(fuzzy);op.Build();q=b.Compound(op.Shape());vals[name]={'done':op.IsDone(),'valid':q.is_valid,'volume':q.volume,'solids':[s.volume for s in q.solids()]}
   if name=='cut' and q.volume>13000:b.export_step(q,OUT/label/f'diagnostic-socket-cut-{fuzzy}.step')
  row.append({'fuzzy_mm':fuzzy,**vals})
 r[label]=row;(OUT/'hose-socket-diagnostic.json').write_text(json.dumps(r,indent=2)+'\n');print(label,row,flush=True)
