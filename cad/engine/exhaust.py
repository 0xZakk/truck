"""Separate three-cylinder cast manifolds; source identity, provisional cavities."""
import build123d as b
SOURCES=['system-9d57ed6d21b9','system-b9d2a4ac71cc']
GAPS=['The factory procedure establishes separate front/rear castings and head attachment. Runner bends, common chamber, flange contours, outlet dimensions and installed stations remain provisional.', 'Production EGR takeoff details, air-injection connections, lifting eye, dowel, head fasteners and exhaust-pipe joints remain unresolved. No production gasket is inferred from the model.']
def build(api):
    define,add,group,cylinders,deck=api
    group('exhaust','Exhaust manifolds')
    z=deck+23.5
    def box(x,y,h,r):return b.extrude(b.RectangleRounded(x,y,r),amount=h/2,both=True)
    for name,ports,number in [('front',cylinders[:3],'F5TZ9430F'),('rear',cylinders[3:],'F5TZ9431F')]:
        center=ports[1]+25
        shape=b.Pos(center,-180,230)*box(280,48,48,12)
        paths=[]
        for x in ports:
            x+=25
            branch=b.Pos(x,-138,z)*b.Rot(90,0,0)*b.Cylinder(18,10)
            path=b.Bezier((x,-138,z),(x,-188,z),(x,-180,258),(x,-180,235))
            paths.append(path)
            branch+=b.sweep(b.Plane(origin=path@0,z_dir=path%0)*b.Circle(18),path=path)
            shape+=branch
        shape+=b.Pos(center,-180,175)*b.Cylinder(27,70)
        shape-=b.Pos(center,-180,230)*box(268,36,36,8)
        shape-=b.Pos(center,-180,175)*b.Cylinder(20,86)
        for path in paths:
            start=path@0
            bore=b.Wire([b.Line((start.X,-125,z),start),path,b.Line(path@1,(start.X,-180,225))])
            shape-=b.sweep(b.Plane(origin=bore@0,z_dir=bore%0)*b.Circle(15),path=bore)
        if name=='rear':
            from egr_tube import manifold_interface
            shape=manifold_interface(shape)
        id='exhaust-'+name
        define(id,shape,name.title()+' exhaust manifold',f'Collects exhaust from three cylinders into a shared chamber and outlet. The catalog lists {number}. Internal and exterior contours are provisional.','exhaust','#7c6e63',SOURCES,GAPS)
        add(id,id,'exhaust',explode=(0,-170,-80))
