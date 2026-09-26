"""Factory-topology splash hood + inferred compliant pushpin interface study."""
import build123d as b
import throttle_linkage_candidate as linkage
PARAMS=dict(mount_x=389.,mount_z=514.,hole_radius=2.4,shank_radius=2.2,barb_radius=2.9,head_radius=4.,ear_front_y=106.5,bracket_back_y=103.)
GAPS=['All dimensions, mounting coordinate, barb and relief slots are inferred educational geometry; Ford production details unverified.','Angular hood approximates factory viewY. Pushpin insertion flexure/material/strength and full cable sheath/connector envelopes are unvalidated.','Spring and its tangs, stops and production calibration remain unresolved; not invented here.']
def cy(r,h):return b.Rot(90,0,0)*b.Cylinder(r,h)
def parts():
 p=PARAMS;x,z=p['mount_x'],p['mount_z'];r=p['hole_radius']
 profile=b.Plane.YZ*b.Polygon((84,524.5),(110,524.5),(113.5,521),(113.5,480),(115,480),(115,521.6),(110.6,526),(84,526),align=None)
 hood=b.Pos(382,0,0)*b.extrude(profile,amount=67)
 ear=b.Pos(x,105.75,z)*b.Box(12,1.5,12)
 for xx in [x-5.25,x+5.25]:ear+=b.Pos(xx,110,z)*b.Box(1.5,10,12)
 shield=(hood+ear)-b.Pos(x,104,z)*cy(r,12)
 bracket=linkage.bracket_proposal()-b.Pos(x,104,z)*cy(r,6)
 head=b.Pos(x,107.25,z)*cy(p['head_radius'],1.5)
 stem=b.Pos(x,103.75,z)*cy(p['shank_radius'],5.5)
 barb=b.Pos(x,102.65,z)*cy(p['barb_radius'],.7)
 cone=b.Pos(x,101,z)*b.Rot(-90,0,0)*b.Cone(p['shank_radius'],p['barb_radius'],1.3,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
 pin=head+stem+barb+cone
 # Four flexible fingers remain connected at the head; deformation not modeled.
 pin-=b.Pos(x,102.75,z)*b.Box(.6,3.5,8)
 pin-=b.Pos(x,102.75,z)*b.Box(8,3.5,.6)
 return {'throttle-linkage-shield-estimated':shield.clean(),'throttle-shield-pushpin-estimated':pin.clean(),'accelerator-bracket-shield-hole-estimated':bracket.clean()}
