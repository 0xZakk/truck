"""Read-only bounded feasibility witnesses for pan21 Y-95 proposal."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import timing_cover_seven_fastener_candidate as main
import timing_cover_attachment_v2 as a
OUT=ROOT/'cad/engine/generated/timing-cover-seven-fastener-candidate'
cover=b.import_step(OUT/'cover.step');screw=b.import_step(OUT/'main-cover-screw-1.step');p=(390.,-95.,-32.1)
stock=b.Pos(p[0],p[1])*a.cz(10,p[2]+7.6,p[2]+23.6)
wall=b.Pos(p[0],p[1])*a.cz(6.2,p[2]+7.6,p[2]+23.6)
access=main.front.c.cx(main.ACCESS_RADIUS,main.SEAT,435,*main.AXES[0])
def vol(s):
 if s is None:return 0.
 if isinstance(s,b.ShapeList):return sum(vol(t)for t in s)
 v=0.
 for t in s.solids():
  q=GProp_GProps();e=BRepGProp.VolumeProperties_s(t.wrapped,q,1e-9,True,False);assert e<=1e-7,e;v+=abs(q.Mass())
 return v
points=[main.front.c.yz(q,main.front.P)for q in main.front.source.OUTLINE_NORMALIZED]
outer=main.front.face(points[:45]+[(main.front.RIGHT,main.front.PLANE),(main.front.RIGHT,-70),(main.front.LEFT,-70),(main.front.LEFT,main.front.PLANE)])
source_cavity=main.front.c.extrude_x(b.offset(outer,amount=-6),372.8,39.2)
# Geometry probes only; no revised material is exported or accepted.
r={'status':'READ-ONLY preflight; candidate not built','new_station21_mm':p,'source_status':'Explicit estimated feasibility datum, not measured Ford geometry','new_stock_source_cover_cavity_overlap_mm3':vol(stock.intersect(source_cavity)),'new_stock_cavity_currently_void_mm3':vol(a.norm(stock.intersect(source_cavity)).cut(cover)),'new_stock_main1_head_overlap_mm3':vol(stock.intersect(screw)),'new_stock_main1_access_overlap_mm3':vol(stock.intersect(access)),'new_stock_other_pan23_guard_overlap_mm3':vol(stock.intersect(a.pan_socket_guards()[23])) if hasattr(a,'pan_socket_guards') else vol(stock.intersect(main.pan_socket_guards()[23])),'new_stock_missing_from_existing_cover_mm3':vol(stock.cut(cover)),'new_r6p2_wall_envelope_missing_from_existing_cover_mm3':vol(wall.cut(cover)),'analytic_separation_mm':{'stock_to_pan_upper_wall_front_x':380-378,'stock_to_arch_radial_y_limit':85-main.front.RADIUS,'stock_to_main1_access_y':-105-(main.AXES[0][0]+main.ACCESS_RADIUS),'new_clearance_bore_to_pan_upper_wall_x':390-4.3-378},'inputs_sha256':{str(q.relative_to(ROOT)):hashlib.sha256(q.read_bytes()).hexdigest()for q in[OUT/'cover.step',OUT/'main-cover-screw-1.step',Path(main.__file__),Path(__file__)]}}
Path(ROOT/'inventory/engine/timing-pan21-lateral-datum-preflight.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
