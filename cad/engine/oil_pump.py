"""Source-grounded pump component identities; explicit provisional geometry in mm.

Inspection diagrams establish rotor architecture, not manufacturing profiles.
No pressure/flow simulation or verified production fit is claimed.
"""
import math
import build123d as b

SOURCES=['fsm-6f023139b5f8','fsm-59c6d1fb5ae3','fsm-76412d392bb7','fsm-3ceaca21ab73','ford-industrial-parts']
GAPS=['All housing, rotor, shaft and hardware dimensions and installed transforms are provisional. The manual establishes component identities and inspection procedures, not these CAD dimensions.',
      'Rotor curves are smooth illustrative profiles, not conjugate production gerotors. This assembly does not simulate oil pressure, sealing or pump motion.',
      'Four cover bolts and relief plunger/spring envelope dimensions follow the industrial book listing for the same C5AZ-6600-A service assembly. Truck applicability of internal revisions, ports, mounting geometry and relief-valve retention still needs verification.']

def build(api, include_root=True):
    define,add,group,cx,spring=api
    if include_root:group('lubrication','Lubrication')
    # Reflect the staged assembly about the pan midplane Y=-12: -80 becomes56.
    # Drive alignment is still unresolved; this retains the verified sump clearance.
    group('oil-pump-assembly','Oil pump','lubrication',position=(210,56,-112))
    group('oil-pump-rotors','Rotor set','oil-pump-assembly')
    group('oil-pump-relief','Pressure relief valve','oil-pump-assembly')
    group('oil-pickup-assembly','Pickup & strainer','lubrication',position=(210,56,-112))
    def part(id,shape,name,function,parent='oil-pump-assembly',pos=(0,0,0),explode=(0,0,0),rotation=(0,0,0),color='#91a4aa',sources=SOURCES):
        # Reflect the provisional local assembly with the corrected cam-side layout.
        # This preserves its internal interfaces; installed drive/boss still unverified.
        define(id,shape.mirror(b.Plane.XZ),name,function,'lubrication',color,sources,GAPS)
        add(id,id,parent,(pos[0],-pos[1],pos[2]),(explode[0],-explode[1],explode[2]),(-rotation[0],rotation[1],-rotation[2]))
    ears=[(x,y) for x in [-28,28] for y in [-28,28]]
    def outline(height):
        s=b.Cylinder(34,height)
        for x,y in ears:s+=b.Pos(x,y,0)*b.Cylinder(9,height)
        return s
    housing=outline(32)+b.Pos(-41.5,43,0)*cx(13,163)
    housing+=b.Pos(0,0,-14)*b.extrude(b.RectangleRounded(76,76,10),amount=2,both=True)
    # Open rotor pocket below a top deck, and the independent relief bore.
    housing-=b.Pos(0,0,-5)*b.Cylinder(29.5,30)
    housing-=b.Pos(3.5,0,0)*b.Cylinder(5.1,60)
    housing-=b.Pos(-37.5,43,0)*cx(10.2,157)
    for x,y in ears:housing-=b.Pos(x,y,0)*b.Cylinder(3.2,40)
    housing-=b.Pos(-30,0,5)*cx(6,30)
    part('oil-pump-housing',housing,'Oil pump housing','Locates the rotor set and relief valve. Oil drawn from the pickup is displaced toward the filter. Pocket, inlet and relief bores are visible; the complete internal oil routing remains unresolved.',explode=(0,0,65))
    # Four-lobe inner / five-lobe outer arrangement interpreted from the inspection drawing.
    def lobes(mean,amplitude,n):
        pts=[]
        for i in range(240):
            a=i*2*math.pi/240;r=mean+amplitude*math.cos(n*a)
            pts.append((r*math.cos(a),r*math.sin(a)))
        return b.Polygon(*pts,align=None)
    inner=b.extrude(lobes(17,4,4),amount=12,both=True)-b.Cylinder(4.8,30)
    outer=b.Cylinder(29.3,24)-b.extrude(lobes(26,1.8,5),amount=15,both=True)
    part('oil-pump-inner-rotor',inner,'Inner pump rotor','Receives drive torque and turns inside the outer rotor. Changing chamber volumes draw in and displace oil; the displayed lobe profile is illustrative.','oil-pump-rotors',(3.5,0,-3.85),(0,0,-70),color='#b99b67')
    part('oil-pump-outer-rotor',outer,'Outer pump rotor','The offset outer rotor forms pumping chambers with the inner rotor. Inspect the rotor surfaces and clearances using the applicable manual.','oil-pump-rotors',(0,0,-3.85),(0,0,-120),color='#a8b8bd')
    shaft=b.Cylinder(4.75,42)-b.Pos(0,0,20)*b.extrude(b.RegularPolygon(3,6),amount=9,both=True)
    part('oil-pump-rotor-shaft',shaft,'Pump rotor shaft','Couples the driven inner rotor to the intermediate drive. The hex socket and shaft connection are provisional; the full distributor-to-pump intermediate shaft is still missing.','oil-pump-rotors',(3.5,0,5),(0,0,125))
    cover=b.extrude(b.RectangleRounded(76,76,10),amount=3,both=True)
    for x,y in ears:cover-=b.Pos(x,y,0)*b.Cylinder(3.2,12)
    part('oil-pump-cover',cover,'Oil pump cover','Closes the rotor pocket and provides an end surface. Wear here can increase internal leakage. The manual gives a rotor endplay inspection limit; it is not a housing dimension.',pos=(0,0,-19.1),explode=(0,0,-180))
    bolt=b.Pos(0,0,-12.5)*b.Cylinder(3,25)+b.extrude(b.RegularPolygon(5.2,6),amount=4)
    define('oil-pump-cover-bolt',bolt,'Pump cover bolt','Clamps the cover to the housing. Four bolts follow the comparison parts book for C5AZ-6600-A; thread and installed length in this model remain provisional.','lubrication','#7e8b94',SOURCES,GAPS)
    for i,(x,y) in enumerate(ears,1):add(f'oil-pump-cover-bolt-{i}','oil-pump-cover-bolt','oil-pump-assembly',(x,y,-22.1),(0,0,-215),(180,0,0),name=f'Pump cover bolt {i}')
    part('oil-pump-relief-plunger',cx(9.525,57.15),'Pressure relief plunger','Moves against its spring to open the bypass. Its 3/4-inch diameter and 2-1/4-inch length follow the comparison book for C5AZ-6600-A; truck revision, end details and running fit remain unverified.','oil-pump-relief',(-76.575,43,0),(-140,50,0),color='#b9bec2')
    # Subtract two wire radii so the free envelope, not helix centerline, matches.
    relief_spring=b.Rot(0,90,0)*spring(8.525,1,76.99375-2,12)
    part('oil-pump-relief-spring',relief_spring,'Pressure relief spring','Loads the relief plunger. The 3-1/32-inch length and 3/4-inch outside diameter follow the comparison book; wire size, turns, installed compression, spring rate and opening pressure remain assumptions.','oil-pump-relief',(-46.8,43,0),(65,50,0),color='#b8b3a5')
    part('oil-pump-relief-cap',cx(10.1,5.8),'Relief chamber closure','Retains the relief spring in its bore. Exact production retention and staking details remain unverified.','oil-pump-relief',(35.3,43,0),(165,50,0))
    # A continuous hollow pickup is a layout study, not a traced E3TZ-6622-F tube.
    path=b.Spline((-34,0,5),(-100,8,-6),(-240,15,-14),(-320,15,-70),(-380,15,-133),(-400,15,-133),tangents=[(-1,0,0),(-1,0,0)])
    tube=b.sweep(b.Plane(origin=path@0,z_dir=path%0)*(b.Circle(6)-b.Circle(4.8)),path=path)
    part('oil-pickup-tube',tube,'Oil pickup tube','Carries oil from the sump strainer to the pump inlet. The factory catalog lists E3TZ6622F for the pickup; the bends and tube dimensions here remain a layout study.','oil-pickup-assembly',explode=(0,-100,-60),sources=['fsm-00314a45e241','fsm-6f023139b5f8'])
    cup=b.Cylinder(32,18)-b.Pos(0,0,-3)*b.Cylinder(29,18)
    cup-=b.extrude(b.Plane(origin=(26,0,0),z_dir=path%1)*b.Circle(6.5),amount=15,both=True)
    part('oil-pickup-bell',cup,'Pickup strainer shell','Holds the inlet screen above the sump floor and connects it to the pickup tube. Shell shape and sump clearance need truck-specific measurements.','oil-pickup-assembly',(-426,15,-133),(0,-100,-100),sources=['fsm-00314a45e241','fsm-6f023139b5f8'])
    screen=b.Cylinder(29,1)
    for x in range(-24,25,6):
        for y in range(-24,25,6):
            if x*x+y*y<25**2:screen-=b.Pos(x,y,0)*b.Cylinder(2,3)
    part('oil-pickup-screen',screen,'Pickup inlet screen','Intercepts larger debris before it reaches the pump. This perforated representation explains the screen function; it is not the production mesh weave.','oil-pickup-assembly',(-426,15,-141.5),(0,-100,-150),color='#b5a980',sources=['fsm-00314a45e241','fsm-6f023139b5f8'])
