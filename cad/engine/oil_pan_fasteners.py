"""Source-counted pan screw/washer study; hole stations are NOT a factory pattern.

The factory service figure supports 25 screw-and-washer assemblies, nominal
5/16-18 x .87 inch. It does not dimension the hole locations, washer/head,
thread fit or block bosses. These remain an explicit illustrative interface.
"""
import math
import build123d as b

SOURCES = ['truck-oil-pan-hardware']
GAPS = [
    'Ford service figure specifies 25 screw/washer assemblies, 5/16-18 × .87 inch. The separate washer shape illustrates that assembly; captive retention is not reconstructed.',
    'The 13/12 side-rail layout, head, washer, clearance holes and dry block pads are provisional. The service illustration is not a dimensioned drilling template. No production fit, thread engagement or clamp-load claim is made.',
    'This does not complete the pan gasket: the old side strips remain provisional and the applicable molded-rubber end/perimeter sealing is unfinished.',
]
DIAMETER = 25.4 * 5/16
PITCH = 25.4/18
LENGTH = 25.4*.87
WASHER_THICKNESS = 1.6
UNDER_HEAD_Z = -39.6
# Preserve supported count while making the unsupported layout explicit.
STATIONS = tuple([(i*688/12-344,111.0) for i in range(13)] +
                 [(i*688/11-344,-135.0) for i in range(12)])


def cylinder(radius, bottom, top):
    return b.Pos(0,0,(bottom+top)/2)*b.Cylinder(radius,top-bottom)


def screw_shape():
    shape = cylinder(DIAMETER/2,0,LENGTH)
    shape += b.Pos(0,0,-5.3)*b.extrude(b.RegularPolygon(12.7/math.sqrt(3),6),amount=5.3)
    path = b.Helix(PITCH,LENGTH+2,DIAMETER/2,center=(0,0,-1))
    profile=b.Plane(origin=path@0,x_dir=(1,0,0),z_dir=path%0)*b.Polygon(
        (-.61343*PITCH,0),(.2,-.615),(.2,.615),align=None)
    cutter=b.sweep(profile,path=path,is_frenet=True)
    cutter=cutter.intersect(cylinder(5,1.6,LENGTH))
    return shape-cutter


def washer_shape():
    return cylinder(7.5,0,WASHER_THICKNESS)-cylinder(4.15,-1,WASHER_THICKNESS+1)


def block_interface(block):
    for x,y in STATIONS:
        # Local dry rail extension; stays outside the crankcase and oil passages.
        block += b.Pos(x,y,0)*cylinder(7,-32,-15)
        block -= b.Pos(x,y,0)*cylinder(4.15,-33,-16.5)
    return block


def perforate(shape, offset):
    """Input definition-local geometry; offset is its assembled translation."""
    frame=b.Pos(*offset)
    result=frame*shape
    for x,y in STATIONS:
        result-=b.Pos(x,y,0)*cylinder(4.3,-40,-30)
    return frame.inverse()*result


def pan_api(api):
    define,add,group,*rest=api
    def adapted(key,shape,*args,**kwargs):
        if key=='oil-pan': shape=perforate(shape,(0,-12,-96))
        elif key.startswith('pan-side-gasket-'): shape=perforate(shape,(0,-12,-33))
        return define(key,shape,*args,**kwargs)
    return (adapted,add,group,*rest)


def build(api):
    define,add,group=api
    group('oil-pan-fastener-assembly','Oil-pan screw & washer study','oil-pan-assembly')
    define('oil-pan-mounting-screw',screw_shape(),'Pan mounting screw · 5/16-18 × .87',
           'Clamps the oil-pan flange through its washer. The nominal thread, length and assembly count follow the factory service figure; placement and thread fit are illustrative.',
           'closures','#a3adb3',SOURCES,GAPS)
    define('oil-pan-mounting-washer',washer_shape(),'Pan mounting washer',
           'Spreads the screw-head load across the thin flange. This separate ring illustrates the factory screw/washer assembly; washer dimensions and captive construction are unverified.',
           'closures','#8f9aa4',SOURCES,GAPS)
    for n,(x,y) in enumerate(STATIONS,1):
        for role in ('screw','washer'):
            add(f'oil-pan-mounting-{role}-{n}',f'oil-pan-mounting-{role}',
                'oil-pan-fastener-assembly',(x,y,UNDER_HEAD_Z),(0,0,-360 if role=='screw' else -340))
