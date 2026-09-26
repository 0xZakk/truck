"""Bounded estimated linkage + coordinated shaft/bracket revision study.

Factory topology only; dimensions, D joint, pin and bracket offset are inferred.
Shared shaft and bracket remain unchanged until independent integration review.
"""
from pathlib import Path
import importlib.util
import build123d as b
PARAMS=dict(shaft_end_y=62.,shoulder_length=2.,arm_thickness=2.,hub_radius=6.,arm_radius=24.,arm_width=7.,key_radius=2.5,key_flat_x=2.,key_length=4.,pin_radius=.75,pin_length=8.,ball_radius=3.,neck_radius=1.8,ball_offset=4.,bracket_web_y=104.,cable_window_x=(431.,449.),cable_window_z=484.,cable_window_radius=12.,cable_envelope_radius=1.)
GAPS=['All new dimensions, D-section shaft coupling and retention pin inferred; production retention unverified.','Bracket web offset11 mm and ear extensions are a coordinated educational revision, not a Ford dimension.','Spring, shield, cable/socket, plate screws and preset stops absent;0–90 degrees is inherited educational travel.']
def cy(radius,length):return b.Rot(90,0,0)*b.Cylinder(radius,length)
def parts(existing_shaft,overrides=None):
 p=PARAMS|(overrides or {});y=p['shaft_end_y'];sl=p['shoulder_length'];t=p['arm_thickness'];r=p['arm_radius'];R=b.Rot(0,-90,0)
 shoulder=b.Pos(0,y+sl/2,0)*cy(3.,sl)
 key=b.Pos(0,y+sl+p['key_length']/2,0)*cy(p['key_radius'],p['key_length'])
 key-=b.Pos(p['key_flat_x']+2,y+sl+2,0)*b.Box(4,6,8)
 hub=b.Pos(0,y+sl+t/2,0)*cy(p['hub_radius'],t)
 arm=b.Pos(r/2,y+sl+t/2,0)*b.Box(r,t,p['arm_width'])
 arm+=b.Pos(r,y+sl+t/2,0)*cy(p['arm_width']/2,t)
 lever=R*((hub+arm)-key).clean()
 shaft=(existing_shaft+shoulder+R*key).clean()
 # Transverse pin directly touches the lever outer face atY66; drilled shaft
 # passage matches the pin. Shoulder atY64 captures the opposite hub face.
 py=y+sl+t+p['pin_radius']
 pin=b.Pos(0,py,0)*b.Rot(0,90,0)*b.Cylinder(p['pin_radius'],p['pin_length'])
 shaft-=b.Pos(0,py,0)*b.Rot(0,90,0)*b.Cylinder(p['pin_radius'],p['pin_length']+2)
 seat=y+sl+t
 ball=b.Pos(r,seat+p['ball_offset'],0)*b.Sphere(p['ball_radius'])
 ball+=b.Pos(r,seat+p['ball_offset']/2,0)*cy(p['neck_radius'],p['ball_offset'])
 return {'throttle-lever-estimated':lever,'throttle-cable-ball-stud-estimated':R*ball.clean(),'throttle-shaft-keyed-estimated':shaft.clean(),'throttle-lever-retaining-pin-estimated':pin}
def bracket_proposal():
 path=Path(__file__).resolve().parent/'pilot/throttle-bracket/candidate.py'
 spec=importlib.util.spec_from_file_location('bracket_study',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
 s=m.shape({'web_y':PARAMS['bracket_web_y']})
 # Explicit estimated clearance window for the direct cable envelope.
 x1,x2=PARAMS['cable_window_x'];y=PARAMS['bracket_web_y'];z=PARAMS['cable_window_z'];r=PARAMS['cable_window_radius']
 cut=b.Pos(x1,y,z)*cy(r,4)+b.Pos(x2,y,z)*cy(r,4)
 cut+=b.Pos((x1+x2)/2,y,z)*b.Box(x2-x1,4,2*r)
 return (s-cut).clean()
