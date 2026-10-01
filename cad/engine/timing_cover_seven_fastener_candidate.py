"""Bounded comparison trial; preserves frozen inputs, factory application unknown."""
from pathlib import Path
import math,hashlib
import build123d as b
import timing_cover_front_joint_candidate as front
import timing_cover_attachment_v2 as pan
ROOT=Path(__file__).resolve().parents[2]
BLOCK=ROOT/'cad/engine/generated/timing-front-block-expanded-seat-v3-candidate/block.step'
COVER=ROOT/'cad/engine/generated/front-seal-2692-candidate/cover.step'
SEAT=379.8;LENGTH=22.225;PITCH=25.4/18;MAJOR=7.9375
SUPPORT_BACK=354.575;HOLE_BACK=356.575;SUPPORT_RADIUS=8.;ACCESS_RADIUS=10.5
HEAD_RADIUS=8.75;HEAD_HEIGHT=5.3;HEX_AF=12.7;FLANGE_THICKNESS=1.6
AXES=[front.c.yz(p,front.P)for p in front.source.HOLES_NORMALIZED]
def norm(s):return b.Compound(children=list(s))if isinstance(s,b.ShapeList)else s
def cz(r,a,z):return b.Pos(0,0,(a+z)/2)*b.Cylinder(r,z-a)
def one(s):
 ss=s.solids()
 if len(ss)!=1:raise ValueError(f'Expected one solid, got {len(ss)}')
 return b.Solid(ss[0].wrapped)
def male():
 # Nominal source comparison thread; profile/runout/head are model estimates.
 half=.1+(MAJOR/2-3.)/math.sqrt(3)
 profile=b.Plane.XZ*b.Polygon((3.,-half),(MAJOR/2,-.1),(MAJOR/2,.1),(3.,half),align=None)
 loop=one(b.loft([b.Pos(0,0,PITCH*i/12)*b.Rot(0,0,360*i/12)*profile for i in range(13)]))
 coils=[b.Pos(0,0,PITCH*i)*loop for i in range(-1,math.ceil(LENGTH/PITCH)+1)]
 body=one(cz(3.2,-PITCH,LENGTH+PITCH).fuse(*coils));body=one(body.intersect(b.Pos(0,0,(1.7+LENGTH)/2)*b.Box(20,20,LENGTH-1.7)))
 head=b.Pos(0,0,-HEAD_HEIGHT)*b.extrude(b.RegularPolygon(HEX_AF/math.sqrt(3),6),amount=HEAD_HEIGHT-FLANGE_THICKNESS)
 return one(body+cz(3.2,0,1.71)+cz(MAJOR/2,0,1.6)+cz(HEAD_RADIUS,-FLANGE_THICKNESS,0)+head)
def frame(y,z):return b.Pos(SEAT,y,z)*b.Rot(0,-90,0)
def pan_socket_guards():
 return {n:b.Pos(x,y)*cz(10,z+7.6,z+23.6)for n,(x,y,z)in pan.RELOCATIONS.items()if n in[21,22,23]}
def build():
 assert hashlib.sha256(BLOCK.read_bytes()).hexdigest()=='66917915d9244f49cd96c2965315cba4bbb7007b236d36de67ac7c32fe4635b8'
 assert hashlib.sha256(COVER.read_bytes()).hexdigest()=='76f2210c143596b4b5c4d4c1361b1cbcc0cd91dde6e1088b6cf3e2b02713c66b'
 oldblock=b.import_step(BLOCK);oldcover=b.import_step(COVER);screw=male()
 local_region=cz(4.17,SEAT-373,SEAT-HOLE_BACK)
 # Analytical master thread cavity, not an assembled-neighbor subtraction.
 coupon=one(local_region.cut(one(screw.fuse(cz(4.,LENGTH-.1,LENGTH+1)))))
 cavity=norm(local_region.cut(coupon));supports={};pockets={};fullpockets={};screws={};coupons={};voids={};guards=pan_socket_guards()
 block=oldblock;cover=oldcover
 with b.SkipClean():
  for n,(y,z)in enumerate(AXES,1):
   supports[n]=front.c.cx(SUPPORT_RADIUS,SUPPORT_BACK,373,y,z);fullpockets[n]=front.c.cx(ACCESS_RADIUS,SEAT,435,y,z);pocket=fullpockets[n]
   for g in guards.values():pocket=norm(pocket.cut(g))
   pockets[n]=pocket;loc=frame(y,z);screws[n]=loc*screw;coupons[n]=loc*coupon;voids[n]=loc*cavity
   block=norm(block.fuse(supports[n]));cover=norm(cover.cut(pocket))
  for void in voids.values():block=norm(block.cut(void))
 return {'block':block,'cover':cover,**{f'main-cover-screw-{n}':s for n,s in screws.items()}},{'oldblock':oldblock,'oldcover':oldcover,'supports':supports,'pockets':pockets,'fullpockets':fullpockets,'screws':screws,'coupons':coupons,'voids':voids,'pan_guards':guards}
