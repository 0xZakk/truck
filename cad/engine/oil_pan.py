"""Rear-sump pan study, retaining unresolved block flange interface explicitly."""
import math
import build123d as b
DRAIN_LOCAL=(40-59*25/105,0,-104)
DRAIN_ROTATION=(0,90+math.degrees(math.atan(25/105)),0)
SOURCES=['truck-oil-pan-hardware','dorman-264011-pan','fel-pro-vin-y-gaskets']
GAPS=['Rear-sump architecture and maximum depth follow the Dorman264-011 comparison. The retained flange, overall length/width, transition station and contours are provisional and do not yet reproduce the published replacement envelope.', 'The pan gasket/block flange, mounting-hole stations and pickup depth need coordinated reconstruction. The side strips are incomplete placeholders: the VIN-Y replacement catalog specifies molded rubber, and the older separate-piece illustration does not establish installed construction. No capacity or production-fit claim is made. Replacement drain uses M14x1.5, which must not be mixed with the older1/2-20 comparison plug.']

def build(api):
    define,add,group,rounded_box,cx,length=api
    group('oil-pan-assembly','Oil pan & seals','closures')
    outer=rounded_box(length,242,122,24)
    inner=b.Pos(0,0,3)*rounded_box(length-6,236,122,21)
    # Rear lies at -X. The only applied manufacturer envelope dimension is depth:
    # flange upper face localZ62 to rear floor localZ-172.95 =234.95mm.
    rear=b.loft([b.Pos(-165,0,z)*b.RectangleRounded(l,w,r) for z,l,w,r in [(-172.95,350,214,24),(-150,360,220,24),(-45,410,242,24)]],ruled=True)
    rear_inner=b.loft([b.Pos(-165,0,z)*b.RectangleRounded(l,w,r) for z,l,w,r in [(-169.95,344,208,21),(-150,354,214,21),(-42,410,236,21)]],ruled=True)
    pan=(outer+rear)-(inner+rear_inner)
    pan+=b.Pos(0,0,60)*(rounded_box(length+16,258,4,28)-rounded_box(length-6,236,8,21))
    pan-=b.Pos(377,12,96)*cx(45,40)
    pan-=b.Pos(-377,12,96)*cx(49.1,30)
    drain_frame=b.Pos(*DRAIN_LOCAL)*b.Rot(*DRAIN_ROTATION)
    # Local machined seat in the sloping rear-sump wall. Boss construction is
    # provisional; this is not a claim about a welded nut or production stamping.
    pan+=drain_frame*(b.Pos(0,0,-4.5)*b.Cylinder(11,9))
    pan-=drain_frame*(b.Pos(0,0,-4)*b.Cylinder(7.1,30))
    # Flatten the gasket seating patch without cutting the surrounding sump.
    pan-=drain_frame*(b.Pos(0,0,5)*b.Cylinder(12,10))
    define('oil-pan',pan,'Oil pan','Stores returning oil in a deeper rear sump. The forward section clears the crankcase region; transition and flange geometry remain provisional. Drain dimensions beyond the published thread, sealing details and the pickup-to-floor interface remain provisional.','closures','#42686c',SOURCES,GAPS)
    add('oil-pan','oil-pan','oil-pan-assembly',(0,-12,-96),(0,0,-320))
    plug=b.Pos(0,0,-4)*b.Cylinder(7,10)
    plug+=b.Pos(0,0,1)*b.extrude(b.RegularPolygon(17/math.sqrt(3),6),amount=5)
    path=b.Helix(1.5,13,7,center=(0,0,-10.5))
    profile=b.Plane(origin=path@0,x_dir=(1,0,0),z_dir=path%0)*b.Polygon((-.85,0),(.3,-.664),(.3,.664),align=None)
    cutter=b.sweep(profile,path=path,is_frenet=True)
    cutter=cutter.intersect(b.Pos(0,0,-4.5)*b.Cylinder(8,9))
    plug-=cutter
    drain_gasket=b.Pos(0,0,.5)*(b.Cylinder(11,1)-b.Cylinder(7.15,3))
    for key,shape,name,fn,color in [('oil-pan-drain-plug',plug,'Pan drain plug · M14×1.5 comparison','Closes the replacement-pan drain. Nominal thread diameter and pitch follow Dorman264-011; head size, length, tolerance and location remain provisional.','#a3adb3'),('oil-pan-drain-gasket',drain_gasket,'Pan drain sealing washer','Seals the plug shoulder against the modeled flat seating patch. Washer dimensions, material and installed compression are unverified.','#b59560')]:
        define(key,shape,name,fn,'closures',color,SOURCES,GAPS)
        add(key,key,'oil-pan-assembly',(DRAIN_LOCAL[0],-12,DRAIN_LOCAL[2]-96),(100,0,-80),DRAIN_ROTATION)
    gasket=rounded_box(length+16,258,2,28)-rounded_box(length-6,236,5,21)
    gasket-=b.Pos(377,12,33)*cx(45,40)
    gasket-=b.Pos(-377,12,33)*cx(49.1,30)
    for i,side in enumerate(sorted(gasket.solids(),key=lambda s:s.center().Y),1):
        key=f'pan-side-gasket-{i}'
        define(key,side,f'Pan gasket side study {i}','Illustrates the side sealing region of the sump flange. This strip is not a verified separate production part. The applicable replacement uses molded rubber; its continuous perimeter and end sections still need reconstruction.','closures','#b49967',SOURCES,GAPS)
        add(key,key,'oil-pan-assembly',(0,-12,-33),(0,0,-210))
