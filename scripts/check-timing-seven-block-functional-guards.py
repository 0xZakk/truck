"""Resolve broad guard overlaps using actual source pan20/pump interfaces."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import timing_cover_seven_fastener_candidate as c
import timing_cover_attachment_v2 as owner
import water_pump_joint_candidate as pump
newpath=ROOT/'cad/engine/generated/timing-cover-seven-fastener-candidate/block.step';q=b.import_step(newpath);old=b.import_step(c.BLOCK);paths=[newpath,c.BLOCK,Path(__file__)];rows=[]
def vol(s):
 if s is None:return 0.
 if isinstance(s,b.ShapeList):return sum(vol(t)for t in s)
 v=0.
 for t in s.solids():
  p=GProp_GProps();e=BRepGProp.VolumeProperties_s(t.wrapped,p,1e-9,True,False);assert e<=1e-7,e;v+=abs(p.Mass())
 return v
for n in[10,20]:
 p=owner.RELOCATIONS[n];loc=b.Pos(*p);female_path=ROOT/'cad/engine/generated/pan-fastener-thread-candidate/female-test-coupon.step';male_path=female_path.with_name('pan-screw.step');paths.extend([female_path,male_path]);female=loc*b.import_step(female_path);male=loc*b.import_step(male_path);wall=loc*(owner.cz(6.2,7.6,23.6)-owner.cz(4.17,7.5,23.7));floor=loc*owner.cz(4.15,22.6,23.6);neighborhood=loc*owner.cz(6.2,7.6,23.6)
 a=c.norm(q.intersect(neighborhood));d=c.norm(old.intersect(neighborhood));rows.append({'station':n,'actual_male_overlap_mm3':vol(q.intersect(male)),'source_female_missing_mm3':vol(female.cut(q)),'wall_missing_mm3':vol(wall.cut(q)),'floor_missing_mm3':vol(floor.cut(q)),'functional_neighborhood_added_mm3':vol(a.cut(d)),'functional_neighborhood_removed_mm3':vol(d.cut(a))})
wet=[]
for name,shape in [('pump-chamber',pump.cx(59,359.5,374,-32,170)),('pump-fifth',pump.cx(6.5,359.5,374,pump.EXTRA[0]-32,pump.EXTRA[1]+170))]:wet.append({'name':name,'old_obstruction_mm3':vol(old.intersect(shape)),'new_obstruction_mm3':vol(q.intersect(shape))})
r={'pan_sockets':rows,'pump_declared_fluid_spaces':wet,'status':'PASS functional interfaces only'if all(v<1e-5 for row in rows for k,v in row.items()if k!='station')and all(row['new_obstruction_mm3']<1e-5 for row in wet)else'FAIL','scope':'Does not erase prior broadR12pan20/R85pump guard failures. Exact functional female/wall/floor and declared fluid-space checks are distinct evidence; root must decide whether exterior stock change is acceptable.','input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths+[Path(owner.__file__),Path(pump.__file__)]}};(ROOT/'inventory/engine/timing-seven-block-functional-guards.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
