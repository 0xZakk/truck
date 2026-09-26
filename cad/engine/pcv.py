"""PCV valve study: factory mechanism and manufacturer replacement exterior."""
import build123d as b
POSITION=(-240,-12,416)
SOURCES=['truck-pcv-valve-operation','truck-pcv-service','truck-pcv-parts','standard-v219-pcv']
GAPS=['The factory diagram is a typical mechanism, and the exterior follows a Standard V219 replacement photograph. Installed identity, external dimensions and internal calibration remain unverified.', 'All model dimensions and clocking are provisional. The catalog inlet-diameter field is not assigned to a geometric feature without a dimensioned drawing. Hose routing, unused-outlet closure and valve-cover baffle remain unresolved. No airflow, spring-rate or backfire simulation is claimed.']

def build(api):
    define,add,group,spring=api
    group('crankcase-ventilation','Crankcase ventilation')
    group('pcv-valve-assembly','PCV valve & grommet','crankcase-ventilation',position=POSITION)
    def cz(r,a,z):return b.Pos(0,0,(a+z)/2)*b.Cylinder(r,z-a)
    def ring(ro,ri,a,z):return cz(ro,a,z)-cz(ri,a-1,z+1)
    def cy(r,a,y,z):return b.Pos(0,(a+y)/2,z)*b.Rot(90,0,0)*b.Cylinder(r,y-a)
    body=cz(10,-25,0)+cz(12,-2,0)
    body-=cz(8.5,-24,-2)
    body-=cz(4,-26,-23)
    body-=cz(4.8,-3,1)
    head=cz(6,0,28)
    for z,r in [(12,5.5),(24,3.8)]:
        head+=cy(r,-19,0,z)
        for y in [-17,-13]:head+=cy(r+.5,y-1,y,z)
    head-=cz(4.8,-1,26)
    for z,r in [(12,3),(24,2.5)]:head-=cy(r,-20,2,z)
    plunger=cz(4,-22,-20)+cz(2.5,-20,-10)+b.Pos(0,0,-5.5)*b.Cone(2.5,1.5,9)
    washer=ring(8.4,2.8,-3,-2)
    coil=b.Pos(0,0,-19.5)*spring(5.5,.4,16,8)
    grommet=ring(17,10.05,-8,-6)+ring(14.1,10.05,-6,-3)+ring(17,10.05,-3,-2)
    rows=[('body',body,'PCV metal valve body','Houses the metering mechanism and inserts into the cover grommet. The external shoulder follows the replacement photo; rolled seams and production dimensions are unresolved.','#a2afb5',(25,0,-30)),('outlet-head',head,'PCV angled outlet head','Connects the valve passage to two perpendicular hose outlets, following the V219 replacement exterior. Which outlet is used or closed on this truck remains unverified.','#303d3c',(0,-20,35)),('plunger',plunger,'PCV metering plunger','Moves under the balance of pressure and spring force to change the flow opening. The factory describes metering and preventing backfire propagation; this pose has no calibrated flow or motion.','#b6bec1',(25,0,15)),('orifice-washer',washer,'PCV orifice washer','Provides the metering opening around the tapered plunger. Factory cutaway establishes this separate element; its bore and profile are provisional.','#899aa2',(-20,0,25)),('spring',coil,'PCV metering spring','Loads the plunger against pressure forces. Wire diameter, coil count, spring rate and preload are illustrative.','#a1b0b5',(-25,0,-10)),('grommet',grommet,'PCV mounting grommet','Locates and seals the valve at the cover opening. Ford calls for inspecting this separate grommet for deterioration. The lips fit the provisional cover opening without modeled rubber compression.','#3e4742',(0,25,-20))]
    for key,shape,name,fn,color,ex in rows:
        ident='pcv-'+key
        define(ident,shape,name,fn,'crankcase-ventilation',color,SOURCES,GAPS)
        add(ident,ident,'pcv-valve-assembly',explode=ex)
