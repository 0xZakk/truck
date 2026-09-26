"""Unpublished matched pan joint, following OS34601R's observed25-hole topology.

Continuous gasket and10+10+3+2hole distribution follow the exact part photo.
Dimensions, orientation assignment, end profiles and lands remain assumptions.
"""
import build123d as b
from oil_pan_fasteners import screw_shape,washer_shape,cylinder,DIAMETER,PITCH,LENGTH
SOURCES=['truck-oil-pan-hardware','fel-pro-vin-y-gaskets','felpro-os34601r-topology']
GAPS=[
 'Exact OS34601R product photo supports a continuous gasket and10holes per long rail plus3and2at its ends. Hole coordinates, central rail offset and photo-end orientation remain unmeasured.',
 'All gasket thicknesses, radii, pads, compression, washers, head geometry, clearances and blind sockets are provisional. This is a matched geometric study, not a production gasket or dimensional drawing.',
 'V9 narrows the complete shallow shell to726mm length with720mm inner cavity; the original rear sump profile, floor depth and drain datum remain. This keeps the continuous front end wall behind the bolt extraction corridor; overall stamping remains unmeasured.',
 'The continuous inset pan neck uses assumed726x242-to726x232mm envelopes between Z-90and-76, with its center shifted5mm toward+Y and a wider flat flange; it reconciles bolt clearance with the existing provisional starter and does not establish production stamping or capacity. Front and rear end lands are illustrative dry block extensions. The actual timing-cover/block/pan junction and local sealant remain unresolved.',
]
# x,y,under-head Z. Assigning the three-hole bridge to+X is provisional.
STATIONS=tuple([(i*688/9-344,y,-39.6) for y in (116.6,-131.) for i in range(10)] +
 [(371.,y,-39.6) for y in (-85.,85.)]+[(371.,0.,-67.)]+
 [(-371.,y,-39.6) for y in (-85.,85.)])
ENDS=((365.,381.,59.4,61.4),(-380.,-365.,51.1,53.1))

def x_cylinder(radius,start,end):
    return b.Pos((start+end)/2,0,0)*b.Rot(0,90,0)*b.Cylinder(radius,end-start)

def low_half(shape):
    return shape & b.Pos(0,0,-116)*b.Box(1000,400,168)

def ring_profile():
    return b.Pos(0,-12,-34)*b.extrude(b.RectangleRounded(762,258,28)-b.RectangleRounded(740,236,21),amount=2)

def joined(shape):
    solids=list(shape.solids())
    fused=solids[0].fuse(*solids[1:]) if len(solids)>1 else solids[0]
    return b.Compound(children=list(fused)) if isinstance(fused,b.ShapeList) else fused

def gasket_shape():
    shape=ring_profile()
    for x,y,z in STATIONS:
        shape=joined(shape+b.Pos(x,y)*cylinder(9,z+5.6,z+7.6))
    for a,c,inner,outer in ENDS:
        shape=joined(shape-x_cylinder(outer,a-1,c+1))
        shape=joined(shape+low_half(x_cylinder(outer,a,c)-x_cylinder(inner,a-1,c+1)))
    # Flat seal island at the center of the three-hole bridge; section assumed.
    shape=joined(shape+b.Pos(371.,0)*cylinder(9,-61.4,-59.4))
    shape-=b.Pos(371.,0)*cylinder(10.1,-59.4,-54)
    for x,y,z in STATIONS:shape-=b.Pos(x,y)*cylinder(4.3,z-1,z+9)
    return shape

def block_interface(shape):
    for a,c,inner,outer in ENDS:
        bore=42 if a>0 else 49.1
        shape+=low_half(x_cylinder(inner,a,c)-x_cylinder(bore,a-1,c+1))
    for x,y,z in STATIONS:
        bottom=z+7.6
        shape+=b.Pos(x,y)*cylinder(10 if y>0 or (x in (-371.,371.) and y!=0) else 7,bottom,z+25)
        shape-=b.Pos(x,y)*cylinder(4.15,bottom-1,z+LENGTH+1)
    return shape

def _narrow_base_pan():
    # Reconstruct only original oil_pan.py shell with coherent shorter endwalls.
    # Rear sump, drain frame, local boss and seat exactly retain original values.
    from oil_pan import DRAIN_LOCAL,DRAIN_ROTATION
    def rounded(x,y,z,r):return b.extrude(b.RectangleRounded(x,y,r),amount=z/2,both=True)
    outer=rounded(726,242,122,24)
    inner=b.Pos(0,0,3)*rounded(720,236,122,21)
    rear=b.loft([b.Pos(-165,0,z)*b.RectangleRounded(l,w,24) for z,l,w in [(-172.95,350,214),(-150,360,220),(-45,410,242)]],ruled=True)
    rear_inner=b.loft([b.Pos(-165,0,z)*b.RectangleRounded(l,w,21) for z,l,w in [(-169.95,344,208),(-150,354,214),(-42,410,236)]],ruled=True)
    pan=(outer+rear)-(inner+rear_inner)
    pan+=b.Pos(0,0,60)*(rounded(742,258,4,28)-rounded(720,236,8,21))
    pan-=b.Pos(377,12,96)*x_cylinder(45,-20,20)
    pan-=b.Pos(-377,12,96)*x_cylinder(49.1,-15,15)
    drain=b.Pos(*DRAIN_LOCAL)*b.Rot(*DRAIN_ROTATION)
    pan+=drain*(b.Pos(0,0,-4.5)*b.Cylinder(11,9))
    pan-=drain*(b.Pos(0,0,-4)*b.Cylinder(7.1,30))
    pan-=drain*(b.Pos(0,0,5)*b.Cylinder(12,10))
    return pan

def pan_interface(shape):
    # Input/output are the pan definition's existing local frame.
    frame=b.Pos(0,-12,-96);shape=frame*_narrow_base_pan()
    # Continuous inset stamped-neck study, not per-fastener collision relief.
    shape=joined(shape-b.Pos(0,0,-64)*b.Box(1000,500,52))
    outer=b.loft([b.Pos(0,y,z)*b.RectangleRounded(l,w,24) for z,l,w,y in [(-90,726,242,-12),(-76,726,232,-7),(-38,726,232,-7)]],ruled=True)
    inner=b.loft([b.Pos(0,y,z)*b.RectangleRounded(l,w,21) for z,l,w,y in [(-91,720,236,-12),(-90,720,236,-12),(-76,720,226,-7),(-38,720,226,-7),(-37,720,226,-7)]],ruled=True)
    shape=joined((shape+outer)-inner)
    flange=b.Pos(0,-12,-38)*b.extrude(b.RectangleRounded(762,258,28)-b.Pos(0,5)*b.RectangleRounded(720,226,21),amount=4)
    shape=joined(shape+flange)
    for a,c,inner_r,outer_r in ENDS:
        pa,pc=(a-6,c) if a>0 else (a,c+6)
        collar=(x_cylinder(outer_r+4,pa,pc)-x_cylinder(outer_r,pa-1,pc+1)) & b.Pos(0,0,-117)*b.Box(1000,400,166)
        shape=joined(shape+collar)
    for a,c,inner,outer in ENDS:
        pa,pc=(a-6,c) if a>0 else (a,c+6)
        shape-=x_cylinder(outer,pa-1,pc+1)
    for x,y,z in STATIONS:shape+=b.Pos(x,y)*cylinder(9,z+1.6,z+5.6)
    shape-=b.Pos(371.,0)*cylinder(9.1,-61.4,-56)
    for x,y,z in STATIONS:shape-=b.Pos(x,y)*cylinder(4.3,z-1,z+9)
    return frame.inverse()*shape


def build(api):
    define,add,group=api
    group('oil-pan-fastener-assembly','Oil-pan screw & washer study','oil-pan-assembly')
    define('oil-pan-mounting-screw',screw_shape(),'Pan mounting screw · 5/16-18 × .87','Clamps the flange through its washer; nominal size and total count follow Ford service evidence.','closures','#a3adb3',SOURCES,GAPS)
    define('oil-pan-mounting-washer',washer_shape(),'Pan mounting washer','Distributes clamp load; captive construction and dimensions remain illustrative.','closures','#8f9aa4',SOURCES,GAPS)
    define('oil-pan-molded-gasket',gasket_shape(),'Continuous molded pan gasket study','A continuous seal crosses both long rails and the front/rear end bridges. Shape is a provisional interface study informed by the exact replacement image.','closures','#3e75bd',SOURCES,GAPS)
    add('oil-pan-molded-gasket','oil-pan-molded-gasket','oil-pan-assembly',(0,0,0),(0,0,-210))
    for n,(x,y,z) in enumerate(STATIONS,1):
        for role in ('screw','washer'):
            add(f'oil-pan-mounting-{role}-{n}',f'oil-pan-mounting-{role}','oil-pan-fastener-assembly',(x,y,z),((25 if x>0 else -25) if n>20 else 0,(25 if y>0 else -25) if n<=20 else 0,-360 if role=='screw' else -340))
