"""Rotary potentiometer teaching construction based on Ford operation description."""
import build123d as b
SOURCES=['system-5691d2ae0a6c','system-f6b16c0f51f5']
GAPS=['Factory text establishes a curved resistor, moving wiper, direct shaft coupling and two mounting screws. Internal packaging, track sweep, dimensions, connector and installed orientation are illustrative.', 'No voltage calibration or electrical fault simulation is inferred from the throttle slider. Production preload and stop angles are unresolved.']
def build(api):
    define,add,group=api
    def cy(r,h):return b.Rot(90,0,0)*b.Cylinder(r,h)
    group('throttle-sensor','Throttle-position sensor','throttle-assembly',position=(394,-44,490))
    group('throttle-sensor-moving','Sensor rotor & wiper','throttle-sensor',motion={'type':'throttle'})
    def d(id,s,name,fn,color='#424d48'):define(id,s,name,fn,'induction',color,SOURCES,GAPS)
    body=cy(18,14)+b.Box(10,14,44)
    for z in [-22,22]:body+=b.Pos(0,0,z)*cy(5,14)
    body-=b.Pos(0,-1,0)*cy(15,12)
    body-=cy(3.2,20)
    for z in [-22,22]:body-=b.Pos(0,0,z)*cy(2.2,20)
    d('tps-housing',body,'TPS housing','Supports the stationary resistance track around the rotating shaft coupling. Molded exterior and connector details remain provisional.')
    add('tps-housing','tps-housing','throttle-sensor',explode=(0,-65,0))
    cap=cy(18,2)+b.Box(10,2,44)
    for z in [-22,22]:cap+=b.Pos(0,0,z)*cy(5,2);cap-=b.Pos(0,0,z)*cy(2.2,5)
    d('tps-cover',cap,'TPS cover','Closes the sensor cavity. Separation here is for teaching; it does not imply the installed sensor is serviceable.')
    add('tps-cover','tps-cover','throttle-sensor',(0,-8,0),(0,-115,0))
    rotor=b.Pos(0,1.5,0)*cy(3,10)+b.Pos(0,-2,0)*cy(8,1)
    d('tps-rotor',rotor,'TPS shaft coupling rotor','Turns with the throttle shaft and carries the moving contact. The teaching model shares the throttle-opening control.','#9b9274')
    add('tps-rotor','tps-rotor','throttle-sensor-moving',explode=(0,-45,0))
    # Three-quarter resistor arc, kept separate from the wiper.
    track=(cy(14,0.6)-cy(11.5,2))-b.Pos(-15,0,-15)*b.Box(30,4,30)
    d('tps-resistance-track',track,'TPS resistance track','A curved resistor forms a voltage divider. The position of the wiper determines the signal sent to the controller.','#6e6053')
    add('tps-resistance-track','tps-resistance-track','throttle-sensor',(0,-4,0),(0,-90,0))
    wiper=b.Pos(9,-2.6,0)*b.Box(10,.2,1)+b.Pos(13,-3.1,0)*b.Box(2,1,1)
    d('tps-wiper',wiper,'TPS moving wiper','A conductive contact travels across the stationary track. Its contact shape is illustrative.','#bba775')
    add('tps-wiper','tps-wiper','throttle-sensor-moving',explode=(0,-70,0))
    screw=b.Pos(0,4,0)*cy(1.8,26)+b.Pos(0,-10.5,0)*cy(3.2,3)
    d('tps-screw',screw,'TPS retaining screw','One of the two factory-described sensor mounting screws. Thread and drive geometry are provisional.','#a3afb2')
    for i,z in enumerate([-22,22],1):add(f'tps-screw-{i}','tps-screw','throttle-sensor',(0,0,z),(0,-140,0),name=f'TPS mounting screw {i}')
