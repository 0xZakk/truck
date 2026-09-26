"""Unvented IAC teaching study; installed valve variant and dimensions unverified."""
import build123d as b
SOURCES=['system-1cf529afa81d','truck-throttle-operation']
GAPS=['The factory chapter illustrates both unvented and vent/filter IAC valves. This study uses the unvented architecture; the installed truck variant is not established.', 'All dimensions, bypass routing, mounting pattern, valve travel and spring/magnetic details are provisional. The model does not simulate idle speed, duty cycle, vacuum or flow.']
def build(api):
    define,add,group,cx=api
    group('idle-air','Idle-air bypass valve','throttle-assembly',position=(397,25,540))
    def part(id,s,name,fn,pos=(0,0,0),explode=(0,0,0),color='#95a3a9'):
        define(id,s,name,fn,'induction',color,SOURCES,GAPS);add(id,id,'idle-air',pos,explode)
    body=b.Box(48,30,26)
    for x in [-13,13]:body-=b.Pos(x,0,0)*cx(8.5,22)
    body-=cx(5.1,6)
    for x in [-12,12]:body-=b.Pos(x,0,-8)*b.Cylinder(5,20)
    part('iac-valve-body',body,'IAC valve body','Connects upstream and downstream bypass passages through a pintle-controlled opening. The divider and routing illustrate the factory diagram.',explode=(0,0,60))
    gasket=b.Pos(0,0,-13.5)*b.Box(48,30,1)
    for x in [-12,12]:gasket-=b.Pos(x,0,-13.5)*b.Cylinder(5,3)
    part('iac-gasket',gasket,'IAC mounting gasket','Separates and seals the two bypass openings at the throttle housing.',explode=(0,0,-35),color='#b8a17b')
    part('iac-end-plug',cx(8.4,1),'IAC chamber end closure','Closes the outer valve chamber. Production retention details remain unresolved.',(-23.5,0,0),(-45,0,0))
    can=b.Pos(46,0,0)*(cx(12,44)-cx(10,46))
    part('iac-solenoid-can',can,'IAC solenoid casing','Encloses the coil and provides the magnetic return structure.',explode=(70,0,0))
    coil=b.Pos(46,0,0)*(cx(9.8,39)-cx(4,41))
    part('iac-coil',coil,'IAC solenoid coil','The controller varies solenoid duty cycle to regulate bypass air. Shown as a winding envelope.',explode=(45,0,30),color='#b47647')
    armature=b.Pos(46,0,0)*(cx(3.8,20)-cx(1.6,22))
    part('iac-armature',armature,'IAC armature','Receives magnetic force and transfers movement to the valve stem.',explode=(85,0,0))
    pintle=b.Pos(25.25,0,0)*cx(1.5,56.5)+b.Pos(-3.5,0,0)*cx(7.5,1)
    part('iac-pintle',pintle,'IAC stem and reverse-seated pintle','Meters the bypass opening. This separate moving element is shown near its seat; calibrated travel and restoring mechanism remain unresolved.',explode=(-65,0,0))
    cap=b.Pos(69,0,0)*(cx(12,2)-cx(2,4))+b.Pos(75,0,0)*b.Box(10,14,12)
    cap-=b.Pos(78,0,0)*b.Box(8,10,8)
    part('iac-connector-cap',cap,'IAC electrical connector cap','Insulates the solenoid connection. Terminal geometry and electrical harness are still missing.',explode=(110,0,0),color='#404d46')
