"""Independent58/29 replacement-comparison hypothesis; no assembly adapter.

Source count PBM; diameters Elgin C-2766S interpreted as tooth-tip envelopes.
Module, helix, pressure angle, width, web holes and marks are estimates.
Canonical axes and parts are never written by this module.
"""
import math
import numpy as np
import build123d as b
from cam_retention import machine_gear_back
PARAMS=dict(crank_teeth=29,cam_teeth=58,transverse_module_mm=2.8,helix_angle_deg=25.,transverse_pressure_angle_deg=20.,width_mm=14.,backlash_mm=.12,crank_tip_diameter_mm=86.36,cam_tip_diameter_mm=167.894,crank_bore_radius_mm=21.025,cam_bore_radius_mm=15.9)
CENTER=PARAMS['transverse_module_mm']*(PARAMS['crank_teeth']+PARAMS['cam_teeth'])/2
AXIS_ANGLE=math.atan2(72,90)
CAM_YZ=(CENTER*math.cos(AXIS_ANGLE),CENTER*math.sin(AXIS_ANGLE))
def gear(teeth,tip,hand):
 p=PARAMS;r=p['transverse_module_mm']*teeth/2;base=r*math.cos(math.radians(p['transverse_pressure_angle_deg']));root=r-1.25*p['transverse_module_mm'];half=math.pi/(2*teeth)-p['backlash_mm']/(2*r)
 def inv(rad):t=math.sqrt(max(0,(rad/base)**2-1));return t-math.atan(t)
 radii=np.linspace(max(root,base),tip,10);pts=[]
 for i in range(teeth):
  a=2*math.pi*i/teeth
  profile=[(root,a-math.pi/teeth),(root,a-half-inv(r))]
  profile += [(rr,a-half-inv(r)+inv(rr)) for rr in radii]
  profile += [(rr,a+half+inv(r)-inv(rr)) for rr in reversed(radii)]
  profile += [(root,a+half+inv(r))]
  pts.extend((rr*math.cos(t),rr*math.sin(t)) for rr,t in profile)
 twist=hand*math.degrees(p['width_mm']*math.tan(math.radians(p['helix_angle_deg']))/r)
 face=(b.Plane.YZ*b.Polygon(*pts,align=None)).face()
 q=b.Solid.extrude_linear_with_rotation(face,(0,0,0),(p['width_mm'],0,0),twist)
 return b.Pos(-p['width_mm']/2,0,0)*b.Rot(-twist/2,0,0)*q

def parts():
 p=PARAMS;out={}
 for key,teeth,tip,hand in [('crank',p['crank_teeth'],p['crank_tip_diameter_mm']/2,1),('cam',p['cam_teeth'],p['cam_tip_diameter_mm']/2,-1)]:
  q=gear(teeth,tip,hand);phase=math.degrees(AXIS_ANGLE)+(180-180/teeth if key=='cam' else 0)
  q=b.Rot(phase,0,0)*q
  q-=b.Rot(0,90,0)*b.Cylinder(p[key+'_bore_radius_mm'],20)
  if key=='cam':
   q=machine_gear_back(q)
   # Two visible puller/web holes, explicitly estimated dimensions. Their
   # inner edges preserve the inherited central47mm relief interface.
   for y in [-58,58]:q-=b.Pos(0,y,0)*b.Rot(0,90,0)*b.Cylinder(10,20)
  out[key]=q
 return out

def posed(parts,crank_degrees=0,center=CENTER):
 return {'crank':b.Rot(crank_degrees,0,0)*parts['crank'],'cam':b.Pos(0,center*math.cos(AXIS_ANGLE),center*math.sin(AXIS_ANGLE))*b.Rot(-crank_degrees/2,0,0)*parts['cam']}
