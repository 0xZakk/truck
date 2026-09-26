"""Single 4.9L engine-oil indicator study. All mm; origin = assumed seating stop.
Positive Z is toward handle. The withdrawn blade points down. No guide tube.
"""
from dataclasses import dataclass,asdict
import build123d as b
import math
@dataclass(frozen=True)
class Parameters:
    blade_axial_length: float=692.15 # seller roughly 27.25 in, datum unclear
    stem_width: float=2.2
    blade_thickness: float=.8
    tip_width: float=6.5
    tip_length: float=90
    wave_amplitude: float=3.0
    stop_radius: float=7.0
    stop_height: float=12.0
    handle_wire_radius: float=2.6
    handle_height: float=72.0
    stamp: bool=True
P=Parameters()
PROVISIONAL_POSE={'position_cad_mm':[-120,170,445],'rotation_cad_deg':[-8.5,0,0]}
def parts(p=P):
    L=p.blade_axial_length
    def center(s):
        return p.wave_amplitude*math.sin(2*math.pi*(s-5)/24) if 5<s<53 else 0
    stations=sorted(set([0,5,53,L-p.tip_length-15,L-p.tip_length,L-3,L]+list(range(6,53,2))))
    def width(s):
        if s<L-p.tip_length-15:return p.stem_width
        if s<L-p.tip_length:return p.stem_width+(p.tip_width-p.stem_width)*(s-(L-p.tip_length-15))/15
        if s>L-3:return p.tip_width-(p.tip_width-1.3)*(s-(L-3))/3
        return p.tip_width
    outline=[(center(s)-width(s)/2,-s) for s in stations]+[(center(s)+width(s)/2,-s) for s in reversed(stations)]
    face=b.Plane.XZ*b.Polygon(*outline,align=None)
    blade=b.extrude(face,amount=p.blade_thickness/2,both=True)
    if p.stamp:
        plane=b.Plane(origin=(0,-p.blade_thickness/2-.01,-635),x_dir=(0,0,-1),z_dir=(0,-1,0))
        letters=plane*b.Text('E9TE-6750-DA  M',font_size=1.7)
        blade-=b.extrude(letters,amount=-.16)
    # Open loop, based on specimen photograph; section and size estimated.
    pts=[(0,0,4),(0,0,22),(-4,0,37),(-16,0,48),(-17,0,62),(-8,0,p.handle_height),(5,0,p.handle_height-1),(12,0,61),(9,0,50)]
    path=b.Spline(*pts)
    profile=b.Plane(origin=pts[0],z_dir=path%0)*b.Circle(p.handle_wire_radius)
    handle=b.sweep(profile,path=path)
    stop=b.Pos(0,0,p.stop_height/2-.5)*b.Cylinder(p.stop_radius,p.stop_height)
    return {'engine-oil-dipstick-blade':blade,'engine-oil-dipstick-handle':handle+stop}
def shape(p=P):return b.Compound(children=list(parts(p).values()))
def installed(s):return b.Pos(*PROVISIONAL_POSE['position_cad_mm'])*b.Rot(*PROVISIONAL_POSE['rotation_cad_deg'])*s
