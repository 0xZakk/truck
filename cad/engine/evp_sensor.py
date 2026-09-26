"""EVP sensor teaching section; electrical topology sourced, internals assumed.

Ford EVTM23-4 shows a three-terminal potentiometer at C182. The archive's
external drawing and Standard valve photos establish a removable top sensor.
They do not establish the dimensions or exact internal contact construction.
Coordinates are shared with egr.py, with the sensor nose entering the cap.
"""
import build123d as b
from egr import cyl,ring,SENSOR_HOLES

def body_shape():
    s=cyl(16,23,102.8)+cyl(13.3,8.8,94)
    s+=cyl(23,3,99.8)
    for x,y in SENSOR_HOLES:s+=b.Pos(x,y,99.8)*cyl(5,3)
    s+=b.Pos(23,0,116)*b.Box(30,20,18)
    s-=cyl(3.05,12,93)
    s-=cyl(13.8,22,104)
    s-=b.Pos(27,0,116)*b.Box(24,16,14)
    for x,y in SENSOR_HOLES:s-=b.Pos(x,y,98)*cyl(1.8,7)
    return s

def follower_shape():
    return cyl(2.5,44,62)+cyl(6.5,2.5,106)

def follower_spring():
    path=b.Helix(2.2,11,5)
    return b.Pos(0,0,109)*b.sweep(b.Plane(origin=path@0,z_dir=path%0)*b.Circle(.5),path=path)

def screw_shape():
    return cyl(1.5,8,94.8)+b.Pos(0,0,102.8)*b.extrude(b.RegularPolygon(3,6),amount=2)

def parts():
    p={
      'evp-body':(body_shape(),'EVP sensor housing','Supports the follower, electrical contact study and three-terminal connector. The exact internal molding is not established.'),
      'evp-lid':(cyl(16,1.5,125.8),'EVP sensor lid','Closes the illustrative sensor housing. Whether the production molding uses this separate lid construction is unresolved.'),
      'evp-flange-seal':(ring(17,13.35,.8,99),'EVP flange seal','Illustrates the separate circular seal shown with the replacement valve. Profile and compression are unverified.'),
      'evp-follower':(follower_shape(),'EVP spring-loaded follower','Follows the valve stem to provide a displacement input to the position sensor.'),
      'evp-follower-spring':(follower_spring(),'EVP follower spring','Keeps the illustrative follower in contact with the valve. Rate and installed preload are not established.'),
      'evp-spring-stop':(cyl(7,1,120.5)+cyl(2,4.3,121.5),'EVP spring stop','Illustrative fixed stop above the follower spring; production support construction remains unresolved.'),
      'evp-resistor-carrier':((b.Pos(11.025,0,115)*b.Box(5.55,8,18)) & cyl(13.8,30,100),'EVP resistive-element carrier','Insulating support for the illustrative linear resistance track.'),
      'evp-resistance-track':(b.Pos(8.1,-1.8,115)*b.Box(.3,2.5,18),'EVP resistance track','Represents the potentiometer resistance between reference voltage and signal return. Physical track shape and resistance are unverified.'),
      'evp-collector-track':(b.Pos(8.1,1.8,115)*b.Box(.3,2.5,18),'EVP signal collector','Illustrative sliding-contact collector for the sensor output; the EVTM establishes three-terminal topology, not this contact layout.'),
      'evp-wiper':((b.Pos(6.975,0,107)*b.Box(1.95,6,.3))-follower_shape(),'EVP wiper contact','Bridges the resistance track and output collector in this teaching layout. Displacement changes the sampled potential.'),
    }
    for i,y in enumerate([-5,0,5],1):
        p[f'evp-terminal-{i}']=(b.Pos(28,y,116)*b.Box(18,1,2),f'EVP terminal {i}',
            'One of three electrical connections: reference, signal and return. Physical cavity assignment and internal termination are not yet mapped.')
    for i,(x,y) in enumerate(SENSOR_HOLES,1):
        p[f'evp-screw-{i}']=(b.Pos(x,y,0)*screw_shape(),f'EVP retaining screw {i}',
            'One of three sensor fasteners shown in the replacement kit. Thread, length and torque remain unverified.')
    return p


def build(api):
    define,add,group=api
    from egr import POSITION
    group('egr-position-sensor','EGR valve position sensor','egr')
    sources=['truck-egr-evtm','standard-egv258','system-d015c4a19a04']
    gaps=['Three-wire potentiometer topology follows Ford EVTM23-4. All internal dimensions, contact layout, spring rate and physical part decomposition are illustrative rather than teardown-verified.',
          'The external three-fastener mounting and circular seal follow replacement photographs. Installed sensor identity, cavity assignment, electrical leads, resistance and calibration remain unresolved.']
    for i,(id,(shape,name,function)) in enumerate(parts().items()):
        color='#323f3d' if id in ('evp-body','evp-lid','evp-flange-seal','evp-resistor-carrier') else '#b1a176'
        define(id,shape,name,function,'induction',color,sources,gaps)
        add(id,id,'egr-position-sensor',POSITION,(-100,0,190+i*12))
