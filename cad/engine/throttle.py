"""Twin-bore throttle teaching mechanism; dimensions are provisional millimeters."""
import build123d as b
SOURCES=['truck-throttle-operation','truck-throttle-service','truck-throttle-catalog']
GAPS=['The factory manual supports dual bores, a separate gasket and four mounting studs/nuts. Bore diameter, shaft/plate construction, casting contour and fastener dimensions are assumed.', 'IAC/TPS studies and bypass passages are present; their exact variants and internal details remain unresolved. Purge ports, linkage, return spring, accelerator bracket and plate screws remain unmodeled. Idealized 0–90 degree motion is not the production stop calibration.']
def build(api):
    define,add,group,rounded_box,cx=api
    group('throttle-assembly','Throttle body','induction')
    group('throttle-hardware','Mounting hardware','throttle-assembly')
    group('throttle-moving','Shaft & butterfly plates','throttle-assembly',motion={'type':'throttle'},position=(394,25,490))
    # Housing axes and mounting face match the provisional upper intake adapter.
    body=b.Pos(375.5,25,490)*b.Box(6,124,68)
    for y in [-2,52]:body+=b.Pos(397.5,y,490)*cx(24,50)
    body+=b.Pos(394,25,490)*b.Rot(90,0,0)*b.Cylinder(7,124)
    # Provisional IAC mounting pad joins the casting; drill main bores after union.
    body+=b.Pos(397,9,516)*b.Box(48,62,20)
    for y in [-2,52]:body-=b.Pos(397.5,y,490)*cx(20,60)
    body-=b.Pos(394,25,490)*b.Rot(90,0,0)*b.Cylinder(3.2,140)
    # Sensor screw bosses on the shaft end.
    for z in [468,512]:
        body+=b.Pos(394,-25,z)*b.Box(10,24,10)
        body-=b.Pos(394,-31,z)*b.Rot(90,0,0)*b.Cylinder(2.2,24)
    # Two separate L-shaped passages connect either side of the closed plates.
    for x in [385,409]:
        body-=b.Pos(x,25,517)*b.Cylinder(5,24)
        body-=b.Pos(x,10,506)*b.Rot(90,0,0)*b.Cylinder(5,40)
    gasket=b.Pos(371.75,25,490)*b.Box(1.5,124,68)
    for y in [-2,52]:gasket-=b.Pos(371.75,y,490)*cx(20,4)
    for y in [-24,74]:
        for z in [464,516]:
            body-=b.Pos(397.5,y,z)*cx(4.4,60)
            body-=b.Pos(403.5,y,z)*cx(7.5,50)
            gasket-=b.Pos(371.75,y,z)*cx(4.4,4)
    def d(id,shape,name,function,color):define(id,shape,name,function,'induction',color,SOURCES,GAPS)
    d('throttle-housing',body,'Twin-bore throttle housing','Two passages carry inlet air into the plenum. The manual-transmission catalog lists F6PZ9E926GA for the complete service assembly. A provisional two-port bypass connects the separate IAC study; other controls remain incomplete.','#9da8ac')
    add('throttle-housing','throttle-housing','throttle-assembly',explode=(180,0,0))
    d('throttle-gasket',gasket,'Throttle body gasket','Seals the throttle housing against the upper intake manifold. Twin openings and four mounting holes follow the factory layout; their dimensions are provisional.','#b6996a')
    add('throttle-gasket','throttle-gasket','throttle-assembly',explode=(85,0,0))
    shaft=b.Rot(90,0,0)*b.Cylinder(3,124)
    for y in [-27,27]:shaft-=b.Pos(0,y,0)*b.Box(1.4,40,8)
    d('throttle-shaft',shaft,'Throttle shaft','Rotates both butterfly plates together. Slots keep the modeled plates distinct from the shaft; exact slot, screw and linkage geometry is not established.','#657981')
    add('throttle-shaft','throttle-shaft','throttle-moving',explode=(180,0,90))
    d('throttle-plate',cx(19.6,1),'Throttle butterfly plate','A rotating disc restricts its air passage when closed and turns edge-on when open. This idealized disc omits production bevels, idle orifice and retaining screws.','#c5a56b')
    for i,y in enumerate([-27,27],1):add(f'throttle-plate-{i}','throttle-plate','throttle-moving',(0,y,0),(260,0,90),name=f'Throttle butterfly plate {i}')
    d('throttle-mount-stud',cx(4,30),'Throttle mounting stud','One of four studs locating the gasket and retaining the throttle body. Threads and installed depth are provisional.','#687983')
    nut=b.extrude(b.Plane.YZ*b.RegularPolygon(7,6),amount=3,both=True)-cx(4.2,8)
    d('throttle-mount-nut',nut,'Throttle retaining nut','One of four nuts securing the housing. The accelerator bracket sharing this interface remains unmodeled.','#657781')
    i=0
    for y in [-24,74]:
        for z in [464,516]:
            i+=1
            add(f'throttle-stud-{i}','throttle-mount-stud','throttle-hardware',(371,y,z),(100,0,0),name=f'Throttle mounting stud {i}')
            add(f'throttle-nut-{i}','throttle-mount-nut','throttle-hardware',(381.5,y,z),(230,0,0),name=f'Throttle retaining nut {i}')
