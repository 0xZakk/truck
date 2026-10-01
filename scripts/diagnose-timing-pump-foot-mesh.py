from pathlib import Path
import build123d as b
from OCP.BRep import BRep_Tool
from OCP.TopLoc import TopLoc_Location
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'cad/engine/generated/timing-pump-foot-candidate/block.step'
for tolerance in [.12,.03]:
 q=b.import_step(p);q.mesh(tolerance,.15)
 missing=[(i,f.area,list(f.center())) for i,f in enumerate(q.faces()) if BRep_Tool.Triangulation_s(f.wrapped,TopLoc_Location()) is None]
 print(tolerance,'missing',missing,flush=True)
q=b.import_step(p);q=q.clean();print('clean valid',q.is_valid,flush=True)
try:v,f=q.tessellate(.12,.15);print('clean mesh',len(v),len(f),flush=True)
except Exception as e:print('clean failed',repr(e),flush=True)
from OCP.BRepMesh import BRepMesh_IncrementalMesh
q=b.import_step(p);mesher=BRepMesh_IncrementalMesh(q.wrapped,.03,False,.1,True)
missing=[(i,f.area,list(f.center())) for i,f in enumerate(q.faces()) if BRep_Tool.Triangulation_s(f.wrapped,TopLoc_Location()) is None]
print('absolute missing',missing,flush=True)
from OCP.BRepBuilderAPI import BRepBuilderAPI_NurbsConvert
q=b.import_step(p);q=b.Compound(BRepBuilderAPI_NurbsConvert(q.wrapped,True).Shape());print('nurbs valid',q.is_valid,flush=True)
try:v,f=q.tessellate(.12,.15);print('nurbs mesh',len(v),len(f),flush=True)
except Exception as e:print('nurbs failed',repr(e),flush=True)
