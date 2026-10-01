"""Trial1 estimated PS/AC/TENS matched load-path prototype; not factory casting CAD."""
from pathlib import Path
import json,math
import build123d as b
import accessory_brackets as base
import accessory_carrier_1994 as old
R=Path(__file__).resolve().parents[2];SELECT=json.loads((R/'inventory/engine/accessory-constrained-layout-step-check.json').read_text());C=SELECT['selection']['centers_yz_mm'];FACE=432.56
PS_EARS=[(y+SELECT['posedelta_yz_mm']['PS'][0],z+SELECT['posedelta_yz_mm']['PS'][1])for y,z in base.PS_EARS]
AC_EARS=[(y+SELECT['posedelta_yz_mm']['AC'][0],z+SELECT['posedelta_yz_mm']['AC'][1])for y,z in base.AC_EARS]
PIVOT=(C['TENS'][0],C['TENS'][1]+75);SIDE=[*old.BLOCK_STATIONS,old.HEAD_SIDE]
def union(s,*others):
 q=s.fuse(*others)
 return b.Compound(children=list(q))if isinstance(q,b.ShapeList)else q

def carrier():
 py,pz=C['PS'];ay,az=C['AC'];left=ay-90;right=ay+90
 s=base.boss(FACE,py,pz,79,68)
 for y,z in PS_EARS:
  dy,dz=y-py,z-pz;s=union(s,base.web(FACE,(y,z),(py+dy*75/62,pz+dz*75/62)),base.boss(FACE,y,z,10,4.8))
 for y,z in AC_EARS:s=union(s,base.boss(FACE,y,z,11,5.5),base.web(FACE,(y,z),(left if y<ay else right,z),18))
 # Open frame, joined to upper annulus; inherited ear stock is preserved.
 paths=[[(py-78,pz),(left,az+90),(left,50),(right,50),(right,pz),(py+78,pz)]]
 for path in paths:
  for a,c in zip(path[:-1],path[1:]):s=union(s,base.web(FACE,a,c,18))
 target_y=(py-78)+(left-(py-78))*(pz-300)/(pz-(az+90))
 s=union(s,base.engine_foot(90,300,FACE+5,target_y))
 for x,z in SIDE:s=union(s,old.sideways(16,28,x,149,z))
 for a,c in [((292,155,110),(340,155,110)),((340,155,110),(340,155,310)),((292,155,110),(340,155,310)),((340,155,270),(FACE+5,left,az+90)),((340,155,310),(FACE+5,target_y,300))]:s=union(s,old.bridge(a,c))
 ty,tz=PIVOT;s=union(s,base.axial(32,20,(390.56,ty,tz)),old.bridge((390.56,ty+25,tz),(390.56,ty+45,tz),18),old.bridge((390.56,ty+45,tz),(FACE+5,py-78,pz),18))
 for y,z in PS_EARS:s=s.cut(base.axial(4.8,14,(FACE+5,y,z)))
 for y,z in AC_EARS:s=s.cut(base.axial(5.5,14,(FACE+5,y,z)))
 s=s.cut(base.axial(5.5,22,(379,90,300)),base.axial(11,20,(395,90,300)))
 for x,z in SIDE:s=s.cut(old.sideways(5.5,40,x,155,z),old.sideways(13,58,x,192,z))
 s=s.cut(base.axial(5.8,17,(393.06,ty,tz)),base.axial(6.35,13,(395.06,ty+20,tz)))
 return s
