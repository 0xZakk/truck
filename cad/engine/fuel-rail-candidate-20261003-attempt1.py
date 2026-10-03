"""Approved isolated +/- transverse fuel studies. No canonical mutations."""
from pathlib import Path
import json,hashlib,math
import build123d as b
from assembly_math import transforms
ROOT=Path(__file__).resolve().parents[2]
PARAM=Path(__file__).with_name('fuel-rail-candidate-20261003-parameters.json')
P=json.loads(PARAM.read_text())
MANIFEST=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())
DEFS={d['id']:d for d in MANIFEST['definitions']}
OCC={o['id']:o for o in MANIFEST['occurrences']}
POSES=transforms(MANIFEST)
def baseline(ident):return b.import_step(ROOT/DEFS[ident]['step'].lstrip('/'))
def solid(s):return b.Compound(children=list(s)) if isinstance(s,b.ShapeList) else s
def cyl(r,a,z,x=0,y=0):return b.Pos(x,y,(a+z)/2)*b.Cylinder(r,z-a)
def line(a,c):return b.Edge.make_line(a,c)
def arc(a,mid,c):return b.Edge.make_three_point_arc(a,mid,c)
def sweep(edges,r):
 w=b.Wire(edges);return b.sweep(b.Plane(origin=w@0,z_dir=w%0)*b.Circle(r),path=w,is_frenet=True)
def paths(sign):
 gy=-163+24*sign;q=math.sqrt(.5)
 rear=[line((-354.997,-163,410),(-354.997,-163,387)),arc((-354.997,-163,387),(-336.997-18*q,-163,387-18*q),(-336.997,-163,369)),line((-336.997,-163,369),(280.618,-163,369))]
 loop=arc((280.618,-163,369),(293.618,-163+12*sign,364),(280.618,gy,359))
 rise=[line((280.618,gy,359),(204.136,gy,359)),arc((204.136,gy,359),(204.136-18*q,gy,377-18*q),(186.136,gy,377))]
 supply=rear+[loop]+rise
 ret=[line((174.136,gy,383.5),(174.136,gy,381)),arc((174.136,gy,381),(162.136+12*q,gy,381-12*q),(162.136,gy,369)),line((162.136,gy,369),(-320.238,gy,369)),arc((-320.238,gy,369),(-320.238-12*q,gy,381-12*q),(-332.238,gy,381)),line((-332.238,gy,381),(-332.238,gy,410))]
 return supply,ret

def parts(sign):
 gy=-163+24*sign;gx=174.136;G=b.Pos(gx,gy,385)
 supply,ret=paths(sign)
 outer=sweep(supply+[line((186.136,gy,377),(186.136,gy,381))],6)
 inner=sweep(supply,4.5)+b.Pos(186.136,gy,379)*b.Cone(4.5,3,4)
 xs=[259.48-113.792*i for i in range(6)]
 rail=outer
 for x in xs:rail+=cyl(9,350,370,x,-163)
 for x in [-250,-40,220]:rail+=b.Pos(x,-163,367)*b.Box(18,46,6)
 flange=cyl(20,377.5,383,gx,gy)
 for angle in [0,120,240]:
  dx=24*math.cos(math.radians(angle));dy=24*math.sin(math.radians(angle))
  flange+=cyl(5,377.5,383,gx+dx,gy+dy)
  flange+=b.Pos(gx+dx/2,gy+dy/2,380.25)*b.Box(abs(dx)+2,abs(dy)+2,5.5)
 flange=solid(flange)
 rail+=flange;rail=solid(rail)
 rail-=inner
 for x in xs:rail-=cyl(7.6,347,371,x,-163)
 for x in [-250,-40,220]:rail-=cyl(3.4,362,372,x,-178)
 # Supply annulus and central socket remain distinct.
 gallery=cyl(16,379,383.001,gx,gy)-cyl(7,378.9,383.1,gx,gy)
 rail-=gallery;rail-=cyl(4.55,377,384,gx,gy)
 for angle in [0,120,240]:rail-=cyl(2.2,377,384,gx+24*math.cos(math.radians(angle)),gy+24*math.sin(math.radians(angle)))
 # Retained diagnostic branch, exact old station.
 rail+=cyl(5,370,378,100,-163);rail-=cyl(3,366,380,100,-163)
 rail=solid(rail)
 return_outer=sweep(ret,4)+cyl(4.5,377,383.5,gx,gy)
 return_inner=sweep(ret,2.8)
 returned=solid(return_outer-return_inner)
 returned-=b.Pos(gx,gy,378)*b.Torus(4.25,.25)
 defs={'fuel-supply-rail':rail,'fuel-return-tube':solid(returned)}
 for key,rad in [('regulator-lower-housing',2.5),('regulator-gasket',2.5),('regulator-inlet-screen',1.2)]:
  shape=baseline(key)
  for k in range(8):
   a=k*math.pi/4;shape-=cyl(rad,-4,4,11.5*math.cos(a),11.5*math.sin(a))
  defs[key]=solid(shape)
 # Existing fitting remains stationary; only hose changes.
 controls=[(gx,gy,420),(gx,gy,444),(145,(-120 if sign==1 else -170),460),(80,-90,460),(0,-75,460),(0,-55,460)]
 route=b.Bezier(*controls);plane=b.Plane(origin=route@0,z_dir=route%0)
 hose=b.sweep(plane*b.Circle(6),path=route,is_frenet=True)-b.sweep(plane*b.Circle(4.1),path=route,is_frenet=True)
 hose-=cyl(4.15,419,430,gx,gy);defs['regulator-vacuum-hose']=solid(hose)
 worlds={};poses={};reused={}
 for ident in ['fuel-supply-rail','fuel-return-tube','regulator-vacuum-hose']:
  worlds[ident]=defs[ident];poses[ident]=b.Pos()
 for ident,o in OCC.items():
  if o['parent']=='fuel-regulator':
   local=defs.get(o['definition'])
   if local is None:local=baseline(o['definition']);reused[o['definition']]=local
   pose=G*b.Pos(*o['position_cad_mm'])*b.Rot(*o['rotation_cad_deg']);worlds[ident]=pose*local;poses[ident]=pose
  if o['parent'] in ['fuel-supply-coupling','fuel-return-coupling']:
   is_supply=o['parent']=='fuel-supply-coupling';origin=(-354.997,-163,410) if is_supply else (-332.238,gy,410)
   local=baseline(o['definition']);reused[o['definition']]=local
   pose=b.Pos(*origin)*b.Rot(0,90,0)*b.Pos(*o['position_cad_mm'])*b.Rot(*o['rotation_cad_deg'])
   worlds[ident]=pose*local;poses[ident]=pose
 return defs,worlds,poses,{'gx':gx,'gy':gy,'supply_gallery':gallery,'return_inner':return_inner,'supply_inner':inner,'reused':reused}
