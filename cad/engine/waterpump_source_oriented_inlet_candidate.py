"""Source-sector orientation hypothesis; all metric inlet dimensions remain estimates."""
from pathlib import Path
import build123d as b
import water_pump_joint_candidate as pump
import water_pump_inlet_v3_candidate as inlet
import timing_pump_rear_flange_candidate as rear
R=Path(__file__).resolve().parents[2];O=R/'cad/engine/generated/waterpump-source-oriented-inlet-candidate'
NOMINAL=-130.;ANGLES=(NOMINAL,-147.14379790833655,-119.62711351597319)
SOURCE=R/'cad/engine/generated/water-pump-housing.step';FROZEN_REAR=rear.O/'housing.step'
FRAME=b.Pos(*pump.PUMP_POSITION)
def build(angle=NOMINAL):
 canonical=b.import_step(SOURCE);base=pump.housing_interface(canonical);old=inlet.housing_interface(base)
 rot=b.Rot(angle,0,0);outer=rot*inlet.outer();passage=rot*inlet.passage();fresh=(base+outer)-passage
 return rear.norm((FRAME*fresh).cut(rear.masks()['housing'])),FRAME*old,FRAME*base,FRAME*outer,FRAME*passage
