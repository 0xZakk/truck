"""Reviewed educational dipstick interfaces; no factory-calibration promotion.

Call after the base block/cover builders. The adapter emits finished shapes with
prepared=True so the shared exporter does not machine the block a second time.
"""
from pathlib import Path
import hashlib,json
import build123d as b
from OCP.BRepTools import BRepTools
import dipstick_tube_candidate as tube
import dipstick_inserted_candidate as inserted

ROOT=Path(__file__).resolve().parents[2]
GROUP='engine-oil-dipstick-assembly'
RETAINER='pushrod-cover-dipstick-retainer-estimated'
BLADE='engine-oil-dipstick-blade'
HANDLE='engine-oil-dipstick-handle'
TUBE_IDS={'engine-oil-dipstick-tube','engine-oil-dipstick-tube-retaining-nut',
          'engine-oil-dipstick-tube-bracket','engine-oil-dipstick-tube-support-nut'}
CHANGED_IDS={'block',RETAINER,BLADE,HANDLE}|TUBE_IDS
# Blade/handle are upserts: absent in the current baseline, replaced if present.
NEW_IDS=CHANGED_IDS-{'block'}
SOURCE_IDS=['dipstick-specimen-e9te','dipstick-service-catalog','dipstick-tube-1995-adjacent-study']
GAPS=[
 'Educational interface estimates, not production dimensions or machining instructions. Exact1994 tube/indicator identity and upper support station remain unverified.',
 'Lower and upper mating threads are clearance envelopes. Thread engagement, sealing construction, bracket manufacturing joint, clamp load and retention strength are unvalidated.',
 'The pilot692.15mm approximate axial route comprises558.476126mm guide and133.673874mm free extension. Estimated waves add6.572804mm of material centerline; the material length is698.722804mm.',
 'Blade sections, waves, handle and stamp placement are inherited estimates. E9TE-6750-DA is specimen evidence, not owner identification; no ADD/FULL mark or oil calibration is reconstructed.',
 'The inserted blade is a rigid flexed display pose. Elastic insertion/withdrawal, twist, wave compression, handle retention force and service removal are not simulated.'
]
DESCRIPTIONS={
 'block':('Cylinder block','Holds the cylinders and crankshaft supports. An estimated rear-side dipstick boss and passage connect the guide to the crankcase without cutting the protected main/cylinder regions.'),
 RETAINER:('Dipstick support / cover retainer · estimated','Replaces only the rear cover bolt with a cover-clamping envelope and exposed support stud. Upper thread engagement and factory identity remain unverified.'),
 'engine-oil-dipstick-tube':('Engine oil dipstick guide · estimated','Routes the flexible indicator from the seated mouth through an estimated block receiver to the rear sump.'),
 'engine-oil-dipstick-tube-retaining-nut':('Dipstick lower retaining nut · estimated','Its shoulder bears on the tube shoulder at the proposed block receiver. Threads and sealing construction remain unverified.'),
 'engine-oil-dipstick-tube-bracket':('Dipstick tube support bracket · estimated','Connects the guide tube collar to the rear pushrod-cover retainer. Actual manufactured joint and bracket station remain unverified.'),
 'engine-oil-dipstick-tube-support-nut':('Dipstick support nut · estimated','Bears on the upper bracket beside the exposed cover-retainer stud. Thread surfaces and retention strength are not established.'),
 BLADE:('Engine oil dipstick blade · flexed study','A continuous specimen-informed strip follows the guide and extends into the sump. Approximate axial length is preserved; oil-level marks remain unknown.'),
 HANDLE:('Engine oil dipstick handle and stop · study','The original pilot handle and stop seat on the guide mouth. The stop supplies a modeled axial reference; friction retention and calibration remain unverified.')}


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def sources():
    pilot_path=ROOT/'reference/engine/pilot/dipstick/evidence.json'
    result={s['id']:{'title':s['kind']+' · '+s['id'],'url':s['url'],
             'path':'/'+str(pilot_path.relative_to(ROOT)),'sha256':digest(pilot_path)}
            for s in json.loads(pilot_path.read_text())['sources']}
    path=ROOT/'reference/engine/dipstick-tube-review.json'
    result[SOURCE_IDS[-1]]={'title':'Adjacent1995 Ford tube retention architecture;1994 applicability unresolved',
        'url':'https://www.scribd.com/document/720481789/1995-FORD-F-150-F-250-F-350-BRONCO-F-SUPER-DUTY-POWERTRAIN-DRIVETRAIN',
        'path':'/'+str(path.relative_to(ROOT)),'sha256':digest(path)}
    return result


def static_frame(parent,assemblies):
    rows={a['id']:a for a in assemblies};frame=b.Location();chain=[]
    while parent in rows:
        row=rows[parent]
        if row.get('motion'):raise ValueError('Dipstick world-coordinate geometry requires static ancestry')
        chain.append(row);parent=row['parent']
    for row in reversed(chain):
        frame*=b.Pos(*row.get('position_cad_mm',[0,0,0]))*b.Rot(*row.get('rotation_cad_deg',[0,0,0]))
    return frame


def install(define,add,group,definitions,occurrences,assemblies,shapes):
    previous={d['id']:d for d in definitions}
    occs={o['id']:o for o in occurrences}
    if 'pushrod-cover-bolt-1' not in occs:raise ValueError('Expected rear cover occurrence is missing')
    def load(ident):
        return shapes[ident] if ident in shapes else b.import_step(ROOT/previous[ident]['step'].lstrip('/'))
    anchor=occs['pushrod-cover-bolt-1']
    anchor_frame=static_frame(anchor['parent'],assemblies)*b.Pos(*anchor['position_cad_mm'])*b.Rot(*anchor.get('rotation_cad_deg',[0,0,0]))
    expected=b.Pos(-285,113.592,185)*b.Rot(-90,0,0)
    if max((b.Vertex(*p).moved(anchor_frame).center()-b.Vertex(*p).moved(expected).center()).length for p in [(0,0,0),(1,0,0),(0,0,1)])>1e-6:
        raise ValueError('Cover anchor differs from the reviewed candidate datum')
    # All emitted blade/tube definitions are in world coordinates. Put them under
    # a verified identity parent, never inherit a rejected pilot transform.
    parent_frame=static_frame('lubrication',assemblies)
    if max((b.Vertex(*p).moved(parent_frame).center()-b.Vector(*p)).length for p in [(0,0,0),(1,0,0),(0,1,0),(0,0,1)])>1e-6:
        raise ValueError('Lubrication frame is not identity; world definitions need a reviewed local-frame conversion')
    parts,_=tube.candidate(load('block'),anchor_frame*load('pushrod-cover-bolt'))
    parts['block']=parts.pop('block-candidate')
    parts[RETAINER]=anchor_frame.inverse()*parts.pop('pushrod-cover-retainer-candidate')
    blade_parts,_=inserted.parts()
    parts[BLADE]=blade_parts['engine-oil-dipstick-blade-inserted']
    parts[HANDLE]=blade_parts['engine-oil-dipstick-handle-inserted']
    old_blades={}
    for ident in [BLADE,HANDLE]:
        found=[o for o in occurrences if o['definition']==ident]
        if len(found)>1:raise ValueError('Multiple dipstick material occurrences require explicit review')
        old_blades[ident]=found[0].copy() if found else None
    definitions[:]=[d for d in definitions if d['id'] not in CHANGED_IDS]
    owned_occ=TUBE_IDS|{BLADE,HANDLE}|{o['id'] for o in old_blades.values() if o}
    occurrences[:]=[o for o in occurrences if o['id'] not in owned_occ]
    assemblies[:]=[a for a in assemblies if a['id']!=GROUP]
    group(GROUP,'Engine oil dipstick and guide · educational study','lubrication')
    for ident,shape in parts.items():
        old=previous.get(ident,{})
        gaps=(old.get('unresolved',[]) if ident=='block' else [])+GAPS
        # Pre-mesh at stricter tolerances; the shared exporter then reuses this
        # triangulation, avoiding OCC's coarse-angular null-face failure.
        if ident=='engine-oil-dipstick-tube':
            BRepTools.Clean_s(shape.wrapped);shape.tessellate(.1,.1)
        name,function=DESCRIPTIONS[ident]
        define(ident,shape,name,function,old.get('system','lubrication'),
               old.get('color','#dfb61e' if ident==HANDLE else '#a5acb4'),
               list(dict.fromkeys(old.get('sources',[])+SOURCE_IDS)),list(dict.fromkeys(gaps)),
               old.get('dimension_claims',[]),prepared=True)
        if ident in TUBE_IDS:add(ident,ident,GROUP,explode=(0,150,80))
        elif ident in (BLADE,HANDLE):
            old_occ=old_blades[ident]
            if old_occ:
                old_occ.update(parent=GROUP,position_cad_mm=[0,0,0],rotation_cad_deg=[0,0,0],
                               name=name,function=function,explode_cad_mm=[0,0,180 if ident==BLADE else 260])
                old_occ.pop('valvetrain',None);old_occ.pop('motion',None)
                occurrences.append(old_occ)
            else:add(ident,ident,GROUP,explode=(0,0,180 if ident==BLADE else 260))
    anchor['definition']=RETAINER
    anchor['name'],anchor['function']=DESCRIPTIONS[RETAINER]
    # Object reference survives the bounded occurrence-list filtering above.
    return {'changed_definitions':sorted(CHANGED_IDS),'changed_occurrences':sorted(owned_occ|{'pushrod-cover-bolt-1'}),
            'new_material_occurrences':[i for i,o in old_blades.items() if o is None]}
