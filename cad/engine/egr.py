"""EGR valve architecture study from the archived Ford sectional illustration.

All dimensions below are provisional. The undimensioned section establishes
relationships, not a scale. Local Z follows the pintle; +X is the intake outlet.
Factory service identity: E9PZ9H473C; Standard confirms EGV258 cross-reference.
"""
import build123d as b

SOURCES=['system-d015c4a19a04','system-6ed79f4b7975','efi-intake-drawing','standard-egv258']
GAPS=['Factory sectional architecture only; every dimension and material thickness is provisional.',
      'Casting profile, calibrated orifice, diaphragm reinforcement, crimp, spring rate, stem seal and production fasteners are not verified.',
      'EVP internals are an illustrative study. Vacuum hose, exhaust tube, exact mounting interface and calibrated motion remain unfinished.']

POSITION=(-412,25,460)  # provisional rear-plenum placement
MOUNT=b.Pos(*POSITION)
SENSOR_HOLES=[(-21,0),(10.5,18.1865),(10.5,-18.1865)]  # assumed bolt circle

def cyl(r,h,z=0):
    return b.Pos(0,0,z)*b.Cylinder(r,h,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))

def ring(ro,ri,h,z=0):
    return cyl(ro,h,z)-cyl(ri,h+2,z-1)

def body_shape():
    # The stepped chamber forms an inlet below the pintle seat, then a side outlet.
    body=cyl(18,43)+cyl(24,4,40)+cyl(12,16,-16)
    body+=b.Pos(21.75,0,29)*b.Rot(0,90,0)*b.Cylinder(13,43.5)
    body+=b.Pos(37.5,0,29)*b.Rot(0,90,0)*b.extrude(b.RectangleRounded(28,62,12),amount=6)
    body-=cyl(9,34,-17)
    body-=cyl(14,22,19)
    body-=cyl(8,4,16)
    body-=cyl(4.05,8,39)
    body-=b.Pos(26,0,29)*b.Rot(0,90,0)*b.Cylinder(9,54)
    for y in [-22,22]:body-=b.Pos(40.5,y,29)*b.Rot(0,90,0)*b.Cylinder(4.2,9)
    return body

def lower_shell_shape():
    # Open chamber under the flexible diaphragm, with a vent to atmosphere.
    shell=cyl(33,15,44)-cyl(31.8,15,45.2)
    shell+=ring(36,31.8,1.2,57.8)
    shell-=cyl(4.05,5,42)
    for angle in range(0,360,45):
        shell-=b.Rot(0,0,angle)*(b.Pos(32,0,51)*b.Rot(0,90,0)*b.Cylinder(2.8,7))
    return shell

def upper_shell_shape():
    # Replacement photos show a cylindrical shell and raised sensor collar.
    shell=(cyl(33,31,60)-cyl(31.8,31,60))
    shell+=ring(33,13.5,1.2,89.8)
    shell+=ring(27,13.5,8,91)
    shell+=ring(36,31.8,1.2,60)
    for x,y in SENSOR_HOLES:shell-=b.Pos(x,y,96)*b.Cylinder(1.7,10)
    shell-=b.Pos(0,31,77)*b.Rot(90,0,0)*b.Cylinder(2.05,12)
    return shell

def diaphragm_shape():
    # Separate reinforced rubber disk; flexible convolution remains unresolved.
    return ring(35.8,3.05,1,59)

def pintle_shape():
    # Flat-contact closed pose. Actual conical seat and calibrated lift unknown.
    return cyl(2.5,43,19)+cyl(10,2,19)

def spring_shape():
    path=b.Helix(5.64,28.2,10)
    return b.Pos(0,0,65)*b.sweep(b.Plane(origin=path@0,z_dir=path%0)*b.Circle(.8),path=path)

def parts():
    """Each entry is one physical-part study, already in assembly coordinates."""
    return {
        'egr-body':(body_shape(),'EGR valve body','Routes exhaust through a pintle-controlled seat to the intake outlet.'),
        'egr-stem-guide':(ring(4,2.55,11,39),'EGR pintle guide','Guides the sliding stem between the hot passage and diaphragm chamber. Seal construction remains unresolved.'),
        'egr-pintle':(pintle_shape(),'EGR pintle and stem','Lifts away from the seat as the vacuum diaphragm moves, admitting exhaust into the intake passage.'),
        'egr-lower-shell':(lower_shell_shape(),'EGR lower diaphragm housing','Supports the diaphragm and provides the atmospheric side of its pressure difference.'),
        'egr-diaphragm':(diaphragm_shape(),'EGR diaphragm','Converts the pressure difference across the flexible membrane into stem motion.'),
        'egr-diaphragm-lower-plate':(ring(9,2.55,1.2,57.8),'EGR lower diaphragm support plate','Supports the diaphragm around its center; the production reinforcement and attachment remain provisional.'),
        'egr-diaphragm-upper-plate':(ring(9,2.55,1.2,60),'EGR upper diaphragm support plate','Transfers load between the diaphragm and pintle attachment.'),
        'egr-stem-retainer':(ring(5,2.55,1.5,61.2),'EGR stem retainer','Illustrates the center attachment; its actual staking or fastening process is not established.'),
        'egr-return-spring':(spring_shape(),'EGR closing spring','Biases the valve closed when the vacuum command is removed. Spring rate and preload are unverified.'),
        'egr-spring-seat':(ring(15,2.55,1.2,63),'EGR closing-spring seat','Illustrative separate seat supporting the spring above the diaphragm center.'),
        'egr-upper-shell':(upper_shell_shape(),'EGR vacuum chamber cover','Encloses the vacuum side of the diaphragm, with passages for the vacuum nipple and EVP follower.'),
        'egr-vacuum-nipple':(b.Pos(0,32,77)*b.Rot(-90,0,0)*ring(2,1.2,12),'EGR vacuum nipple','Connects the chamber to the regulator-controlled vacuum hose. Tube size is assumed.'),
    }

def gasket_shape():
    # One functional outlet; replacement kit's unused second opening is not
    # copied into the manifold without application evidence.
    s=b.Pos(43.5,0,29)*b.Rot(0,90,0)*b.extrude(b.RectangleRounded(28,62,12),amount=1.5)
    for y,r in [(0,9),(-22,4.2),(22,4.2)]:
        s-=b.Pos(44,y,29)*b.Rot(0,90,0)*b.Cylinder(r,5)
    return s

def intake_interface(upper):
    # Coordinates shared with the valve so its passage actually reaches plenum.
    pad=MOUNT*(b.Pos(48,0,29)*b.Box(6,62,28))
    upper+=pad
    for y,r in [(0,9),(-22,4.2),(22,4.2)]:
        upper-=MOUNT*(b.Pos(51,y,29)*b.Rot(0,90,0)*b.Cylinder(r,20))
    return upper

def mounting_bolt():
    # Assumed M8-like envelope. Thread/grade and production engagement unresolved.
    shank=cyl(3.95,20)
    head=b.Pos(0,0,-5)*b.extrude(b.RegularPolygon(7.5,6),amount=5)
    return shank+head

def build(api):
    define,add,group=api
    group('egr','Exhaust gas recirculation','induction')
    group('egr-valve-assembly','EGR valve & vacuum actuator','egr')
    for i,(id,(s,name,function)) in enumerate(parts().items()):
        color='#525452' if id=='egr-body' else '#8f9b91'
        if id=='egr-diaphragm':color='#343b3d'
        define(id,s,name,function,'induction',color,SOURCES,GAPS)
        add(id,id,'egr-valve-assembly',POSITION,(-100,0,i*16))
    define('egr-intake-gasket',gasket_shape(),'EGR intake gasket',
        'Seals the valve outlet to the upper intake. This fit-study contour has one functional passage; the replacement kit photograph includes a two-port gasket whose second opening is not yet reconciled.',
        'induction','#a3947b',SOURCES,GAPS)
    add('egr-intake-gasket','egr-intake-gasket','egr',POSITION,(-50,0,0))
    define('egr-mount-bolt',mounting_bolt(),'EGR mounting bolt','One of two fasteners retaining the valve. Size, thread, washer arrangement and torque remain unverified.',
        'induction','#a5acb0',SOURCES,GAPS)
    for i,y in enumerate([-22,22],1):
        add(f'egr-mount-bolt-{i}','egr-mount-bolt','egr',(POSITION[0]+37.5,POSITION[1]+y,POSITION[2]+29),(-160,0,0),(0,90,0))
