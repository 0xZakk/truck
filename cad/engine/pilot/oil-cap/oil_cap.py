"""EC743-style cap candidate. Millimetres; origin preserves existing cap occurrence.
Ford photos establish topology, not dimensions. MO100 dimensions are comparison
values. The frozen cover has no female threads: this is NOT a validated fit.
"""
from dataclasses import dataclass, asdict
import math
import build123d as b

@dataclass(frozen=True)
class Parameters:
    shell_diameter: float = 69.09  # MO100 comparison, not measured Ford EC743
    overall_height: float = 38.10  # MO100 comparison
    thread_major: float = 31.24  # MO100 comparison
    thread_root: float = 28.84  # assumed
    pitch: float = 4.5  # assumed; photo does not establish lead
    thread_height: float = 18.0
    stem_bottom: float = -25.0
    seal_bottom: float = -6.0  # frozen cover top is world Z413, cap origin Z419
    seal_thickness: float = 3.0
    seal_outer: float = 22.0
    seal_inner: float = 15.8
    scallop_depth: float = 4.0

POSITION=(240.0,-12.0,419.0)

def parts(p=Parameters()):
    if not (p.thread_root < p.thread_major < 2*p.seal_inner < 2*p.seal_outer < p.shell_diameter):
        raise ValueError('Inconsistent diameters')
    top=p.stem_bottom+p.overall_height
    # Four hand-grip scallops and tapered shoulders follow Ford reference photos.
    def outline(z,shrink):
        pts=[]
        for n in range(128):
            a=n*2*math.pi/128
            r=p.shell_diameter/2-p.scallop_depth*(1-math.cos(4*a))/2-shrink
            pts.append((r*math.cos(a),r*math.sin(a)))
        return b.Pos(0,0,z)*b.Polygon(*pts,align=None)
    body=b.loft([outline(-3,1),outline(-1,0),outline(top-3,0),outline(top,2)],ruled=True)
    # Underside annular molding relief leaves roof, outer skirt, and central boss.
    relief=b.Cylinder(28,8)-b.Cylinder(22,10)
    body-=b.Pos(0,0,-1)*relief
    stem=b.Pos(0,0,(p.stem_bottom-3)/2)*b.Cylinder(p.thread_root/2,-3-p.stem_bottom)
    body+=stem
    # Actual helical raised retention, not stacked toroidal fake threads.
    path=b.Helix(p.pitch,p.thread_height,p.thread_root/2)
    profile=b.Plane.XZ*b.Polygon((p.thread_root/2-.25,-.75),(p.thread_major/2,0),(p.thread_root/2-.25,.75),align=None)
    thread=b.Pos(0,0,p.stem_bottom+1.5)*b.sweep(profile,path=path,is_frenet=True)
    body+=thread
    gasket=b.Pos(0,0,p.seal_bottom+p.seal_thickness/2)*(b.Cylinder(p.seal_outer,p.seal_thickness)-b.Cylinder(p.seal_inner,p.seal_thickness+2))
    return {'oil-filler-cap':body,'oil-filler-cap-seal':gasket}

def build(api,p=Parameters()):
    """Use after removing the original two define/add cap lines; api=(define,add)."""
    define,add=api
    for ident,shape in parts(p).items():
        seal=ident.endswith('seal')
        define(ident,shape,'Oil filler cap seal' if seal else 'Oil filler cap',
               'Rubber annulus closes the oil-fill joint.' if seal else 'Nonvented screw-retained oil cap with hand grips; Ford EC743-style candidate.',
               'closures','#403d36' if seal else '#252b30',
               ['pilot-oil-cap-ford','pilot-oil-cap-motorad'],
               ['Ford production dimensions and thread pitch are unverified; frozen cover lacks female retention.',
                'MO100 dimensions are manufacturer replacement comparison dimensions, not Ford metrology.'])
        add(ident,ident,'closures',POSITION,(0,0,550 if seal else 580))
