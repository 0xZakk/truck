"""Illustrative ONE torsion spring, explicitly not Ford count/construction.

Integration lead authorized this educational scope; all dimensions estimated.
World CAD frame. Fixed bracket hook never rotates; moving hook follows Y axis.
"""
import math
from functools import lru_cache
import numpy as np
import build123d as b
import throttle_linkage_candidate as linkage
import throttle_shield_candidate as shield
PARAMS=dict(wire_radius=.45,initial_radius=8.8,turns=3.,coil_y_fixed=100.,coil_y_moving=94.,fixed_angle_deg=math.degrees(math.atan2(-5,13)),anchor_radius=math.sqrt(194),moving_radius=18.)
AXIS=np.array([394.,25.,490.])
def point(radius,angle,y):return np.array([394+radius*math.sin(angle),y,490+radius*math.cos(angle)])
def path_points(angle,radius):
 wire=centerline(angle,radius)
 return np.array([tuple(wire.position_at(t)) for t in np.linspace(0,1,801)])
def length(points):return float(np.linalg.norm(np.diff(points,axis=0),axis=1).sum())
@lru_cache(maxsize=512)
def centerline(angle,radius):
 p=PARAMS;a=math.radians(p['fixed_angle_deg']);t=math.radians(angle)
 span=2*math.pi*p['turns']+t-a;delta=.18;R=radius;A=p['anchor_radius'];edges=[]
 def P(r,u,y):return tuple(point(r,u,y))
 def line(x,y):edges.append(b.Edge.make_line(x,y))
 def bez(*pts):edges.append(b.Edge.make_bezier(*pts))
 line(P(A+2,a,107),P(A+1,a,107))
 bez(P(A+1,a,107),P(A,a,107),P(A,a,106))
 line(P(A,a,106),P(A,a,101))
 bez(P(A,a,101),P(A,a,100),P(A-1,a,100))
 line(P(A-1,a,100),P(R+1,a,100))
 helix=b.Pos(394,100-6*delta/span,490)*b.Rot(0,math.degrees(a+delta)-90,0)*b.Rot(90,0,0)*b.Edge.make_helix(6*2*math.pi/span,6*(1-2*delta/span),R,lefthand=True)
 h0=np.array(tuple(helix.position_at(0)));h1=np.array(tuple(helix.position_at(1)))
 v0=np.array(tuple(helix.tangent_at(0)));v1=np.array(tuple(helix.tangent_at(1)))
 bez(P(R+1,a,100),P(R+.4,a,100),tuple(h0-.7*v0),tuple(h0))
 edges.extend(helix.edges())
 bez(tuple(h1),tuple(h1+.7*v1),P(R+.4,t,94),P(R+1,t,94))
 line(P(R+1,t,94),P(17,t,94))
 bez(P(17,t,94),P(18,t,94),P(18,t,93))
 line(P(18,t,93),P(18,t,88.5))
 bez(P(18,t,88.5),P(18,t,87.5),P(19,t,87.5))
 line(P(19,t,87.5),P(20,t,87.5))
 return b.Wire(edges)

def analytical_length(angle,radius):
 # Exact CAD curve length includes the tangent-continuous bend transitions.
 return centerline(angle,radius).length

@lru_cache(maxsize=181)
def radius_at(angle):
 target=analytical_length(0,PARAMS['initial_radius']);lo,hi=6.,10.
 for _ in range(35):
  mid=(lo+hi)/2
  if analytical_length(angle,mid)>target:hi=mid
  else:lo=mid
 return (lo+hi)/2

def spring(angle):
 wire=centerline(angle,radius_at(angle))
 profile=b.Plane(origin=wire.position_at(0),z_dir=wire.tangent_at(0))*b.Circle(PARAMS['wire_radius'])
 return b.sweep(profile,path=wire,is_frenet=True).clean()


def seats(existing_shaft):
 fixed=shield.parts();moving=linkage.parts(existing_shaft)
 # Captured through-holes. Hooks extend behind both plate backs; wire legs
 # on opposite faces prevent straight axial disengagement in this abstraction.
 r=PARAMS['wire_radius']+.05
 a=math.radians(PARAMS['fixed_angle_deg']);f=point(PARAMS['anchor_radius'],a,104)
 fixed['accelerator-bracket-spring-seat-estimated']=fixed.pop('accelerator-bracket-shield-hole-estimated')-b.Pos(*f)*linkage.cy(r,6)
 moving['throttle-lever-spring-seat-estimated']=moving.pop('throttle-lever-estimated')-b.Pos(0,65,18)*linkage.cy(r,6)
 return fixed,moving
