"""Dorman 902-1002-inspired outlet casting; sourced holes, provisional contours."""
import build123d as b

def build(api):
    define,add,group,_cx=api
    def cx(radius,length):
        return b.Solid.make_cylinder(radius,length,b.Plane(origin=(-length/2,0,0),z_dir=(1,0,0)))
    group('coolant-outlet-assembly','Coolant outlet and thermostat','cooling',position=(415,0,295))
    src=['dorman-902-1002','truck-thermostat-housing-parts','system-44801c5452af']
    gaps=['Manufacturer specifies two 0.313-inch mounting holes and a 1.5-inch outside diameter. Neck OD uses that catalog field; its measurement station is not supplied.',
          'Photo-informed flange outline, bolt spacing, secondary passage, neck curvature, lengths, wall thickness and installed position are provisional. Thread form and hose barb need measurements.',
          'Passages are open in this casting, but matching head coolant passages and hose connections remain unfinished. Fastener dimensions are assumptions, not a service specification.']
    holes=[(-40,0),(40,0)]
    hole_radius=.313*25.4/2
    def flange(thickness):
        f=cx(33,thickness)
        for y,z in holes:
            f+=b.Pos(0,y,z)*cx(10,thickness)
            f+=b.Pos(0,y/2,z)*b.Box(thickness,abs(y),18)
        f+=b.Pos(0,28,-30)*cx(16,thickness)
        f+=b.Pos(0,20,-20)*b.Box(thickness,25,32)
        for y,z in holes:f-=b.Pos(0,y,z)*cx(hole_radius,thickness+2)
        return f
    # Construct each hollow section before joining it. Cutting the broad
    # throat through an already-fused torus triggers an OCCT extrema stall.
    quadrant=b.Pos(90,0,-13)*b.Box(70,100,70)
    def elbow(radius):
        bend=(b.Pos(55,0,22)*b.Rot(90,0,0)*b.Torus(22,radius)) & quadrant
        return bend + b.Pos(50,0,0)*cx(radius,10) + b.Pos(77,0,54)*b.Cylinder(radius,64)
    print("Outlet: hollow neck",flush=True)
    neck=elbow(19.05)-elbow(16)
    print("Outlet: hollow chamber",flush=True)
    chamber=b.Pos(14.85,0,0)*cx(32,28.3)-b.Pos(14.85,0,0)*cx(27.1,30)
    taper=b.Pos(37,0,0)*b.Rot(0,90,0)*(b.Cone(32,19.05,16)-b.Cone(27.1,16,16))
    base=b.Pos(3.7,0,0)*flange(6)-cx(27.1,15)
    side=b.Pos(19,28,-30)*(cx(16,36)-cx(11,38))
    base-=b.Pos(0,28,-30)*cx(11,15)
    side-=b.Pos(14.85,0,0)*cx(27.1,30)
    chamber-=b.Pos(19,28,-30)*cx(11,42)
    taper-=b.Pos(19,28,-30)*cx(11,42)
    side-=b.Pos(37,0,0)*b.Rot(0,90,0)*b.Cone(27.1,16,16)
    print("Outlet: joining hollow sections",flush=True)
    casting=base+chamber+taper+neck+side
    print("Outlet: gasket and hardware",flush=True)
    gasket=b.Pos(-1.235,0,0)*(flange(1.2)-cx(27.1,4)-b.Pos(0,28,-30)*cx(11,4))
    fastener=b.Pos(-8,0,0)*cx(3.5,29.4)+b.Pos(9.7,0,0)*b.extrude(b.Plane.YZ*b.RegularPolygon(6,6),amount=3,both=True)
    for id,shape,name,fn,color in [
      ('coolant-outlet-housing',casting,'Coolant outlet housing','Carries coolant from the thermostat chamber into the radiator-hose connection. A separate passage and threaded boss follow the replacement casting photo.','#8a9fa7'),
      ('coolant-outlet-gasket',gasket,'Coolant outlet gasket','Seals both the thermostat opening and the adjacent passage at the mounting face.','#b09a76'),
      ('coolant-outlet-bolt',fastener,'Coolant outlet mounting bolt','Clamps the outlet flange and gasket. Unthreaded geometry and assumed dimensions are not a torque specification.','#73858f')]:
        define(id,shape,name,fn,'cooling',color,src,gaps)
    add('coolant-outlet-housing','coolant-outlet-housing','coolant-outlet-assembly',explode=(350,0,0))
    add('coolant-outlet-gasket','coolant-outlet-gasket','coolant-outlet-assembly',explode=(-120,0,0))
    for i,(y,z) in enumerate(holes,1):add('coolant-outlet-bolt-'+str(i),'coolant-outlet-bolt','coolant-outlet-assembly',pos=(0,y,z),explode=(450,0,0))
