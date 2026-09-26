"""Closed-bowl distributor teaching assembly from factory exploded architecture.

Unverified dimensions and mounting datum; no claimed production drive-gear mesh.
"""
import math
import build123d as b

def build(api):
    define,add,group=api
    src=['system-4fe310c18acd','system-2ea2c28d7cca','system-0452beae4961','fsm-2f144bda5e08','ford-1996-distributor-drive']
    gaps=['Factory references establish closed-bowl Hall-effect architecture with remote ignition module, not these dimensions or installed casting identity.',
          'All dimensions, shaft station, bushings, cap contacts, vane widths, connector layout and mounting position are provisional. Gear tooth count/profile, pin dimensions and cam/pump engagement remain unverified.',
          'Rotation is clockwise viewed from the cap, following the factory firing-order diagram, at half crank speed. Terminal indexing and absolute timing remain unverified; harness and plug leads remain outstanding.']
    group('ignition','Ignition system')
    group('distributor-assembly','Distributor · closed-bowl study','ignition',position=(200,190,145))
    group('distributor-rotation','Distributor shaft, vane and rotor','distributor-assembly',motion={'type':'distributor'})
    def ring(ro,ri,h):return b.Cylinder(ro,h)-b.Cylinder(ri,h+2)
    body=b.Pos(0,0,23)*ring(43,38,46)+b.Pos(0,0,1)*ring(43,9,2)
    body+=b.Pos(0,0,-29)*ring(13,9,60)
    body+=b.Pos(0,0,-34)*ring(19,13,5)
    body-=b.Pos(0,0,-45)*ring(13.5,11.4,2.4)
    for x in [-46,46]:
        body+=b.Pos(x,0,43)*b.Box(14,12,6)
        body-=b.Pos(x,0,43)*b.Cylinder(2.1,10)
    for a in range(0,360,90):body+=b.Rot(0,0,a)*b.Pos(14,0,-14)*b.Box(4,4,27)
    body-=b.Pos(45,15,30)*b.Box(18,16.2,12.2)
    shaft=b.Pos(0,0,-11.5)*b.Cylinder(5.9,183)+b.Pos(0,0,59.5)*b.Cylinder(12,1)
    # Factory exploded architecture; these dimensions and 16 teeth are a
    # provisional visual reconstruction, NOT a verified conjugate gear pair.
    gear=b.Pos(0,0,-85)*ring(14,6.05,12)+b.Pos(0,0,-70)*ring(9,6.05,18)
    for i in range(16):
        section=b.Polygon((13.5,-1.7),(17,-1.15),(17,1.15),(13.5,1.7),align=None).face()
        tooth=b.Solid.extrude_linear_with_rotation(section,(0,0,0),(0,0,12),24)
        gear+=b.Pos(0,0,-91)*b.Rot(0,0,i*22.5)*tooth
    # Matching transverse bores make the pin a separate retained component.
    bore=b.Solid.make_cylinder(1.55,22,b.Plane(origin=(-11,0,-70),z_dir=(1,0,0)))
    shaft-=bore;gear-=bore
    pin=b.Solid.make_cylinder(1.5,17.8,b.Plane(origin=(-8.9,0,-70),z_dir=(1,0,0)))
    pin-=b.Solid.make_cylinder(.95,18,b.Plane(origin=(-9,0,-70),z_dir=(1,0,0)))
    pin-=b.Pos(0,0,-68.65)*b.Box(19,.4,1)
    washer=b.Pos(0,0,-60.5)*ring(10,6.05,1)
    # Trigger disk and six representative vanes; widths are not a calibration.
    vane=b.Pos(0,0,61)*ring(25,6.05,2)
    for a in range(0,360,60):
        outer=b.CenterArc((0,0),25,a,25)
        inner=b.CenterArc((0,0),23,a+25,-25)
        outline=b.Wire([outer,b.Line(outer@1,inner@0),inner,b.Line(inner@1,outer@0)])
        vane+=b.Pos(0,0,50.1)*b.extrude(b.Face(outline),amount=10)
    for x in [-9,9]:
        vane-=b.Pos(x,0,61)*b.Cylinder(1.6,4)
        shaft-=b.Pos(x,0,59.5)*b.Cylinder(1.6,3)
    rotor=b.Pos(0,0,75)*ring(10,6.05,12)+b.Pos(17,0,81.5)*b.Box(34,10,3)
    rotor-=b.Pos(0,0,81.5)*b.Cylinder(2.1,5)
    contact=b.Pos(16,0,83.75)*b.Box(34,6,1.5)
    cap=b.Pos(0,0,70)*ring(43,39,46)+b.Pos(0,0,94)*b.Cylinder(43,2)
    stations=[(33*math.cos(math.radians(a)),33*math.sin(math.radians(a))) for a in range(0,360,60)]
    for x,y in [(0,0)]+stations:
        cap+=b.Pos(x,y,103)*b.Cylinder(6,18)
        cap-=b.Pos(x,y,100)*b.Cylinder(3.1,30)
    for x in [-46,46]:
        cap+=b.Pos(x,0,50)*b.Box(14,12,6)
        cap-=b.Pos(x,0,50)*b.Cylinder(2.1,10)
    # Hall sensor C-shaped slot straddles the shutter radius without touching it.
    sensor=b.Pos(28,0,54)*b.Box(17,14,12)-b.Pos(24,0,55)*b.Box(7,16,10)
    connector=b.Pos(47,15,30)*b.Box(16,16,12)-b.Pos(51,15,30)*b.Box(12,11,7)
    # Forked hold-down bears on the housing flange. The factory procedure
    # establishes a separate clamp/bolt; this envelope is not dimensioned OEM CAD.
    clamp=b.Pos(0,26,-30)*b.Box(34,38,3)
    clamp-=b.Pos(0,0,-30)*b.Cylinder(14,5)
    clamp-=b.Pos(0,37,-30)*b.Cylinder(4.5,5)
    hold_bolt=b.Pos(0,37,-39.5)*b.Cylinder(4,22)
    hold_bolt+=b.Pos(0,37,-28.5)*b.extrude(b.RegularPolygon(13/math.sqrt(3),6),amount=5)
    pieces=[
      ('distributor-hold-down-clamp',clamp,'Distributor hold-down clamp · provisional','Bears on the housing flange to retain the distributor after timing is set. Shape, thickness and mounting station are provisional; the block attachment is not yet modeled.','#8e9ca4','distributor-assembly',-110),
      ('distributor-hold-down-bolt',hold_bolt,'Distributor hold-down bolt · provisional','Clamps the distributor housing against its engine mounting pad. The factory service procedure specifies 23–34 Nm; modeled diameter, length and head dimensions are unverified and threads remain unfinished.','#82949d','distributor-assembly',-160),
      ('distributor-drive-gear',gear,'Distributor helical drive gear · provisional','Transfers camshaft rotation to the distributor shaft. Sixteen representative helical teeth illustrate the mechanism; count, profile, material and installed mesh remain unverified.','#8b969c','distributor-rotation',-270),
      ('distributor-drive-pin',pin,'Distributor gear retaining spring pin','Passes through matching transverse bores in the gear hub and shaft. Dimensions and spring-pin construction are provisional.','#66777f','distributor-rotation',-310),
      ('distributor-thrust-washer',washer,'Distributor thrust washer','Separate washer shown above the drive gear in the factory exploded diagram. Thickness and running clearance remain provisional.','#b2a275','distributor-rotation',-230),
      ('distributor-housing',body,'Distributor housing','Supports the shaft and trigger inside the closed bowl. The ignition module is remote.','#8c9b9f','distributor-assembly',-100),
      ('distributor-shaft',shaft,'Distributor shaft','Carries the shutter and rotor; the camshaft drives the distributor through gearing.','#a0b0ba','distributor-rotation',-160),
      ('distributor-vane',vane,'Distributor rotary vane','Passes through the Hall sensor gap to generate the position signal. Vane widths and indexing are illustrative.','#82949a','distributor-rotation',110),
      ('distributor-rotor',rotor,'Distributor rotor insulator','Insulates and supports the high-voltage rotor contact.','#a77659','distributor-rotation',180),
      ('distributor-rotor-contact',contact,'Distributor rotor contact','Transfers coil voltage from the center contact toward each cap terminal as the shaft turns.','#c6ad69','distributor-rotation',210),
      ('distributor-cap',cap,'Distributor cap','Insulates the center coil connection and six plug-wire terminals. Terminal locations are not a wiring-order guide.','#815b4c','distributor-assembly',300),
      ('distributor-hall-sensor',sensor,'Distributor Hall sensor · package','Senses the passing vane to provide Profile Ignition Pickup information. Internal electronics remain an envelope.','#3d4447','distributor-assembly',80),
      ('distributor-connector',connector,'Distributor connector shell','Carries the trigger wiring connection; contacts and harness routing remain unfinished.','#40484a','distributor-assembly',50),
      ('distributor-bushing',ring(8.95,6,10),'Distributor shaft bushing','Illustrative bearing surface supports the shaft; material, count and production construction require confirmation.','#b8a570',None,0),
      ('distributor-o-ring',b.Pos(0,0,-45)*b.Torus(12.2,.75),'Distributor housing O-ring','Seals the housing at the engine mounting bore.','#3f4749','distributor-assembly',-230),
      ('distributor-cap-terminal',b.Pos(0,0,99)*b.Cylinder(3,24),'Distributor cap terminal','Conducts high voltage between an internal cap contact and a plug-wire connection.','#c6ac72',None,0),
      ('distributor-center-contact',b.Pos(0,0,85.75)*b.Cylinder(2,2.5),'Distributor center brush · envelope','Connects the central coil feed toward the rotor contact. Spring/contact construction remains unfinished.','#474e51','distributor-assembly',245),
      ('distributor-cap-screw',b.Pos(0,0,45)*b.Cylinder(1.9,16)+b.Pos(0,0,54)*b.Cylinder(2.9,2),'Distributor cap screw','Retains the cap on its mounting ears. Threads and production dimensions remain unmodeled.','#899ca7',None,0),
      ('distributor-vane-screw',b.Pos(0,0,60)*b.Cylinder(1.4,6)+b.Pos(0,0,64)*b.Cylinder(2.4,2),'Distributor vane retaining screw','Retains the trigger disk to the shaft flange; dimensional details are provisional.','#899ca7',None,0)
    ]
    for id,shape,name,fn,color,parent,ex in pieces:
        define(id,shape,name,fn,'ignition',color,src,gaps)
        if parent:add(id,id,parent,explode=(0,0,ex))
    for i,z in enumerate([-52,-5],1):add('distributor-bushing-'+str(i),'distributor-bushing','distributor-assembly',pos=(0,0,z),explode=(0,0,-180-i*30))
    for i,(x,y) in enumerate(stations,1):add('distributor-terminal-'+str(i),'distributor-cap-terminal','distributor-assembly',pos=(x,y,0),explode=(0,0,330),name='Cap peripheral terminal '+str(i)+' · not cylinder assignment')
    add('distributor-coil-terminal','distributor-cap-terminal','distributor-assembly',explode=(0,0,360))
    for i,x in enumerate([-46,46],1):add('distributor-cap-screw-'+str(i),'distributor-cap-screw','distributor-assembly',pos=(x,0,0),explode=(0,0,400))
    for i,x in enumerate([-9,9],1):add('distributor-vane-screw-'+str(i),'distributor-vane-screw','distributor-rotation',pos=(x,0,0),explode=(0,0,140))
