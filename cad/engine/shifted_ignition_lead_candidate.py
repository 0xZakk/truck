"""Separate cap-end re-registration; preserve source opposite-end routes and IDs."""
import build123d as b
import ignition_leads as src
from timing_block_axis_feature_candidate import DELTA
D=b.Vector(*DELTA)
def path_and_contract(cylinder=None):
 if cylinder is not None:
  sf=src.cap_frame(src.TOWER_BY_CYLINDER[cylinder]);ef=src.plug_frame(cylinder)
  start,exit=src.point(sf,116),src.point(sf,145);approach,end=src.point(ef,80),src.point(ef,46)
  lane=b.Vector((exit.X+approach.X)/2,src.LANE_Y[cylinder],340+cylinder*12)
  import math
  travel=b.Vector(math.copysign(min(60,abs(exit.X-approach.X)/4),approach.X-exit.X),0,0)
  controls=[exit,exit+src.direction(sf)*20,lane-travel,lane]
  changed=[controls[0]+D,controls[1]+D,controls[2],controls[3]]
  fixed=b.Bezier(lane,lane+travel,approach+src.direction(ef)*50,approach)
  edges=[b.Line(start+D,exit+D),b.Bezier(*changed),fixed,b.Line(approach,end)]
  return b.Wire(edges),b.Pos(*DELTA)*sf,{'old_controls':[list(x) for x in controls],'new_controls':[list(x) for x in changed],'fixed_path':b.Wire([fixed,b.Line(approach,end)]),'fixed_frame':ef,'cap_frame':b.Pos(*DELTA)*sf}
 sf=src.coil_frame();ef=src.cap_frame();start,exit=src.point(sf,62),src.point(sf,92);approach,end=src.point(ef,175),src.point(ef,116);lane=b.Vector(130,300,400)
 fixed=b.Bezier(exit,exit+b.Vector(50,0,0),lane-b.Vector(20,0,0),lane)
 controls=[lane,lane+b.Vector(20,0,0),approach+src.direction(ef)*50,approach];changed=[controls[0],controls[1],controls[2]+D,controls[3]+D]
 edges=[b.Line(start,exit),fixed,b.Bezier(*changed),b.Line(approach+D,end+D)]
 return b.Wire(edges),sf,{'old_controls':[list(x) for x in controls],'new_controls':[list(x) for x in changed],'fixed_path':b.Wire([b.Line(start,exit),fixed]),'fixed_frame':sf,'cap_frame':b.Pos(*DELTA)*ef}
def build(cylinder=None):
 path,frame,data=path_and_contract(cylinder);jacket,core=src.cable(path,frame)
 prefix=f'ignition-lead-{cylinder}' if cylinder else 'ignition-coil-lead'
 return {prefix+'-jacket':jacket,prefix+'-carbon-core':core,prefix+'-cap-boot':data['cap_frame']*src.cap_boot(),prefix+'-cap-contact':data['cap_frame']*src.cap_contact()},data
