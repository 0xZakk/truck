"""Source-compared rear collector; all new cross sections are explicit estimates."""
import build123d as b
import exhaust_front_profile as front
import exhaust_rear_entries as rear

# X, Z and radius: a rounded cross-section arm rises toward each outside runner
# and broadens into the center outlet. No pixel-to-mm measurement is implied.
SECTIONS=[(-259.48,236,24),(-225,230,23),(-190,224,26),
          (-145.688,225,35),(-100,224,26),(-65,230,23),(-31.896,236,24)]
WALL=6.

def collector(shrink=0):
    sections=[b.Plane(origin=(x,-180,z),x_dir=(0,1,0),z_dir=(1,0,0))*b.Circle(r-shrink)
              for x,z,r in SECTIONS]
    s=b.loft(sections,ruled=False)
    for x,z,r in (SECTIONS[0],SECTIONS[-1]):s=s.fuse(b.Pos(x,-180,z)*b.Sphere(r-shrink))
    return s

def protected_regions():
    return {'head_entries_and_bolt_lands':b.Pos(-145,-35,260)*b.Box(500,230,230),
            'outlet_and_flange':b.Pos(-145,-180,140)*b.Box(500,200,100),
            'provisional_egr_end':b.Pos(-291,-180,229.5)*b.Box(54,50,51)}

def old_collector():
    return b.Pos(rear.PORTS[1],-180,230)*b.extrude(b.RectangleRounded(280,48,12),amount=24,both=True)

def compound(s):
    return b.Compound(children=list(s)) if isinstance(s,b.ShapeList) else s

def build(baseline):
    outer=collector()
    inner=collector(WALL)
    # The inherited radius-18 swept exterior has singular triangulation near
    # its tight inner bend despite valid BRep status. A ruled six-section loft
    # replaces only that provisional exterior; original gas void stays exact.
    shape=outer.fuse(b.Pos(rear.PORTS[1],-180,175)*b.Cylinder(27,70))
    path=front.runner_path(0)
    profiles=[b.Plane(origin=path@t,x_dir=(1,0,0),z_dir=path%t)*b.Circle(18)
              for t in [.27,.40,.55,.70,.85,1]]
    runner=front.transition(0,outside=True).fuse(b.loft(profiles,ruled=True))
    runner &= b.Pos(0,-183,front.PORT_Z)*b.Box(80,100,100)
    for x in rear.PORTS:shape=shape.fuse(b.Pos(x,0,0)*runner)
    shape-=inner
    # Reopen original branch and discharge lumens; they are never guessed from
    # an external photo. The resulting wall is independently sampled by checker.
    for x in rear.PORTS:shape-=front.runner_void(x)
    shape-=b.Pos(rear.PORTS[1],-180,175)*b.Cylinder(20,86)
    # Exact local baseline patches retain existing provisional interfaces.
    for region in protected_regions().values():
        shape=compound(shape-region).fuse(compound(baseline&region))
    return shape

def flow_witness():
    # Piecewise centerline witness; small cylinders overlap spherical joins.
    # This checks connected topology, not the full hydraulic cross section.
    segments=[((-287,-180,230),(-31.896,-180,230)),
              ((-145.688,-180,139),(-145.688,-180,230))]
    for x in rear.PORTS:
        route=front.runner_path(x)
        pts=[tuple(route@t) for t in [0,.25,.5,.75,1]]+[(x,-180,230)]
        segments.extend(zip(pts[:-1],pts[1:]))
    pieces=[];points=set()
    for start,end in segments:
        vector=b.Vector(end)-b.Vector(start)
        pieces.append(b.Plane(origin=start,z_dir=vector)*b.Cylinder(2,vector.length,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN)))
        points.add(start);points.add(end)
    pieces.extend(b.Pos(*pt)*b.Sphere(2) for pt in points)
    return pieces[0].fuse(*pieces[1:])
