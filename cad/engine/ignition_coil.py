"""DG470 exterior study with explicitly illustrative winding-pack decomposition.

Photo-supported topology; dimensions, internal construction and installation unverified.
"""
import build123d as b

def build(api):
    define,add,group=api
    src=['system-f015ea2ab18c','system-f1571449160a','system-4fe310c18acd','ford-dg470']
    gaps=['DG470/F7PZ12029AA matches the archived service part, but the installed coil identity has not been read.',
          'All dimensions, mounting datum, winding order, wire turns, core lamination count and internal connections are unverified. Winding packs are aggregate teaching volumes, not individual wires.',
          'Bracket, fasteners, potting, interference capacitor and installed harness remain unfinished. This is not a service-disassembly sequence.']
    group('ignition-coil-assembly','Ignition coil · DG470 study','ignition',position=(-40,210,235))
    def cx(r,l):
        return b.Solid.make_cylinder(r,l,b.Plane(origin=(-l/2,0,0),z_dir=(1,0,0)))
    def ring(ro,ri,l):return cx(ro,l)-cx(ri,l+2)
    # E and I magnetic paths are separate stack envelopes, not individual sheets.
    core=b.Pos(-38,0,0)*b.Box(8,76,22)
    for y,w in [(-34,8),(0,14),(34,8)]:core+=b.Pos(0,y,0)*b.Box(68,w,22)
    end=b.Pos(38.2,0,0)*b.Box(8,76,22)
    for y in [-33,33]:
        core-=b.Pos(-38,y,0)*b.Cylinder(2.8,26)
        end-=b.Pos(38.2,y,0)*b.Cylinder(2.8,26)
    bobbin=ring(14,13.2,42)
    for x in [-21.5,21.5]:bobbin+=b.Pos(x,0,0)*ring(25.6,13.2,1)
    primary=ring(19,14.2,40)
    separator=ring(20.5,19.3,40.5)
    secondary=ring(25.4,20.7,40)
    case=ring(29,26,52)
    for x in [-26.5,26.5]:case+=b.Pos(x,0,0)*ring(29,13.2,1)
    # The high-voltage tower and two-pin shroud follow the two manufacturer views.
    case+=b.Pos(39,0,22)*cx(8,26)
    case-=b.Pos(42,0,22)*cx(3.6,34)
    shroud=b.Pos(35,0,-27)*b.Box(34,29,15)-b.Pos(41,0,-27)*b.Box(32,24,11)
    case+=shroud
    case-=cx(26,52)
    for y in [-7,7]:case-=b.Pos(23,y,-27)*b.Box(10,4,1.8)
    hv=b.Pos(45,0,22)*cx(3.4,18)+b.Pos(54,0,22)*cx(4.5,3)
    terminal=b.Pos(30,0,-27)*b.Box(20,3,1.2)
    pieces=[
      ('ignition-coil-core-e',core,'Coil E-core · lamination stack','The magnetic core guides flux through the windings. Individual laminations and their joints remain unresolved.','#71848c',(0,-90,0)),
      ('ignition-coil-core-i',end,'Coil core closing stack','Closes the illustrative E-core magnetic path; the air gap and sheet construction are not production dimensions.','#71848c',(100,0,0)),
      ('ignition-coil-bobbin',bobbin,'Coil bobbin · illustrative','Supports and electrically isolates the winding packs from the core.','#c9b988',(-90,0,0)),
      ('ignition-coil-primary',primary,'Coil primary winding pack','Current switched by the ignition module builds magnetic flux. This volume represents a winding pack, not individual turns.','#b37c4d',(0,0,90)),
      ('ignition-coil-insulation',separator,'Coil interwinding insulation · illustrative','Separates the primary and secondary winding packs electrically. Thickness and layering are unverified.','#d0bf90',(0,0,140)),
      ('ignition-coil-secondary',secondary,'Coil secondary winding pack','A changing magnetic field induces the high voltage routed to the distributor. Actual turns and winding order remain unverified.','#bb8e5e',(0,0,190)),
      ('ignition-coil-case',case,'Coil molded insulation and connectors','Insulates the winding assembly and supports the high-voltage tower and primary connector shroud.','#434c4e',(0,0,260)),
      ('ignition-coil-hv-terminal',hv,'Coil high-voltage terminal','Connects the secondary output to the coil-to-distributor lead. Internal joining details are not modeled.','#c2b57e',(160,0,0))]
    for id,shape,name,fn,color,ex in pieces:
        define(id,shape,name,fn,'ignition',color,src,gaps)
        add(id,id,'ignition-coil-assembly',explode=ex)
    define('ignition-coil-primary-terminal',terminal,'Coil primary terminal','Connects a primary-circuit wire. The pair is not labeled as a verified connector pinout.','ignition','#c2b57e',src,gaps)
    for i,y in enumerate([-7,7],1):add('ignition-coil-primary-terminal-'+str(i),'ignition-coil-primary-terminal','ignition-coil-assembly',pos=(0,y,0),explode=(130,0,-60))
