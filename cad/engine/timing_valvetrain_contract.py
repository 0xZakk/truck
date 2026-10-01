"""Isolated source-sized phase/closure proposal; no geometry or global mutation."""
import math
import timing_axis_kinematic_candidate as feasibility
from timing_coupled_core_candidate import AXIS,K,cam_frame
DELTA=(AXIS[0]-90,AXIS[1]-72)
BASE=feasibility.layout(False)
PROPOSED=feasibility.layout(True)

def effective_crank(theta,axial=0):
    """Cam angle=-theta/2+K*axial, so same profile sees theta-2K*axial."""
    return theta-2*math.degrees(K*axial)

def state(theta,cylinder,kind,axial=0,shifted=True,retain_pivot=False):
    layout=PROPOSED if shifted else BASE
    lift=feasibility.cam_lift(effective_crank(theta,axial),cylinder,kind)
    py=BASE['PIVOT_Y'] if retain_pivot else layout['PIVOT_Y']
    return {'lifter_lift':lift,**layout['solve'](lift,kind,py)}

def tangent(theta,cylinder,kind,axial=0,x=0):
    t=(effective_crank(theta,axial)-(468 if kind=='intake' else 246)-[1,5,3,6,2,4].index(cylinder)*120+360)%720-360
    u=t/135;lift=feasibility.cam_lift(effective_crank(theta,axial),cylinder,kind)
    q=96/135;k=-math.log(.05/.247)*(1-q*q)/(q*q)
    slope=0 if abs(u)>=1 else lift*(-2*k*u/(1-u*u)**2)/math.radians(67.5)
    return [x+axial,AXIS[0]-slope,AXIS[1]+18+lift]
