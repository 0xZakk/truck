"""Illustrative accelerator cable engine end; no Ford fitting/spring dimensions.

Parent-local CAD frame matches existing throttle assembly before ancestor shift.
The fixed-end spherical seat is an explicit educational construction, not an
observed production detail. C6 and unverified cruise hardware are excluded.
"""
import math
import numpy as np
import build123d as b
PIVOT=np.array([465.3,112.,467.]);EXIT=np.array([470.,112.,467.])
PARAMS=dict(ball_radius=3.,socket_inner_radius=3.04,socket_outer_radius=4.2,socket_mouth_y=-1.4,wire_radius=.25,coil_radius_neutral=3.75,coil_turns=24,core_radius=.4)
def cx(r,h):return b.Rot(0,90,0)*b.Cylinder(r,h)
def unit(v):return v/np.linalg.norm(v)
def state(angle):
 t=math.radians(angle);ball=np.array([394+24*math.sin(t),95.,490+24*math.cos(t)]);u=unit(PIVOT-ball)
 yy=unit(np.array([0.,1.,0.])-u*u[1]);zz=np.cross(u,yy)
 frame=b.Plane(origin=tuple(ball),x_dir=tuple(u),z_dir=tuple(zz))
 fixed=b.Plane(origin=tuple(PIVOT),x_dir=tuple(u),z_dir=tuple(zz))
 length=float(np.linalg.norm(PIVOT-ball))-39.4
 return ball,u,frame,fixed,length

def bracket_proposal(existing):
 # Coordinated inferred correction: mounting/shaft-spring/shield datums stay;
 # only the distal cable flange moves+5X and the cable window grows.
 q=existing.cut(b.Pos(464,115,478)*b.Box(2.02,20,44.02))
 q+=b.Pos(467.5,104,478)*b.Box(5.,2.,44.)
 q+=b.Pos(469,114,478)*b.Box(2.,20.,44.)
 q=q.cut(b.Pos(470,112,467)*cx(5.5,4),b.Pos(470,110,488)*b.Box(4,11,12))
 def cy(r,h):return b.Rot(90,0,0)*b.Cylinder(r,h)
 for x,z,r in [(422,499,10.5),(431,484,16),(449,484,16),(460,468,7)]:q=q.cut(b.Pos(x,104,z)*cy(r,4))
 return q.clean()

def stationary():
 # Replacement-comparison topology: rear flange plus slotted snap fingers.
 # Actual tab profile, polymer and insertion flexure remain unverified.
 retainer=b.Pos(468.5,112,467)*cx(5.3,4.)
 retainer+=b.Pos(470.3,112,467)*cx(7.,.6)
 retainer+=b.Pos(467,112,467)*b.Rot(0,90,0)*b.Cone(4.8,6.,2.)
 retainer=retainer.cut(b.Pos(465.75,112,467)*cx(4.1,7.5))
 for y,z,dy,dz in [(112,467,.6,20),(112,467,20,.6)]:retainer=retainer.cut(b.Pos(467.5,y,z)*b.Box(3.4,dy,dz))
 retainer+=b.Pos(467.65,112,467)*cx(1.1,4.7)
 retainer+=b.Pos(*PIVOT)*b.Sphere(2.5)
 retainer=retainer.cut(b.Pos(475,112,467)*cx(.9,26),b.Pos(*PIVOT)*b.Sphere(2.))
 retainer=retainer.cut(b.Pos(PIVOT[0]-3.4,112,467)*b.Box(5.2,8,8))
 # Captive sheath bead in a matching receiver provides retention rather
 # than an unsupported bonded end face; construction remains inferred.
 retainer=retainer.cut(b.Pos(472,112,467)*cx(1.25,4.2),b.Pos(470.15,112,467)*cx(1.6,.3))
 sheath=b.Pos(478.95,112,467)*cx(1.25,18.1)+b.Pos(470.15,112,467)*cx(1.6,.3)
 sheath=sheath.cut(b.Pos(479,112,467)*cx(.9,19.))
 return {'throttle-cable-snap-retainer-illustrative':retainer.clean(),'throttle-cable-sheath-stub-illustrative':sheath.clean()}

def moving(angle,include_spring=True):
 p=PARAMS;ball,u,frame,fixed,L=state(angle)
 socket=b.Sphere(p['socket_outer_radius'])-b.Sphere(p['socket_inner_radius'])
 socket=socket.cut(b.Pos(0,-6.4,0)*b.Box(12,10,12))
 socket+=b.Pos(19.75,0,0)*cx(3.4,32.5)
 socket+=b.Pos(42,0,0)*cx(2.6,12.)
 socket+=b.Pos(35.7,0,0)*cx(4.5,.6)
 socket=socket.cut(b.Pos(9,0,0)*cx(p['core_radius'],8.),b.Pos(5,0,0)*cx(.7,1.2),b.Pos(30,0,0)*cx(1.3,36.))
 # Spherical swivel seat captures the fixed hollow pivot. Its rear mouth
 # clears the fixed neck as cable direction changes; flexure not simulated.
 cup=b.Sphere(3.4)-b.Sphere(2.54)
 cup=cup.cut(b.Pos(5.8,0,0)*b.Box(10,12,12))
 cup+=b.Pos(-3.1,0,0)*cx(4.5,.6)
 cup=cup.cut(b.Pos(-2,0,0)*cx(.8,6.),b.Pos(-4,0,0)*cx(1.2,1.6),b.Pos(-3,0,0)*cx(1.5,.4))
 guide=b.Pos(-17.3,0,0)*cx(1.2,28.2)+b.Pos(-3,0,0)*cx(1.5,.4)
 guide=guide.cut(b.Pos(-17,0,0)*cx(.6,30.))
 start=ball+5*u;transition=PIVOT-1.2*u;end=PIVOT+np.array([2.,0,0])
 # This short flexible core bend joins the changing free span tangent to
 # the fixed ferrule/sheath axis; no diagonal rigid wire through the wall.
 bend=b.Edge.make_bezier(tuple(transition),tuple(transition+.9*u),tuple(end-np.array([1.,0,0])),tuple(end))
 path=b.Wire([b.Edge.make_line(tuple(start),tuple(transition)),bend,b.Edge.make_line(tuple(end),(487.8,112,467))])
 core=b.sweep(b.Plane(origin=tuple(start),z_dir=tuple(u))*b.Circle(p['core_radius']),path=path,is_frenet=True)
 core=(core+frame*(b.Pos(5,0,0)*cx(.7,1.2))).clean()
 result={'throttle-cable-socket-illustrative':frame*socket.clean(),'throttle-cable-swivel-seat-illustrative':fixed*cup.clean(),'throttle-cable-core-illustrative':core,'throttle-cable-fixed-guide-illustrative':fixed*guide}
 if include_spring:
  L0=state(0)[4];N=p['coil_turns'];r=math.sqrt((2*math.pi*N*p['coil_radius_neutral'])**2+L0**2-L**2)/(2*math.pi*N)
  helix=b.Helix(L/N,L,r)
  coil=b.sweep(b.Plane(origin=helix.position_at(0),z_dir=helix.tangent_at(0))*b.Circle(p['wire_radius']),path=helix,is_frenet=True)
  # Ground-end planes bear on the two explicit seats. This clips only the
  # swept end profile; the continuous centerline retains its analytic length.
  coil=coil.intersect(b.Pos(0,0,L/2)*b.Box(20,20,L))
  springframe=b.Plane(origin=tuple(ball+36*u),z_dir=tuple(u))
  result['throttle-cable-compression-spring-illustrative']=springframe*coil
 return result,dict(angle_deg=angle,span_mm=float(np.linalg.norm(PIVOT-ball)),spring_axial_length_mm=L,spring_radius_mm=r if include_spring else None,spring_centerline_length_mm=math.sqrt((2*math.pi*N*r)**2+L**2) if include_spring else None,spring_cad_centerline_length_mm=helix.length if include_spring else None,core_centerline_length_mm=path.length,ball_center=ball.tolist(),fixed_pivot=PIVOT.tolist())
