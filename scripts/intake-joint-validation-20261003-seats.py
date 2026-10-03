#!/usr/bin/env python3
"""Independently bounded actual seat comparisons, not a broad-region waiver."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut,BRepAlgoAPI_Common
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
from OCP.TopAbs import TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer
OUT=ROOT/'cad/engine/generated/intake-joint-validation-20261003';oldp=ROOT/'cad/engine/generated/efi-lower-intake.step';newp=ROOT/'cad/engine/generated/intake-joint-candidate-20261003/efi-lower-intake.step';old=b.import_step(oldp);new=b.import_step(newp)
def op(kind,a,c):
 algo=kind(a,c);algo.Build();s=algo.Shape();r={'IsDone':algo.IsDone(),'null':s.IsNull()}
 if not s.IsNull():
  r['valid']=BRepCheck_Analyzer(s).IsValid();g=GProp_GProps();BRepGProp.VolumeProperties_s(s,g);r['volume_mm3']=g.Mass();e=TopExp_Explorer(s,TopAbs_SOLID);count=0
  while e.More():count+=1;e.Next()
  r['solids']=count
 return s,r
masks=[]
for i,x in enumerate([(2.5-i)*113.792 for i in range(6)],1):
 masks.append((f'head-face-{i}',b.Pos(x-25,-135.55,277.5)*b.Box(52,.1,52),'head flange final0.1mm depth'))
 masks.append((f'injector-seat-{i}',b.Pos(x-25,-163,313.95)*b.Cylinder(10.1,.1),'socket upper0.1mm annular seat'))
for i,x in enumerate([-250,-40,220],1):masks.append((f'rail-seat-{i}',b.Pos(x,-178,363.95)*b.Cylinder(8.1,.1),'rail mount upper0.1mm annular seat'))
rows=[]
for name,mask,scope in masks:
 a,ra=op(BRepAlgoAPI_Common,old.wrapped,mask.wrapped);c,rc=op(BRepAlgoAPI_Common,new.wrapped,mask.wrapped)
 _,ac=op(BRepAlgoAPI_Cut,a,c);_,ca=op(BRepAlgoAPI_Cut,c,a)
 valid=all(v.get('IsDone') and not v.get('null') and v.get('valid') for v in [ra,rc,ac,ca]);difference=abs(ac.get('volume_mm3',0))+abs(ca.get('volume_mm3',0)) if valid else None
 row={'seat':name,'scope':scope,'old_region':ra,'new_region':rc,'old_minus_new':ac,'new_minus_old':ca,'symmetric_difference_mm3':difference,'status':'PASS bounded seat' if valid and difference<.1 else 'FAIL/ERROR'};rows.append(row);print(name,row['status'],difference,flush=True)
report={'inputs_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [oldp,newp]},'rows':rows,'limits':'Thin actual seating regions only; broad head/injector curved-region Boolean failure remains unpassed. Does not certify whole casting preservation, compression or retention.'};(OUT/'seats.json').write_text(json.dumps(report,indent=2)+'\n')
