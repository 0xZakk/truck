#!/usr/bin/env python3
"""Diagnose the exact protected-region Boolean through lower-level OCC state."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut,BRepAlgoAPI_Common
from OCP.TopAbs import TopAbs_SOLID,TopAbs_FACE
from OCP.TopExp import TopExp_Explorer
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
out=ROOT/'cad/engine/generated/intake-joint-validation-20261003'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inspect(shape):
 if shape.IsNull():return {'null':True,'solids':None,'faces':None,'volume_mm3':None}
 counts=[]
 for kind in [TopAbs_SOLID,TopAbs_FACE]:
  exp=TopExp_Explorer(shape,kind);count=0
  while exp.More():count+=1;exp.Next()
  counts.append(count)
 props=GProp_GProps();BRepGProp.VolumeProperties_s(shape,props)
 return {'null':False,'valid':BRepCheck_Analyzer(shape).IsValid(),'solids':counts[0],'faces':counts[1],'volume_mm3':props.Mass()}
def operation(kind,a,c):
 op=kind(a,c);op.Build();row={'IsDone':op.IsDone(),'result':inspect(op.Shape())}
 for method in ['HasErrors','HasWarnings','ErrorStatus','WarningStatus']:
  if hasattr(op,method):
   try:row[method]=getattr(op,method)()
   except Exception as e:row[method]='unavailable:'+str(e)
 row['available_error_methods']=[x for x in dir(op) if 'Error' in x or 'Warning' in x or 'Report' in x]
 return op.Shape(),row
manifest=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in manifest['definitions']};oldp=ROOT/defs['efi-lower-intake']['step'].lstrip('/');newp=ROOT/'cad/engine/generated/intake-joint-candidate-20261003/efi-lower-intake.step'
old=b.import_step(oldp);new=b.import_step(newp);mask=b.Pos(0,-156,295)*b.Box(800,38,110)
a,ra=operation(BRepAlgoAPI_Common,old.wrapped,mask.wrapped);c,rc=operation(BRepAlgoAPI_Common,new.wrapped,mask.wrapped)
report={'inputs_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [oldp,newp,ROOT/'inventory/engine/full-assembly.json']},'old_region':ra,'new_region':rc}
for name,one,two in [('old_minus_new',a,c),('new_minus_old',c,a),('identical_old_minus_old',a,a)]:
 shape,row=operation(BRepAlgoAPI_Cut,one,two);report[name]=row
# A real nonempty negative control must survive the same low-level operation.
shift=b.Pos(.5,0,0)*new;cc,rcc=operation(BRepAlgoAPI_Common,shift.wrapped,mask.wrapped);_,control=operation(BRepAlgoAPI_Cut,a,cc);report['shifted_half_mm_control']=control
(out/'boolean.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
