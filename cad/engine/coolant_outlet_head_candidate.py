"""Local two-passage outlet/head interface; dimensions remain illustrative."""
import build123d as cad
import cooling_connections as cooling

POSITION=(373,0,295)
THERMOSTAT_POSITION=(-.635,0,0)
HEAD_Z=295-255.5
HOLES=[(-27,29),(32,-25)]
SIDE=(-42,0)
ECT_POSITION=(423,-36,315)
SUPPLY_START=(400,-42,295)
SUPPLY_ENDPOINT=cooling.SUPPLY_ENDPOINT
SOURCES=['dorman-902-1002','motorad-244-192','water-pump-mounting-topology']+cooling.SOURCES
GAPS=[
 'Automotive front-face photograph establishes the head-front outlet, two diagonal fasteners and adjacent smaller opening, not calibrated positions or dimensions.',
 'Dorman902-1002 establishes two .313-inch holes, 1.5-inch catalog outside diameter and separate gasket/main/secondary apertures; neck contours and measurement station remain uncertain.',
 'All modeled hole coordinates, gasket contour, neck curvature, bolt engagement and receiver depths are assumptions. Only thermostat flange53.85mmOD/1.27mmthickness are manufacturer dimensions.',
 'The head adapter creates bounded local blind coolant receiver pockets with modeled wall material. It does not reconstruct or validate the complete head water jacket.',
 'The current longblock front plane X373 and outlet center Y0/Z295 are provisional reference datums. Placement corrects the floating joint without optimizing a belt length.',
 'The illustrative thermostat piston front is shortened0.01mm to seat exactly against the existing bridge; this corrects an inherited interference, not a sourced actuator dimension.',
 'The adjacent heater-supply passage remains separate from the thermostat-controlled radiator chamber. Its thread and deeper head-jacket connectivity remain unverified.',
 'The heater-supply/ECT elbow follows the relocated secondary outlet while retaining the existing engine-side vehicle endpoint(488,-57,335). New bend control points, collar, shoulder and sensor station are provisional; the boss is located1mm farther forward than the rejected trial to clear the outlet casting.'
]

def axial(r,length,xyz):
 return cad.Pos(*xyz)*cad.Rot(0,90,0)*cad.Cylinder(r,length)

def flange(thickness,center):
 s=axial(33,thickness,(center,0,0))
 for y,z in HOLES:s+=axial(10,thickness,(center,y,z))
 s+=axial(16,thickness,(center,*SIDE))
 for y,z in HOLES:s-=axial(.313*25.4/2,thickness+2,(center,y,z))
 s-=axial(27.1,thickness+2,(center,0,0))
 s-=axial(11,thickness+2,(center,*SIDE))
 return s

def housing():
 quadrant=cad.Pos(90,0,-13)*cad.Box(70,100,70)
 def elbow(r):
  return ((cad.Pos(55,0,22)*cad.Rot(90,0,0)*cad.Torus(22,r))&quadrant)+axial(r,10,(50,0,0))+cad.Pos(77,0,54)*cad.Cylinder(r,64)
 neck=cad.Pos(.5,0,0)*(elbow(19.05)-elbow(16))
 chamber=axial(32,28.3,(15.35,0,0))-axial(27.1,30,(15.35,0,0))
 taper=cad.Pos(37.5,0,0)*cad.Rot(0,90,0)*(cad.Cone(32,19.05,16)-cad.Cone(27.1,16,16))
 side=axial(16,36,(19.2,*SIDE))-axial(11,38,(19.2,*SIDE))
 side-=axial(27.1,40,(20,0,0))
 chamber-=axial(11,40,(20,*SIDE))
 taper-=axial(11,40,(20,*SIDE))
 shape=flange(6,4.2)+chamber+taper+neck+side
 return shape

def gasket():return flange(1.2,.6)

def bolt():
 return axial(3.5,24.2,(-4.9,0,0))+cad.Pos(7.2,0,0)*cad.Rot(0,90,0)*cad.extrude(cad.RegularPolygon(6,6),amount=6)

def parts():
 return {'coolant-outlet-housing':housing(),'coolant-outlet-gasket':gasket(),'coolant-outlet-bolt':bolt(),
         'thermostat-piston':axial(1.5,23.99,(8.495,0,0)),
         'heater-supply-ect-elbow':supply_elbow()}

def supply_path():
 return cad.Wire([
  cad.Edge.make_line(SUPPLY_START,(445,-42,295)),
  cad.Edge.make_bezier((445,-42,295),(465,-42,295),(488,-57,300),(488,-57,320)),
  cad.Edge.make_line((488,-57,320),SUPPLY_ENDPOINT)
 ])

def supply_sweep(radius):
 return cad.sweep(cad.Plane(origin=SUPPLY_START,z_dir=(1,0,0))*cad.Circle(radius),supply_path())

def supply_elbow():
 s=supply_sweep(8)
 s+=axial(10.8,10.2,(405.1,-42,295))
 s+=axial(13,6,(413.2,-42,295))
 s+=cooling.cylinder(12,20,(ECT_POSITION[0],ECT_POSITION[1],ECT_POSITION[2]-10))
 s+=cooling.cylinder(8.5,2,(488,-57,331))
 s-=supply_sweep(6.5)
 s-=cooling.cylinder(8.6,23,(ECT_POSITION[0],ECT_POSITION[1],ECT_POSITION[2]-10))
 return s

def ect_position(identifier):
 x,y,z=ECT_POSITION
 if identifier.endswith('terminal-1'):x-=1.5
 if identifier.endswith('terminal-2'):x+=1.5
 return (x,y,z)

def flow_probes():
 return {'outlet-secondary-to-supply':axial(.7,20,(400,-42,295)),
         'heater-supply-bore':supply_sweep(.7),
         'ect-wet-tip-clearance':cad.Pos(ECT_POSITION[0],ECT_POSITION[1]-5,ECT_POSITION[2]-18.5)*cad.Sphere(.2)}

def head_interface(head):
 # Adapter uses head-definition coordinates and preserves other recent adapters.
 head+=axial(31,38,(354,0,HEAD_Z))
 head+=axial(14,24,(361,SIDE[0],HEAD_Z))
 for y,z in HOLES:head+=axial(9,24,(361,y,HEAD_Z+z))
 # Receiver behind the thermostat:35mm blind depth,3mm assumed rear floor.
 head-=axial(25.5,35.01,(355.505,0,HEAD_Z))
 # Manufacturer flange sits flush with the head face, with .125mm radial gap.
 head-=axial(27.05,1.28,(372.37,0,HEAD_Z))
 head-=axial(11,22.01,(362.005,SIDE[0],HEAD_Z))
 for y,z in HOLES:head-=axial(3.8,18.01,(364.005,y,HEAD_Z+z))
 return head
