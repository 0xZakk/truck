"""Numeric inclined-rod alternative. No geometry or existing module mutation."""
import math
from timing_valvetrain_contract import effective_crank,DELTA
from timing_axis_kinematic_candidate import cam_lift
from valve_source_layout import LENGTHS,PUSHROD_CENTERS,BALL_R
LOWER_Y=90+DELTA[0];LOWER_Z=139.7+DELTA[1];VALVE_Y=-12

def layout(upper_y=90):
    L=PUSHROD_CENTERS
    cup_z=LOWER_Z+math.sqrt(L*L-(upper_y-LOWER_Y)**2)-(261+LENGTHS['intake']+13.5)
    def rest(kind,py):
        tip=261+LENGTHS[kind];a=upper_y-py;v=py-VALVE_Y;lo,hi=-.02,.02
        for _ in range(65):
            t=(lo+hi)/2;pz=tip+v*math.sin(t)+1.5*math.cos(t)+12
            top=[py+a*math.cos(t)-cup_z*math.sin(t),pz+a*math.sin(t)+cup_z*math.cos(t)]
            if math.hypot(top[0]-LOWER_Y,top[1]-LOWER_Z)<L:lo=t
            else:hi=t
        return {'angle':t,'pivot_z':pz,'top':top,'tip_z':tip}
    def solve(lift,kind='intake',py=None):
        py=pivot if py is None else py;r=rest(kind,py);a=upper_y-py;v=py-VALVE_Y;lo=r['angle']-.001;hi=r['angle']+.3;bottom=[LOWER_Y,LOWER_Z+lift]
        for _ in range(65):
            t=(lo+hi)/2;top=[py+a*math.cos(t)-cup_z*math.sin(t),r['pivot_z']+a*math.sin(t)+cup_z*math.cos(t)]
            if math.dist(top,bottom)<L:lo=t
            else:hi=t
        tip=r['pivot_z']-v*math.sin(t)-1.5*math.cos(t)-12
        return {'angle':t,'pivot_z':r['pivot_z'],'valve_lift':r['tip_z']-tip,'top':top,'bottom':bottom,'closure_error':math.dist(top,bottom)-L,'pad_y':py-v*math.cos(t)+1.5*math.sin(t)}
    lo,hi=40.,65.
    assert solve(.247*25.4,py=lo)['valve_lift']<.395*25.4<solve(.247*25.4,py=hi)['valve_lift']
    for _ in range(70):
        mid=(lo+hi)/2
        if solve(.247*25.4,py=mid)['valve_lift']<.395*25.4:lo=mid
        else:hi=mid
    pivot=(lo+hi)/2
    return {'upper_y':upper_y,'cup_z':cup_z,'pivot_y':pivot,'solve':solve,'rest':rest}

def state(layout,theta,cylinder,kind,axial=0):
    lift=cam_lift(effective_crank(theta,axial),cylinder,kind)
    return {'lifter_lift':lift,**layout['solve'](lift,kind)}

def section_y(s,z):
    top,bottom=s['top'],s['bottom'];dy=top[0]-bottom[0];dz=top[1]-bottom[1]
    center=bottom[0]+(z-bottom[1])*dy/dz
    # Elliptic horizontal cut through unchanged circular pushrod tube.
    half=BALL_R*math.hypot(dy,dz)/abs(dz)
    return center,half
