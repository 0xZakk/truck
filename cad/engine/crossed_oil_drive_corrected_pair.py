"""Estimated corrected signed-lead pair. No complete shaft or axis changes."""
import math
import build123d as b
import oil_drive_layout as old
TEETH=16
PITCH_RADIUS=18.
WIDTH=12.
CAM_PHASE=2.5
DISTRIBUTOR_PHASE=11.25
ROOT_RADIUS=PITCH_RADIUS-1.25*(2*PITCH_RADIUS*math.cos(math.radians(45))/TEETH)
def tooth_blank(phase=0):
 pitch=PITCH_RADIUS;teeth=TEETH;module=2*pitch*math.cos(math.radians(45))/teeth;pressure=math.atan(math.tan(math.radians(20))/math.cos(math.radians(45)));base=pitch*math.cos(pressure);root=pitch-1.25*module;tip=pitch+module
 def involute(r):
  t=math.sqrt(max(0,(r/base)**2-1));return t-math.atan(t)
 half=math.pi/(2*teeth)-.25/(2*pitch);radii=[max(base,root)+(tip-max(base,root))*i/7 for i in range(8)];points=[]
 for i in range(teeth):
  angle=math.tau*i/teeth;profile=[(root,angle-math.pi/teeth),(root,angle-half-involute(pitch))];profile +=[(r,angle-half-involute(pitch)+involute(r))for r in radii];profile +=[(r,angle+half+involute(pitch)-involute(r))for r in reversed(radii)];profile +=[(root,angle+half+involute(pitch))];points +=[(r*math.cos(a),r*math.sin(a))for r,a in profile]
 twist=math.degrees(WIDTH/pitch);face=b.Polygon(*points,align=None).face();s=b.Solid.extrude_linear_with_rotation(face,(0,0,0),(0,0,WIDTH),twist)
 return b.Pos(0,0,-WIDTH/2)*b.Rot(0,0,phase-twist/2)*s

def pair():
 cam=b.Rot(0,90,0)*tooth_blank(CAM_PHASE)
 distributor=tooth_blank(DISTRIBUTOR_PHASE)+old.axial_cylinder(9,5.9,24)
 distributor-=old.axial_cylinder(6.05,-7,25)
 distributor-=b.Solid.make_cylinder(1.55,22,b.Plane(origin=(-11,0,15),z_dir=(1,0,0)))
 return cam,distributor
