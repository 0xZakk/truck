"""Coordinated inferred heater root/tube; no factory dimensional claim."""
from pathlib import Path
import math,numpy as np,build123d as b
import waterpump_source_offset_inlet_candidate as inlet
from cooling_connections import cylinder
R=inlet.R;O=R/'cad/engine/generated/waterpump-heater-source-candidate'
pump=inlet.pump;rear=inlet.rear;FRAME=inlet.FRAME
ROOT=np.array([410.,-80.,230.3]);DIR=np.array([0.,math.cos(math.radians(145)),math.sin(math.radians(145))]);END=np.array([236.,-171.,415.]);ENDDIR=np.array([-.68,-.28,.67]);ENDDIR/=np.linalg.norm(ENDDIR)
def segment(r,a,z):
 d=np.array(z)-np.array(a);return b.Solid.make_cylinder(r,float(np.linalg.norm(d)),b.Plane(origin=tuple(a),z_dir=tuple(d)))
def bare_base(old):
 # Replay source chamber, lugs and fifth passage exactly; omit only heater operations.
 s=old & (b.Pos(110,0,0)*b.Box(168,500,500))
 def section(x,r):return b.Pos(x,0,0)*b.Rot(0,90,0)*b.Circle(r)
 outer=b.loft([section(x,r)for x,r in [(-65,66),(-57,66),(-51,55),(18,29)]],ruled=True)
 inner=b.loft([section(x,r)for x,r in [(-66,59),(-57,59),(-51,51),(18,24),(27,24)]],ruled=True)
 s+=(outer+pump.cx(29,18,26))-inner
 for y,z in pump.MOUNTING:s+=pump.cx(11.5,-65,-51,y,z)
 s+=pump.cx(11.5,-65,-46,*pump.EXTRA)
 for y,z in pump.MOUNTING:s-=pump.cx(4.3,-66,-50,y,z)
 s-=pump.cx(6.5,-66,-51,*pump.EXTRA)
 y,z=pump.EXTRA;inside=(y*.78,z*.78)
 s-=b.Solid.make_cylinder(6.5,math.hypot(y-inside[0],z-inside[1]),b.Plane(origin=(-54,y,z),z_dir=(0,inside[0]-y,inside[1]-z)))
 return s
P0=ROOT+25*DIR;P1=ROOT+70*DIR;P3=END-25*ENDDIR;P2=P3-65*ENDDIR
START=ROOT-12*DIR

def path():return b.Wire([b.Edge.make_line(tuple(START),tuple(P0)),b.Edge.make_bezier(tuple(P0),tuple(P1),tuple(P2),tuple(P3)),b.Edge.make_line(tuple(P3),tuple(END))])
def sweep(radius):return b.sweep(b.Plane(origin=tuple(START),z_dir=tuple(DIR))*b.Circle(radius),path())
def tube():return (sweep(8)+segment(8.5,END-5*ENDDIR,END-3*ENDDIR))-sweep(6.5)
def build():
 old=b.import_step(inlet.SOURCE);base=bare_base(old)
 # Independent replay of removed old analytical heater construction.
 replay=base+cylinder(12,32,(-2,-45,15),(0,1,0));replay-=cylinder(8.1,39,(-2,-44.5,15),(0,1,0));replay-=cylinder(8.1,26,(-2,-67,15),(0,-1,0))
 rot=b.Rot(inlet.ANGLE,0,0);largeouter=rot*inlet.outer(inlet.NOMINAL);largevoid=rot*inlet.passage(inlet.NOMINAL)
 oldworld=rear.norm((FRAME*((replay+largeouter)-largevoid)).cut(rear.masks()['housing']))
 s=FRAME*((base+largeouter)-largevoid)
 s+=segment(12,ROOT-42*DIR,ROOT)
 s-=segment(6.5,ROOT-46*DIR,ROOT+DIR)
 s-=segment(8,START,ROOT+DIR)
 s=rear.norm(s.cut(rear.masks()['housing']))
 return s,tube(),oldworld
