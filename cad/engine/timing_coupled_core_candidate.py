"""Rigid keyed cam-group study; stationary plate fasteners stay stationary."""
from pathlib import Path
import math
import build123d as b
ROOT=Path(__file__).resolve().parents[2]
AXIS=(95.1098209901611,76.08785679212888)
GEAR_X=385.259375
MOVING=frozenset(['camshaft','cam-timing-gear','cam-timing-key','cam-gear-spacer'])
STATIONARY=tuple([f'cam-bearing-{i}' for i in range(1,5)]+['rear-cam-plug','cam-thrust-plate']+[f'cam-thrust-{kind}-{i}' for kind in ['bolt','washer'] for i in [1,2]])
K=-math.tan(math.radians(25))/81.2

def cam_frame(crank_degrees=0,axial_mm=0):
    angle=-crank_degrees/2+math.degrees(K*axial_mm)
    return b.Pos(axial_mm,*AXIS)*b.Rot(angle,0,0)*b.Pos(0,-AXIS[0],-AXIS[1])

def parts():
    folder=ROOT/'cad/engine/generated/timing-thrust-land-candidate'
    out={key:b.import_step(folder/(key+'.step')) for key in list(MOVING)+list(STATIONARY)+['crank-timing-gear']}
    revised=ROOT/'cad/engine/generated/timing-gear-backlash-candidate'
    out['cam-timing-gear']=b.Pos(GEAR_X,*AXIS)*b.import_step(revised/'cam.step')
    out['crank-timing-gear']=b.Pos(GEAR_X,0,0)*b.import_step(revised/'crank.step')
    return out

def posed(parts,crank_degrees=0,axial_mm=0):
    frame=cam_frame(crank_degrees,axial_mm)
    return {key:(frame*q if key in MOVING else b.Rot(crank_degrees,0,0)*q if key=='crank-timing-gear' else q) for key,q in parts.items()}

def cylinder(radius,xmin,xmax):
    return b.Pos((xmin+xmax)/2,*AXIS)*b.Rot(0,90,0)*b.Cylinder(radius,xmax-xmin)
