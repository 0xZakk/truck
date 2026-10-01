"""Nominal registration of estimated crossed drive under bounded cam endplay.
No geometry mutation. q is crank event degrees; x is cam axial millimeters.
"""
import math
import build123d as b
import oil_drive_layout as drive
from timing_coupled_core_candidate import AXIS, K
CROSSED_LEAD_RAD_PER_MM=1/18
AXIAL_MIN_MM=-.1
AXIAL_MAX_MM=0.

def angles(event_degrees, axial_mm=0.):
    if not all(math.isfinite(v) for v in (event_degrees,axial_mm)):
        raise ValueError('Finite event degrees and axial millimeters required')
    if not AXIAL_MIN_MM <= axial_mm <= AXIAL_MAX_MM:
        raise ValueError('Only cam axial range [-0.1,0] mm is supported')
    cam=event_degrees/2+math.degrees(K*axial_mm)
    distributor=-event_degrees/2+math.degrees((CROSSED_LEAD_RAD_PER_MM-K)*axial_mm)
    return cam,distributor

def frames(event_degrees, axial_mm=0.):
    """World frames for frozen gear-centered local STEP pair."""
    cam,distributor=angles(event_degrees,axial_mm)
    return {'cam': b.Pos(drive.DRIVE_X+axial_mm,*AXIS)*b.Rot(cam,0,0),
            'distributor': b.Pos(0,AXIS[0]-90,AXIS[1]-72)*drive.GEAR_FRAME*b.Rot(0,0,distributor)}
