"""Regenerate only crank throw rest phases; retain existing end adapters."""
import math
import build123d as b
import full_engine as e
from flywheel import crank_interface
from pilot_bearing import crank_interface as pilot_interface
from damper_attachment import crank_interface as damper_interface

EVENT_PHASES = tuple(e.PHASES)
REST_PHASES = tuple((-phase) % 360 for phase in EVENT_PHASES)

def shape(phases=REST_PHASES):
    crank = None
    def fuse(s):
        nonlocal crank
        crank = s if crank is None else crank + s
    for x in e.MAINS:
        fuse(b.Pos(x, 0, 0) * e.cx(e.MAIN_R, 32))
    for x, phase in zip(e.CYLINDERS, phases):
        t = math.radians(phase)
        y, z = -e.R * math.sin(t), e.R * math.cos(t)
        fuse(b.Pos(x, y, z) * e.cx(e.ROD_R, 27.2))
        for sign in [-1, 1]:
            cheek = e.cx(43,28) + b.Pos(0,0,e.R/2) * b.Box(28,66,e.R) + b.Pos(0,0,e.R) * e.cx(37,28)
            cheek += b.Pos(0,0,-20) * e.cx(49,28)
            fuse(b.Pos(x + sign*27,0,0) * b.Rot(phase,0,0) * cheek)
    fuse(b.Pos(e.MAINS[0]+43,0,0) * e.cx(21,102))
    fuse(b.Pos(e.MAINS[-1]-20,0,0) * e.cx(e.MAIN_R,30))
    fuse(b.Pos(-375,0,0) * e.cx(45,24))
    fuse(b.Pos(-388,0,0) * e.cx(51,10))
    return damper_interface(pilot_interface(crank_interface(crank)))
