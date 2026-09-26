"""Fuel-rail diagnostic valve; generic core construction, provisional dimensions."""
import math
import build123d as b
POSITION=(100,-163,378)

def build(api):
    define,add,group,spring=api
    src=['fsm-4840fb38c793','schrader-core-construction']
    gaps=['Ford establishes a fuel-rail Schrader fitting. Exact installed fitting/core identity, dimensions, thread forms and location are unverified.', 'Internal construction is a generic spring-actuated valve study, not a production Ford section. No pressure rating, leakage, material compatibility or spring calibration is established.']
    group('fuel-test-valve','Fuel pressure test valve','fuel-rail-assembly',position=POSITION)
    def cz(r,a,z):return b.Pos(0,0,(a+z)/2)*b.Cylinder(r,z-a)
    def ring(ro,ri,a,z):return cz(ro,a,z)-cz(ri,a-1,z+1)
    body=cz(4.5,0,14)+b.Pos(0,0,2)*b.extrude(b.RegularPolygon(10/math.sqrt(3),6),amount=4)
    body-=cz(3,-1,15)
    core=ring(2.8,2.5,0,12)+ring(2.5,.8,0,1)+ring(2.5,1.3,4.5,5.5)
    # Separate static sleeve seals the cartridge to the diagnostic fitting.
    core-=ring(2.9,2.6,9,10)
    sleeve=ring(3,2.61,9,10)
    stem=cz(.6,3,15)+cz(2,3,4)
    seal=ring(2,.65,4,4.5)
    coil=b.Pos(0,0,1.2)*spring(1.6,.18,1.62,4)
    cap=ring(6,4.7,10,18)+cz(6,18,20)
    capseal=ring(4.7,3,14,15)
    # Cap seals on the body top through its annular insert; the interior height
    # illustrates removal clearance, not an OEM cap/thread specification.
    rows=[('body',body,'Pressure-test fitting body','Connects the diagnostic valve to the rail fuel passage. Thread geometry and installed station remain provisional.','#a59871',(25,0,0)),
          ('core',core,'Pressure-test valve core housing','Removable cartridge supports the seat and actuating pin. Windows and threads remain simplified.','#bdac7b',(-25,0,0)),
          ('static-seal',sleeve,'Valve-core static seal','Separates the cartridge from its mating cavity to limit leakage around the core. Material and profile require installed-part verification.','#c8c5aa',(0,20,8)),
          ('pin',stem,'Valve-core actuating pin and poppet','Depressing the pin moves its sealing face away from the seat to provide diagnostic access. Travel is not simulated.','#b5bfc1',(0,0,-25)),
          ('seat-seal',seal,'Valve-core seating washer','Soft seat closes the passage around the actuating pin. Compression is not modeled.','#404947',(15,0,-15)),
          ('spring',coil,'Valve-core return spring','Biases the poppet toward its closed seat. Spring rate and force are unverified.','#9ca6a9',(-15,0,-20)),
          ('cap',cap,'Fuel pressure test-port cap','Protects the fitting and supplies a secondary sealing boundary. Shape and threads remain provisional.','#394649',(0,0,30)),
          ('cap-seal',capseal,'Pressure test-port cap seal','Illustrative annular cap insert at the fitting lip; installed cap construction remains unverified.','#424b45',(0,15,22))]
    for key,shape,name,fn,color,ex in rows:
        id='fuel-test-'+key
        define(id,shape,name,fn,'induction',color,src,gaps)
        add(id,id,'fuel-test-valve',explode=ex)
