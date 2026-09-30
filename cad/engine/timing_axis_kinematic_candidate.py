"""Numeric-only same-ray study; does not import CAD or change installed datums."""
import ast
import math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CENTER=121.8
OLD_CENTER=math.hypot(90,72)
DELTA=(90*CENTER/OLD_CENTER-90,72*CENTER/OLD_CENTER-72)
MAX_CAM_LIFT=.247*25.4
TARGET_VALVE_LIFT=.395*25.4

def layout(shift=False):
    """Reuse exact baseline numeric functions, excluding all CAD imports/functions.

    Candidate freedoms: lateral pivot and cup axial offset. Valve/head datums,
    pad geometry, valve length and catalog pushrod length remain fixed.
    """
    n={'math':math,'LENGTHS':{'intake':4.749*25.4,'exhaust':4.750*25.4},
       'PUSHROD_CENTERS':10.14*25.4-2*math.sqrt((.312*25.4/2)**2-1.2**2),
       'VALVE_Y':-12.,'PUSHROD_Y':90.+(DELTA[0] if shift else 0),
       'VALVE_BASE_Z':261.,'LOWER_BALL_Z':139.7+(DELTA[1] if shift else 0),
       'PAD_CENTER_Z':-1.5,'PAD_R':12.}
    n['CUP_Z']=n['LOWER_BALL_Z']+n['PUSHROD_CENTERS']-(261+n['LENGTHS']['intake']+1.5+12)
    tree=ast.parse((ROOT/'cad/engine/valve_source_layout.py').read_text())
    selected=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name in ('rest','solve')]
    exec(compile(ast.Module(body=selected,type_ignores=[]),'baseline-numeric-functions','exec'),n)
    # Broad explicit search interval, bracketed; unlike a blind clipped calibration.
    lo,hi=40.,65.
    def error(py):return n['solve'](MAX_CAM_LIFT,'intake',py)['valve_lift']-TARGET_VALVE_LIFT
    assert error(lo)<0<error(hi),'No pivot solution in declared candidate bracket'
    for _ in range(70):
        mid=(lo+hi)/2
        if error(mid)<0:lo=mid
        else:hi=mid
    n['PIVOT_Y']=(lo+hi)/2
    return n

def cam_lift(degrees,cylinder,kind):
    center=(468 if kind=='intake' else 246)+[1,5,3,6,2,4].index(cylinder)*120
    t=((degrees-center+360)%720-360)/135
    q=96/135;k=-math.log(.05/.247)*(1-q*q)/(q*q)
    return 0 if abs(t)>=1 else MAX_CAM_LIFT*math.exp(-k*t*t/(1-t*t))

def drive(shift=False):
    """Current drive frame equations, translated as a connected branch."""
    dy,dz=DELTA if shift else (0.,0.)
    s,c=math.sin(math.radians(20)),math.cos(math.radians(20))
    g=(227.584,90+36*c+dy,72-36*s+dz)
    def point(x,z):return [g[0]+x,g[1]+z*s,g[2]+z*c]
    length=4.520*25.4
    return {'gear':list(g),'distributor':point(0,85),'pump':point(-3.5,-53-length-17),
       'shaft_top':point(0,-53),'shaft_bottom':point(0,-53-length),
       'axis':[0,s,c],'shaft_length_mm':length,'tilt_deg':20,'spacing_mm':36}
