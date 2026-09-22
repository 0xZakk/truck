"""Parametric engine reconstruction, mm, X crank axis / Z cylinder axis.

The assembly is deliberately evidence-tagged. Neither fit nor attractive rendering
establishes OEM accuracy. See each definition's outstanding geometry questions.
"""
from pathlib import Path
import json
import math
import hashlib
import build123d as b
import numpy as np
import trimesh
from first_assembly import ROOT, P, cx, annulus, split_ring
from assembly_math import transforms

OUT = ROOT / 'models/engine'
STEP = ROOT / 'cad/engine/generated'
BASE = json.loads((ROOT/'inventory/engine/first-assembly.json').read_text())
INDEX = json.loads((ROOT/'inventory/engine/research-index.json').read_text())
PITCH = 113.792  # provisional 4.480 inch station spacing, not factory-verified
DECK = 254.0  # provisional, not a measured casting dimension
LENGTH = 746.0
R = P['stroke']/2
MAIN_R = sum(P['main_journal_diameter_range'])/4
ROD_R = sum(P['rod_journal_diameter_range'])/4
CYLINDERS = [(2.5-i)*PITCH for i in range(6)]
MAINS = [(3-i)*PITCH for i in range(7)]
PHASES = [0, 240, 120, 120, 240, 0]
defs, occurrences, assemblies, shapes = [], [], [], {}


def ringx(ro, ri, length):
    return cx(ro, length)-cx(ri, length+2)


def shellbox(x, y, z, wall, open_top=True):
    return b.Box(x,y,z)-b.Pos(0,0,wall if open_top else 0)*b.Box(x-2*wall,y-2*wall,z if open_top else z-2*wall)


def rounded_box(x,y,z,r):
    return b.extrude(b.RectangleRounded(x,y,r),amount=z/2,both=True)


def rounded_shell(x,y,z,wall,r):
    return rounded_box(x,y,z,r)-b.Pos(0,0,wall)*rounded_box(x-2*wall,y-2*wall,z,max(r-wall,1))


def bolt(radius=5, length=40):
    return b.Pos(0,0,-length/2)*b.Cylinder(radius,length)+b.extrude(b.RegularPolygon(radius*1.7,6),amount=radius)


def spring(radius, wire, height, turns):
    path=b.Helix(height/turns,height,radius)
    return b.sweep(b.Plane(origin=path@0,z_dir=path%0)*b.Circle(wire),path=path)


def gear(radius, teeth, width):
    # Standard 20-degree involute, with provisional pitch/count and backlash.
    module=2*radius/teeth
    base=radius*math.cos(math.radians(20));root=radius-1.25*module;tip=radius+module
    def inv(r):
        t=math.sqrt(max(0,(r/base)**2-1));return t-math.atan(t)
    half=math.pi/(2*teeth)-.12/(2*radius)
    radii=np.linspace(max(root,base),tip,8)
    pts=[]
    for i in range(teeth):
        a=2*math.pi*i/teeth
        profile=[(root,a-math.pi/teeth),(root,a-half-inv(radius))]
        profile += [(r,a-half-inv(radius)+inv(r)) for r in radii]
        profile += [(r,a+half+inv(radius)-inv(r)) for r in reversed(radii)]
        profile += [(root,a+half+inv(radius))]
        pts.extend((r*math.cos(t),r*math.sin(t)) for r,t in profile)
    return b.extrude(b.Plane.YZ*b.Polygon(*pts,align=None),amount=width/2,both=True)


def define(id, shape, name, function, group, color='#8498a3', sources=(), gaps=(), claims=()):
    if not shape.is_valid or shape.volume<=0 or len(shape.solids())!=1:
        raise ValueError(f'{id}: invalid or disconnected ({len(shape.solids())} solids)')
    shape.label=id
    shapes[id]=shape
    b.export_step(shape,STEP/f'{id}.step',unit=b.Unit.MM)
    vertices,faces=shape.tessellate(.18,.22)
    mesh=trimesh.Trimesh(vertices=np.array([[v.X,v.Z,-v.Y] for v in vertices])/1000,faces=faces,process=False)
    mesh.visual=trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
        baseColorFactor=trimesh.visual.color.hex_to_rgba(color),metallicFactor=.65,roughnessFactor=.38))
    scene=trimesh.Scene(mesh)
    (OUT/f'{id}.glb').write_bytes(scene.export(file_type='glb'))
    defs.append(dict(id=id,name=name,function=function,system=group,color=color,glb=f'/models/engine/{id}.glb',
        step=f'/cad/engine/generated/{id}.step',geometry_status='provisional',sources=list(sources),dimension_claims=list(claims),
        unresolved=list(gaps) or ['Exact production contours, dimensions and tolerances need applicable drawings or measurements.'],
        volume_mm3=shape.volume,solid_count=1,triangle_count=len(faces)))
    print('CAD',id,len(faces),'triangles',flush=True)


def group(id,name,parent='engine',motion=None,position=(0,0,0)):
    assemblies.append(dict(id=id,name=name,parent=parent,motion=motion,position_cad_mm=list(position)))


def add(id,definition,parent,pos=(0,0,0),explode=(0,0,0),rotation=(0,0,0),name=None):
    d=next(d for d in defs if d['id']==definition)
    occurrences.append(dict(id=id,definition=definition,parent=parent,name=name or d['name'],function=d['function'],
        position_cad_mm=list(pos),rotation_cad_deg=list(rotation),explode_cad_mm=list(explode)))


def rotating():
    group('rotating','Crankshaft & six piston assemblies')
    for d in BASE['definitions']:
        if d['id']=='crank-throw-demo': continue
        item=next(o for o in BASE['occurrences'] if o['definition']==d['id'])
        defs.append({**d,'name':item['name'],'function':item['function'],'system':'rotating',
            'sources':['fsm-2e5473b2bf99','silvolite-1186','hastings-592'],
            'unresolved':['Inherited piston-study assumptions; exact forging, ring profiles, pin offset and fastener threads remain unresolved.']})
    for i,(x,phase) in enumerate(zip(CYLINDERS,PHASES),1):
        for k,label in [('piston','Piston'),('rod','Connecting rod')]:
            group(f'{k}-group-{i}',f'Cylinder {i} · {label}','rotating',dict(type=k,phase_deg=phase), (x,0,0))
        for o in BASE['occurrences']:
            if o['parent']=='crank-group': continue
            parent=o['parent'].replace('-group',f'-group-{i}')
            add(f'c{i}-{o["id"]}',o['definition'],parent,o['position_cad_mm'],o['explode_cad_mm'],name=f'{o["name"]} · cylinder {i}')
    crank=None
    def fuse(s):
        nonlocal crank
        crank=s if crank is None else crank+s
    for x in MAINS: fuse(b.Pos(x,0,0)*cx(MAIN_R,32))
    for x,phase in zip(CYLINDERS,PHASES):
        t=math.radians(phase);y=-R*math.sin(t);z=R*math.cos(t)
        fuse(b.Pos(x,y,z)*cx(ROD_R,27.2))
        for sign in [-1,1]:
            # Two connected crank cheeks; casting counterweights remain provisional.
            cheek=cx(43,28)+b.Pos(0,0,R/2)*b.Box(28,66,R)+b.Pos(0,0,R)*cx(37,28)
            cheek+=b.Pos(0,0,-20)*cx(49,28)
            fuse(b.Pos(x+sign*27,0,0)*b.Rot(phase,0,0)*cheek)
    fuse(b.Pos(MAINS[0]+43,0,0)*cx(21,102))
    fuse(b.Pos(MAINS[-1]-20,0,0)*cx(MAIN_R,30))
    fuse(b.Pos(-375,0,0)*cx(45,24))
    fuse(b.Pos(-388,0,0)*cx(51,10))
    define('crankshaft',crank,'Crankshaft','Six throws turn reciprocating piston force into rotation. The seven main journals support the shaft; paired throws follow the 1–5–3–6–2–4 firing order.','rotating','#637f8b',
        ['fsm-2e5473b2bf99','fsm-2f144bda5e08'],['Journal widths, axial stations, counterweight contours, fillets, oil drillings and flange holes remain provisional.'],['stroke','rod_journal_diameter_range','main_journal_diameter_range'])
    group('crank-motion','Crankshaft','rotating',dict(type='crank'))
    add('crankshaft','crankshaft','crank-motion',explode=(0,0,-170))


def structure():
    group('structure','Block, bearings & main caps')
    # Open crankcase and continuous deck with bored cylinders. No substitute sleeves.
    block=b.Pos(0,-12,156.5)*rounded_box(LENGTH,242,195,14)
    block-=b.Pos(0,0,167)*rounded_box(LENGTH-18,150,146,12)
    for x in CYLINDERS:
        block+=b.Pos(x,0,169)*b.Cylinder(P['bore']/2+7,170)
    block+=b.Pos(0,-12,14)*(rounded_box(LENGTH,242,92,14)-rounded_box(LENGTH-18,224,96,5))
    # Provisional cam-side gallery, bored along X.
    block+=b.Pos(0,-90,84)*b.Box(LENGTH,55,110)
    block-=b.Pos(0,-90,72)*cx(25,LENGTH+2)
    for x in CYLINDERS: block-=b.Pos(x,0,180)*b.Cylinder(P['bore']/2,300)
    # Provisional swept crankcase clearance, cut before adding the main saddles.
    block-=cx(98,LENGTH-24)
    for x in MAINS:
        saddle=b.Pos(x,-12,45)*b.Box(31,242,90)-b.Pos(x,0,0)*cx(MAIN_R+2,35)
        block+=saddle
        for y in [-56,56]:block-=b.Pos(x,y,27)*b.Cylinder(5.6,60)
    for x in CYLINDERS:
        for dx in [-25,25]: block-=b.Pos(x+dx,-90,150)*b.Cylinder(11,235)
    # Machined deck holes are separate from the cast external envelope.
    for x in MAINS:
        for y in [-67,67]:block-=b.Pos(x,y,237)*b.Cylinder(6.1,36)
    block-=cx(MAIN_R+2,LENGTH+4)
    block-=b.Pos(-374,0,0)*cx(49.1,24)
    block-=b.Pos(0,-90,72)*cx(25,LENGTH+2)
    for x in CYLINDERS:block-=b.Pos(x,0,180)*b.Cylinder(P['bore']/2,300)
    define('block',block,'Cylinder block','Holds six cylinder bores, seven crankshaft supports and the cam-side structure. The visible water space is a simplified cast cavity, not a traced coolant network.','structure','#477176',['fsm-ed8704e3446e'],
        ['Bore pitch 113.792 mm, deck height 254 mm and casting envelope are assumptions. Water jackets, oil drillings, bosses, plugs and deck passages need reconstruction.'],['bore'])
    add('block','block','structure',explode=(0,0,70))
    cap=b.Pos(0,0,-23)*b.Box(31,144,46)-cx(MAIN_R+2,35)
    for y in [-56,56]: cap-=b.Pos(0,y,-24)*b.Cylinder(6,60)
    define('main-cap',cap,'Main bearing cap','Closes the crankshaft main bearing bore beneath the block. Each installed cap must retain its original position and orientation.','structure')
    shell=ringx(MAIN_R+2,MAIN_R+.025,30)
    for name,sign in [('upper',1),('lower',-1)]:
        part=shell & b.Pos(0,0,sign*50.02)*b.Box(100,100,100)
        if sign==1:part-=b.Pos(0,0,MAIN_R)*b.Cylinder(2.5,12)
        define('main-bearing-'+name,part,f'{name.title()} main bearing shell','A replaceable bearing surface carries the crankshaft on a pressurized oil film. Thrust-bearing details remain unresolved.','structure','#c6ab7c',claims=['main_journal_diameter_range'])
    define('main-cap-bolt',bolt(5.5,65),'Main cap bolt','Clamps a main cap to the cylinder block. Smooth shank; thread and grade are not modeled.','structure')
    for i,x in enumerate(MAINS,1):
        add(f'main-cap-{i}','main-cap','structure',(x,0,0),(0,0,-110),name=f'Main cap {i}')
        for key,sign in [('upper',1),('lower',-1)]:add(f'main-bearing-{key}-{i}','main-bearing-'+key,'structure',(x,0,0),(0,sign*70,sign*40))
        for j,y in enumerate([-56,56],1):add(f'main-cap-bolt-{i}-{j}','main-cap-bolt','structure',(x,y,-46),(0,0,-180),(180,0,0))


def top_end():
    group('head','Head, valves & springs')
    group('valvetrain','Camshaft, lifters, pushrods & rockers')
    head=b.Pos(0,-12,39)*rounded_box(LENGTH,242,78,12)
    # Open upper rocker trough and individual chamber/port abstractions.
    head-=b.Pos(0,-12,76)*rounded_box(LENGTH-24,216,55,10)
    for x in CYLINDERS:
        head-=b.Pos(x,0,0)*b.Cylinder(45,10)
        for dx in [-25,25]:
            head+=b.Pos(x+dx,-36,78)*b.Cylinder(12,60)
            head-=b.Pos(x+dx,-36,93)*b.Cylinder(4.6,40)
            head-=b.Pos(x+dx,16,28)*b.Cylinder(5,80)
            head-=b.Pos(x+dx,-88,28)*b.Cylinder(6,100)
            # Ports communicate with chamber. Passage routing is illustrative.
            head-=b.Pos(x+dx,-55,22)*b.Rot(90,0,0)*b.Cylinder(15,145)
            head-=b.Pos(x+dx,16,9)*b.Cylinder(17,25)
            vr=22 if dx<0 else 18.5
            head-=b.Pos(x+dx,16,7.1)*b.Cone(vr+.03,vr-1.47,3.25)
            head-=b.Pos(x+dx,16,2.25)*b.Cylinder(vr+.03,6.5)
    for x in MAINS:
        for y in [-67,67]:head-=b.Pos(x,y,40)*b.Cylinder(6.5,90)
    define('cylinder-head',head,'Cylinder head','Closes the cylinders and carries the valves, intake and exhaust passages and rocker supports. Port and chamber shapes here are provisional.','head','#a1afb6',['fsm-1b7a4041a45d'],
        ['Chamber volume/profile, port routing, coolant passages, casting numbers, guides and exact valve/rocker stations remain unverified.'])
    add('cylinder-head','cylinder-head','head',(0,0,DECK+1.5),(0,0,220))
    gasket=b.Pos(0,-12,0)*rounded_box(LENGTH,242,1.5,12)
    for x in CYLINDERS:
        gasket-=b.Pos(x,0,0)*b.Cylinder(51.5,5)
        for dx in [-25,25]:gasket-=b.Pos(x+dx,-88,0)*b.Cylinder(6,5)
    for x in MAINS:
        for y in [-67,67]:gasket-=b.Pos(x,y,0)*b.Cylinder(7,5)
    define('head-gasket',gasket,'Head gasket','Seals combustion, coolant and oil interfaces between block and head. Fire rings and passage pattern need further evidence.','head','#bba67f')
    add('head-gasket','head-gasket','head',(0,0,DECK+.75),(0,0,160))
    define('head-bolt',bolt(6,100),'Cylinder head bolt','One of fourteen fasteners in the factory head-bolt tightening sequence. Exact shank lengths and threads are pending.','head',sources=['fsm-1b7a4041a45d'])
    for i,x in enumerate(MAINS,1):
        for j,y in enumerate([-67,67],1):add(f'head-bolt-{i}-{j}','head-bolt','head',(x,y,DECK+79.5),(0,0,330))
    for id,r in [('intake-valve',22),('exhaust-valve',18.5)]:
        valve=b.Pos(0,0,1.6)*b.Cone(r,r-1.5,3.2)+b.Pos(0,0,55)*b.Cylinder(4.5,108)
        valve-=b.Pos(0,0,104)*annulus(6,4,1.2)
        define(id,valve,id.replace('-',' ').title(),'Opens its port at the appropriate part of the four-stroke cycle and seals against the head when closed. Stem, face and keeper groove are separate features in one valve.','head','#becbd2',['fsm-ff8bb019d348'])
    define('valve-spring',spring(13,2,51,6),'Valve spring','Returns the valve to its seat and keeps the valvetrain in contact with the cam profile. Coil count, rate and installed height are provisional.','head','#657d86')
    define('spring-retainer',annulus(17,5.65,4),'Valve spring retainer','Captures the top of the spring; paired keepers lock it to the valve stem.','head','#899ba5')
    keeper=(annulus(5.6,4.55,5)+annulus(4.6,4.05,1))&b.Pos(0,5.1,0)*b.Box(20,10,10)
    define('valve-keeper',keeper,'Valve keeper half','One half of the split lock connecting the spring retainer to the valve stem. Taper and lock profile are provisional.','head','#bdac7d')
    define('valve-seal',annulus(8,4.65,9),'Valve stem seal','Limits oil passing down the valve guide into the port. Seal construction and exact application remain unverified.','head','#494d49')
    pushrod=b.Cylinder(3.8,214.6)+b.Pos(0,0,107.3)*b.Sphere(3.8)+b.Pos(0,0,-107.3)*b.Sphere(3.8)
    pushrod-=b.Cylinder(1.2,225)
    define('pushrod',pushrod,'Hollow pushrod','Transfers lifter motion to the rocker and provides an oil route to the rocker interface. Length and end geometry are provisional.','valvetrain','#9eacb2',['fsm-6f023139b5f8'])
    rocker=b.Pos(0,0,0)*b.Box(17,119,11)
    rocker-=b.Pos(0,0,8)*b.Sphere(15)
    rocker-=b.Pos(0,-54,-8)*b.Sphere(4)
    rocker-=b.Cylinder(5,30)
    define('rocker-arm',rocker,'Rocker arm','Pivots on its fulcrum: a rising pushrod pushes the opposite end down against the valve. Stamped contours and exact leverage remain provisional.','valvetrain','#929da7',['fsm-c69f7255fa10'])
    define('rocker-fulcrum',b.Sphere(13)&b.Pos(0,0,-5)*b.Box(30,30,10)-b.Cylinder(5.2,30),'Rocker fulcrum','Provides the pivot bearing under the rocker attachment bolt.','valvetrain','#b0b9ba',['fsm-c69f7255fa10'])
    define('rocker-bolt',bolt(4.5,35),'Rocker attachment bolt','Retains the fulcrum on the threaded head pedestal.','valvetrain',sources=['fsm-c69f7255fa10'])
    define('rocker-guide',b.Box(22,20,4)-b.Cylinder(5,8),'Fulcrum guide','Locates the fulcrum on its head pedestal; the factory diagram identifies it as a separate component.','valvetrain',sources=['fsm-c69f7255fa10'])
    # Nine distinct lifter internals from the 1994 factory exploded diagram.
    lifter_body=b.Cylinder(10.5,52)-b.Pos(0,0,4)*b.Cylinder(8.3,50)-b.Pos(0,0,24)*annulus(8.7,7.5,1.2)
    lifter_body-=b.Pos(0,0,5)*annulus(12,9.65,7)
    lifter_body-=b.Pos(0,0,5)*cx(1.1,25)
    lifter_parts={
        'body':(lifter_body,'Hydraulic lifter body','Rides the cam lobe and houses the hydraulic lash-adjusting components. Separate retaining-ring groove, annular oil-feed groove and radial oil port are modeled; their dimensions are provisional.'),
        'plunger':(b.Cylinder(8.1,23)-b.Pos(0,0,2)*b.Cylinder(5.6,23)-b.Cylinder(1.2,26),'Lifter plunger','Moves inside the body to take up valve-train clearance. Its bottom closes the hydraulic chamber around the small check-valve port.'),
        'plunger-spring':(spring(5.5,.65,14.2,5),'Lifter plunger spring','Biases the plunger outward during lash adjustment.'),
        'check-ball':(b.Sphere(1.5),'Lifter check valve','Closes the oil chamber during lift so the lifter transmits force.'),
        'check-spring':(spring(2,.3,3.5,3),'Lifter check-valve spring','Biases the check valve toward its seat.'),
        'check-retainer':(b.Cylinder(4,1)-b.Cylinder(1,3),'Lifter check-valve retainer','Retains the check-valve spring at the plunger base.'),
        'metering-disc':(b.Cylinder(6.5,.7)-b.Cylinder(.8,2),'Lifter metering disc','Meters the oil delivered toward the pushrod cup.'),
        'pushrod-cup':(b.Cylinder(8,5)-b.Pos(0,0,4)*b.Sphere(4)-b.Cylinder(1,10),'Lifter pushrod cup','Supports the spherical pushrod end and admits lubricating oil.'),
        'lock-ring':(split_ring(8.5,7.5,.8,2),'Lifter retaining ring','Keeps the internal parts inside the lifter body.')}
    for key,(shape,name,fn) in lifter_parts.items():define('lifter-'+key,shape,name,fn,'valvetrain','#baa376' if 'spring' in key else '#97aab4',['fsm-7261979bd1f1'])
    for i,x in enumerate(CYLINDERS,1):
        for vi,dx in enumerate([-25,25]):
            kind='intake' if vi==0 else 'exhaust';tag=f'c{i}-{kind}';vx=x+dx
            group(tag+'-valve-assembly',f'Cylinder {i} · {kind} valve','head')
            vg=tag+'-valve-assembly'
            add(tag+'-valve',kind+'-valve',vg,(vx,16,DECK+7),(0,0,140))
            add(tag+'-spring','valve-spring',vg,(vx,16,DECK+56),(0,0,210))
            add(tag+'-retainer','spring-retainer',vg,(vx,16,DECK+111),(0,0,240))
            for n,rot in enumerate([0,180],1):add(tag+f'-keeper-{n}','valve-keeper',vg,(vx,16,DECK+111),(0,(-1 if n==1 else 1)*25,270),(0,0,rot))
            add(tag+'-seal','valve-seal',vg,(vx,16,DECK+56),(0,0,170))
            group(tag+'-actuation',f'Cylinder {i} · {kind} actuation','valvetrain')
            ag=tag+'-actuation'
            add(tag+'-pushrod','pushrod',ag,(vx,-90,DECK+113.5-107.3),(0,-110,160))
            add(tag+'-rocker','rocker-arm',ag,(vx,-36,DECK+121.5),(0,-70,270))
            add(tag+'-fulcrum','rocker-fulcrum',ag,(vx,-36,DECK+129.5),(0,-70,300))
            add(tag+'-rocker-bolt','rocker-bolt',ag,(vx,-36,DECK+129.5),(0,-70,350))
            add(tag+'-guide','rocker-guide',ag,(vx,-36,DECK+111.5),(0,-70,250))
            group(tag+'-lifter',f'Cylinder {i} · {kind} hydraulic lifter',ag)
            stations={'body':0,'plunger-spring':-20.35,'check-retainer':-12.5,'check-spring':-11.7,'check-ball':-6.4,'plunger':6,'metering-disc':17.9,'pushrod-cup':20.9,'lock-ring':24}
            offsets=[0,55,85,100,120,155,185,200,215]
            for n,(key,z) in enumerate(stations.items()):add(tag+'-lifter-'+key,'lifter-'+key,tag+'-lifter',(vx,-90,128+z),(0,-140,offsets[n]))
    cam=cx(15,710)
    for x in [-330,-110,110,330]:cam+=b.Pos(x,0,0)*cx(24,23)
    for i,x in enumerate(CYLINDERS):
        for vi,dx in enumerate([-25,25]):
            t=PHASES[i]/2+(105 if vi else 0)
            lobe=cx(18,15)+b.Pos(0,0,6.3)*cx(18,15)
            cam+=b.Pos(x+dx,0,0)*b.Rot(t,0,0)*lobe
    define('camshaft',cam,'Camshaft','Twelve lobes time the intake and exhaust valves. Four bearing journals locate the shaft; the timing gears turn it once per two crankshaft revolutions.','valvetrain','#729093',['fsm-33bfe47109d5'],['Lobe profiles, timing events, distributor drive, journal sizes and axial positions are not yet reconstructed.'])
    group('cam-motion','Camshaft','valvetrain',dict(type='cam'),(0,-90,72))
    add('camshaft','camshaft','cam-motion',explode=(100,-100,0))
    define('cam-bearing',ringx(25,24.025,22),'Camshaft bearing','Supports a camshaft journal in the block. Oil feed holes and individual bearing sizes require verification.','valvetrain','#b7a77e')
    for i,x in enumerate([-330,-110,110,330],1):add(f'cam-bearing-{i}','cam-bearing','valvetrain',(x,-90,72),(0,-100,0))


def closures():
    group('closures','Timing drive, covers, pan & seals')
    center=math.hypot(90,72)
    for id,rad,teeth in [('crank-timing-gear',center/3,24),('cam-timing-gear',center*2/3,48)]:
        shape=gear(rad,teeth,14)-cx(21.025 if id.startswith('crank') else 15.025,20)
        phase=math.degrees(math.atan2(72,-90)) if id.startswith('crank') else math.degrees(math.atan2(-72,90))-180/teeth
        shape=b.Rot(phase,0,0)*shape
        define(id,shape,id.replace('-',' ').title(),'The direct gear mesh maintains a 2:1 crank-to-cam speed ratio. These are 20-degree involute teaching gears; tooth count and pitch are not verified for the truck.','closures','#b29c72',['fsm-33bfe47109d5'],['Exact tooth count, pressure angle, material and timing-mark stations are unverified.'])
    add('crank-timing-gear','crank-timing-gear','crank-motion',(384,0,0),(160,0,0))
    add('cam-timing-gear','cam-timing-gear','cam-motion',(384,0,0),(160,0,0))
    cover=b.Pos(0,-32,56)*b.Rot(0,-90,0)*rounded_shell(230,242,24,4,34)
    cover-=cx(24,40)
    cover-=b.Pos(11,0,0)*cx(27.1,10)
    define('timing-cover',cover,'Timing cover','Encloses the gear drive and carries the front crankshaft seal. Casting profile, mounting pattern and water-pump interface remain provisional.','closures','#8fa1aa')
    add('timing-cover','timing-cover','closures',(403,0,0),(245,0,0))
    define('front-seal',ringx(27,21,8),'Front crankshaft seal','Seals around the rotating front crankshaft snout. The lip is represented by a simple annular solid.','closures','#514c43')
    add('front-seal','front-seal','closures',(414,0,0),(285,0,0))
    define('rear-seal',ringx(49,45,10),'Rear crankshaft seal','Limits oil leakage at the rear crankshaft exit. Seal lip and housing fit need exact dimensions.','closures','#514c43')
    add('rear-seal','rear-seal','closures',(-377,0,0),(-150,0,0))
    pan=rounded_shell(LENGTH,242,122,3,24)
    pan+=b.Pos(0,0,60)* (rounded_box(LENGTH+16,258,4,28)-rounded_box(LENGTH-6,236,8,21))
    for y in [-65,0,65]:pan+=b.Pos(0,y,-60)*rounded_box(LENGTH-70,8,4,3)
    pan-=b.Pos(377,12,96)*cx(45,40)
    pan-=b.Pos(-377,12,96)*cx(49.1,30)
    define('oil-pan',pan,'Oil pan','Stores the engine oil beneath the crankcase. The sump profile, baffles and pickup clearance need truck-specific references.','closures','#42686c',gaps=['This is an envelope study; the truck sump contour and all baffles are not yet modeled.'])
    add('oil-pan','oil-pan','closures',(0,-12,-96),(0,0,-320))
    pan_gasket=rounded_box(LENGTH+16,258,2,28)-rounded_box(LENGTH-6,236,5,21)
    pan_gasket-=b.Pos(377,12,33)*cx(45,40)
    pan_gasket-=b.Pos(-377,12,33)*cx(49.1,30)
    for i,side in enumerate(sorted(pan_gasket.solids(),key=lambda s:s.center().Y),1):
        key=f'pan-side-gasket-{i}'
        define(key,side,f'Oil pan side gasket {i}','Seals one side of the sump flange. Separate end seals remain missing; exact truck gasket construction needs confirmation.','closures','#b49967')
        add(key,key,'closures',(0,-12,-33),(0,0,-210))
    cover=rounded_shell(LENGTH-12,232,76,3,28)
    cover=b.Rot(180,0,0)*cover
    cover-=b.Pos(240,0,38)*b.Cylinder(17,20)
    for y in [-60,-35,35,60]:cover+=b.Pos(0,y,38)*rounded_box(LENGTH-100,8,4,3)
    define('valve-cover',cover,'Valve cover','Contains oil around the rocker gear and provides the oil-fill and ventilation interfaces. Stamping ribs and PCV openings are pending.','closures','#5c777c')
    add('valve-cover','valve-cover','closures',(0,-12,DECK+121),(0,0,460))
    define('valve-cover-gasket',rounded_box(LENGTH-12,232,3,28)-rounded_box(LENGTH-24,220,6,22),'Valve cover gasket','Seals the rocker cover to the head. Bolt-hole pattern and corner radii are pending.','closures','#b49c77')
    add('valve-cover-gasket','valve-cover-gasket','closures',(0,-12,DECK+81.5),(0,0,390))
    define('oil-filler-cap',b.Cylinder(23,12)+b.Pos(0,0,-8)*b.Cylinder(16,10),'Oil filler cap','Closes the oil-fill opening in the valve cover. Retention features are provisional.','closures','#3f4848')
    add('oil-filler-cap','oil-filler-cap','closures',(240,-12,DECK+165),(0,0,530))


def main():
    OUT.mkdir(exist_ok=True,parents=True);STEP.mkdir(exist_ok=True,parents=True)
    group('engine','Ford 4.9L engine',None)
    rotating();structure();top_end();closures()
    source_ids=set(s for d in defs for s in d.get('sources',[]))
    sources={p['id']:{k:p[k] for k in ['title','url','path','sha256']} for p in INDEX['sources'] if p['id'] in source_ids}
    sources.update(json.loads((ROOT/'inventory/engine/dimensions.json').read_text())['sources'])
    sources.update(json.loads((ROOT/'inventory/engine/comparison-sources.json').read_text()))
    manifest=dict(schema_version=2,title='Ford 4.9L · engine atlas',status='In-progress reconstruction; not a complete or verified OEM engine',
        coordinate_system=BASE['coordinate_system'],definitions=defs,assemblies=assemblies,occurrences=occurrences,sources=sources,
        mechanism={**BASE['mechanism'],'firing_order':[1,5,3,6,2,4],'cylinder_phases_deg':PHASES,'bore_pitch_mm':PITCH,'deck_height_mm':DECK},
        omissions=['Oil pump and pickup internals','Intake and exhaust manifolds, fuel system and EGR','Distributor, ignition, starter and accessory drive',
          'Water pump, thermostat and cooling passages','Flywheel and clutch boundary','Casting plugs, dowels, remaining gaskets and fasteners',
          'Exact casting surfaces, cam profiles and valve events','Manufacturing drawings or measurements for provisional dimensions',
          'Complete assembly collision audit and verified valvetrain kinematics'],
        coverage={'modeled_occurrences':len(occurrences),'modeled_definitions':len(defs),'verified_complete':False,
          'note':'Counts describe the current reconstruction, not a verified complete engine bill of materials. Some parts have unconfirmed applicability.'})
    for d in defs:
        if d['id'] not in shapes:shapes[d['id']]=b.import_step(ROOT/d['step'].lstrip('/'))
        size=shapes[d['id']].bounding_box().size
        d['model_bounds_mm']=[size.X,size.Y,size.Z]
    poses=transforms(manifest)
    placed=[]
    for o in occurrences:
        s=shapes[o['definition']].moved(poses[o['id']]);s.label=o['id'];placed.append(s)
    b.export_step(b.Compound(children=placed),STEP/'full-assembly.step',unit=b.Unit.MM)
    (ROOT/'inventory/engine/full-assembly.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Wrote {len(defs)} definitions / {len(occurrences)} individual parts',flush=True)


if __name__=='__main__': main()
