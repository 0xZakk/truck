"""Shared v2 seat: full radius10 protected socket flats; no neighbor carving."""
import math
import build123d as b
import timing_cover_front_joint_candidate as joint
from timing_cover_attachment_v2 import norm,RELOCATIONS
START=300.;STRAIGHT_END=310.;RETURN_END=355.;FRONT=365.
ML=1.5/45;MR=75/45
BL=-123-ML*310+4*math.sqrt(1+ML*ML)
BR=109-MR*310-4*math.sqrt(1+MR*MR)
LX=(BL+150)/(.1-ML);LK=(-117.5-BL)/ML
RK0=(105-BR)/MR;RK1=(180-BR)/MR
wall_outer=[(300,-123),(310,-123),(355,-121.5),(378,-121.5),(378,184),(355,184),(310,109),(300,109)]
wall_inner=[(295,-120),(300,-120),(LX,.1*LX-150),(LK,-117.5),(374,-117.5),(374,180),(RK1,180),(RK0,105),(310,105),(300,106),(295,106)]
def clip_x(s,lo,hi):return norm(s.intersect(b.Pos((lo+hi)/2,0,0)*b.Box(hi-lo,1000,1000)))
def seat_z(x):return -32+7.5*(x-START)/(FRONT-START)
def interp(x,points):
 for (a,u),(d,v) in zip(points,points[1:]):
  if a-1e-8<=x<=d+1e-8:return u+(v-u)*(x-a)/(d-a)
 raise ValueError(x)
def side_limits(x,footprint):
 t=(x-300)/65;left_outer=-141-8*t;right_outer=117+96*t
 gl=-130+15*t;gr=106+73*t
 if footprint=='gasket':return left_outer,gl,gr,right_outer
 li=interp(x,[(300,-120),(LX,.1*LX-150),(LK,-117.5),(365,-117.5)])
 ri=interp(x,[(300,106),(310,105),(RK0,105),(RK1,180),(365,180)])
 return left_outer,max(li,-120+5*t),min(ri,gr),right_outer

def band(bottom_offset,top_offset,footprint='pan',holes=False):
 assert footprint in ('pan','gasket') and top_offset>bottom_offset
 stations=sorted(set([300.,310.,LX,LK,RK0,RK1,355.,365.]))
 # Include exact switches of max/min footprint branches; no unrecorded chord.
 for points,baseline in [([(300,-120),(LX,.1*LX-150),(LK,-117.5),(365,-117.5)],lambda x:-120+5*(x-300)/65), ([(300,106),(310,105),(RK0,105),(RK1,180),(365,180)],lambda x:106+73*(x-300)/65)]:
  for (a,u),(d,v)in zip(points,points[1:]):
   fa=u-baseline(a);fd=v-baseline(d)
   if fa*fd<0:stations.append(a+(d-a)*(-fa)/(fd-fa))
 stations=sorted(set(stations))
 pieces=[]
 for side in [0,1]:
  sections=[]
  for x in stations:
   l,li,ri,r=side_limits(x,footprint);a,d=(l,li)if side==0 else(ri,r)
   sections.append(b.Plane(origin=(x,(a+d)/2,seat_z(x)+(bottom_offset+top_offset)/2),x_dir=(0,1,0),z_dir=(1,0,0))*b.Rectangle(d-a,top_offset-bottom_offset))
  pieces.append(b.loft(sections,ruled=True))
 pieces.append(clip_x(joint.front_blank(bottom_offset,top_offset)[0],365,500))
 s=norm(pieces[0].fuse(*pieces[1:]))
 for n in [20,10]:
  x,y,z=RELOCATIONS[n];s=norm(s.cut(joint.disk(10,x,y,-220,180)));s=norm(s.fuse(joint.disk(10,x,y,-24.5+bottom_offset,-24.5+top_offset)))
 if holes:
  for x,y,z in RELOCATIONS.values():s=norm(s.cut(joint.disk(4.3,x,y,-220,180)))
 return s

def pan_flange():return band(-6,-2,'pan',True)
def gasket_band():return band(-2,0,'gasket',True)
def below_mating_seat():return band(-160,0,'pan',False)
def upper_wall_envelope():return band(-160,-6,'pan',False)

def transition_seat_support(height=8):
 """Estimated extra casting land above gasket top; block worker proves joins.

 Eight mm is an explicit model estimate, not a strength/minimum-wall claim.
 Retain clearance holes to avoid overwriting existing female socket geometry.
 """
 return clip_x(band(0,height,'gasket',True),300,365)

def transition_below_seat():return clip_x(below_mating_seat(),300,365)
