"""Isolated illustrative idle screw/pad and WOT lug; no production calibration.

Source supports idle screw-to-lever-pad contact and existence of a WOT stop.
All dimensions, thread, casting/pad contours and 0/90 contacts are estimates.
Housing uses throttle parent coordinates; lever uses throttle-moving coordinates.
"""
import build123d as b
PARAMS=dict(idle_axis_y=90.,idle_axis_z=502.,idle_tip_x=389.,screw_core_radius=1.15,thread_major_radius=1.45,thread_pitch=.5,thread_start_x=378.25,thread_length=6.5,thread_radial_clearance=.02,thread_axial_clearance=.02,idle_pad_x=-4.25,idle_pad_z=12.,wot_pad_y=66.875,wot_pad_z=12.)
def cx(r,h):return b.Rot(0,90,0)*b.Cylinder(r,h)
def thread(tap=False):
 p=PARAMS;extra=1. if tap else 0.;start=-extra;length=p['thread_length']+2*extra;rad=p['thread_radial_clearance'] if tap else 0.;axial=p['thread_axial_clearance'] if tap else 0.
 helix=b.Pos(0,0,start)*b.Helix(p['thread_pitch'],length,1.2)
 profile=b.Pos(0,0,start)*(b.Plane.XZ*b.Polygon((1.10,-.18-axial),(p['thread_major_radius']+rad,0),(1.10,.18+axial),align=None))
 ridge=b.sweep(profile,path=helix,is_frenet=True)
 return b.Pos(p['thread_start_x'],p['idle_axis_y'],p['idle_axis_z'])*b.Rot(0,90,0)*ridge

def screw():
 p=PARAMS;y,z=p['idle_axis_y'],p['idle_axis_z']
 q=b.Pos((376+p['idle_tip_x'])/2,y,z)*cx(p['screw_core_radius'],p['idle_tip_x']-376)+thread()
 head=b.Pos(375.5,y,z)*b.extrude(b.Plane.YZ*b.RegularPolygon(2.2,6),amount=1,both=True)
 head=head.cut(b.Pos(374.6,y,z)*b.Box(.5,.6,3.6))
 return (q+head).clean()

def parts(housing,lever):
 p=PARAMS;y,z=p['idle_axis_y'],p['idle_axis_z']
 idle_boss=b.Pos(381,90,502)*b.Box(8,8,8)
 idle_boss=b.fillet(idle_boss.edges(),radius=.65)
 root=b.Pos(376.5,84,502)*b.Box(4,6,8)
 idle_boss+=b.fillet(root.edges(),radius=.4)
 # L-shaped casting extension: bridge below the bare lever, then rise only
 # outside its outer Y face. This avoids using the lever itself as a housing.
 wot_lug=b.Pos(406,83,481.5)*b.Box(4,20,3)
 wot_lug=b.fillet(wot_lug.edges(),radius=.25)
 upright=b.Pos(406,92.125,484.25)*b.Box(4,1.75,5.5)
 # Estimated casting edge relief; retain the upper planar contact face.
 upright=b.fillet(upright.edges().filter_by(b.Axis.Z),radius=.25)
 wot_lug+=upright
 new_housing=(housing+idle_boss+wot_lug).clean()
 new_housing=new_housing.cut(b.Pos(381,y,z)*cx(p['screw_core_radius']+p['thread_radial_clearance'],12),thread(tap=True)).clean()
 idle_pad=b.Pos(p['idle_pad_x'],65,p['idle_pad_z'])*b.Box(1.5,2,2)
 wot_pad=b.Pos(0,p['wot_pad_y'],p['wot_pad_z'])*b.Box(6,2.75,4)
 new_lever=(lever+idle_pad+wot_pad).clean()
 return {'throttle-housing-stop-proposal':new_housing,'throttle-lever-stop-proposal':new_lever,'throttle-idle-stop-screw-illustrative':screw()},dict(idle_boss=idle_boss,wot_lug=wot_lug,idle_pad=idle_pad,wot_pad=wot_pad)
