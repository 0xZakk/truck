"""Spin-on filter construction study; comparison envelope, provisional internals."""
import math
import build123d as b
# Factory lubrication diagram puts the filter on the cam/gallery side (+Y).
# The station/angle are still provisional until the block boss is reconstructed.
POSITION=(70,160,65)
ROTATION=(-120,0,0)
SOURCES=['system-8b605c7dd171','fsm-d975f341ee63','fsm-6f023139b5f8','wix-51515-envelope','motorcraft-filter-construction','ford-industrial-csg649']
GAPS=['This is a construction study, not a verified FL-1A or WIX51515 internal replica. The 93mm diameter/132mm overall envelope and72/63/5mm gasket use WIX published metric comparison dimensions; the truck factory specifies FL-1A.', 'Pleat count, wall thicknesses, internal seats, valve parts and spring geometry are illustrative. No oil flow, filtering efficiency, bypass pressure or seal compression is simulated.', 'Filter station and inclination are provisional. The block sealing boss, threaded adapter insert and oil galleries are not yet connected; do not interpret the staged placement as installed fit.']

def build(api):
    define,add,group,spring=api
    group('oil-filter-assembly','Oil filter construction study','lubrication',position=POSITION)
    def cz(r,a,z):return b.Pos(0,0,(a+z)/2)*b.Cylinder(r,z-a)
    def ring(ro,ri,a,z):return cz(ro,a,z)-cz(ri,a-1,z+1)
    case=ring(46.5,45.5,6,130)+cz(46.5,130,132)
    for i in range(24):
        a=i*2*math.pi/24
        case-=b.Pos(50*math.cos(a),50*math.sin(a),118)*b.Cylinder(4,20)
    base=ring(46.5,9.525,3,6)
    base-=ring(36.1,31.4,2,5)
    for i in range(8):
        a=i*math.pi/4;base-=b.Pos(27*math.cos(a),27*math.sin(a),4.5)*b.Cylinder(3,6)
    gasket=ring(36,31.5,0,5)
    flap=ring(30.5,22.3,6,7)
    def polygon(delta):
        return b.Polygon(*[((39 if i%2==0 else 24)+delta)*b.Vector(math.cos(i*math.pi/64),math.sin(i*math.pi/64)) for i in range(128)],align=None)
    media=b.Pos(0,0,20)*b.extrude(polygon(.25)-polygon(-.25),amount=95)
    tube=ring(23,22.2,20,115)
    for z in range(26,111,12):
        for i in range(8):
            a=i*math.pi/4;v=(math.cos(a),math.sin(a),0)
            tube-=b.Plane(origin=(22.6*v[0],22.6*v[1],z),z_dir=v)*b.Cylinder(2,4)
    low=ring(40,22.2,18.5,20);top=cz(40,115,116.5)
    # Separate the dirty bypass pocket from the central clean outlet. Without
    # this standpipe, the side windows would short-circuit the media even with
    # the bypass disc seated. The pocket must also seat against the baseplate.
    valve=ring(22.2,20.8,6,16)+ring(24,10,16,18.5)
    valve+=ring(10,9.525,6,18.5)
    for i in range(8):
        a=i*math.pi/4
        valve-=b.Pos(16*math.cos(a),16*math.sin(a),17)*b.Cylinder(2,5)
    for i in range(4):
        a=i*math.pi/2;v=(math.cos(a),math.sin(a),0)
        valve-=b.Plane(origin=(21.5*v[0],21.5*v[1],11.5),z_dir=v)*b.Cylinder(3,5)
    poppet=ring(20,10.2,18.5,19)
    coil=b.Pos(0,0,19.5)*spring(14,.5,8,4)
    retainer=ring(22.2,10.2,28,29)
    path=b.Bezier((-25,0,117),(0,0,142),(25,0,117))
    tension=b.sweep(b.Plane(origin=path@0,x_dir=(0,1,0),z_dir=path%0)*b.Rectangle(8,1),path=path)
    for x in [-25,25]:tension+=b.Pos(x,0,117)*b.Box(8,8,1)
    rows=[('case',case,'Oil filter steel case','Contains the pressurized filter assembly. Shallow removal flutes are illustrative; the shell uses a WIX comparison envelope.','#d0d6d7'),('baseplate',base,'Oil filter baseplate','Outer inlet holes admit unfiltered oil; the central outlet returns oil toward the engine. The3/4-16 catalog thread is represented by nominal bore only; thread form and adapter are unresolved.','#98a7ad'),('gasket',gasket,'Oil filter mounting gasket','Seals the filter to the engine mounting face. Its uncompressed dimensions follow the WIX metric comparison listing.','#3d4944'),('anti-drainback',flap,'Oil filter anti-drainback valve','Flexible annular flap covers the inlet holes when reverse flow would drain the canister. Shown closed without deformation.','#967052'),('media',media,'Pleated oil filter media','Folded media separates the dirty outer chamber from the clean center. Individual pleats are modeled; pore size, material structure, pleat count and filtration performance are not established.','#c3a25e'),('center-tube',tube,'Oil filter perforated center tube','Supports the media against inward pressure and carries filtered oil toward the central outlet. Hole pattern and corrugation details remain provisional.','#9fadb4'),('lower-endcap',low,'Oil filter inlet-side end cap','Closes the end of the pleated pack while allowing clean oil into the outlet region. Adhesive and production seal details remain unresolved.','#a8b6bd'),('upper-endcap',top,'Oil filter closed-end end cap','Closes the opposite end of the media to prevent oil from bypassing the pleats through that end.','#a8b6bd'),('bypass-housing',valve,'Filter bypass housing and seat','Illustrates a threaded-end bypass path around restricted filter media. Do not confuse this valve with the oil-pump pressure relief or the Ford adapter drainback remedy.','#84959e'),('bypass-poppet',poppet,'Filter bypass valve disc','Lifts from the illustrative seat when pressure difference overcomes its spring. This geometric study has no calibrated opening pressure.','#b8c2c5'),('bypass-spring',coil,'Filter bypass valve spring','Loads the bypass disc. WIX catalog pressure data is not assigned to this uncalibrated spring.','#8c9ea8'),('bypass-retainer',retainer,'Filter bypass spring retainer','Provides a provisional reaction surface for the valve spring. Retention construction needs a part-specific section.','#82949d'),('tension-clip',tension,'Filter element tension clip','Keeps the element stack seated inside the canister. Bow shape and preload are illustrative; a metal tension clip appears in the Motorcraft comparison cutaways.','#91a5b0')]
    for i,(key,shape,name,fn,color) in enumerate(rows):
        ident='oil-filter-'+key
        define(ident,shape,name,fn,'lubrication',color,SOURCES,GAPS)
        add(ident,ident,'oil-filter-assembly',rotation=ROTATION,explode=((i%3-1)*65,i*20,0))
