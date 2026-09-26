"""Isolated, illustrative female mate for the pilot's assumed 4.5 mm helix.

No OEM thread designation or manufacturing-process claim. All dimensions below
are study assumptions; the existing cap is imported unchanged from its source.
"""
from pathlib import Path
import sys
from functools import lru_cache
import build123d as b
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'cad/engine/pilot/oil-cap'))
from oil_cap import parts, POSITION

PITCH = 4.5
NECK_BOTTOM = 399.
NECK_TOP = 413.
NECK_OUTER_R = 17.8
BORE_R = 14.62

def candidate(cover):
    ring = b.Pos(240,-12,(NECK_BOTTOM+NECK_TOP)/2)*(
        b.Cylinder(NECK_OUTER_R,NECK_TOP-NECK_BOTTOM)-
        b.Cylinder(BORE_R,NECK_TOP-NECK_BOTTOM+2))
    path = b.Helix(PITCH,18.,14.42)
    profile = b.Plane.XZ*b.Polygon((14.,-.95),(15.85,-.2),(15.85,.2),(14.,.95),align=None)
    groove = b.Pos(240,-12,395.5)*b.sweep(profile,path=path,is_frenet=True)
    neck = ring-groove
    return cover+neck, neck

@lru_cache(maxsize=1)
def cap_parts():
    return parts()

def cap_at(angle=0., lift=None):
    pieces = cap_parts()
    cap, seal = pieces["oil-filler-cap"], pieces["oil-filler-cap-seal"]
    if lift is None: lift = PITCH*angle/360.
    pose = b.Pos(*POSITION)*b.Pos(0,0,lift)*b.Rot(0,0,angle)
    return pose*cap, pose*seal
