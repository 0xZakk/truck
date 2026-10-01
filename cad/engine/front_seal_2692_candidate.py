"""Estimated internal2692 study with sourced replacement envelope; no installation."""
from pathlib import Path
import math
import build123d as b
import front_crank_seal_envelope_candidate as e
ROOT=Path(__file__).resolve().parents[2]
REAR=420.;AIR=REAR+e.WIDTH;FLANGE_T=.8;SEAT=AIR-FLANGE_T
BORE_R=e.HOUSING_BORE/2;TRACK_R=e.SHAFT_DIAMETER/2;FLANGE_R=e.FLANGE_DIAMETER/2
SPRING_X=426.6;SPRING_R=25.6;COIL_R=.45;WIRE_R=.12;TURNS=96

def cx(r,a,z):return e.cylinder(r,a,z)
def ring(ro,ri,a,z):return cx(ro,a,z).cut(cx(ri,a-1,z+1))
def cover_mask():return ring(43,24,406,434.4112)
def hub_mask():return ring(27.000001,TRACK_R,419,435.5)
def cover_adapter(old):return old.fuse(ring(43,24,406,SEAT)).cut(cx(BORE_R,REAR,AIR+1))
def hub_adapter(old_world):return old_world.cut(ring(27.01,TRACK_R,419,435.5))
def case(free=False):
 ro=e.CASE_DIAMETER/2 if free else BORE_R
 outer=ring(ro,BORE_R-.8,REAR,SEAT)
 rear=ring(ro,27.6,REAR,REAR+.8)
 inner=ring(28.4,27.6,REAR,429.4)
 flange=ring(FLANGE_R,BORE_R-.8,SEAT,AIR)
 return outer.fuse(rear).fuse(inner).fuse(flange)
def spring_envelope():return b.Pos(SPRING_X,0,0)*b.Rot(0,90,0)*b.Torus(SPRING_R,COIL_R+WIRE_R)
def elastomer():
 profile=b.Polygon((426.2,24.6),(427.9,TRACK_R),(428.2,TRACK_R),(429.4,24.8),(429.4,27.6),(426.5,27.6),align=None)
 return b.revolve(profile,axis=b.Axis.X).cut(spring_envelope())
def spring():
 # 48 circular sections per turn. Sew ruled side faces to avoid the invalid
 # long-periodic-sweep result; this is an explicitly approximated winding.
 # Nominal coil/strand radii and 96 turns are unchanged. No modeled end joint.
 from OCP.BRepBuilderAPI import BRepBuilderAPI_Sewing
 from OCP.TopoDS import TopoDS
 wires=[]
 for i in range(49):
  t=2*math.pi/TURNS*i/48;u=TURNS*t;r=SPRING_R+COIL_R*math.cos(u);dr=-COIL_R*TURNS*math.sin(u)
  p=(SPRING_X+COIL_R*math.sin(u),r*math.cos(t),r*math.sin(t))
  tangent=(COIL_R*TURNS*math.cos(u),dr*math.cos(t)-r*math.sin(t),dr*math.sin(t)+r*math.cos(t))
  normal=(math.sin(u),math.cos(u)*math.cos(t),math.cos(u)*math.sin(t))
  wires.append((b.Plane(origin=p,x_dir=normal,z_dir=tangent)*b.Circle(WIRE_R)).face().outer_wire())
 side=[]
 for i in range(48):
  piece=b.Solid.make_loft(wires[i:i+2],ruled=True)
  side.extend(f for f in piece.faces() if f.geom_type!=b.GeomType.PLANE)
 sew=BRepBuilderAPI_Sewing(1e-6)
 for j in range(TURNS):
  for f in side:sew.Add((b.Rot(360*j/TURNS,0,0)*f).wrapped)
 sew.Perform()
 return b.Solid(b.Shell(TopoDS.Shell_s(sew.SewedShape())))
