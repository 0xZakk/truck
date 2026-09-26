"""Remote ignition module and fender heat-sink mounting study.

Factory architecture and fastener counts; provisional dimensions and placement.
"""
import build123d as b

def build(api):
    define,add,group=api
    sources=['system-0538e7de7e9d','system-75dcdb21ac74','system-6d43f4508d79']
    gaps=['Factory illustration establishes a fender-mounted module/heat-sink assembly, two module screws and two assembly screws, not these dimensions.',
          'All mounting coordinates, fin spacing/count, casting profile, screw dimensions and connector outline are provisional. The fender and harness are not yet modeled.',
          'Module is an unresolved electronic package, not a complete internal reconstruction. Installed push-start/CCD identity and pinout remain unverified. Neutral display color does not identify its calibration.']
    group('ignition-module-assembly','Remote ignition module & heat sink','ignition',position=(-220,390,265))
    heat=b.Pos(0,0,0)*b.Box(116,62,5)
    for x in range(-48,49,8):
        for y in [-23,23]:heat+=b.Pos(x,y,14)*b.Box(3,16,23)
    for x in [-64,64]:
        heat+=b.Pos(x,0,0)*b.Box(16,26,5)
        heat-=b.Pos(x,0,0)*b.Cylinder(3.4,9)
    for x in [-44,44]:heat-=b.Pos(x,0,0)*b.Cylinder(2.6,9)
    module=b.Pos(0,0,9)*b.Box(80,27,12)
    for x in [-44,44]:
        module+=b.Pos(x,0,4.2)*b.Box(10,12,2.4)
        module-=b.Pos(x,0,4.2)*b.Cylinder(2.6,6)
    # A shell only; do not invent an unverified pin layout or circuit board.
    connector=b.Pos(49,0,14)*b.Box(17,25,12)-b.Pos(53,0,14)*b.Box(17,20,8)
    module_screw=b.Pos(0,0,1)*b.Cylinder(2.3,9)+b.Pos(0,0,6.5)*b.Cylinder(4,2)
    mounting_screw=b.Pos(0,0,-4)*b.Cylinder(3,13)+b.Pos(0,0,4)*b.Cylinder(5,3)
    rows=[('ignition-heat-sink',heat,'Ignition module heat sink','Conducts heat away from the module to its fins. The module mounts on the fender, separately from the distributor.','#8f9da2',(0,0,-80)),
          ('ignition-module-package',module,'Ignition control module · unresolved package','Switches coil primary current using ignition signals. Internal electronics and the installed dwell-control variant remain unresolved.','#64696a',(0,0,100)),
          ('ignition-module-connector',connector,'Ignition module connector shell','Represents the remote module harness connection. Latch detail, contacts and pin assignments are unfinished.','#485254',(90,0,30))]
    for id,shape,name,fn,color,ex in rows:
        define(id,shape,name,fn,'ignition',color,sources,gaps);add(id,id,'ignition-module-assembly',explode=ex)
    for id,shape,name,fn in [('ignition-module-screw',module_screw,'Module retaining screw','One of two screws retaining the module to the heat sink.'),('ignition-heat-sink-screw',mounting_screw,'Heat-sink assembly retaining screw','One of two screws retaining the assembly to the fender; fender engagement is not modeled.')]:
        define(id,shape,name,fn,'ignition','#81939e',sources,gaps)
    for i,x in enumerate([-44,44],1):add('ignition-module-screw-'+str(i),'ignition-module-screw','ignition-module-assembly',pos=(x,0,0),explode=(0,0,160))
    for i,x in enumerate([-64,64],1):add('ignition-heat-sink-screw-'+str(i),'ignition-heat-sink-screw','ignition-module-assembly',pos=(x,0,0),explode=(0,0,200))
