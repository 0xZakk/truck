"""Add photographed Gates 44009 large lateral inlet to frozen mounting study.

Photos establish lateral cast arm and beaded hose neck, not dimensions or inner
passage section. Coordinates below are provisional packaging values. Apply to
already reconstructed water_pump_joint_candidate housing, never old pump alone.
"""
import build123d as b
from cooling_connections import cylinder
SOURCES=['water-pump-mounting-topology']
GAPS=[
 'Gates44009 front/rear/side photos show large lateral cast inlet arm with hose neck and retaining bead. Positive-Y assignment opposite retained heater tube is inferred; no physical pump measurement exists.',
 'Inlet neck localX−10/Z25, endY145, outer radius24 and bore20mm are provisional. Cast arm curves to rear chamber at localX−20/Y19; no internal photograph fixes this path. They are not hose purchasing dimensions.',
 'Smooth tapered open passage demonstrates topology only: the actual volute, impeller-eye feed, casting wall sections, hydraulic capacity and flow simulation remain unverified.'
]
AXIS_X=-10.;AXIS_Z=25.;END_Y=145.;BORE=20.
def cy(radius,start,end):return cylinder(radius,end-start,(AXIS_X,(start+end)/2,AXIS_Z),(0,1,0))
def section(y,r,x=AXIS_X):return b.Plane(origin=(x,y,AXIS_Z),z_dir=(0,1,0))*b.Circle(r)
def outer():
 return b.loft([section(y,r,x) for y,r,x in [(20,29,-20),(60,29,-10),(96,24,-10),(145,24,-10)]],ruled=True)+cy(25.5,140,143)
def passage():return b.loft([section(y,BORE,x) for y,x in [(19,-20),(60,-10),(END_Y+1,-10)]],ruled=True)
def housing_interface(housing):
 return (housing+outer())-passage()
def open_probe():return b.loft([section(y,2,x) for y,x in [(10,-20),(19,-20),(60,-10),(END_Y+1,-10)]],ruled=True)
