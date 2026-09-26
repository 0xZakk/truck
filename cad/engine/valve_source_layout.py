"""Coordinated replacement-sized valvetrain candidate; never edits installed assets.

Known lengths are hard constraints. Lifter internal seat, rocker pad/cup shapes,
absolute cam/deck/valve-seat datums and casting contours remain assumptions.
Neither Crower nor Howards seat height is selected to force this mechanism fit.
"""
from pathlib import Path
import math,json
import build123d as b
from valve_dimensions_candidate import LENGTHS,STEM_D,PUSHROD_D,PUSHROD_OVERALL,BALL_R,PUSHROD_CENTERS,pushrod,valve
from valve_spring_seating_candidate import INSTALLED,GUIDE_DIAMETER
ROOT=Path(__file__).resolve().parents[2];OUT=ROOT/'cad/engine/candidates/valve-source-layout';BASE=OUT/'baseline'
VALVE_Y=-12.;PUSHROD_Y=90.;VALVE_BASE_Z=261.;HEAD_Z=255.5;HEAD_FLOOR_LOCAL=48.5
CAM_Z=72.;CAM_BASE_R=18.;LIFTER_FOOT_Z=CAM_Z+CAM_BASE_R
LIFTER_HEIGHT=50.8
# Lowering retained internal stack1.2mm preserves its positions relative to top.
# The shortened body's lower floor thickness changes from5mm to3.8mm, assumed.
LIFTER_DATUM_Z=114.8
LOWER_BALL_Z=139.7
PAD_CENTER_Z=-1.5;PAD_R=12.
CUP_Z=LOWER_BALL_Z+PUSHROD_CENTERS-(VALVE_BASE_Z+LENGTHS['intake']-PAD_CENTER_Z+PAD_R)


def rest(kind,pivot_y):
    tip=VALVE_BASE_Z+LENGTHS[kind];a=PUSHROD_Y-pivot_y;v=pivot_y-VALVE_Y
    lo,hi=-.02,.02
    for _ in range(65):
        t=(lo+hi)/2;pz=tip+v*math.sin(t)-PAD_CENTER_Z*math.cos(t)+PAD_R
        top=[pivot_y+a*math.cos(t)-CUP_Z*math.sin(t),pz+a*math.sin(t)+CUP_Z*math.cos(t)]
        length=math.hypot(top[0]-PUSHROD_Y,top[1]-LOWER_BALL_Z)
        if length<PUSHROD_CENTERS:lo=t
        else:hi=t
    return {'angle':t,'pivot_z':pz,'top':top,'tip_z':tip}


def solve(lift,kind='intake',pivot_y=None):
    py=PIVOT_Y if pivot_y is None else pivot_y;r=rest(kind,py)
    a=PUSHROD_Y-py;v=py-VALVE_Y;lo=r['angle']-.001;hi=r['angle']+.3
    bottom=[PUSHROD_Y,LOWER_BALL_Z+lift]
    for _ in range(65):
        t=(lo+hi)/2;top=[py+a*math.cos(t)-CUP_Z*math.sin(t),r['pivot_z']+a*math.sin(t)+CUP_Z*math.cos(t)]
        length=math.hypot(top[0]-bottom[0],top[1]-bottom[1])
        if length<PUSHROD_CENTERS:lo=t
        else:hi=t
    tip=r['pivot_z']-v*math.sin(t)+PAD_CENTER_Z*math.cos(t)-PAD_R
    return {'angle':t,'pivot_z':r['pivot_z'],'valve_lift':r['tip_z']-tip,'top':top,'bottom':bottom,
      'closure_error':math.hypot(top[0]-bottom[0],top[1]-bottom[1])-PUSHROD_CENTERS,
      'pad_y':py-v*math.cos(t)-PAD_CENTER_Z*math.sin(t)}


def calibrate():
    lo,hi=45.,55.
    for _ in range(65):
        py=(lo+hi)/2
        if solve(.247*25.4,'intake',py)['valve_lift']<.395*25.4:lo=py
        else:hi=py
    return py
PIVOT_Y=calibrate()


def rocker():
    # Same solid for intake/exhaust; rest angle changes for their0.0254mm length
    # difference. Retain fulcrum neighborhood; raise only pushrod socket end.
    low=VALVE_Y-PIVOT_Y-10;high=PUSHROD_Y-PIVOT_Y+6;landing=PUSHROD_Y-PIVOT_Y-10;bottom=CUP_Z+2.5
    profile=b.Plane.YZ*b.Polygon((low,-13.5),(20,-13.5),(landing,bottom),(high,bottom),(high,bottom+8),(landing,bottom+8),(20,-2.5),(low,-2.5),align=None)
    s=b.extrude(profile,amount=8.5,both=True)
    patch=b.Pos(0,VALVE_Y-PIVOT_Y,-11)*b.Box(30,20,6);original=s
    s-=patch;s+=(b.Pos(0,VALVE_Y-PIVOT_Y,PAD_CENTER_Z)*b.Sphere(PAD_R))&patch&original
    s-=b.Sphere(15)
    s-=b.Pos(0,PUSHROD_Y-PIVOT_Y,CUP_Z)*b.Sphere(BALL_R)
    s-=b.Pos(0,0,-8)*b.Cylinder(5,30)
    relief=b.Pos(0,0,-14)*b.Cylinder(6.15,6)
    for degree in range(-1,12):s-=b.Rot(-degree,0,0)*relief
    return s


def lifter_body(old):
    # Keep original top-frame anatomy; shorten the flat bottom to sourced50.8mm.
    return old & (b.Pos(0,0,.6)*b.Cylinder(.874*25.4/2,LIFTER_HEIGHT))


def lifter_cup():
    return b.Cylinder(8,5)-b.Pos(0,0,4)*b.Sphere(BALL_R)-b.Cylinder(1,10)


def head_adapter(head,stations):
    old_py=51.62143599494969
    for kind,x in zip(['intake','exhaust'],stations):
        r=rest(kind,PIVOT_Y);pedestal_top=r['pivot_z']-20-HEAD_Z
        # Replace only prior study pedestal above the inherited head floor.
        head-=b.Pos(x,old_py,(HEAD_FLOOR_LOCAL+135)/2)*b.Cylinder(12.01,135-HEAD_FLOOR_LOCAL)
        head+=b.Pos(x,PIVOT_Y,(48+pedestal_top)/2)*b.Cylinder(12,pedestal_top-48)
        head-=b.Pos(x,PIVOT_Y,pedestal_top-14.5)*b.Cylinder(4.6,43)
        head-=b.Pos(x,PUSHROD_Y,28)*b.Cylinder(6,100)
        # Guide bore and spring seat heights constrained by service dimensions.
        delta=LENGTHS[kind]-109;seat=363+delta-INSTALLED[kind]-HEAD_Z
        sleeve=b.Cylinder(5.01,48.5-21)-b.Cylinder(GUIDE_DIAMETER/2,50)
        head+=b.Pos(x,VALVE_Y,(21+48.5)/2)*sleeve
        boss=b.Cylinder(18,seat-48)-b.Cylinder(GUIDE_DIAMETER/2,100)
        head+=b.Pos(x,VALVE_Y,(seat+48)/2)*boss
    return head


def spring(kind,lift=0):
    if not -1e-10<=lift<=.4*25.4:raise ValueError("Outside source open-test envelope")
    lift=max(0.,lift)
    h=INSTALLED[kind]-lift;path=b.Helix(h/6,h,13)
    return b.sweep(b.Plane(origin=path@0,z_dir=path%0)*b.Circle(2),path=path)&(b.Pos(0,0,h/2)*b.Box(40,40,h))


def seal():
    return b.Cylinder(8,9)-b.Cylinder(STEM_D/2+.05,12)


def cover():
    # Cam-side shoulder extension only; flange and cap/PCV bore datums retained.
    # This is an assumed stamping envelope required by the longer sourced parts.
    outer=b.loft([b.Pos(0,y,z)*b.RectangleRounded(x,w,r) for z,x,w,r,y in [(-38,734,232,28,0),(-28,728,222,28,0),(24,698,186,32,28),(38,680,174,35,28)]],ruled=True)
    inner=b.loft([b.Pos(0,y,z)*b.RectangleRounded(x,w,r) for z,x,w,r,y in [(-42,728,226,25,0),(-28,722,216,25,0),(24,692,180,29,28),(35,674,168,32,28)]],ruled=True)
    return outer-inner-b.Pos(240,0,38)*b.Cylinder(17,20)-b.Pos(-240,0,38)*b.Cylinder(14.2,20)


def metadata():
    return {'hard_constraints':{'valve_overall_mm':LENGTHS,'valve_stem_diameter_mm':STEM_D,'pushrod_overall_mm':PUSHROD_OVERALL,'pushrod_diameter_mm':PUSHROD_D,'lifter_body_height_mm':LIFTER_HEIGHT,'spring_installed_mm':INSTALLED,'guide_diameter_mm':GUIDE_DIAMETER},
      'assumed_datums':{'cam_z':CAM_Z,'cam_base_radius':CAM_BASE_R,'valve_seat_base_z':VALVE_BASE_Z,'lower_pushrod_ball_center_z':LOWER_BALL_Z,'head_z':HEAD_Z,'valve_y':VALVE_Y},
      'derived':{'pivot_y':PIVOT_Y,'rocker_cup_local_z':CUP_Z,'pushrod_ball_centers_mm':PUSHROD_CENTERS,'stations':{k:{'rest':rest(k,PIVOT_Y),'peak':solve(.247*25.4,k)} for k in LENGTHS}},
      'seat_height_policy':'Melling publishes body height only. Internal cup/clip offsets are explicitly retained assumptions after1.2mm reduction; Crower/Howards seat-height numbers are not chosen or equated. Exact production socket datum unresolved.'}
if __name__=='__main__':print(json.dumps(metadata(),indent=2))
