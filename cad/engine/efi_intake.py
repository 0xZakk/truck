"""EFI intake architecture from Ford illustrations; dimensions remain provisional."""
import build123d as b
from fuel_mounts import MOUNT_X

SOURCES=['fsm-212bf152ff88','fsm-9e1b0b719d0e','efi-intake-drawing']
GAPS=['Upper/lower split and seven retaining studs are supported by the truck manual. Runner curves, plenum volume, port profiles, wall thickness and installed stations remain provisional.',
      'Fuel rail, injectors and throttle controls are provisional studies. EGR, vacuum fittings, heat shield, support bracket and head-mounting hardware remain to be reconstructed. No airflow simulation is claimed.']

def build(api):
    define,add,group,rounded_box,cx,cylinders,mains,deck=api
    group('induction','EFI intake')
    group('intake-castings','Manifolds & gaskets','induction')
    group('intake-studs','Upper manifold retaining studs','induction')
    zhead=deck+23.5
    zbase=360.0
    ports=list(cylinders)
    # Lower manifold has six short rising passages and a common upper flange.
    lower=b.Pos(0,-228,zbase-5)*rounded_box(734,56,10,14)
    flange=b.Pos(0,-140.5,zhead+23)*b.Box(688,10,10)
    gasket=b.Pos(0,-134.25,zhead+23)*b.Box(688,2.5,8)
    paths=[]
    for x in ports:
        hx=x-25
        flange+=b.Pos(hx,-140.5,zhead)*b.Rot(90,0,0)*b.Cylinder(25,10)
        gasket+=b.Pos(hx,-134.25,zhead)*b.Rot(90,0,0)*b.Cylinder(23,2.5)
        path=b.Bezier((hx,-140.5,zhead),(hx,-183,zhead),(x,-228,315),(x,-228,zbase-5))
        paths.append(path)
        lower+=b.sweep(b.Plane(origin=path@0,z_dir=path%0)*b.Circle(21),path=path)
    lower+=flange
    # Seven threaded bosses connect each runner station at the upper flange.
    for x in mains:lower+=b.Pos(x,-228,344)*b.Cylinder(10,32)
    for x,path in zip(ports,paths):
        # Extend the bore through both flanges as a single tangent wire. Ending a
        # separate drill inside the bend creates tiny coincident sliver faces.
        bore=b.Wire([b.Line((x-25,-125,zhead),path@0),path,b.Line(path@1,(x,-228,zbase+8))])
        lower-=b.sweep(b.Plane(origin=bore@0,z_dir=bore%0)*b.Circle(15),path=bore)
        gasket-=b.Pos(x-25,-134.25,zhead)*b.Rot(90,0,0)*b.Cylinder(15,6)
    for x in mains:lower-=b.Pos(x,-228,348)*b.Cylinder(4.2,45)
    # Six provisional injector sockets opening into the lower runners.
    for x in ports:
        lower+=b.Pos(x-25,-163,300)*b.Cylinder(10,28)
        lower-=b.Pos(x-25,-163,298)*b.Cylinder(7.6,40)
    # Shared rail support stations. Boss contours/heights are provisional;
    # separate bolts follow the factory three-fastener architecture.
    for x in MOUNT_X:
        lower+=b.Pos(x,-157.5,300.5)*b.Box(14,42,10)
        lower+=b.Pos(x,-178,331.5)*b.Cylinder(8,65)
        lower-=b.Pos(x,-178,352)*b.Cylinder(3.2,26)
    define('efi-lower-intake',lower,'Lower EFI intake manifold','Connects the six upper runners to the cylinder-head intake ports. The truck parts catalog lists E7TZ9424D. Internal passages are open in this study, but production port and injector-socket dimensions remain unverified.','induction','#a2a8aa',SOURCES,GAPS)
    add('efi-lower-intake','efi-lower-intake','intake-castings',explode=(0,-150,60))
    define('efi-head-intake-gasket',gasket,'Intake-to-head gasket','Seals the six lower-manifold intake interfaces at the cylinder head. This provisional connected-pad layout omits the exact bolt pattern and production gasket contour.','induction','#a7926b',SOURCES+['fsm-4069bc7976d8'],GAPS)
    add('efi-head-intake-gasket','efi-head-intake-gasket','intake-castings',explode=(0,-70,0))
    joint=b.Pos(0,-228,360.75)*rounded_box(734,56,1.5,14)
    for x in ports:joint-=b.Pos(x,-228,360.75)*b.Cylinder(16.5,5)
    for x in mains:joint-=b.Pos(x,-228,360.75)*b.Cylinder(4.4,5)
    define('efi-upper-intake-gasket',joint,'Upper-to-lower intake gasket','Seals the joint between the two intake castings. A leak at this joint can admit unmetered air. The gasket remains a dimensional study, not a traced production outline.','induction','#b6996a',SOURCES,GAPS)
    add('efi-upper-intake-gasket','efi-upper-intake-gasket','intake-castings',explode=(0,-150,150))
    # Hollow plenum, six curved runners and common lower flange form one casting.
    upper=b.Pos(0,25,490)*rounded_box(734,145,90,25)
    upper+=b.Pos(0,-228,366.5)*rounded_box(734,56,10,14)
    paths=[]
    for x in ports:
        path=b.Bezier((x,-228,366.5),(x,-228,490),(x,-145,490),(x,-20,490))
        paths.append(path)
        upper+=b.sweep(b.Plane(origin=path@0,z_dir=path%0)*b.Circle(22),path=path)
    upper-=b.Pos(0,25,490)*rounded_box(726,137,82,21)
    for x,path in zip(ports,paths):
        bore=b.Wire([b.Line((x,-228,354),path@0),path])
        upper-=b.sweep(b.Plane(origin=bore@0,z_dir=bore%0)*b.Circle(16.5),path=bore)
    for x in mains:upper-=b.Pos(x,-228,366.5)*b.Cylinder(4.4,16)
    # Provisional mounting pad and four stud bores for the separate throttle body.
    upper+=b.Pos(367,25,490)*b.Box(8,124,68)
    for y in [-24,74]:
        for z in [464,516]:upper-=b.Pos(362,y,z)*cx(4.2,22)
    # Twin air openings extend through the mounting pad.
    for y in [-2,52]:upper-=b.Pos(367,y,490)*cx(20,22)
    from egr import intake_interface
    upper=intake_interface(upper)
    from regulator_vacuum import intake_interface as vacuum_interface
    upper=vacuum_interface(upper)
    define('efi-upper-intake',upper,'Upper EFI intake manifold','A common plenum distributes air into six curved runners feeding the lower manifold. The catalog lists E7TZ9424A. This is one casting, not six removable runner tubes. The throttle-body interface is open; a separate throttle mechanism mounts at this interface.','induction','#a7afb3',SOURCES,GAPS)
    add('efi-upper-intake','efi-upper-intake','intake-castings',explode=(0,-150,310))
    stud=b.Pos(0,0,-19)*b.Cylinder(3.97,64)+b.extrude(b.RegularPolygon(6.5,6),amount=5)
    define('efi-upper-stud',stud,'Upper intake retaining stud','One of seven fasteners retaining the upper manifold. Quantity is confirmed by the truck removal procedure; smooth-shank geometry, shoulder and installed length are provisional.','induction','#697a85',SOURCES,GAPS)
    for i,x in enumerate(mains,1):add(f'efi-upper-stud-{i}','efi-upper-stud','intake-studs',(x,-228,371.5),(0,-150,420),name=f'Upper manifold retaining stud {i}')
