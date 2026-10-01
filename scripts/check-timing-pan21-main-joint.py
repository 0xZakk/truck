"""Bind all seven main screw contacts to the coordinated cover export."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import timing_pan21_lateral_candidate as c
OUT=ROOT/'cad/engine/generated/timing-pan21-lateral-candidate';cover=b.import_step(OUT/'cover.step');blockpath=c.COVER.with_name('block.step');block=b.import_step(blockpath);paths=[OUT/'cover.step',blockpath];rows=[]
def vol(s):
 if s is None:return 0.
 if isinstance(s,b.ShapeList):return sum(vol(t)for t in s)
 total=0.
 for t in s.solids():
  p=GProp_GProps();e=BRepGProp.VolumeProperties_s(t.wrapped,p,1e-9,True,False);assert e<=1e-7,e;total+=abs(p.Mass())
 return total
for n,(y,z)in enumerate(c.main.AXES,1):
 p=c.COVER.with_name(f'main-cover-screw-{n}.step');s=b.import_step(p);paths.append(p);seat=c.main.front.c.cx(8.75,379.78,379.8,y,z)-c.main.front.c.cx(4.2,379.77,379.81,y,z);tool=c.main.front.c.cx(10.5,379.8,435,y,z)
 rows.append({'station':n,'cover_overlap':vol(cover.intersect(s)),'block_overlap':vol(block.intersect(s)),'full_head_seat_missing':vol(seat.cut(cover)),'tool_obstruction':vol(tool.intersect(cover)),'head_cover_distance_mm':s.distance_to(cover),'male_block_distance_mm':s.distance_to(block)})
for n in ['pan','pan-gasket']:
 p=OUT/(n+'.step');paths.append(p);s=b.import_step(p);rows.append({'part':n,'block_overlap':vol(block.intersect(s))})
r={'rows':rows,'status':'PASS'if all(v<1e-5 for row in rows for k,v in row.items()if k not in ['station','part'])else'FAIL','inputs_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths+[Path(__file__)]},'limits':['Seven-screw trial block unchanged; exact1994 head/length/thread transfer and complete block wet/material guards remain unverified','Distance0 plus complete seating/source female checks establishes nominal geometric contact, not load capacity']};(ROOT/'inventory/engine/timing-pan21-main-joint.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
