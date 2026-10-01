"""Source-sector orientation hypothesis; all metric inlet dimensions remain estimates."""
from pathlib import Path
import build123d as b
import water_pump_joint_candidate as pump
import water_pump_inlet_v3_candidate as inlet
import timing_pump_rear_flange_candidate as rear
R=Path(__file__).resolve().parents[2];O=R/'cad/engine/generated/waterpump-source-offset-inlet-candidate'
ANGLE=-130.;NOMINAL=6.;ANGLES=(NOMINAL,-1.0714774533552998,12.777418688313674)
SOURCE=R/'cad/engine/generated/water-pump-housing.step';FROZEN_REAR=rear.O/'housing.step'
FRAME=b.Pos(*pump.PUMP_POSITION)
from cooling_connections import cylinder
AXIS_X=-10.;END_Y=145.
def cy(radius,start,end,offset):return cylinder(radius,end-start,(AXIS_X,(start+end)/2,offset),(0,1,0))
def section(y,r,x,offset):return b.Plane(origin=(x,y,offset),z_dir=(0,1,0))*b.Circle(r)
def outer(offset):return b.loft([section(y,r,x,offset)for y,r,x in [(20,29,-20),(60,29,-10),(96,24,-10),(145,24,-10)]],ruled=True)+cy(25.5,140,143,offset)
def passage(offset):return b.loft([section(y,20,x,offset)for y,x in [(19,-20),(60,-10),(146,-10)]],ruled=True)
def open_probe(offset):return b.loft([section(y,2,x,offset)for y,x in [(10,-20),(19,-20),(60,-10),(146,-10)]],ruled=True)
def build(offset=NOMINAL):
 canonical=b.import_step(SOURCE);base=pump.housing_interface(canonical);old=inlet.housing_interface(base)
 rot=b.Rot(ANGLE,0,0);stock=rot*outer(offset);void=rot*passage(offset);fresh=(base+stock)-void
 return rear.norm((FRAME*fresh).cut(rear.masks()['housing'])),FRAME*old,FRAME*base,FRAME*stock,FRAME*void
