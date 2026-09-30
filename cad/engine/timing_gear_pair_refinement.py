"""Source-visible interior shoulder/key/mark refinement of frozen tooth study.

All numeric shoulder/key/mark dimensions are explicit estimates. No tooth-ring
or installed-axis edits; no inference that the owner's gear is this replacement.
"""
import math
import build123d as b
import timing_gear_pair_candidate as base
PARAMS=dict(cam_recess_inner_radius_mm=26.,cam_recess_outer_radius_mm=70.,cam_recess_depth_mm=2.5,crank_recess_inner_radius_mm=26.,crank_recess_outer_radius_mm=33.,crank_recess_depth_mm=1.2,crank_key_width_mm=6.35,crank_key_depth_mm=3.175,cam_mark_radius_mm=.75,cam_mark_depth_mm=.6,crank_mark_depth_mm=.5)
def cylinder_x(radius,length):return b.Rot(0,90,0)*b.Cylinder(radius,length)
def parts(frozen):
 out={}
 for key,q in frozen.items():
  inner=PARAMS[key+'_recess_inner_radius_mm'];outer=PARAMS[key+'_recess_outer_radius_mm'];depth=PARAMS[key+'_recess_depth_mm']
  q=q-(b.Pos(7-depth/2,0,0)*(cylinder_x(outer,depth)-cylinder_x(inner,depth+1)))
  if key=='crank':
   r=base.PARAMS['crank_bore_radius_mm'];depth=PARAMS['crank_key_depth_mm']
   q-=b.Pos(0,0,r+depth/2-.05)*b.Box(16,PARAMS['crank_key_width_mm'],depth+.1)
   # An estimated triangular timing mark on the rim, aligned with modeled
   # reference mesh rather than a claimed factory key-to-mark station.
   phi=base.AXIS_ANGLE;r=35.;center=(r*math.cos(phi),r*math.sin(phi));t=(-math.sin(phi),math.cos(phi));u=(math.cos(phi),math.sin(phi))
   pts=[(center[0]+u[0],center[1]+u[1]),(center[0]-u[0]+t[0],center[1]-u[1]+t[1]),(center[0]-u[0]-t[0],center[1]-u[1]-t[1])]
   q-=b.Pos(6.5,0,0)*b.extrude(b.Plane.YZ*b.Polygon(*pts,align=None),amount=.6)
  else:
   phi=base.AXIS_ANGLE+math.pi;r=74.5
   q-=b.Pos(7-PARAMS['cam_mark_depth_mm']/2,r*math.cos(phi),r*math.sin(phi))*cylinder_x(PARAMS['cam_mark_radius_mm'],PARAMS['cam_mark_depth_mm']+.01)
  out[key]=q
 return out
