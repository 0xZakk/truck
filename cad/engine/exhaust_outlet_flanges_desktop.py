"""Integral two-hole exhaust outlet flange studies, not separate cosmetic parts."""
import build123d as cad

CENTERS={'exhaust-front':195.688,'exhaust-rear':-145.688}
HOLES=((-32.,22.),(32.,-22.))
BOTTOM,TOP=140.,150.
SOURCES=['dorman-674185-opposite-photo','dorman-674185-application',
         'dorman-674186-opposite-photo','dorman-674186-catalog-application']
GAPS=[
    'Manufacturer replacement photographs show an integral outlet flange with two opposed mounting holes on each manifold. Installed casting identity remains unknown.',
    'The40mm outlet opening,10mm flange thickness,32mm central outer radius,12mm ear radii and77.67mm diagonal hole spacing are explicit geometric assumptions, not measurements from the photos.',
    'Outlet axes and elevations retain the provisional model. Production sealing seat, mating pipe flange, fastener identity, thread engagement, gasket applicability and thermal performance remain unresolved.'
]


def cylinder(radius,bottom,top):
    return cad.Pos(0,0,(bottom+top)/2)*cad.Cylinder(radius,top-bottom)


def flange(horizontal):
    profile=cad.Circle(32)
    for x,y in HOLES:
        profile+=cad.Pos(x,y)*cad.Circle(12)
        # A broad triangular web connects each integral ear to the outlet neck.
        profile+=cad.Polygon((-y*.48,x*.48),(y*.48,-x*.48),(x,y),align=None)
    shape=cad.Pos(0,0,BOTTOM)*cad.extrude(profile,amount=TOP-BOTTOM)
    shape-=cylinder(20,BOTTOM-1,TOP+1)
    for x,y in HOLES:shape-=cad.Pos(x,y)*cylinder(5.5,BOTTOM-1,TOP+1)
    return cad.Pos(horizontal,-180,0)*shape


def interface(shape,identifier):
    return shape.fuse(flange(CENTERS[identifier]))


ADAPTERS={identifier:(lambda shape,key=identifier:interface(shape,key)) for identifier in CENTERS}
