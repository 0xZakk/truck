"""EGR tube routing candidate. Replacement diameter sourced; route provisional.

Not installed until collision and interface validation pass. Dorman 598-105
confirms application and OD, but its length field has no measurement definition.
"""
import build123d as b

OUTSIDE_DIAMETER=0.74*25.4
WALL=1.4  # assumed; not in the manufacturer specifications
SOURCES=['dorman-598-105','efi-intake-drawing']
GAPS=['Tube OD is from the applicable replacement catalog; wall thickness, bend coordinates and fitting dimensions are provisional.',
      'The published 17.9 inch length has no measurement definition and is not treated as a verified developed centerline length.',
      'Protective sleeve construction, thread forms and sealing seats remain unverified. Route is a candidate, not installed factory routing.']
MANIFOLD_FACE=(-285.688,-180,230)
START=(-315.688,-180,230)
END=(-412,25,434)

def path():
    # Leave rear collector behind the block before rising to the valve inlet.
    return b.Bezier(START,(-470,-180,230),(-455,25,365),(-412,25,404),END)

def sweep_ring(route,outer,inner):
    plane=b.Plane(origin=route@0,z_dir=route%0)
    return b.sweep(plane*(b.Circle(outer)-b.Circle(inner)),path=route)

def parts():
    route=path()
    tube=sweep_ring(route,OUTSIDE_DIAMETER/2,OUTSIDE_DIAMETER/2-WALL)
    # Separate machined end geometry is fused into this tube assembly study;
    # brazing, flare formation and production construction remain unverified.
    tube+=b.Pos(*END)*ring(OUTSIDE_DIAMETER/2,OUTSIDE_DIAMETER/2-WALL,5)
    tube+=b.Pos(END[0],END[1],END[2]+5)*ring(11,OUTSIDE_DIAMETER/2-WALL,5)
    # Sleeve stops short of both fittings; actual weave is not approximated as
    # individual strands without evidence for the braid construction.
    sleeve_path=route.trim(.08,.92)
    sleeve=sweep_ring(sleeve_path,12.5,OUTSIDE_DIAMETER/2+.2)
    return {'egr-exhaust-tube':(tube,'EGR exhaust tube'),
            'egr-tube-heat-sleeve':(sleeve,'EGR tube protective sleeve'),
            'egr-tube-valve-nut':(valve_nut(),'EGR tube valve union nut'),
            'egr-tube-manifold-fitting':(manifold_fitting(),'EGR tube manifold fitting')}


def ring(ro,ri,height):
    return b.extrude(b.Circle(ro)-b.Circle(ri),amount=height)

def valve_nut():
    s=b.extrude(b.RegularPolygon(16,6),amount=24)
    s-=b.Pos(0,0,-1)*b.Cylinder(9.5,7,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
    s-=b.Pos(0,0,5)*b.Cylinder(11.1,5,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
    s-=b.Pos(0,0,10)*b.Cylinder(12.1,15,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
    # Remove the central remnant of the initial bore too.
    s-=b.Cylinder(9.5,26,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
    return b.Pos(*END)*s

def manifold_fitting(insertion_length=19):
    s=ring(OUTSIDE_DIAMETER/2,OUTSIDE_DIAMETER/2-WALL,5)
    s+=b.Pos(0,0,5)*b.extrude(b.RegularPolygon(16,6)-b.Circle(OUTSIDE_DIAMETER/2-WALL),amount=18)
    s+=b.Pos(0,0,23)*ring(12,OUTSIDE_DIAMETER/2-WALL,insertion_length)
    return b.Pos(*START)*b.Rot(0,90,0)*s

def manifold_interface(manifold):
    # Bore opens the rear end wall to its existing collector cavity. Thread
    # envelopes remain smooth until an applicable thread specification is found.
    bore=b.Pos(MANIFOLD_FACE[0]-1,MANIFOLD_FACE[1],MANIFOLD_FACE[2])*b.Rot(0,90,0)*b.Cylinder(12.1,17,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
    return manifold-bore

def build(api):
    define,add,group=api
    group('egr-exhaust-line','EGR exhaust tube & connections','egr')
    functions={
      'egr-exhaust-tube':'Carries exhaust from the rear manifold to the valve inlet. End construction and routing remain a fit study.',
      'egr-tube-heat-sleeve':'Protective woven covering visible on the replacement tube. This smooth sleeve omits unverified braid construction and thermal properties.',
      'egr-tube-valve-nut':'Captures the tube end at the externally threaded EGR valve inlet. Thread and seat geometry are simplified, not production verified.',
      'egr-tube-manifold-fitting':'Joins the tube to the rear exhaust collector. The hollow fitting and collector bore share a gas passage; thread and sealing details remain unverified.'}
    for i,(id,(shape,name)) in enumerate(parts().items()):
        define(id,shape,name,functions[id],'induction','#363835' if 'sleeve' in id else '#989f9e',SOURCES,GAPS)
        add(id,id,'egr-exhaust-line',explode=(-70-i*30,-50-i*25,-i*20))
