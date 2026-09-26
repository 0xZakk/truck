"""Six-hole stamped pushrod-cover study with a matching block-interface study.

Architecture: EngineQuest FSP300N photograph. Envelope, rib sections, hole stations
and thickness are modeling assumptions, not measured replacement dimensions.
"""
import math
import build123d as b

LENGTH=670.0
HEIGHT=110.0
THICKNESS=1.2
STATIONS=[(i-2.5)*114.0 for i in range(6)]
SOURCES=['enginequest-fsp300n','fel-pro-vin-y-gaskets','ford-industrial-parts','fel-pro-10740-retailer']

# Provisional placement shared by the block interface and component publisher.
MOUNT=b.Pos(0,119,185)*b.Rot(-90,0,0)


def block_interface_shape(block):
    """Open the cam-side wall and add connected provisional fastener supports.

    Neither the window section nor the six supporting webs is a traced casting.
    Blind bores use a clearance envelope, not female thread geometry. Keeping
    this separate allows a fit study without publishing an untested block.
    """
    window=b.Pos(0,0,-50)*b.extrude(b.RectangleRounded(LENGTH-18,HEIGHT-18,8),amount=70)
    block=block-MOUNT*window
    rail_profile=b.RectangleRounded(LENGTH,HEIGHT,10)-b.RectangleRounded(LENGTH-18,HEIGHT-18,8)
    block+=MOUNT*(b.Pos(0,0,-14)*b.extrude(rail_profile,amount=12.5))
    for x in STATIONS:
        # Webs join both perimeter rails. Pushrods are offset from their centers.
        block+=MOUNT*(b.Pos(x,0,-20.75)*b.Box(16,HEIGHT-16,38.5))
        block-=MOUNT*(b.Pos(x,0,-5.5)*b.Cylinder(4,8.2))
    return block


def cover_shape():
    outer=b.loft([b.Pos(0,0,z)*b.RectangleRounded(l,h,r) for z,l,h,r in
                  [(0,LENGTH,HEIGHT,10),(3,LENGTH-12,HEIGHT-12,8),(9,LENGTH-18,HEIGHT-18,8)]],ruled=True)
    inner=b.loft([b.Pos(0,0,z)*b.RectangleRounded(l,h,r) for z,l,h,r in
                  [(-2,LENGTH-2.4,HEIGHT-2.4,8.8),(2.5,LENGTH-14.4,HEIGHT-14.4,6.8),(7.8,LENGTH-20.4,HEIGHT-20.4,6.8)]],ruled=True)
    # Matching outer and inner rib envelopes form pressed relief in the sheet,
    # rather than adding disconnected bars to the cover's visible surface.
    for x in STATIONS:
        for sign in [-1,1]:
            a=(x-32,-32*sign,9);c=(x+32,32*sign,9)
            path=b.Line(a,c)
            outer+=b.sweep(b.Plane(origin=a,z_dir=path%0)*b.Circle(3),path=path)
            ipath=b.Line((a[0],a[1],7.8),(c[0],c[1],7.8))
            inner+=b.sweep(b.Plane(origin=ipath@0,z_dir=ipath%0)*b.Circle(3),path=ipath)
    for x in STATIONS:
        # Stop the inner rib relief at the seating land. Otherwise flattening
        # the exterior rib crowns would break through into star-shaped holes.
        inner-=b.Pos(x,0,22.8)*b.Cylinder(13,30)
    cover=outer-inner
    for x in STATIONS:
        # Keep a flat annulus around each grommet seat.
        cover-=b.Pos(x,0,14)*b.Cylinder(13,10)
        cover-=b.Pos(x,0,5)*b.Cylinder(6.75,30)
    return cover


def gasket_shape():
    """Perimeter study; compressed thickness and exact outline are unverified."""
    profile=b.RectangleRounded(LENGTH,HEIGHT,10)-b.RectangleRounded(LENGTH-18,HEIGHT-18,8)
    return b.Pos(0,0,-1.5)*b.extrude(profile,amount=1.5)


def bolt_shape(length=25.4):
    """5/16-18 x1-inch industrial comparison; head/thread tolerances assumed."""
    radius=25.4*5/32
    pitch=25.4/18
    bolt=b.Pos(0,0,length/2)*b.Cylinder(radius,length)
    bolt+=b.Pos(0,0,length)*b.extrude(b.RegularPolygon(12.7/math.sqrt(3),6),amount=5.3)
    path=b.Helix(pitch,length+2, radius,center=(0,0,-1))
    profile=b.Plane(origin=path@0,x_dir=(1,0,0),z_dir=path%0)*b.Polygon(
        (-.61343*pitch,0),(.2,-.615),(.2,.615),align=None)
    cutter=b.sweep(profile,path=path,is_frenet=True)
    threaded_length=length-1.6
    cutter=cutter.intersect(b.Pos(0,0,threaded_length/2)*b.Cylinder(5,threaded_length))
    return bolt-cutter


def grommet_shape():
    """Replacement-envelope study; lower neck and compressed shape unverified.

    Retailer-listed10740 envelope:0.48-inch thickness, approximately1-inch OD,
    0.318–0.338-inch ID. This is not a manufacturer dimensioned section.
    """
    bottom=7.8
    top=bottom+.48*25.4
    profile=b.Plane.XZ*b.Polygon(
        (4.2,bottom),(6.65,bottom),(6.65,9),(12.7,9),
        (12.7,top-.5),(12.2,top),(11.7,top),(11.4,top-1.5),
        (8,top-1.5),(7.5,top),(4.2,top),align=None)
    return b.revolve(profile,axis=b.Axis.Z)


def build(api):
    """Publish only alongside the matching block-interface reconstruction."""
    define,add,group=api
    parent='pushrod-cover-assembly'
    group(parent,'Pushrod side cover & seals','structure')
    gaps=[
        'Cover envelope, hole stations, stamped ribs, gasket section and casting interface are provisional.',
        'Grommet dimensions are a retailer replacement envelope; hidden section and compression are unverified.',
        '5/16-18 x1-inch bolt is an industrial comparison. The present uncompressed stack gives only3.908mm engagement; installed bolt identity and adequacy remain unverified.'
    ]
    for key,shape,name,function,color in [
        ('pushrod-cover',cover_shape(),'Pushrod side cover','Closes the block-side access opening beside the pushrods and lifters. Stamped ribs stiffen the thin cover.','#42686c'),
        ('pushrod-cover-gasket',gasket_shape(),'Pushrod cover perimeter gasket','Seals the perimeter where the cover meets the block. This is separate from the six fastener grommets.','#b49967'),
        ('pushrod-cover-grommet',grommet_shape(),'Pushrod cover bolt grommet','Seals around one cover fastener. The modeled rubber section is an uncompressed replacement-envelope study.','#353a39'),
        ('pushrod-cover-bolt',bolt_shape(),'Pushrod cover bolt · industrial comparison','Clamps through the grommet toward a blind block mounting bore. Thread pitch is modeled; clamp load and female threads are not.','#a3adb3')
    ]:
        define(key,shape,name,function,'structure',color,SOURCES,gaps)
    add('pushrod-cover','pushrod-cover',parent,(0,119,185),(0,180,0),(-90,0,0))
    add('pushrod-cover-gasket','pushrod-cover-gasket',parent,(0,119,185),(0,100,0),(-90,0,0))
    for i,x in enumerate(STATIONS,1):
        add(f'pushrod-cover-grommet-{i}','pushrod-cover-grommet',parent,(x,119,185),(0,235,0),(-90,0,0),name=f'Cover bolt grommet {i}')
        add(f'pushrod-cover-bolt-{i}','pushrod-cover-bolt',parent,(x,119+7.8+.48*25.4-25.4,185),(0,285,0),(-90,0,0),name=f'Cover bolt {i}')
