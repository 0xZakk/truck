"""WR4-1 replacement-envelope study; head placement and detailed internals provisional."""
import math
import build123d as b
from plug_mounts import PLUG_Y, PLUG_LOCAL_Z, PLUG_ANGLE, HEAD_WORLD_Z

def build(api):
    define,add,group,cylinders=api
    src=['ngk-2019-spark-plugs','ngk-plug-construction','ngk-uk-2017-thread-families']
    gaps=['NGK lists WR4-1/4652 for 1993–94 F-150 4.9L. This does not identify the installed plug brand.',
          'Sourced envelope: 18 mm thread diameter, 11.684 mm reach, 20.6375 mm hex and tapered seat; .044 inch application gap. 1.5 mm pitch is inferred from NGK 18 mm families; exact thread tolerances, overall length, projection length and seat angle remain unresolved.',
          'Internal materials/layer dimensions are illustrative and require a WR4-1 section drawing. Head bore angle and station are photo-informed provisional datums shared with the head. Leads and production fit remain unfinished.']
    reach=.460*25.4;hex_af=13/16*25.4;gap=.044*25.4
    def cz(r,z0,z1):return b.Pos(0,0,(z0+z1)/2)*b.Cylinder(r,z1-z0)
    shell=cz(9,-reach,0)+b.Pos(0,0,1)*b.Cone(9,10.4,2)+cz(10.4,2,7)
    shell+=b.Pos(0,0,7)*b.extrude(b.RegularPolygon(hex_af/math.sqrt(3),6),amount=5)
    shell+=cz(8.5,12,14)
    shell-=cz(6.4,-reach-1,15)
    # Family-derived M18 x 1.5 teaching thread; not a production tolerance profile.
    z0=-reach-1.5
    path=b.Helix(1.5,reach+3,9,center=(0,0,z0))
    profile=b.Plane(origin=path@0,x_dir=(1,0,0),z_dir=path%0)*b.Polygon((-.85,0),(.3,-.664),(.3,.664),align=None)
    cutter=b.sweep(profile,path=path,is_frenet=True)
    cutter=cutter.intersect(cz(10,-reach,0))
    shell-=cutter
    ceramic=cz(2.5,-14,-8)+b.Pos(0,0,-4)*b.Cone(2.5,6.2,8)+cz(6.2,0,18)+cz(5.4,18,37)
    for z in [23,26,29,32]:ceramic+=b.Pos(0,0,z)*b.Torus(5.35,.7)
    ceramic-=cz(1.4,-15,38)
    electrode=cz(1.25,-15,-3)-cz(.7,-14,-4)
    core=cz(.65,-14,-4)
    resistor=cz(1.25,-1,7)
    lowerseal=cz(1.25,-3,-1);upperseal=cz(1.25,7,9)
    terminal=cz(1.25,9,37)+cz(3.5,37,39)+cz(3,39,42)+cz(3.5,42,44)
    strap_top=-15-gap;strap_bottom=strap_top-1.4
    ground=b.Pos(8.5,0,(-reach+strap_bottom)/2)*b.Box(2,2.5,-reach-strap_bottom)
    ground+=b.Pos(4.25,0,(strap_top+strap_bottom)/2)*b.Box(8.5,2.5,1.4)
    rows=[('spark-plug-shell',shell,'Spark-plug threaded metal shell','Seats in the head and carries the ground electrode. A helical thread replaces the smooth envelope; pitch is family-derived and production thread tolerances remain unverified.','#99a6ad',(35,0,0)),
          ('spark-plug-insulator',ceramic,'Spark-plug ceramic insulator','Isolates the center conductor from the grounded shell. Nose and corrugation dimensions are provisional.','#e4e1d5',(-35,0,0)),
          ('spark-plug-center-electrode',electrode,'Spark-plug center electrode','The firing end faces the ground strap across the specified application gap. Electrode construction is illustrative.','#b6a780',(0,0,-45)),
          ('spark-plug-copper-core',core,'Spark-plug electrode core · illustrative','Illustrates a separate heat-conducting electrode core; WR4-1 internal dimensions remain unverified.','#bb8055',(0,25,-25)),
          ('spark-plug-resistor',resistor,'Spark-plug suppressor resistor · illustrative','Represents the internal interference-suppression element; resistance and construction are not specified by this model.','#555654',(0,30,0)),
          ('spark-plug-lower-seal',lowerseal,'Spark-plug lower conductive seal · illustrative','Illustrates an internal conducting seal between electrode and resistor.','#a7a096',(0,-25,-15)),
          ('spark-plug-upper-seal',upperseal,'Spark-plug upper conductive seal · illustrative','Illustrates an internal conducting seal between resistor and terminal stem.','#a7a096',(0,-25,15)),
          ('spark-plug-terminal',terminal,'Spark-plug terminal and stem','Receives the plug-wire connection and carries voltage toward the internal resistor.','#a9adb0',(0,0,50)),
          ('spark-plug-ground-electrode',ground,'Spark-plug ground electrode','The ground strap returns spark current through the shell to the cylinder head. Its gap is modeled at .044 inch.','#a0a8ab',(20,0,-45))]
    for id,shape,name,fn,color,ex in rows:define(id,shape,name,fn,'ignition',color,src,gaps)
    group('spark-plugs','Six spark plugs','ignition')
    for i,x in enumerate(cylinders,1):
        parent='spark-plug-'+str(i)
        group(parent,'Cylinder '+str(i)+' · spark plug','spark-plugs',position=(x,PLUG_Y,HEAD_WORLD_Z+PLUG_LOCAL_Z))
        for id,shape,name,fn,color,ex in rows:
            a=math.radians(PLUG_ANGLE)
            rotated_ex=(ex[0],ex[1]*math.cos(a)-ex[2]*math.sin(a),ex[1]*math.sin(a)+ex[2]*math.cos(a))
            add(parent+'-'+id.removeprefix('spark-plug-'),id,parent,rotation=(PLUG_ANGLE,0,0),explode=rotated_ex,name=name+' · cylinder '+str(i))
