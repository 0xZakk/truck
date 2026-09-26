"""Ford service-diagram injector decomposition and provisional rail arrangement."""
import math
import build123d as b
from fuel_mounts import MOUNT_X
from fuel_couplings import build as build_couplings
from fuel_test_valve import build as build_test_valve, POSITION as TEST_POSITION
SOURCES=['system-bd3903b7892e','system-57b3dbc66361','system-750bd1047639','system-73d3dd2d32e7','system-12bc4a9dabbf']
GAPS=['Architecture and component identities follow factory service illustrations. All modeled envelopes, internal profiles, fits, rail bends and installed positions are provisional, not measured production dimensions.', 'Coils and filters are simplified material envelopes; winding count, mesh, calibrated orifices, spring rates and injector flow calibration are not established. No fuel-pressure or atomization simulation is claimed.']
def build(api):
    define,add,group,cx,spring,cylinders=api
    group('fuel-system','Fuel rail & injection','induction')
    group('fuel-rail-assembly','Rail & mounting','fuel-system')
    group('fuel-regulator','Fuel pressure regulator','fuel-system',position=(0,-163,385))
    def d(id,s,name,fn,color='#899ba5'):
        define(id,s,name,fn,'induction',color,SOURCES,GAPS)
    def ring(ro,ri,h):return b.Cylinder(ro,h)-b.Cylinder(ri,h+2)
    # One reusable set of internal components, six independently identified injectors.
    shell=b.Pos(0,0,10)*b.Cylinder(6.5,20)+b.Pos(0,0,33)*b.Cylinder(10,26)+b.Pos(0,0,59)*b.Cylinder(6.5,26)
    shell-=b.Pos(0,0,36)*b.Cylinder(3.1,76)
    shell-=b.Pos(0,0,34)*ring(8.9,4.2,20)
    for z in [15,65]:shell-=b.Pos(0,0,z)*b.Torus(6.6,1.0)
    d('injector-metal-body',shell,'Injector metal body','Carries the fuel passage and locates the magnetic and valve components. The stepped envelope and internal cavity are illustrative.')
    polymer=b.Pos(0,0,34)*ring(12.5,10.1,24)+b.Pos(0,-14,39)*b.Box(12,10,12)
    polymer-=b.Pos(0,-17,39)*b.Box(8,8,8)
    polymer-=b.Pos(0,0,34)*b.Cylinder(10.1,26)
    d('injector-connector-shell',polymer,'Injector connector and insulation','Insulates the coil and provides a plug connection to the engine wiring harness. Molded details and terminal retention are provisional.','#424b48')
    d('injector-coil',b.Pos(0,0,34)*ring(8.8,4.3,19.8),'Injector solenoid coil','Current from the engine controller creates a magnetic field that lifts the armature. Shown as a winding envelope, not individual copper turns.','#b97745')
    inlet=b.Pos(0,0,61)*ring(3,2.4,21)+b.Pos(0,0,50.6)*ring(3,1.4,.4)
    d('injector-inlet-filter',inlet,'Injector inlet filter','Screens fuel entering from the rail. The cup illustrates the integral filter; actual mesh and flow resistance are unresolved.','#c6b780')
    d('injector-armature',b.Pos(0,0,26)*b.Cylinder(2.9,7)+b.Pos(0,0,33)*ring(2.4,1.5,7),'Injector armature','Moves inward when the solenoid is energized and transfers motion to the needle. Exact magnetic gaps and travel are unverified.')
    d('injector-needle',b.Pos(0,0,12)*b.Cylinder(.8,21)+b.Pos(0,0,1)*b.Cone(.4,.8,1),'Injector needle','Lifts off its seat to permit injection and closes against the seat under spring force. Pintle contour and metering geometry are illustrative.','#c3c9c9')
    d('injector-return-spring',b.Pos(0,0,37.1)*spring(1.7,.3,11.8,7),'Injector return spring','Returns the armature and needle toward the closed position when coil current stops. Coil count and spring rate are assumptions.')
    d('injector-seat',b.Pos(0,0,1)*ring(3,1,2),'Injector valve seat','Provides the closing surface around the outlet. The simple circular opening is not the calibrated production orifice.','#b5babc')
    cap=b.Pos(0,0,-1.5)*b.Cylinder(7,3)-b.Pos(0,0,-1.5)*b.Cylinder(2,6)
    d('injector-protection-cap',cap,'Injector pintle protection cap','Protects the nozzle end. Its outlet opening is simplified.','#706341')
    d('injector-o-ring',b.Torus(6.6,.9),'Injector O-ring','Seals either the injector-to-rail or injector-to-manifold interface. Modeled without elastomer compression.','#35413e')
    d('injector-terminal',b.Box(1,5,1),'Injector electrical terminal','One of two conductive contacts connecting the solenoid to its harness. Wire bonds and internal routing remain unresolved.','#b9a677')
    component_ids=['metal-body','connector-shell','coil','inlet-filter','armature','needle','return-spring','seat','protection-cap']
    for i,x in enumerate(cylinders,1):
        parent=f'fuel-injector-{i}';group(parent,f'Cylinder {i} fuel injector','fuel-system',position=(x-25,-163,294))
        for j,key in enumerate(component_ids):add(f'injector-{i}-{key}','injector-'+key,parent,explode=((j%3-1)*35,0,j*18),name=f'Cylinder {i} · '+key.replace('-',' '))
        for name,z in [('lower',15),('upper',65)]:add(f'injector-{i}-{name}-seal','injector-o-ring',parent,(0,0,z),(0,-40,z/2),name=f'Cylinder {i} {name} injector O-ring')
        for n,xpin in enumerate([-2,2],1):add(f'injector-{i}-terminal-{n}','injector-terminal',parent,(xpin,-16,39),(0,-50,40),name=f'Cylinder {i} injector terminal {n}')
    # Factory exploded image648486791 specifies three1/4-20x.90in bolts/washer.
    length=.90*25.4;radius=.25*25.4/2;pitch=25.4/20
    bolt=b.Pos(0,0,-length/2)*b.Cylinder(radius,length)
    bolt+=b.extrude(b.RegularPolygon((7/16*25.4)/math.sqrt(3),6),amount=4.3)
    z0=-length-pitch
    path=b.Helix(pitch,length+2*pitch,radius,center=(0,0,z0))
    profile=b.Plane(origin=path@0,x_dir=(1,0,0),z_dir=path%0)*b.Polygon((-.48,0),(.2,-.43),(.2,.43),align=None)
    cutter=b.sweep(profile,path=path,is_frenet=True)
    cutter=cutter.intersect(b.Pos(0,0,-length/2)*b.Cylinder(radius+1,length))
    bolt-=cutter
    define('fuel-rail-mount-bolt',bolt,'Fuel rail retaining bolt · 1/4-20 × .90 inch','One of three rail bolts specified in Ford exploded image648486791. Nominal diameter, pitch and under-head length follow the drawing; head shape, thread tolerances and installed station remain provisional.','induction','#889aa3',['system-12bc4a9dabbf'],GAPS)
    washer=ring(7,3.3,1.5)
    d('fuel-rail-mount-washer',washer,'Fuel rail retaining washer','Separate washer beneath a rail bolt head. Quantity follows the factory assembly drawing; washer dimensions remain provisional.','#9caab1')
    for i,x in enumerate(MOUNT_X,1):
        add(f'fuel-rail-mount-bolt-{i}','fuel-rail-mount-bolt','fuel-rail-assembly',(x,-178,371.5),(0,0,75),name=f'Fuel rail retaining bolt {i}')
        add(f'fuel-rail-mount-washer-{i}','fuel-rail-mount-washer','fuel-rail-assembly',(x,-178,370.75),(0,0,50),name=f'Fuel rail retaining washer {i}')
    # Supply tube and injector cups form one joined service manifold.
    rail=b.Pos(-25,-163,369)*cx(6,690)
    for x in cylinders:rail+=b.Pos(x-25,-163,360)*b.Cylinder(9,20)
    for x in MOUNT_X:rail+=b.Pos(x,-163,367)*b.Box(18,46,6)
    rail-=b.Pos(-25,-163,369)*cx(4.5,692)
    for x in cylinders:rail-=b.Pos(x-25,-163,359)*b.Cylinder(7.6,24)
    for x in MOUNT_X:rail-=b.Pos(x,-178,367)*b.Cylinder(3.4,10)
    # Raised regulator flange connects to the supply channel.
    mount=b.Pos(0,-163,379)*b.Cylinder(20,8)
    mount+=b.Pos(0,-163,374)*b.Cylinder(7,8)
    for a in [0,120,240]:
        x=24*math.cos(math.radians(a));y=-163+24*math.sin(math.radians(a))
        mount+=b.Pos(x,y,379)*b.Cylinder(5,8)
        mount+=b.Pos(x/2,(y-163)/2,379)*b.Box(abs(x)+2,abs(y+163)+2,8)
        mount-=b.Pos(x,y,379)*b.Cylinder(2.2,12)
    mount-=b.Pos(0,-163,375)*b.Cylinder(4.5,24)
    rail+=mount
    # Bore the joined rail as well as the flange; otherwise the return tube
    # intersects the original supply-tube wall underneath the added mount.
    rail-=b.Pos(0,-163,374)*b.Cylinder(4.5,26)
    for a in [0,120,240]:
        rail-=b.Pos(24*math.cos(math.radians(a)),-163+24*math.sin(math.radians(a)),379.95)*b.Cylinder(2.2,12.1)
    # Diagnostic branch is open to the rail, not a detached decorative fitting.
    tx,ty,tz=TEST_POSITION
    rail+=b.Pos(tx,ty,374)*b.Cylinder(5,8)
    rail-=b.Pos(tx,ty,373)*b.Cylinder(3,14)
    d('fuel-supply-rail',rail,'Fuel supply rail','Distributes pressurized fuel to six injector cups. Three mounting stations and the regulator flange follow the factory architecture; all bends and stations remain provisional.')
    add('fuel-supply-rail','fuel-supply-rail','fuel-rail-assembly',explode=(0,-65,160))
    # Joined straight bores and rounded junctions keep the teaching route robust.
    # This route is explicitly provisional, not a traced production tube bend.
    points=[(0,-163,383.5),(0,-163,345),(0,-190,345),(0,-190,370),(-345,-190,370)]
    def return_envelope(radius):
        result=None
        for a,c in zip(points,points[1:]):
            vector=b.Vector(c)-b.Vector(a)
            segment=b.Plane(origin=(b.Vector(a)+b.Vector(c))*.5,z_dir=vector)*b.Cylinder(radius,vector.length)
            result=segment if result is None else result+segment
        for p in points[1:-1]:result+=b.Pos(*p)*b.Sphere(radius)
        return result
    returntube=return_envelope(4)-return_envelope(2.8)
    d('fuel-return-tube',returntube,'Fuel return tube','Returns unused fuel toward the tank. The provisional return passage connects the regulator seat to the line; the tank-side hose routing remains provisional.','#a8afb1')
    add('fuel-return-tube','fuel-return-tube','fuel-rail-assembly',explode=(0,-100,100))
    # Regulator diaphragm study, mounted over the provisional rail flange.
    lower=ring(20,17,4)+b.Pos(0,0,-1)*ring(17,4.6,2)
    for a in [0,120,240]:
        x=24*math.cos(math.radians(a));y=24*math.sin(math.radians(a))
        lower+=b.Pos(x,y,-1)*b.Cylinder(5,2)
        lower+=b.Pos(x/2,y/2,-1)*b.Box(abs(x)+2,abs(y)+2,2)
        lower-=b.Pos(x,y,-1)*b.Cylinder(2.2,5)
    lower-=b.Cylinder(4.6,12)
    d('regulator-lower-housing',lower,'Regulator lower housing','Supports the diaphragm and receives fuel pressure. The return valve and outlet routing remain incomplete.')
    add('regulator-lower-housing','regulator-lower-housing','fuel-regulator',(0,0,1),(0,0,-35))
    upper=b.Pos(0,0,17)*ring(20,17,24)+b.Pos(0,0,30)*ring(20,2.5,2)+b.Pos(0,0,37)*ring(4,2.5,12)
    d('regulator-upper-housing',upper,'Regulator spring housing and vacuum nipple','Connects the spring side of the diaphragm to manifold vacuum. This keeps the relevant pressure difference referenced to the intake.','#9aa8ad')
    add('regulator-upper-housing','regulator-upper-housing','fuel-regulator',explode=(0,0,100))
    d('regulator-diaphragm',b.Pos(0,0,4.5)*b.Cylinder(19.8,.8),'Regulator diaphragm','Separates fuel pressure from the vacuum/spring chamber. Its deflection balances fuel pressure against spring force and manifold pressure.','#42504a')
    add('regulator-diaphragm','regulator-diaphragm','fuel-regulator',explode=(0,0,30))
    d('regulator-spring-seat',b.Pos(0,0,5.6)*b.Cylinder(10,1.2),'Regulator spring seat','Distributes spring force onto the diaphragm. Exact formed contour and valve coupling remain unresolved.')
    add('regulator-spring-seat','regulator-spring-seat','fuel-regulator',explode=(0,0,45))
    d('regulator-spring',b.Pos(0,0,7.2)*spring(8,1,20,7),'Regulator spring','Loads the diaphragm. This geometric spring has no assigned calibrated pressure setting or stiffness.')
    add('regulator-spring','regulator-spring','fuel-regulator',explode=(0,0,65))
    d('regulator-gasket',b.Pos(0,0,-1.5)*ring(19.8,5,1),'Regulator mounting gasket','Seals the regulator mounting flange. Exact production outline and sealing details remain unresolved.','#b8a17c')
    add('regulator-gasket','regulator-gasket','fuel-regulator',explode=(0,0,-50))

    d('regulator-valve-seat',b.Pos(0,0,-1)*ring(4.4,1.8,1),'Regulator return valve seat','Provides the closure at the return outlet. Port diameter and ball contour are provisional.')
    add('regulator-valve-seat','regulator-valve-seat','fuel-regulator',explode=(0,0,-65))
    ball_z=-.5+math.sqrt(2**2-1.8**2)
    valve=b.Pos(0,0,ball_z)*b.Sphere(2)+b.Pos(0,0,3.05)*b.Cylinder(1,2.1)
    d('regulator-valve',valve,'Regulator diaphragm valve','Moves with the diaphragm to open the return path when the pressure balance demands more bypass flow. Shown seated; motion is not simulated.')
    add('regulator-valve','regulator-valve','fuel-regulator',explode=(0,0,20))
    d('regulator-inlet-screen',b.Pos(0,0,1.6)*ring(16,5,.6),'Regulator inlet screen','Screens the regulator inlet region. This annular envelope does not reproduce the screen weave.','#b6a677')
    add('regulator-inlet-screen','regulator-inlet-screen','fuel-regulator',explode=(0,0,-25))
    d('regulator-o-ring',b.Pos(0,0,-7)*b.Torus(4.25,.25),'Regulator O-ring','Seals the regulator tube interface. The uncompressed shape and groove dimensions are provisional.','#38473f')
    add('regulator-o-ring','regulator-o-ring','fuel-regulator',explode=(0,0,-75))
    screw=b.Pos(0,0,-5)*b.Cylinder(2,12)+b.Pos(0,0,2)*b.Cylinder(3,2)
    d('regulator-retaining-screw',screw,'Regulator retaining screw','One of three retaining screws described by the factory removal procedure. Thread, head drive and length remain provisional.')
    for i,a in enumerate([0,120,240],1):add(f'regulator-screw-{i}','regulator-retaining-screw','fuel-regulator',(24*math.cos(math.radians(a)),24*math.sin(math.radians(a)),0),(0,0,90),name=f'Regulator screw {i}')

    build_test_valve((define,add,group,spring))
    build_couplings((define,add,group))
