"""Analytic matched open cradles, all routing dimensions explicitly estimated."""
from pathlib import Path
import json
import build123d as b
import accessory_brackets as base
R=Path(__file__).resolve().parents[2]
SELECT=json.loads((R/'inventory/engine/accessory-constrained-layout-step-check.json').read_text())
CENTERS=SELECT['selection']['centers_yz_mm']
ENGINE_SEATS=[(-100,220),(-100,310),(-100,90),(-125,140)]
FACES={'ALT':438.56,'AP':449.06}
EARS={g:[(CENTERS[g][0]+dy,CENTERS[g][1])for dy in (-r,r)]for g,r in [('ALT',77),('AP',85)]}
def union(shape,*others):
 result=shape.fuse(*others)
 return b.Compound(children=list(result))if isinstance(result,b.ShapeList)else result
def band(g):
 y,z=CENTERS[g];ro,ri=(88,70)if g=='ALT'else(98,78);f=FACES[g]
 # Source topology: upper cradle open below, lower cradle open above.
 shape=base.boss(f,y,z,ro,ri)
 direction=1 if g=='ALT'else -1
 keep=b.Pos(f+5,y,z+direction*100)*b.Box(12,240,200)
 shape=shape.intersect(keep)
 for ey,ez in EARS[g]:shape=union(shape,base.boss(f,ey,ez,11,5.5))
 return shape

def carrier():
 shape=union(band('ALT'),band('AP'))
 # Inboard spine is a ruled solid between the two inboard ear neighborhoods.
 a=(FACES['ALT']+5,EARS['ALT'][1][0]+7,CENTERS['ALT'][1]);p=(FACES['AP']+5,EARS['AP'][1][0]+7,CENTERS['AP'][1])
 sections=[b.Plane(origin=q,z_dir=(0,0,1))*b.Rectangle(10,18)for q in [p,a]]
 shape=union(shape,b.loft(sections,ruled=True))
 # Same-height feet end on an analytic extension of that inboard spine.
 for y,z in ENGINE_SEATS:
  u=(z-p[2])/(a[2]-p[2]);x=p[0]+u*(a[0]-p[0]);target=p[1]+u*(a[1]-p[1])
  shape=union(shape,base.engine_foot(y,z,x,target))
 # Extend spine to both extreme engine-foot elevations with the same line.
 sections=[]
 for z in [80,320]:
  u=(z-p[2])/(a[2]-p[2]);sections.append(b.Plane(origin=(p[0]+u*(a[0]-p[0]),p[1]+u*(a[1]-p[1]),z),z_dir=(0,0,1))*b.Rectangle(10,18))
 shape=union(shape,b.loft(sections,ruled=True))
 for g in EARS:
  for y,z in EARS[g]:shape=shape.cut(base.axial(5.5,20,(FACES[g]+5,y,z)))
 for y,z in ENGINE_SEATS:
  shape=shape.cut(base.axial(5.5,22,(379,y,z)),base.axial(11,20,(395,y,z)))
 return shape
