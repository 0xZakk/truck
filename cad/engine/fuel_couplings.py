"""Factory spring-lock architecture; provisional dimensions and rail stations."""
import math
import build123d as b
SOURCES=['truck-fuel-coupler-operation','truck-fuel-coupler-service']
STATIONS={'supply':(-370,-163,369),'return':(-345,-190,370)}

def build(api):
    define,add,group=api
    gaps=['Factory diagrams establish male/female construction, two seals, cage, garter spring and redundant clip. Every modeled dimension, threadless joint fit and installed station is provisional.', 'Large black supply and small gray return clips follow the service text. Tool sizes and service part numbers are not treated as measured fitting dimensions. Seal compression, clip flexure, hose routing and pressure performance are not simulated.']
    def cyl(r,a,z):return b.Pos(0,0,(a+z)/2)*b.Cylinder(r,z-a)
    def ring(ro,ri,a,z):return cyl(ro,a,z)-cyl(ri,a-1,z+1)
    for line,scale,neck,bore in [('supply',1,6,4.5),('return',.8,5,3.5)]:
        # Return neck becomes radius4 after scaling, matching its existing tube.
        male=ring(neck,bore,0,3)+ring(6,bore,3,28)
        for z in (18,24):male-=b.Pos(0,0,z)*b.Torus(5.65,.75)
        cage=ring(11,6.05,3,4)+ring(11,9.7,4,13.4)+ring(11,8.4,13.4,15)
        female=ring(9,6.3,10,12)+ring(7.5,6.3,12,34)+ring(7.5,bore,34,35)+ring(6.3,bore,35,45)
        seal=b.Torus(5.65,.65)
        # Toroidal helix shows individual coils; the end-joining detail is unresolved.
        pts=[]; turns=48
        for i in range(768):
            t=(2*math.pi-.05)*i/767; radius=9.1+.45*math.cos(turns*t)
            pts.append((radius*math.cos(t),radius*math.sin(t),12.8+.45*math.sin(turns*t)))
        path=b.Spline(*pts)
        spring=b.sweep(b.Plane(origin=path@0,z_dir=path%0)*b.Circle(.13),path=path,is_frenet=True)
        clip=ring(13,7.7,1,2)+ring(13,7.7,16,17)
        clip-=b.Pos(0,10,9)*b.Box(15,20,20)
        for x in (-12.2,12.2):clip+=b.Pos(x,0,9)*b.Box(1.5,3,16)
        tetherpath=b.Spline((12.2,0,2),(19,0,16),(17,0,31),(6.9,0,40))
        tether=b.sweep(b.Plane(origin=tetherpath@0,z_dir=tetherpath%0)*b.Circle(.45),path=tetherpath)
        tether+=b.Pos(0,0,40)*b.Torus(6.9,.5)
        # Recess the illustrative tether attachment into the separate clip.
        clip-=tether
        if line=='return':
            # Provisional clip clocking clears the adjacent intake flange.
            clip=b.Rot(0,0,180)*clip
            tether=b.Rot(0,0,180)*tether
        rows=[('male',male,'Male spring-lock fitting','Carries two sealing grooves. Its cage supports the spring that captures the female flare. The modeled neck joins the rail tube.','#a4afb1'),('cage',cage,'Spring-lock cage','Holds the garter spring around the male fitting. Its retaining lip keeps the spring from expanding far enough to release the flare.','#919da4'),('female',female,'Female spring-lock fitting','Slides over the male spigot and both O-rings. Its flared end passes the retaining spring during assembly. Tank-side hose routing remains missing.','#b4bec0'),('seal',seal,'Fuel-resistant coupling O-ring','One of two fuel-resistant seals inside the female socket. Ford specifies dedicated replacement seals; these dimensions and elastomer composition are unverified.','#69503b'),('spring',spring,'Coupling garter spring','Coiled ring expands over the female flare, then contracts behind it. Coil count, wire diameter and spring force remain illustrative; the small end-joining region is unresolved.','#a9b4b9'),('clip',clip,'Fuel coupling safety clip','Redundant horseshoe retainer sits over the metal coupling. Ford specifies a larger black supply clip and smaller gray return clip. Exact stamped profile remains provisional.','#30383a' if line=='supply' else '#999c9b'),('tether',tether,'Coupling clip tether','Keeps the retaining clip associated with its fuel line. The loop and attachment shapes follow the diagram only schematically.','#565f60')]
        parent='fuel-'+line+'-coupling';group(parent,line.title()+' spring-lock coupling','fuel-rail-assembly',position=STATIONS[line])
        for i,(key,shape,name,fn,color) in enumerate(rows):
            ident=parent+'-'+key
            define(ident,b.scale(shape,by=scale),line.title()+' · '+name,fn,'induction',color,SOURCES,gaps)
            for n,z in ([(1,18),(2,24)] if key=='seal' else [(None,0)]):
                oid=ident+(f'-{n}' if n else '')
                add(oid,ident,parent,(-z*scale,0,0),(-i*14,20 if key=='seal' else 0,i*9),rotation=(0,-90,0),name=line.title()+' · '+name+(f' {n}' if n else ''))
