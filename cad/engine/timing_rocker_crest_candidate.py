"""Bounded unmeasured crest reduction; all kinematics and contact surfaces frozen."""
from pathlib import Path
import build123d as b
import timing_valvetrain_inclined_candidate as c
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'cad/engine/generated/timing-valvetrain-inclined-candidate/rocker-arm.step'
REDUCTION=2.
LANDING=c.P['PUSHROD_Y']-c.P['PIVOT_Y']-10
HIGH=c.P['PUSHROD_Y']-c.P['PIVOT_Y']+6
OLD_TOP=c.P['CUP_Z']+10.5
NEW_TOP=OLD_TOP-REDUCTION

def mask():return b.Pos(0,(20+HIGH+.1)/2,(-2.5+OLD_TOP+1)/2)*b.Box(17.2,HIGH+.1-20,OLD_TOP+1+2.5)
def build(old=None):
 old=b.import_step(BASE) if old is None else old
 profile=b.Plane.YZ*b.Polygon((20,-2.5),(LANDING,NEW_TOP),(HIGH+.1,NEW_TOP),(HIGH+.1,OLD_TOP+1),(20,OLD_TOP+1),align=None)
 return old.cut(b.extrude(profile,amount=8.6,both=True))
