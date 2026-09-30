"""Parametric engine reconstruction, mm, X crank axis / Z cylinder axis.

The assembly is deliberately evidence-tagged. Neither fit nor attractive rendering
establishes OEM accuracy. See each definition's outstanding geometry questions.
"""
from pathlib import Path
import json
import math
import hashlib
import sys
import build123d as b
import numpy as np
import trimesh
from first_assembly import ROOT, P, cx, annulus, split_ring
from assembly_math import transforms
from assembly_step import placed_occurrences, verify_roundtrip
from valvetrain_dispatch import occurrence_shape
import valve_source_integration as source_valves
import valve_source_evidence as source_evidence
import valve_source_definition_adapter as source_definitions
from oil_pump import build as build_oil_pump
from efi_intake import build as build_efi_intake
from throttle import build as build_throttle
from fuel_injection import build as build_fuel_injection
from idle_air import build as build_idle_air
from throttle_sensor import build as build_throttle_sensor
from exhaust import build as build_exhaust
from damper import build as build_damper
from water_pump import build as build_water_pump
from thermostat import build as build_thermostat
from coolant_outlet import build as build_coolant_outlet
from distributor import build as build_distributor
from ignition_coil import build as build_ignition_coil
from ignition_module import build as build_ignition_module
from spark_plug import build as build_spark_plug
from plug_mounts import PLUG_Y, PLUG_LOCAL_Z, PLUG_ANGLE
from pushrod_cover import block_interface_shape, build as build_pushrod_cover
from valve_cover import cover_shape as valve_cover_shape
from cam_retention import connect_cam_nose, machine_gear_back, machine_block_bolts, GEAR_CENTER, build as build_cam_retention
from timing_cover import cover_shape as timing_cover_shape
from expansion_plugs import machine_block_seat, build as build_expansion_plugs
from oil_drive_layout import block_interface as oil_drive_block_interface, cam_interface as oil_drive_cam_interface, distributor_api, pump_api, build as build_oil_drive, SOURCES as OIL_DRIVE_SOURCES, GAPS as OIL_DRIVE_GAPS
from accessory_brackets import block_interface as accessory_block_interface, head_interface as accessory_head_interface, SOURCES as ACCESSORY_BRACKET_SOURCES, GAPS as ACCESSORY_BRACKET_GAPS
from thermactor_pump import block_interface as thermactor_block_interface, SOURCES as THERMACTOR_SOURCES, GAPS as THERMACTOR_GAPS
from oil_pump_motion import pump_api as moving_pump_api, drive_api as moving_drive_api
from oil_filter_adapter import block_interface as filter_block_interface, filter_api, build as build_filter_adapter, SOURCES as FILTER_ADAPTER_SOURCES, GAPS as FILTER_ADAPTER_GAPS

OUT = ROOT / 'models/engine'
STEP = ROOT / 'cad/engine/generated'
BASE = json.loads((ROOT/'inventory/engine/first-assembly.json').read_text())
INDEX = json.loads((ROOT/'inventory/engine/research-index.json').read_text())
INDEX['sources'] += json.loads((ROOT/'inventory/engine/system-references.json').read_text())['sources']
PITCH = 113.792  # provisional 4.480 inch station spacing, not factory-verified
DECK = 254.0  # provisional, not a measured casting dimension
LENGTH = 746.0
R = P['stroke']/2
MAIN_R = sum(P['main_journal_diameter_range'])/4
ROD_R = sum(P['rod_journal_diameter_range'])/4
CAM_JOURNAL_R = sum(P['camshaft_journal_diameter_range'])/4
CAM_BEARING_R = sum(P['camshaft_bearing_inside_diameter_range'])/4
CAM_BORE_R = CAM_BEARING_R+1.5  # shell thickness remains a modeling assumption
LIFTER_R = sum(P['lifter_diameter_range'])/4
LIFTER_BORE_R = sum(P['lifter_bore_diameter_range'])/4
CAM_STATIONS = [-330,-110,110,360.5]  # axial stations remain provisional
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


from cad_metrics import solid_volume, support_bounds
import manifold_lifting_eye
import intake_locating_dowel
import exhaust_front_profile
import exhaust_rear_entries
import rear_manifold_mounts_desktop_candidate as rear_mounts
import exhaust_outlet_flanges_desktop as exhaust_outlets
import valve_layout_integration as valve_layout
import rear_cam_clearance_desktop as rear_cam
import water_pump_joint_integration_desktop as pump_joint
import coolant_outlet_head_candidate as outlet_joint
from functools import lru_cache

@lru_cache(maxsize=1)
def outlet_parts(): return outlet_joint.parts()
OUTLET_IDS=('cylinder-head','coolant-outlet-housing','coolant-outlet-gasket','coolant-outlet-bolt','thermostat-piston','heater-supply-ect-elbow')
import alternator_carrier_1994_candidate as alternator94
import alt_thermactor_common_carrier_candidate as common_carrier
import oil_pan_joint_v9_candidate as pan_joint
from explode_stages_candidate import pan_hardware_stages
import accessory_carrier_1994 as carrier94
import accessory_carrier_1994_integration as carrier94_integration


VALVE_IDS = ('head-gasket','cylinder-head','camshaft','intake-valve','exhaust-valve','rocker-arm','rocker-fulcrum','pushrod','lifter-pushrod-cup')
VALVE_SOURCES = ['melling-camshaft-specifications','melling-stock-valve-specifications','melling-pushrod-specifications']
VALVE_GAPS = [
 'Coordinated motion is a teaching construction. The smooth lobe law fits selected Melling SYB-38 scalars; the installed cam, full lift law, advertised checking height and production timing remain unverified.',
 'The current pushrod is226.6mm between ball centers/234.2mm overall, shorter than the application-listed MPR-306257.556mm. Diameter7.6mm also differs from7.9248mm. Absolute lifter/cam/head/rocker datums still require reconciliation; this is not a correctly dimensioned replacement pushrod.',
 'Valve head diameters compare Melling V1504/V1505, whose application exception remains unresolved. Stem/guide, spring heights, spring end seating, keeper geometry and production rocker construction remain unfinished.',
 'Rigid linkage and constant-wire spring deformation explain motion; hydraulic lash adjustment, spring dynamics, lubrication, fatigue and running-engine performance are not simulated.'
]
VALVE_STATIONS = {'occurrences':[{'id':f'c{i}-{kind}-valve','position_cad_mm':[x+dx,0,0]} for i,x in enumerate(CYLINDERS,1) for kind,dx in [('intake',-25),('exhaust',25)]]}

def define(id, shape, name, function, group, color='#8498a3', sources=(), gaps=(), claims=(), prepared=False):
    if not prepared:
        if id in common_carrier.REMOVE_IDS: return
        if id in VALVE_IDS:
            if id=='head-gasket': shape=rear_cam.gasket_interface(shape,[o['position_cad_mm'][0] for o in VALVE_STATIONS['occurrences']])
            elif id=='cylinder-head': shape=valve_layout.adapt_head_all(shape,VALVE_STATIONS)
            elif id=='camshaft': shape=rear_cam.cam_interface(valve_layout.adapt_cam_all(shape,VALVE_STATIONS),sum(P['camshaft_journal_diameter_range'])/4)
            elif id in ('intake-valve','exhaust-valve'): shape=valve_layout.revised_valve(shape,id.split('-')[0])
            else: shape={'rocker-arm':valve_layout.rocker,'rocker-fulcrum':valve_layout.fulcrum,'pushrod':valve_layout.pushrod,'lifter-pushrod-cup':valve_layout.cup}[id]()
            sources=list(dict.fromkeys(list(sources)+VALVE_SOURCES))
            gaps=list(dict.fromkeys(list(gaps)+VALVE_GAPS))
            if id in ('camshaft','head-gasket'): gaps=list(dict.fromkeys(list(gaps)+rear_cam.GAPS))
            if id=='camshaft': function='Twelve hypothetical replacement-catalog lobes coordinate valve motion through a720degree engine cycle. Installed cam identity and full production timing remain unverified.'
        if id in ('alternator-support-bracket','alt-bracket-bolt-1','alt-bracket-bolt-2'):
            shape = alternator94.replacements()[id]
            sources = list(dict.fromkeys(list(sources) + alternator94.SOURCES))
            gaps = list(dict.fromkeys(list(gaps) + alternator94.GAPS))
        if id in ('pan-side-gasket-1','pan-side-gasket-2'): return
        if id in ('block','oil-pan'):
            shape = (pan_joint.block_interface if id=='block' else pan_joint.pan_interface)(shape)
            sources = list(dict.fromkeys(list(sources) + pan_joint.SOURCES))
            gaps = list(dict.fromkeys(list(gaps) + pan_joint.GAPS))
        if id in ('ps-ac-support-bracket','tensioner-mounting-bolt','block','cylinder-head'):
            shape = carrier94_integration.replacement_definition(id, shape)
            if id == 'block': shape = carrier94.block_interface(shape)
            if id == 'cylinder-head': shape = carrier94.head_interface(shape)
            sources = list(dict.fromkeys(list(sources) + carrier94.SOURCES))
            gaps = list(dict.fromkeys(list(gaps) + carrier94.GAPS))
        if id in OUTLET_IDS:
            shape=outlet_joint.head_interface(shape) if id=='cylinder-head' else outlet_parts()[id]
            sources=list(dict.fromkeys(list(sources)+outlet_joint.SOURCES))
            gaps=list(dict.fromkeys(list(gaps)+outlet_joint.GAPS))
        if id in pump_joint.IDS:
            shape=pump_joint.replacement(id,shape)
            sources=list(dict.fromkeys(list(sources)+pump_joint.SOURCES))
            gaps=list(dict.fromkeys(list(gaps)+pump_joint.GAPS))
            if id=='water-pump-housing':
                gaps=[g.replace('Radiator inlet neck remains a separate missing reconstruction.','Radiator inlet neck is modeled with provisional dimensions and passage geometry.').replace('Vehicle hoses, block coolant interface and pump attaching hardware remain outstanding.','Vehicle hoses and deeper coolant routing remain outstanding; local block mounting and four fasteners are modeled.') for g in gaps]
            if id=='water-pump-gasket': function='One shaped gasket seals the four-fastener pump flange directly to the block front. Dimensions and the larger fifth aperture function remain provisional.'
        for interface in (manifold_lifting_eye, intake_locating_dowel, exhaust_front_profile, exhaust_rear_entries, rear_mounts, exhaust_outlets):
            if id in interface.ADAPTERS:
                shape = interface.ADAPTERS[id](shape)
                if not isinstance(shape, b.Shape):
                    shape = b.Compound(children=list(shape))
                sources = list(dict.fromkeys(list(sources) + interface.SOURCES))
                gaps = list(dict.fromkeys(list(gaps) + interface.GAPS))
        if id == 'exhaust-front':
            function = 'Collects exhaust from three rounded-rectangular head entries through open curved runners into a blended collector and outlet. Manufacturer replacement evidence supports the form; dimensions, casting walls and installed identity remain provisional.'
        if id == 'exhaust-rear':
            function = 'Collects exhaust from three rounded-rectangular rear entries. Entry dimensions, retained box collector and EGR end connection remain provisional; manufacturer photos require further collector, flange and auxiliary-port reconstruction.'
        shape=source_definitions.replacement(id,shape,VALVE_STATIONS)
    if not shape.is_valid or shape.volume<=0 or len(shape.solids())!=1:
        raise ValueError(f'{id}: invalid or disconnected ({len(shape.solids())} solids)')
    volume_method="adaptive" if id == "oil-pump-housing" else "default"
    volume=solid_volume(shape,volume_method)
    shape.label=id
    shapes[id]=shape
    b.export_step(shape,STEP/f'{id}.step',unit=b.Unit.MM)
    # A valid in-memory sweep can still serialize with invalid STEP topology.
    # Reject it before publishing mesh/manifest entries for the component.
    reopened=b.import_step(STEP/f'{id}.step')
    if not reopened.is_valid or len(reopened.solids())!=1 or abs(solid_volume(reopened,volume_method)-volume)>max(1e-5,volume*1e-5):
        raise ValueError(f'{id}: STEP round-trip changed topology or volume')
    vertices,faces=shape.tessellate(.18,.22)
    mesh=trimesh.Trimesh(vertices=np.array([[v.X,v.Z,-v.Y] for v in vertices])/1000,faces=faces,process=False)
    if id in ('throttle-cable-ball-stud-estimated', 'throttle-cable-snap-retainer-illustrative', 'throttle-cable-socket-illustrative', 'throttle-cable-swivel-seat-illustrative', 'throttle-housing'):
        # Remove zero-area tessellation faces without changing the CAD geometry.
        mesh.merge_vertices()
        mesh.update_faces(mesh.nondegenerate_faces())
        mesh.update_faces(mesh.unique_faces())
        mesh.remove_unreferenced_vertices()
    smooth_casting = id.startswith(('ignition-coil-', 'distributor-', 'spark-plug-', 'egr-', 'evp-')) or id in ('efi-upper-intake','efi-lower-intake','exhaust-front','exhaust-rear')
    if smooth_casting:
        # Smooth curved casting surfaces while preserving sharp flange edges.
        mesh.merge_vertices()
        mesh=trimesh.graph.smooth_shade(mesh,angle=math.radians(35),facet_minarea=None)
    mesh.visual=trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
        baseColorFactor=trimesh.visual.color.hex_to_rgba(color),
        metallicFactor=0 if id.endswith(('-jacket','-boot','-carbon-core')) or id in ('evr-body','evr-cap','egr-control-vacuum-hose','egr-tube-heat-sleeve','spark-plug-insulator','ignition-coil-case','ignition-coil-bobbin','ignition-coil-insulation','distributor-cap','distributor-rotor','distributor-connector','ps-pump-reservoir','ps-pump-cap-dipstick','engine-coolant-temperature-insulator') else .65,
        roughnessFactor=.6 if id in ('ignition-coil-case','distributor-cap','distributor-rotor') else .38))
    scene=trimesh.Scene(mesh)
    (OUT/f'{id}.glb').write_bytes(scene.export(file_type='glb',include_normals=smooth_casting))
    defs.append(dict(id=id,name=name,function=function,system=group,color=color,glb=f'/models/engine/{id}.glb',
        step=f'/cad/engine/generated/{id}.step',geometry_status='provisional',sources=list(sources),dimension_claims=list(claims),
        unresolved=list(gaps) or ['Exact production contours, dimensions and tolerances need applicable drawings or measurements.'],
        volume_mm3=volume,volume_method=volume_method,solid_count=1,triangle_count=len(mesh.faces)))
    print('CAD',id,len(mesh.faces),'triangles',flush=True)


def group(id,name,parent='engine',motion=None,position=(0,0,0),rotation=(0,0,0)):
    assemblies.append(dict(id=id,name=name,parent=parent,motion=motion,position_cad_mm=list(position),rotation_cad_deg=list(rotation)))


def add(id,definition,parent,pos=(0,0,0),explode=(0,0,0),rotation=(0,0,0),name=None):
    if id in common_carrier.REMOVE_IDS or id in carrier94_integration.REMOVE_OCCURRENCES or id in ('pan-side-gasket-1','pan-side-gasket-2'): return
    if id in carrier94_integration.PLACEMENT_OVERRIDES:
        override = carrier94_integration.PLACEMENT_OVERRIDES[id]
        pos, rotation = override['position_cad_mm'], override['rotation_cad_deg']
    if parent == 'alternator-assembly': pos = alternator94.POSITION
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
    from flywheel import crank_interface
    crank=crank_interface(crank)
    from pilot_bearing import crank_interface as pilot_interface
    crank=pilot_interface(crank)
    from damper_attachment import crank_interface as damper_interface
    crank=damper_interface(crank)
    define('crankshaft',crank,'Crankshaft','Six throws turn reciprocating piston force into rotation. The seven main journals support the shaft; paired throws follow the 1–5–3–6–2–4 firing order.','rotating','#637f8b',
        ['fsm-2e5473b2bf99','fsm-2f144bda5e08'],['Journal widths, axial stations, counterweight contours, fillets, oil drillings and flange holes remain provisional.'],['stroke','rod_journal_diameter_range','main_journal_diameter_range'])
    group('crank-motion','Crankshaft','rotating',dict(type='crank'))
    add('crankshaft','crankshaft','crank-motion',explode=(0,0,-170))


def define_block_casting():
    # Open crankcase and continuous deck with bored cylinders. No substitute sleeves.
    block=b.Pos(0,-12,156.5)*rounded_box(LENGTH,242,195,14)
    block-=b.Pos(0,0,167)*rounded_box(LENGTH-18,150,146,12)
    for x in CYLINDERS:
        block+=b.Pos(x,0,169)*b.Cylinder(P['bore']/2+7,170)
    block+=b.Pos(0,-12,14)*(rounded_box(LENGTH,242,92,14)-rounded_box(LENGTH-18,224,96,5))
    # Cam and pushrods lie on +Y, opposite the -Y manifold face.
    # Relationship follows the Ford external/internal exploded drawings;
    # lateral distances and casting contours remain provisional.
    block+=b.Pos(0,90,84)*b.Box(LENGTH,55,110)
    for x in CYLINDERS: block-=b.Pos(x,0,180)*b.Cylinder(P['bore']/2,300)
    # Provisional swept crankcase clearance, cut before adding the main saddles.
    block-=cx(98,LENGTH-24)
    for x in MAINS:
        saddle=b.Pos(x,-12,45)*b.Box(31,242,90)-b.Pos(x,0,0)*cx(MAIN_R+2,35)
        block+=saddle
        for y in [-56,56]:block-=b.Pos(x,y,27)*b.Cylinder(5.6,60)
    for x in CYLINDERS:
        for dx in [-25,25]: block-=b.Pos(x+dx,90,150)*b.Cylinder(LIFTER_BORE_R,235)
    # Machined deck holes are separate from the cast external envelope.
    for x in MAINS:
        for y in [-67,67]:block-=b.Pos(x,y,237)*b.Cylinder(6.1,36)
    block-=cx(MAIN_R+2,LENGTH+4)
    block-=b.Pos(-374,0,0)*cx(49.1,24)
    block-=b.Pos(0,90,72)*cx(CAM_BORE_R,LENGTH+2)
    for x in CYLINDERS:block-=b.Pos(x,0,180)*b.Cylinder(P['bore']/2,300)
    block=block_interface_shape(block)
    block=machine_block_bolts(block)
    block=machine_block_seat(block,CAM_BORE_R)
    block=oil_drive_block_interface(block)
    block=accessory_block_interface(block)
    block=thermactor_block_interface(block)
    block=filter_block_interface(block)
    define('block',block,'Cylinder block','Holds six cylinder bores, seven crankshaft supports and the cam-side structure. The visible water space is a simplified cast cavity, not a traced coolant network.','structure','#477176',['fsm-ed8704e3446e','fsm-2e5473b2bf99','ford-engine-side-layout']+OIL_DRIVE_SOURCES+ACCESSORY_BRACKET_SOURCES+THERMACTOR_SOURCES+FILTER_ADAPTER_SOURCES,
        ['Bore pitch 113.792 mm, deck height 254 mm and casting envelope are assumptions. The side-cover opening, perimeter rail and six fastener webs are provisional fit-study geometry. The rear cam plug seat and support boss are provisional. Water jackets, oil drillings, other bosses/plugs and deck passages need reconstruction.']+OIL_DRIVE_GAPS+ACCESSORY_BRACKET_GAPS+THERMACTOR_GAPS+FILTER_ADAPTER_GAPS,['bore','lifter_bore_diameter_range'])


def structure():
    group('structure','Block, bearings & main caps')
    define_block_casting()
    add('block','block','structure',explode=(0,0,70))
    build_pushrod_cover((define,add,group))
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


def define_head_casting():
    head=b.Pos(0,-12,39)*rounded_box(LENGTH,242,78,12)
    # Open upper rocker trough and individual chamber/port abstractions.
    head-=b.Pos(0,-12,76)*rounded_box(LENGTH-24,216,55,10)
    for x in CYLINDERS:
        # Photograph-informed chamber outline; exact depth/volume unverified.
        chamber=b.Pos(-23,-16,0)*b.Cylinder(25,10)+b.Pos(23,-16,0)*b.Cylinder(23,10)
        chamber+=b.Pos(0,2,0)*b.Cylinder(37,10)
        head-=b.Pos(x,0,0)*chamber
        # Local firing pocket connects the angled bore to the chamber.
        head-=b.Pos(x,41,6)*b.Cylinder(12,14)
        mount=b.Pos(x,PLUG_Y,PLUG_LOCAL_Z)*b.Rot(PLUG_ANGLE,0,0)
        head-=mount*(b.Pos(0,0,-6)*b.Cylinder(9.65,16))
        head-=mount*(b.Pos(0,0,1)*b.Cone(9.15,10.55,2))
        head-=mount*(b.Pos(0,0,42)*b.Cylinder(17,80))
        for dx in [-25,25]:
            head+=b.Pos(x+dx,36,78)*b.Cylinder(12,60)
            head-=b.Pos(x+dx,36,93)*b.Cylinder(4.6,40)
            head-=b.Pos(x+dx,-16,28)*b.Cylinder(5,80)
            head-=b.Pos(x+dx,88,28)*b.Cylinder(6,100)
            # Ports communicate with chamber. Passage routing is illustrative.
            # Reach the external manifold face; the old 145 mm drilling stopped
            # 5.5 mm short of the side wall and left the modeled ports blind.
            head-=b.Pos(x+dx,-60,22)*b.Rot(90,0,0)*b.Cylinder(15,160)
            head-=b.Pos(x+dx,-16,9)*b.Cylinder(17,25)
            vr=22 if dx<0 else 18.5
            head-=b.Pos(x+dx,-16,7.1)*b.Cone(vr+.03,vr-1.47,3.25)
            head-=b.Pos(x+dx,-16,2.25)*b.Cylinder(vr+.03,6.5)
    for x in MAINS:
        for y in [-67,67]:head-=b.Pos(x,y,40)*b.Cylinder(6.5,90)
    from ignition_leads import head_interface, SOURCES as lead_sources, GAPS as lead_gaps
    head=head_interface(head)
    head=accessory_head_interface(head)
    define('cylinder-head',head,'Cylinder head','Closes the cylinders and carries the valves, intake and exhaust passages and rocker supports. Port and chamber shapes here are provisional.','head','#a1afb6',['fsm-1b7a4041a45d','allied-12952-head-photos']+lead_sources+ACCESSORY_BRACKET_SOURCES,
        ['Photograph-informed chamber outline and plug wells remain provisional. Plug datums are shared with the installed study for geometric coherence, not verified production fit. Chamber volume/profile, port routing, coolant passages, casting identity and valve stations remain unverified.']+lead_gaps+ACCESSORY_BRACKET_GAPS)


def top_end():
    group('head','Head, valves & springs')
    group('valvetrain','Camshaft, lifters, pushrods & rockers')
    define_head_casting()
    add('cylinder-head','cylinder-head','head',(0,0,DECK+1.5),(0,0,220))
    gasket=b.Pos(0,-12,0)*rounded_box(LENGTH,242,1.5,12)
    for x in CYLINDERS:
        gasket-=b.Pos(x,0,0)*b.Cylinder(51.5,5)
        for dx in [-25,25]:gasket-=b.Pos(x+dx,88,0)*b.Cylinder(6,5)
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
    rocker-=b.Pos(0,54,-8)*b.Sphere(4)
    rocker-=b.Cylinder(5,30)
    define('rocker-arm',rocker,'Rocker arm','Pivots on its fulcrum: a rising pushrod pushes the opposite end down against the valve. Stamped contours and exact leverage remain provisional.','valvetrain','#929da7',['fsm-c69f7255fa10'])
    define('rocker-fulcrum',b.Sphere(13)&b.Pos(0,0,-5)*b.Box(30,30,10)-b.Cylinder(5.2,30),'Rocker fulcrum','Provides the pivot bearing under the rocker attachment bolt.','valvetrain','#b0b9ba',['fsm-c69f7255fa10'])
    define('rocker-bolt',bolt(4.5,35),'Rocker attachment bolt','Retains the fulcrum on the threaded head pedestal.','valvetrain',sources=['fsm-c69f7255fa10'])
    define('rocker-guide',b.Box(22,20,4)-b.Cylinder(5,8),'Fulcrum guide','Locates the fulcrum on its head pedestal; the factory diagram identifies it as a separate component.','valvetrain',sources=['fsm-c69f7255fa10'])
    # Nine distinct lifter internals from the 1994 factory exploded diagram.
    lifter_body=b.Cylinder(LIFTER_R,52)-b.Pos(0,0,4)*b.Cylinder(8.3,50)-b.Pos(0,0,24)*annulus(8.7,7.5,1.2)
    lifter_body-=b.Pos(0,0,5)*annulus(12,LIFTER_R-.85,7)
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
    for key,(shape,name,fn) in lifter_parts.items():define('lifter-'+key,shape,name,fn,'valvetrain','#baa376' if 'spring' in key else '#97aab4',['fsm-7261979bd1f1','fsm-2e5473b2bf99'],claims=['lifter_diameter_range'] if key=='body' else [])
    for i,x in enumerate(CYLINDERS,1):
        for vi,dx in enumerate([-25,25]):
            kind='intake' if vi==0 else 'exhaust';tag=f'c{i}-{kind}';vx=x+dx
            group(tag+'-valve-assembly',f'Cylinder {i} · {kind} valve','head')
            vg=tag+'-valve-assembly'
            add(tag+'-valve',kind+'-valve',vg,(vx,-16,DECK+7),(0,0,140))
            add(tag+'-spring','valve-spring',vg,(vx,-16,DECK+56),(0,0,210))
            add(tag+'-retainer','spring-retainer',vg,(vx,-16,DECK+111),(0,0,240))
            for n,rot in enumerate([0,180],1):add(tag+f'-keeper-{n}','valve-keeper',vg,(vx,-16,DECK+111),(0,(-1 if n==1 else 1)*25,270),(0,0,rot))
            add(tag+'-seal','valve-seal',vg,(vx,-16,DECK+56),(0,0,170))
            group(tag+'-actuation',f'Cylinder {i} · {kind} actuation','valvetrain')
            ag=tag+'-actuation'
            add(tag+'-pushrod','pushrod',ag,(vx,90,DECK+113.5-107.3),(0,-110,160))
            add(tag+'-rocker','rocker-arm',ag,(vx,36,DECK+121.5),(0,-70,270))
            add(tag+'-fulcrum','rocker-fulcrum',ag,(vx,36,DECK+129.5),(0,-70,300))
            add(tag+'-rocker-bolt','rocker-bolt',ag,(vx,36,DECK+129.5),(0,-70,350))
            add(tag+'-guide','rocker-guide',ag,(vx,36,DECK+111.5),(0,-70,250))
            group(tag+'-lifter',f'Cylinder {i} · {kind} hydraulic lifter',ag)
            stations={'body':0,'plunger-spring':-20.35,'check-retainer':-12.5,'check-spring':-11.7,'check-ball':-6.4,'plunger':6,'metering-disc':17.9,'pushrod-cup':20.9,'lock-ring':24}
            offsets=[0,55,85,100,120,155,185,200,215]
            for n,(key,z) in enumerate(stations.items()):add(tag+'-lifter-'+key,'lifter-'+key,tag+'-lifter',(vx,90,128+z),(0,-140,offsets[n]))
    cam=cx(15,710)
    for x in CAM_STATIONS:cam+=b.Pos(x,0,0)*cx(CAM_JOURNAL_R,25 if x==CAM_STATIONS[-1] else 23)
    for i,x in enumerate(CYLINDERS):
        for vi,dx in enumerate([-25,25]):
            t=PHASES[i]/2+(105 if vi else 0)
            lobe=cx(18,15)+b.Pos(0,0,6.3)*cx(18,15)
            cam+=b.Pos(x+dx,0,0)*b.Rot(t,0,0)*lobe
    cam=connect_cam_nose(cam)
    cam=oil_drive_cam_interface(cam)
    define('camshaft',cam,'Camshaft','Twelve lobes time the intake and exhaust valves. Four bearing journals locate the shaft; the timing gears turn it once per two crankshaft revolutions.','valvetrain','#729093',['fsm-33bfe47109d5','fsm-2e5473b2bf99']+OIL_DRIVE_SOURCES,['Journal diameter uses the midpoint of the factory range. Front journal, nose and key seat now meet the retention study; axial stations and key dimensions remain assumed. Lobe profiles, timing events and production distributor-drive geometry remain unresolved.']+OIL_DRIVE_GAPS,['camshaft_journal_diameter_range'])
    group('cam-motion','Camshaft','valvetrain',dict(type='cam'),(0,90,72))
    add('camshaft','camshaft','cam-motion',explode=(100,-100,0))
    define('cam-bearing',ringx(CAM_BORE_R,CAM_BEARING_R,22),'Camshaft bearing','Supports a camshaft journal in the block. Inside diameter uses the factory-range midpoint; shell thickness, width, axial stations and oil-feed holes remain provisional.','valvetrain','#b7a77e',['fsm-2e5473b2bf99'],claims=['camshaft_bearing_inside_diameter_range'])
    for i,x in enumerate(CAM_STATIONS,1):add(f'cam-bearing-{i}','cam-bearing','valvetrain',(x,90,72),(0,-100,0))


def define_timing_cover():
    define('timing-cover',timing_cover_shape(),'Timing cover','Encloses the two timing gears and carries the front crankshaft seal. Its two-lobe cavity clears the modeled gear envelopes; production contours, bosses and mounting interfaces remain provisional.','closures','#8fa1aa',['ford-industrial-parts','ford-engine-side-layout'],['Outer radii52/88mm, inner radii48/84mm and24mmdepth are assumed clearance-study dimensions, not a production casting trace. Block flange, bolt pattern and pump interfaces remain unfinished.'])


def closures():
    group('closures','Timing drive, covers, pan & seals')
    build_cam_retention((define,add,group))
    center=math.hypot(90,72)
    for id,rad,teeth in [('crank-timing-gear',center/3,24),('cam-timing-gear',center*2/3,48)]:
        shape=gear(rad,teeth,14)-cx(21.025 if id.startswith('crank') else 15.9,20)
        phase=math.degrees(math.atan2(72,90)) if id.startswith('crank') else math.degrees(math.atan2(-72,-90))-180/teeth
        shape=b.Rot(phase,0,0)*shape
        if id.startswith('cam'):shape=machine_gear_back(shape)
        define(id,shape,id.replace('-',' ').title(),'The direct gear mesh maintains a 2:1 crank-to-cam speed ratio. These are 20-degree involute teaching gears; tooth count and pitch are not verified for the truck.','closures','#b29c72',['fsm-33bfe47109d5'],['Exact tooth count, pressure angle, material and timing-mark stations are unverified.'])
    add('crank-timing-gear','crank-timing-gear','crank-motion',(GEAR_CENTER,0,0),(160,0,0))
    add('cam-timing-gear','cam-timing-gear','cam-motion',(GEAR_CENTER,0,0),(160,0,0))
    define_timing_cover()
    add('timing-cover','timing-cover','closures',(403,0,0),(245,0,0))
    define('front-seal',ringx(27,21,8),'Front crankshaft seal','Seals around the rotating front crankshaft snout. The lip is represented by a simple annular solid.','closures','#514c43')
    add('front-seal','front-seal','closures',(414,0,0),(285,0,0))
    define('rear-seal',ringx(49,45,10),'Rear crankshaft seal','Limits oil leakage at the rear crankshaft exit. Seal lip and housing fit need exact dimensions.','closures','#514c43')
    add('rear-seal','rear-seal','closures',(-377,0,0),(-150,0,0))
    from oil_pan import build as build_oil_pan
    build_oil_pan((define,add,group,rounded_box,cx,LENGTH))
    cover=valve_cover_shape()
    define('valve-cover',cover,'Valve cover','Contains oil around the rocker gear. Sloped shoulders and separate oil-fill/ventilation openings replace the box envelope. Exact stamping contours, mounting holes, baffles and opening stations remain provisional.','closures','#48565e',['engine-exploded-drawing','ford-engine-side-layout'],['Profile lofts are visual approximations. Upper profiles lean22mm toward the cam side to clear the corrected rocker placement; this is a fit-study assumption. The base envelope and fill/ventilation locations require measurements of the installed truck cover.'])
    add('valve-cover','valve-cover','closures',(0,-12,DECK+121),(0,0,460))
    define('valve-cover-gasket',rounded_box(LENGTH-12,232,3,28)-rounded_box(LENGTH-24,220,6,22),'Valve cover gasket','Seals the rocker cover to the head. Bolt-hole pattern and corner radii are pending.','closures','#b49c77')
    add('valve-cover-gasket','valve-cover-gasket','closures',(0,-12,DECK+81.5),(0,0,390))
    define('oil-filler-cap',b.Cylinder(23,12)+b.Pos(0,0,-8)*b.Cylinder(16,10),'Oil filler cap','Closes the oil-fill opening in the valve cover. Retention features are provisional.','closures','#3f4848')
    add('oil-filler-cap','oil-filler-cap','closures',(240,-12,DECK+165),(0,0,530))


def main():
    OUT.mkdir(exist_ok=True,parents=True);STEP.mkdir(exist_ok=True,parents=True)
    refresh=next((key for key in ('peripherals','exhaust','throttle','damper','cooling','ignition','head-interface','fuel','induction','fuel-couplings','ventilation','oil-filter','oil-pressure','oil-pan','timing-cover','block-plugs','egr','egr-tube','evr','egr-hoses','flywheel','pilot-bearing') if '--refresh-'+key in sys.argv),None)
    if '--refresh-accessory-drive' in sys.argv:
        refresh='accessory-drive'
    if '--refresh-ac-compressor' in sys.argv:
        refresh='ac-compressor'
    if '--refresh-starter' in sys.argv:
        refresh='starter'
    if '--refresh-regulator-vacuum' in sys.argv:
        refresh='regulator-vacuum'
    if '--refresh-oil-drive' in sys.argv:
        refresh='oil-drive'
    if '--refresh-cooling-connections' in sys.argv:
        refresh='cooling-connections'
    if '--refresh-ignition-leads' in sys.argv:
        refresh='ignition-leads'
    if '--refresh-manifold-eye' in sys.argv:
        refresh='manifold-eye'
    if '--refresh-intake-dowel' in sys.argv:
        refresh='intake-dowel'
    if '--refresh-exhaust-profile' in sys.argv:
        refresh='exhaust-profile'
    if '--refresh-rear-entries' in sys.argv:
        refresh='rear-entries'
    if '--refresh-rear-mounts' in sys.argv:
        refresh='rear-mounts'
    if '--refresh-exhaust-outlets' in sys.argv:
        refresh='exhaust-outlets'
    if '--refresh-common-carrier' in sys.argv:
        refresh='common-carrier'
    if '--refresh-carrier-1994' in sys.argv:
        refresh='carrier-1994'
    if '--refresh-pump-inlet' in sys.argv:
        refresh='pump-inlet'
    if '--refresh-outlet-joint' in sys.argv:
        refresh='outlet-joint'
    if '--refresh-pump-joint' in sys.argv:
        refresh='pump-joint'
    if '--refresh-pan-joint' in sys.argv:
        refresh='pan-joint'
    if '--refresh-alternator-carrier' in sys.argv:
        refresh='alternator-carrier'
    if '--refresh-valvetrain' in sys.argv:
        refresh='valvetrain'
    if '--refresh-source-valves' in sys.argv:
        refresh='source-valves'
    if refresh:
        # Explicit development shortcut: retain the saved long block/lubrication.
        # Use a full build after changing any core generator or its dimensions.
        previous=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())
        removed={'source-valves':set(),'common-carrier':set(),'pump-inlet':set(),'outlet-joint':set(),'pump-joint':set(),'valvetrain':set(),'alternator-carrier':set(),'pan-joint':{'oil-pan-fastener-assembly'},'carrier-1994':{'carrier-1994-engine-attachments'},'exhaust-outlets':set(),'rear-mounts':{'rear-manifold-mounts'},'rear-entries':set(),'exhaust-profile':set(),'intake-dowel':{'intake-head-locator'},'manifold-eye':{'front-manifold-eye'},'starter':{'starter-assembly'},'ac-compressor':{'ac-compressor'},'peripherals':{'induction','exhaust'},'exhaust':{'exhaust'},'throttle':{'throttle-assembly'},'damper':{'damper-assembly'},'cooling':{'cooling'},'ignition':{'ignition'},'head-interface':{'ignition'},'fuel':{'fuel-system'},'induction':{'induction'},'fuel-couplings':{'fuel-supply-coupling','fuel-return-coupling'},'ventilation':{'crankcase-ventilation'},'oil-filter':{'oil-filter-assembly'},'oil-pressure':{'oil-pressure-switch-assembly'},'oil-pan':{'oil-pan-assembly','oil-pump-assembly','oil-pickup-assembly','oil-drive-assembly'},'timing-cover':set(),'block-plugs':{'block-plugs'},'egr':{'egr'},'egr-tube':{'egr-exhaust-line'},'evr':{'egr-vacuum-regulator'},'egr-hoses':{'egr-vacuum-lines'},'flywheel':{'flywheel-assembly'},'pilot-bearing':{'pilot-bearing-assembly'},'accessory-drive':{'accessory-drive','water-pump-pulley-assembly','fan-clutch-assembly'},'regulator-vacuum':{'regulator-vacuum-line'},'ignition-leads':{'ignition-leads','ignition-coil-mount'},'cooling-connections':{'cooling-connections'},'oil-drive':{'distributor-assembly','oil-pump-assembly','oil-pickup-assembly','oil-drive-assembly'}}[refresh]
        if refresh=='oil-filter':removed.add('oil-filter-adapter-assembly')
        for a in previous['assemblies']:
            if a['parent'] in removed:removed.add(a['id'])
        assemblies.extend(a for a in previous['assemblies'] if a['id'] not in removed)
        old_pan_ids={'oil-pan','pan-side-gasket-1','pan-side-gasket-2'} if refresh=='oil-pan' else set()
        occurrences.extend(o for o in previous['occurrences'] if o['parent'] not in removed and o['id'] not in old_pan_ids)
        occurrences[:] = [o for o in occurrences if o['id'] not in carrier94_integration.REMOVE_OCCURRENCES and o['id'] not in ('pan-side-gasket-1','pan-side-gasket-2') and not (refresh=='pan-joint' and o['id']=='oil-pan-molded-gasket')]
        for occurrence in occurrences:
            if occurrence['id'] in carrier94_integration.PLACEMENT_OVERRIDES:
                occurrence.update(carrier94_integration.PLACEMENT_OVERRIDES[occurrence['id']])
        for occurrence in occurrences:
            override = alternator94.placement_override(occurrence)
            if override is not None: occurrence['position_cad_mm'] = list(override)
        occurrences[:]=[o for o in occurrences if o['id'] not in common_carrier.REMOVE_IDS and not (refresh=='common-carrier' and o['id']==common_carrier.NEW_ID)]
        if refresh=='pump-joint': occurrences[:]=[o for o in occurrences if not o['id'].startswith('water-pump-mounting-screw-')]
        used={o['definition'] for o in occurrences}
        if refresh=='pump-joint': used.difference_update(pump_joint.IDS)
        if refresh=='pump-inlet': used.discard('water-pump-housing')
        if refresh=='outlet-joint': used.difference_update(OUTLET_IDS)
        if refresh=='source-valves': used.difference_update(source_definitions.IDS | {'valve-spring'})
        if refresh=='valvetrain': used.difference_update(VALVE_IDS)
        if refresh=='alternator-carrier': used.difference_update(('alternator-support-bracket','alt-bracket-bolt-1','alt-bracket-bolt-2'))
        if refresh=='pan-joint':
            used.difference_update(('block','oil-pan'))
        if refresh=='carrier-1994':
            used.difference_update(('block','cylinder-head','ps-ac-support-bracket','tensioner-mounting-bolt'))
        if refresh=='oil-filter':used.discard('block')
        if refresh=='manifold-eye':
            used.difference_update(manifold_lifting_eye.ADAPTERS)
        if refresh=='intake-dowel':
            used.difference_update(intake_locating_dowel.ADAPTERS)
        if refresh=='exhaust-profile':
            used.difference_update(exhaust_front_profile.ADAPTERS)
        if refresh=='exhaust-outlets':
            used.difference_update(exhaust_outlets.ADAPTERS)
        if refresh=='rear-mounts':
            used.difference_update(rear_mounts.ADAPTERS)
        if refresh=='rear-entries':
            used.difference_update(exhaust_rear_entries.ADAPTERS)
        defs.extend(d for d in previous['definitions'] if not (refresh=='ignition-leads' and d['id'] in ('distributor-cap','cylinder-head')) and not (refresh=='cooling-connections' and d['id']=='water-pump-housing') and d['id'] in used and not (refresh=='oil-drive' and d['id'] in ('block','camshaft')) and not (refresh=='head-interface' and d['id']=='cylinder-head') and not (refresh=='timing-cover' and d['id']=='timing-cover') and not (refresh=='block-plugs' and d['id']=='block') and not (refresh in ('egr','regulator-vacuum') and d['id']=='efi-upper-intake') and not (refresh=='egr-tube' and d['id']=='exhaust-rear') and not (refresh=='accessory-drive' and d['id'] in ('water-pump-drive-hub','block','cylinder-head')) and not (refresh in ('flywheel','pilot-bearing','damper') and d['id']=='crankshaft'))
        if refresh in ('manifold-eye', 'intake-dowel', 'exhaust-profile', 'rear-entries', 'rear-mounts', 'exhaust-outlets'):
            interface = {'manifold-eye': manifold_lifting_eye, 'intake-dowel': intake_locating_dowel,
                         'exhaust-profile': exhaust_front_profile, 'rear-entries': exhaust_rear_entries, 'rear-mounts': rear_mounts, 'exhaust-outlets': exhaust_outlets}[refresh]
            for identifier in interface.ADAPTERS:
                old = next(definition for definition in previous['definitions'] if definition['id'] == identifier)
                shape = b.import_step(ROOT / old['step'].lstrip('/'))
                define(identifier, shape, old['name'], old['function'], old['system'], old['color'], old['sources'], old['unresolved'], old['dimension_claims'])
        if refresh=='pump-inlet':
            old=next(d for d in previous['definitions'] if d['id']=='water-pump-housing')
            define(old['id'],b.import_step(ROOT/old['step'].lstrip('/')),old['name'],old['function'],old['system'],old['color'],old['sources']+['water-pump-inlet-v3-topology'],old['unresolved']+pump_joint.inlet.GAPS,old['dimension_claims'])
        if refresh=='outlet-joint':
            for identifier in OUTLET_IDS:
                old=next(d for d in previous['definitions'] if d['id']==identifier)
                define(identifier,b.import_step(ROOT/old['step'].lstrip('/')),old['name'],old['function'],old['system'],old['color'],old['sources'],old['unresolved'],old['dimension_claims'])
        if refresh=='pump-joint':
            for identifier in pump_joint.IDS:
                if identifier in common_carrier.REMOVE_IDS: continue
                old=next(d for d in previous['definitions'] if d['id']==identifier)
                define(identifier,b.import_step(ROOT/old['step'].lstrip('/')),old['name'],old['function'],old['system'],old['color'],old['sources'],old['unresolved'],old['dimension_claims'])
        if refresh=='source-valves':
            if previous.get('valvetrain_model')=='source-sized-v2':
                raise ValueError('Source-sized refresh requires the accepted first-stage baseline')
            old_defs={d['id']:d for d in previous['definitions']}
            inputs={key:b.import_step(ROOT/old_defs[key]['step'].lstrip('/')) for key in ['cylinder-head','lifter-body','intake-valve','exhaust-valve']}
            for identifier,shape in source_valves.replacements(inputs,previous).items():
                old=old_defs.get(identifier,old_defs['valve-spring'])
                name=identifier.split('-')[0].title()+' valve spring' if identifier.endswith('-spring') else old['name']
                define(identifier,shape,name,old['function'],old['system'],old['color'],old['sources'],old['unresolved'],old['dimension_claims'],prepared=True)
        if refresh=='valvetrain':
            for identifier in VALVE_IDS:
                old=next(d for d in previous['definitions'] if d['id']==identifier)
                define(identifier,b.import_step(ROOT/old['step'].lstrip('/')),old['name'],old['function'],old['system'],old['color'],old['sources'],old['unresolved'],old['dimension_claims'])
        if refresh=='alternator-carrier':
            for identifier in ('alt-bracket-bolt-1','alt-bracket-bolt-2'):
                old = next(d for d in previous['definitions'] if d['id'] == identifier)
                define(identifier,b.import_step(ROOT/old['step'].lstrip('/')),old['name'],old['function'],old['system'],old['color'],old['sources'],alternator94.GAPS,old['dimension_claims'])
        if refresh=='pan-joint':
            for identifier in ('block','oil-pan'):
                old = next(d for d in previous['definitions'] if d['id'] == identifier)
                gaps = old['unresolved'] if identifier=='block' else pan_joint.GAPS + ['Sump stamping, capacity, installed pan identity and production dimensions remain provisional.']
                define(identifier,b.import_step(ROOT/old['step'].lstrip('/')),old['name'],old['function'],old['system'],old['color'],old['sources'],gaps,old['dimension_claims'])
        if refresh=='carrier-1994':
            for identifier in ('block','cylinder-head','ps-ac-support-bracket','tensioner-mounting-bolt'):
                old = next(d for d in previous['definitions'] if d['id'] == identifier)
                define(identifier,b.import_step(ROOT/old['step'].lstrip('/')),old['name'],old['function'],old['system'],old['color'],old['sources'],old['unresolved'],old['dimension_claims'])
        if refresh=='oil-filter':
            define_block_casting()
        if refresh=='ignition-leads':
            from ignition_leads import cap_interface, head_interface, SOURCES as lead_sources, GAPS as lead_gaps
            for identifier, adapter in [('distributor-cap',cap_interface),('cylinder-head',head_interface)]:
                old=next(d for d in previous['definitions'] if d['id']==identifier)
                shape=adapter(b.import_step(ROOT/old['step'].lstrip('/')))
                define(old['id'],shape,old['name'],old['function'],old['system'],old['color'],list(dict.fromkeys(old['sources']+lead_sources)),list(dict.fromkeys(old['unresolved']+lead_gaps)),old['dimension_claims'])
        if refresh=='cooling-connections':
            from cooling_connections import pump_housing_interface, SOURCES as cooling_sources, GAPS as cooling_gaps
            old=next(d for d in previous['definitions'] if d['id']=='water-pump-housing')
            shape=pump_housing_interface(b.import_step(ROOT/old['step'].lstrip('/')))
            define(old['id'],shape,old['name'],old['function'],old['system'],old['color'],list(dict.fromkeys(old['sources']+cooling_sources)),list(dict.fromkeys(old['unresolved']+cooling_gaps)),old['dimension_claims'])
        if refresh=='oil-drive':
            define_block_casting()
            old=next(d for d in previous['definitions'] if d['id']=='camshaft')
            shape=oil_drive_cam_interface(b.import_step(ROOT/old['step'].lstrip('/')))
            define(old['id'],shape,old['name'],old['function'],old['system'],old['color'],list(dict.fromkeys(old['sources']+OIL_DRIVE_SOURCES)),list(dict.fromkeys(old['unresolved']+OIL_DRIVE_GAPS)),old['dimension_claims'])
            build_distributor(distributor_api((define,add,group),include_root=False))
            build_oil_pump(pump_api(moving_pump_api((define,add,group,cx,spring))),include_root=False)
        if refresh=='accessory-drive':
            for identifier, adapter in [('block',lambda shape: thermactor_block_interface(accessory_block_interface(shape))),('cylinder-head',accessory_head_interface)]:
                old=next(d for d in previous['definitions'] if d['id']==identifier)
                shape=adapter(b.import_step(ROOT/old['step'].lstrip('/')))
                extra_sources=ACCESSORY_BRACKET_SOURCES+(THERMACTOR_SOURCES if identifier=='block' else [])
                extra_gaps=ACCESSORY_BRACKET_GAPS+(THERMACTOR_GAPS if identifier=='block' else [])
                define(old['id'],shape,old['name'],old['function'],old['system'],old['color'],list(dict.fromkeys(old['sources']+extra_sources)),list(dict.fromkeys(old['unresolved']+extra_gaps)),old['dimension_claims'])
            from fan_clutch import hub_interface, SOURCES as fan_sources, GAPS as fan_gaps
            old=next(d for d in previous['definitions'] if d['id']=='water-pump-drive-hub')
            shape=hub_interface(b.import_step(ROOT/old['step'].lstrip('/')))
            define(old['id'],shape,old['name'],old['function'],old['system'],old['color'],list(dict.fromkeys(old['sources']+fan_sources)),fan_gaps,old['dimension_claims'])
        if refresh=='regulator-vacuum':
            from regulator_vacuum import intake_interface, SOURCES as vacuum_sources, GAPS as vacuum_gaps
            old=next(d for d in previous['definitions'] if d['id']=='efi-upper-intake')
            shape=intake_interface(b.import_step(ROOT/old['step'].lstrip('/')))
            define(old['id'],shape,old['name'],old['function'],old['system'],old['color'],list(dict.fromkeys(old['sources']+vacuum_sources)),list(dict.fromkeys(old['unresolved']+vacuum_gaps)),old['dimension_claims'])
        if refresh=='damper':
            from damper_attachment import crank_interface
            old=next(d for d in previous['definitions'] if d['id']=='crankshaft')
            shape=crank_interface(b.import_step(ROOT/old['step'].lstrip('/')))
            define(old['id'],shape,old['name'],old['function'],old['system'],old['color'],old['sources'],old['unresolved']+['Front crank nose length and damper key/retaining bore are provisional attachment-study geometry.'],old['dimension_claims'])
        if refresh=='pilot-bearing':
            from pilot_bearing import crank_interface
            old=next(d for d in previous['definitions'] if d['id']=='crankshaft')
            shape=crank_interface(b.import_step(ROOT/old['step'].lstrip('/')))
            define(old['id'],shape,old['name'],old['function'],old['system'],old['color'],list(dict.fromkeys(old['sources']+['timken-pilot-dimensions'])),old['unresolved'],old['dimension_claims'])
        if refresh=='flywheel':
            from flywheel import crank_interface
            from pilot_bearing import crank_interface as pilot_interface
            old=next(d for d in previous['definitions'] if d['id']=='crankshaft')
            shape=crank_interface(b.import_step(ROOT/old['step'].lstrip('/')))
            if any(d['id']=='pilot-bearing-case' for d in previous['definitions']):shape=pilot_interface(shape)
            define(old['id'],shape,old['name'],old['function'],old['system'],old['color'],list(dict.fromkeys(old['sources']+['hicengine-ffm68'])),old['unresolved'],old['dimension_claims'])
        if refresh=='egr-tube':
            from egr_tube import manifold_interface
            old=next(d for d in previous['definitions'] if d['id']=='exhaust-rear')
            shape=manifold_interface(b.import_step(ROOT/old['step'].lstrip('/')))
            define(old['id'],shape,old['name'],old['function'],old['system'],old['color'],old['sources']+['dorman-598-105'],old['unresolved'],old['dimension_claims'])
        if refresh=='head-interface':define_head_casting()
        if refresh=='timing-cover':define_timing_cover()
        if refresh=='block-plugs':define_block_casting()
        if refresh=='egr':
            from egr import intake_interface
            old=next(d for d in previous['definitions'] if d['id']=='efi-upper-intake')
            shape=intake_interface(b.import_step(ROOT/old['step'].lstrip('/')))
            define(old['id'],shape,old['name'],old['function'],old['system'],old['color'],old['sources'],old['unresolved'],old['dimension_claims'])
        if refresh in ('head-interface','timing-cover','block-plugs'):
            refreshed={'head-interface':'cylinder-head','timing-cover':'timing-cover','block-plugs':'block'}[refresh]
            updated=next(d for d in defs if d['id']==refreshed)
            for o in occurrences:
                if o['definition']==refreshed:o['function']=updated['function']
    else:
        group('engine','Ford 4.9L engine',None)
        rotating();structure();top_end();closures()
        build_oil_pump(pump_api(moving_pump_api((define,add,group,cx,spring))))
    if refresh in (None,'peripherals','induction'):
        build_efi_intake((define,add,group,rounded_box,cx,CYLINDERS,MAINS,DECK))
    if refresh in (None,'peripherals','fuel','induction'):
        build_fuel_injection((define,add,group,cx,spring,CYLINDERS))
    if refresh in (None,'peripherals','throttle','induction'):
        build_throttle((define,add,group,rounded_box,cx))
        build_idle_air((define,add,group,cx))
        build_throttle_sensor((define,add,group))
    if refresh in (None,'peripherals','exhaust'):
        build_exhaust((define,add,group,CYLINDERS,DECK))
    if refresh in (None,'damper'):
        build_damper((define,add,group,cx))
        from damper_attachment import build as build_damper_attachment
        build_damper_attachment((define,add,group))
    if refresh in (None,'cooling'):
        build_water_pump((define,add,group,cx))
        build_coolant_outlet((define,add,group,cx))
        build_thermostat((define,add,group,cx,spring))
    if refresh in (None,'ignition','head-interface'):
        build_distributor(distributor_api((define,add,group)))
        build_ignition_coil((define,add,group))
        build_ignition_module((define,add,group))
        build_spark_plug((define,add,group,CYLINDERS))
    if refresh=='fuel-couplings':
        from fuel_couplings import build as build_fuel_couplings
        build_fuel_couplings((define,add,group))
    if refresh in (None,'ventilation'):
        from pcv import build as build_pcv
        build_pcv((define,add,group,spring))
    if refresh in (None,'oil-filter'):
        from oil_filter import build as build_oil_filter
        build_oil_filter(filter_api((define,add,group,spring)))
        build_filter_adapter((define,add,group))
    if refresh in (None,'oil-pressure'):
        from oil_pressure_switch import build as build_oil_pressure_switch
        build_oil_pressure_switch((define,add,group,spring))
    if refresh=='oil-pan':
        build_oil_pump(pump_api(moving_pump_api((define,add,group,cx,spring))),include_root=False)
        from oil_pan import build as build_oil_pan
        build_oil_pan((define,add,group,rounded_box,cx,LENGTH))
    if refresh in (None,'block-plugs'):
        build_expansion_plugs((define,add,group))
    if refresh in (None,'peripherals','induction','egr'):
        from egr import build as build_egr
        from evp_sensor import build as build_evp
        build_egr((define,add,group))
        build_evp((define,add,group))
    if refresh in (None,'peripherals','induction','egr','egr-tube'):
        from egr_tube import build as build_egr_tube
        build_egr_tube((define,add,group))
    if refresh in (None,'peripherals','induction','egr','evr'):
        from evr import build as build_evr
        build_evr((define,add,group))
    if refresh in (None,'peripherals','induction','egr','egr-hoses'):
        from egr_vacuum_hose import build as build_egr_hose
        build_egr_hose((define,add,group))
    if refresh in (None,'flywheel'):
        from flywheel import build as build_flywheel
        build_flywheel((define,add,group))
    if refresh in (None,'pilot-bearing'):
        from pilot_bearing import build as build_pilot_bearing
        build_pilot_bearing((define,add,group))
    if refresh in (None,'accessory-drive'):
        from tensioner_pulley import build as build_tensioner_pulley
        build_tensioner_pulley((define,add,group))
        from tensioner_arm import build as build_tensioner_arm
        build_tensioner_arm((define,add,group))
        from alternator import build as build_alternator
        build_alternator((define,add,group))
        from power_steering_pump import build as build_power_steering_pump
        build_power_steering_pump((define,add,group))
        from accessory_brackets import build as build_accessory_brackets
        build_accessory_brackets((define,add,group))
        from thermactor_pump import build as build_thermactor_pump
        build_thermactor_pump((define,add,group))
    if refresh in (None,'accessory-drive','ac-compressor'):
        from ac_compressor_manifold_passages import build as build_ac_compressor
        build_ac_compressor((define,add,group))
    if refresh in (None,'cooling','accessory-drive'):
        from water_pump_pulley import build as build_water_pump_pulley
        build_water_pump_pulley((define,add,group))
        from fan_clutch import build as build_fan_clutch
        build_fan_clutch((define,add,group))
    if refresh in (None,'peripherals','fuel','induction','regulator-vacuum'):
        from regulator_vacuum import build as build_regulator_vacuum
        build_regulator_vacuum((define,add,group))
    if refresh in (None,'ignition','head-interface','ignition-leads'):
        from ignition_leads import build as build_ignition_leads
        build_ignition_leads((define,add,group))
    if refresh in (None,'cooling','cooling-connections'):
        from cooling_connections import build as build_cooling_connections
        build_cooling_connections((define,add,group))
    if refresh in (None,'oil-drive','oil-pan'):
        build_oil_drive(moving_drive_api((define,add,group)))
    if refresh in (None,'starter'):
        from starter_motor import build as build_starter
        from starter_explanations import api as starter_metadata_api, solenoid_api as starter_solenoid_metadata_api, wiring_api as starter_wiring_metadata_api
        from starter_solenoid import api as starter_solenoid_api, build as build_starter_solenoid
        from starter_engagement import api as starter_engagement_api
        from starter_wiring import api as starter_wiring_api, build as build_starter_wiring
        from starter_wiring_fit_metadata import api as starter_wiring_fit_api
        from starter_motor_feed_metadata import api as starter_motor_feed_api, build as build_starter_motor_feed
        wired_api = starter_wiring_api(starter_wiring_fit_api(starter_motor_feed_api((define,add,group))))
        build_starter(starter_metadata_api(starter_solenoid_api(starter_engagement_api(wired_api))))
        build_starter_solenoid(starter_solenoid_metadata_api(wired_api))
        build_starter_wiring(starter_wiring_metadata_api(wired_api))
        build_starter_motor_feed(wired_api)
    if refresh in (None, 'intake-dowel', 'peripherals', 'induction'):
        intake_locating_dowel.build((define, add, group))
    if refresh in (None,'pump-joint','cooling'):
        pump_joint.pump.build_hardware((define,lambda id,definition,parent,position=(0,0,0),**kw:add(id,definition,parent,pos=position,**kw),group))
    if refresh in (None,'pan-joint','oil-pan'):
        pan_joint.build((define,add,group))
    if refresh in (None, 'carrier-1994','accessory-drive'):
        carrier94_integration.build_hardware((define,add,group))
    if not any(o['id']==common_carrier.NEW_ID for o in occurrences):
        define(common_carrier.NEW_ID,common_carrier.carrier(),'Alternator / Thermactor common carrier','One provisional cast support carries the alternator and Thermactor pump. Photographs establish a single carrier; hole mapping, contours and dimensions remain assumed.','accessory-drive','#96a4ad',common_carrier.SOURCES,common_carrier.GAPS)
        add(common_carrier.NEW_ID,common_carrier.NEW_ID,'accessory-drive',explode=(180,-90,0))
    source_ids=set(s for d in defs for s in d.get('sources',[]))
    if refresh in (None, 'manifold-eye', 'peripherals', 'exhaust'):
        manifold_lifting_eye.build((define, add, group))
        source_ids.update(manifold_lifting_eye.SOURCES)
    if refresh in (None, 'rear-mounts', 'peripherals', 'exhaust'):
        rear_mounts.build((define, add, group))
        source_ids.update(rear_mounts.SOURCES)
    import component_interface_integration as component_interfaces
    component_interfaces.install(define,add,group,defs,occurrences,assemblies)
    import throttle_linkage_integration as throttle_linkage
    throttle_linkage.install(define,add,defs,occurrences,shapes)
    import throttle_shield_integration as throttle_shield
    throttle_shield.install(define,add,defs,occurrences,shapes)
    import throttle_return_spring_integration as throttle_spring
    throttle_spring.install(define,add,defs,occurrences,shapes)
    import dipstick_integration
    dipstick_integration.install(define,add,group,defs,occurrences,assemblies,shapes)
    import intake_cap_coordination
    intake_cap_coordination.install(define,add,group,defs,occurrences,assemblies,shapes,
        {**BASE['mechanism'],'firing_order':[1,5,3,6,2,4],'cylinder_phases_deg':PHASES,'bore_pitch_mm':PITCH,'deck_height_mm':DECK})
    import iac_attachment_integration
    iac_attachment_integration.install(define,add,group,defs,occurrences,assemblies,shapes)
    import throttle_plate_fasteners_integration as throttle_plate_retention
    throttle_plate_retention.install(define,add,defs,occurrences,assemblies,shapes)
    import intake_exterior_integration
    intake_exterior_integration.install(define,defs,occurrences,assemblies,shapes,
        {**BASE['mechanism'],'firing_order':[1,5,3,6,2,4],'cylinder_phases_deg':PHASES,'bore_pitch_mm':PITCH,'deck_height_mm':DECK},OUT)
    import intake_runner_exterior_integration
    intake_runner_exterior_integration.install(define,defs,occurrences,assemblies,shapes,
        {**BASE['mechanism'],'firing_order':[1,5,3,6,2,4],'cylinder_phases_deg':PHASES,'bore_pitch_mm':PITCH,'deck_height_mm':DECK},OUT)
    import iac_closure_integration
    iac_closure_integration.install(define,add,group,defs,occurrences,assemblies,shapes)
    import iac_electrical_integration
    iac_electrical_integration.install(define,add,group,defs,occurrences,assemblies,shapes)
    import distributor_center_contact_integration
    distributor_center_contact_integration.install(define,add,group,defs,occurrences,assemblies,shapes)
    import throttle_cable_integration
    throttle_cable_integration.install(define,add,defs,occurrences,assemblies,shapes)
    import evr_mechanism_integration
    evr_mechanism_integration.install(define,add,group,defs,occurrences,assemblies,shapes)
    import throttle_stop_integration as throttle_stops
    throttle_stops.install(define,add,defs,occurrences,assemblies,shapes)
    source_ids.update(s for d in defs for s in d.get('sources',[]))
    learning=json.loads((ROOT/'inventory/engine/lubrication-learning.json').read_text())
    learning.update(json.loads((ROOT/'inventory/engine/intake-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/damper-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/cooling-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/water-pump-joint-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/ignition-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/ac-compressor-motion-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/ac-compressor-bearing-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/ac-compressor-manifold-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/ac-compressor-shaft-support-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/ac-compressor-manifold-passages-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/fuel-test-valve-motion-viewer-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/starter-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/starter-solenoid-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/starter-engagement-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/starter-wiring-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/starter-wiring-fit-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/starter-motor-feed-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/manifold-lifting-eye-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/intake-locating-dowel-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/exhaust-front-profile-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/exhaust-rear-entries-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/rear-manifold-mounts-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/carrier-1994-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/common-carrier-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/oil-pan-joint-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/component-interface-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/throttle-linkage-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/dipstick-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/dipstick-assembly-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/intake-cap-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/iac-attachment-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/throttle-plate-fasteners-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/iac-closure-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/iac-electrical-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/distributor-center-contact-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/throttle-cable-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/evr-mechanism-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/intake-runner-exterior-learning.json').read_text()))
    learning.update(json.loads((ROOT/'inventory/engine/throttle-stop-learning.json').read_text()))
    source_ids.update(s for entry in learning.values() for s in entry.get('sources',[]))
    sources={p['id']:{k:p[k] for k in ['title','url','path','sha256']} for p in INDEX['sources'] if p['id'] in source_ids}
    sources.update(json.loads((ROOT/'inventory/engine/dimensions.json').read_text())['sources'])
    sources.update(json.loads((ROOT/'inventory/engine/comparison-sources.json').read_text()))
    sources.update(json.loads((ROOT/'inventory/engine/starter-learning-sources.json').read_text()))
    for source in json.loads((ROOT/'inventory/engine/research-2026-09-23.json').read_text())['sources']:
        if source['id'] in source_ids:
            sources[source['id']]={k:source[k] for k in ('title','url','sha256')}
            sources[source['id']]['path']=source['local_path']
    sources.update(json.loads((ROOT/'inventory/engine/pump-joint-sources.json').read_text()))
    sources.update(json.loads((ROOT/'inventory/engine/carrier-1994-sources.json').read_text()))
    sources.update(json.loads((ROOT/'inventory/engine/common-carrier-sources.json').read_text()))
    sources.update(json.loads((ROOT/'inventory/engine/oil-pan-joint-sources.json').read_text()))
    sources.update(component_interfaces.sources())
    sources.update(throttle_linkage.sources())
    sources.update(throttle_spring.sources())
    sources.update(dipstick_integration.sources())
    sources.update(intake_cap_coordination.sources())
    sources.update(iac_attachment_integration.sources())
    sources.update(throttle_plate_retention.source())
    sources.update(intake_exterior_integration.sources())
    sources.update(iac_closure_integration.sources())
    sources.update(iac_electrical_integration.sources())
    sources.update(distributor_center_contact_integration.sources())
    sources.update(throttle_cable_integration.source())
    sources.update(evr_mechanism_integration.sources())
    sources.update(intake_runner_exterior_integration.sources())
    sources.update(throttle_stops.source())
    for identifier,capture in json.loads((ROOT/'inventory/engine/source-capture-overrides.json').read_text()).items():
        sources[identifier].update(capture)
    functions_by_definition = {definition['id']: definition['function'] for definition in defs}
    for occurrence in occurrences:
        if occurrence['definition'] in (exhaust_front_profile.ADAPTERS | exhaust_rear_entries.ADAPTERS | rear_mounts.ADAPTERS):
            occurrence['function'] = functions_by_definition[occurrence['definition']]
    for kind in ('intake','exhaust'):
        if not any(d['id']==kind+'-spring' for d in defs):
            define(kind+'-spring',source_definitions.v.spring(kind),kind.title()+' valve spring','Returns the valve toward its seat.','valvetrain',sources=['fsm-2e5473b2bf99'],prepared=True)
    defs[:]=[d for d in defs if d['id']!='valve-spring']
    annotated=source_valves.annotate_manifest({'occurrences':occurrences,'assemblies':assemblies})
    occurrences[:]=annotated['occurrences'];assemblies[:]=annotated['assemblies']
    next(o for o in occurrences if o['id']=='cam-bearing-1')['position_cad_mm'][0]=rear_cam.NEW_STATION
    for o in occurrences:
        if o['id'].startswith(('oil-pan-mounting-screw-','oil-pan-mounting-washer-')): o['explode_stages']=pan_hardware_stages(o['explode_cad_mm'])
    pump_joint.annotate(assemblies,occurrences)
    for a in assemblies:
        if a['id']=='coolant-outlet-assembly': a['position_cad_mm']=list(outlet_joint.POSITION)
        elif a['id']=='thermostat-assembly': a['position_cad_mm']=list(outlet_joint.THERMOSTAT_POSITION)
    for o in occurrences:
        if o['id']=='coolant-outlet-bolt-1': o['position_cad_mm']=[0,-27,29]
        elif o['id']=='coolant-outlet-bolt-2': o['position_cad_mm']=[0,32,-25]
        elif o['parent']=='engine-coolant-temperature-assembly': o['position_cad_mm']=list(outlet_joint.ect_position(o['id']))
    manifest=dict(schema_version=2,title='Ford 4.9L · engine atlas',status='In-progress reconstruction; not a complete or verified OEM engine',
        coordinate_system=BASE['coordinate_system'],definitions=defs,assemblies=assemblies,occurrences=occurrences,sources=sources,
        mechanism={**BASE['mechanism'],'firing_order':[1,5,3,6,2,4],'cylinder_phases_deg':PHASES,'bore_pitch_mm':PITCH,'deck_height_mm':DECK},
        omissions=[item['system']+': '+', '.join(item['items']) for item in json.loads((ROOT/'inventory/engine/completion-plan.json').read_text())['remaining']],
        coverage={'modeled_occurrences':len(occurrences),'modeled_definitions':len(defs),'verified_complete':False,
          'note':'Counts describe the current reconstruction, not a verified complete engine bill of materials. Some parts have unconfirmed applicability.'})
    manifest=source_evidence.annotate_evidence(manifest)
    manifest['valvetrain_model']='source-sized-v2'
    defs[:]=manifest['definitions']
    for d in defs:
        if d['id'] not in shapes:shapes[d['id']]=b.import_step(ROOT/d['step'].lstrip('/'))
        size=(support_bounds(shapes[d['id']]) if d['id']=='water-pump-seal-spring' or d['id'] in evr_mechanism_integration.CHANGED_IDS else shapes[d['id']].bounding_box()).size
        d['model_bounds_mm']=[size.X,size.Y,size.Z]
    for key in ('definitions','assemblies','occurrences'):
        ids=[item['id'] for item in manifest[key]]
        if len(ids)!=len(set(ids)):raise ValueError(f'Duplicate IDs in {key}; refusing to publish assembly')
    placed=placed_occurrences(manifest,shapes)
    b.export_step(b.Compound(children=placed),STEP/'full-assembly.step',unit=b.Unit.MM)
    verify_roundtrip(STEP/'full-assembly.step',placed)
    (ROOT/'inventory/engine/full-assembly.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(f'Wrote {len(defs)} definitions / {len(occurrences)} individual parts',flush=True)


if __name__=='__main__': main()
