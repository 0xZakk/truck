"""Bounded station-1-only X377.8 feasibility; no full candidate or stock mutation."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import timing_cover_seven_fastener_candidate as c
OUT=ROOT/'cad/engine/generated/timing-cover-station1-rear-seat-research';OUT.mkdir(exist_ok=True)
base=ROOT/'cad/engine/generated/timing-cover-seven-fastener-candidate';cover=b.import_step(base/'cover.step');screw=b.Pos(-2,0,0)*b.import_step(base/'main-cover-screw-1.step');y,z=c.AXES[0];pocket=c.front.c.cx(c.ACCESS_RADIUS,377.8,435,y,z);cut=pocket
for g in c.pan_socket_guards().values():cut=c.norm(cut.cut(g))
cover=c.norm(cover.cut(cut));head=cover.intersect(screw);access=cover.intersect(pocket)
def vol(s):
 if s is None:return 0.
 if isinstance(s,b.ShapeList):return sum(vol(t)for t in s)
 total=0.
 for t in s.solids():
  p=GProp_GProps();e=BRepGProp.VolumeProperties_s(t.wrapped,p,1e-9,True,False)
  assert e<=1e-7,e
  total+=abs(p.Mass())
 return total
r={'status':'FAIL'if vol(head)>1e-5 or vol(access)>1e-5 else'PASS initial feasibility only','seat_x_estimate_mm':377.8,'unchanged_comparison_length_mm':c.LENGTH,'head_cover_overlap_mm3':vol(head),'access_cover_overlap_mm3':vol(access),'scope':'Station 1 moves 2 mm rearward; full protected pan socket stock retained. Other six unchanged. No block support/cavity revision built because head/access feasibility is prerequisite. Head/tool envelopes remain estimates.','inputs':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in[base/'cover.step',base/'main-cover-screw-1.step',Path(c.__file__),Path(__file__)]}}
for name,s in [('head-cover',head),('access-cover',access)]:
 if s is not None and s.solids():b.export_step(c.norm(s),OUT/(name+'.step'))
(ROOT/'inventory/engine/timing-cover-station1-rear-seat-research.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
