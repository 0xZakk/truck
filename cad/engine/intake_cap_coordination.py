"""Isolated coordinated intake/cap adapter; integration owner controls promotion.

Preserves occurrence identities and uses explicit inverse world-to-local frames.
The added cap seal is a separate illustrative material part, not an OEM claim.
"""
from pathlib import Path
import copy,hashlib,json
import build123d as b
from assembly_math import transforms
import upper_intake_clearance_candidate as study
import intake_egr_routes_candidate as routes
ROOT=Path(__file__).resolve().parents[2]
SEAL='oil-filler-cap-seal'
CHANGED_IDS={'efi-upper-intake','valve-cover','oil-filler-cap',SEAL,
             'egr-exhaust-tube','egr-tube-heat-sleeve','egr-tube-valve-nut','egr-control-vacuum-hose'}
SOURCE='upper-intake-topology-study'
GAPS=[
 'Educational source-compared interface study, not factory dimensions. Plenum size and cap/throttle/EGR stations are inferred.',
 'Cap and matching neck use assumed4.5mm pitch; production thread dimensions and formed-versus-insert neck construction remain unknown.',
 'Nominal seal and hose contact do not establish compression, leak tightness, retention strength or production tolerance.',
 'Casting ribs, bosses and detailed wall distribution remain incomplete.']

def sources():
    p=ROOT/'reference/engine/upper-intake-topology-review.json'
    return {SOURCE:{'title':'Ford intake topology and coordinated estimated interface study',
                   'path':'/'+str(p.relative_to(ROOT)),
                   'url':'https://www.supermotors.net/getfile/1174826/fullsize/tsb870816intakeinstall49l.jpg',
                   'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}}

def shifted_position(record,delta,parent_frame):
    """Translate in world axes while preserving the original local rotation."""
    origin=b.Vertex(*record.get('position_cad_mm',[0,0,0])).moved(parent_frame).center()
    local=b.Vertex(*(origin+b.Vector(*delta))).moved(parent_frame.inverse()).center()
    record['position_cad_mm']=list(local)

def install(define,add,group,definitions,occurrences,assemblies,shapes,mechanism):
    contract_path=ROOT/'reference/engine/intake-cap-frame-contract.json'
    contract=json.loads(contract_path.read_text())
    for path,digest in {**contract['artifacts_sha256'],**contract['geometry_sources_sha256']}.items():
        if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=digest:raise ValueError('Coordination contract dependency changed: '+path)
    contract_digest=hashlib.sha256(contract_path.read_bytes()).hexdigest()
    before={'mechanism':copy.deepcopy(mechanism),'definitions':copy.deepcopy(definitions),'occurrences':copy.deepcopy(occurrences),'assemblies':copy.deepcopy(assemblies)}
    poses=transforms(before);olddefs={d['id']:d for d in definitions};oldocc={o['id']:o for o in before['occurrences']}
    rows={o['id']:o for o in occurrences};parents={a['id']:a for a in assemblies}
    for ident,expected in contract['ancestor_frames'].items():
        row=parents[ident]
        actual={k:row.get(k,[0,0,0] if k in ('position_cad_mm','rotation_cad_deg') else None) for k in expected}
        if actual!=expected:raise ValueError('Ancestor frame changed: '+ident)
    def frame(parent):
        chain=[]
        while parent in parents:
            a=parents[parent]
            if a.get('motion'):raise ValueError('Frame translation requires static ancestry')
            chain.append(a);parent=a.get('parent')
        result=b.Location()
        for a in reversed(chain):result*=b.Pos(*a.get('position_cad_mm',[0,0,0]))*b.Rot(*a.get('rotation_cad_deg',[0,0,0]))
        return result
    def load(ident):return shapes.get(ident) or b.import_step(ROOT/olddefs[ident]['step'].lstrip('/'))
    # Coordinates alone never establish whether the fill opening was adapted.
    # Compare exported world solids against two immutable reviewed states.
    expected_cover=contract['cover_occurrence']
    for key in ('parent','position_cad_mm','rotation_cad_deg'):
        if oldocc['valve-cover'].get(key,[0,0,0])!=expected_cover.get(key,[0,0,0]):raise ValueError('Unexpected cover frame: '+key)
    cover=study.bake(poses['valve-cover']*load('valve-cover'),'adapter-input-cover')
    baseline=poses['valve-cover']*b.import_step(ROOT/'cad/engine/generated/intake-cap-contract/legacy-valve-cover.step')
    target=b.import_step(ROOT/'cad/engine/generated/intake-cap-contract/coordinated-valve-cover.step')
    def difference(a,z):return study.volume(a-z)+study.volume(z-a)
    target_error=difference(cover,target)
    if target_error<.1:
        cover_state='coordinated';newcover=cover
        from oil_fill_neck_candidate import cap_at
        cap,seal=cap_at(0);cap=b.Pos(*study.CAP_DELTA)*cap;seal=b.Pos(*study.CAP_DELTA)*seal
    elif difference(cover,baseline)<.1:
        cover_state='reviewed legacy';newcover,neck,cap,seal=study.coordinated_cap_cover(cover)
    else:raise ValueError('Cover does not match reviewed legacy or coordinated geometry; refusing to cut/fuse it')
    manifold,_=study.candidate()
    world={'efi-upper-intake':manifold,'valve-cover':newcover,'oil-filler-cap':cap,SEAL:seal,**routes.parts()}
    changed_assemblies=[];changed_occurrences=[]
    frame_states={}
    for ident,spec in contract['frames'].items():
        row=parents[ident] if spec['kind']=='assemblies' else rows[ident]
        if row.get('parent')!=spec['parent'] or row.get('rotation_cad_deg',[0,0,0])!=spec['rotation_cad_deg']:
            raise ValueError('Unknown coordinated frame orientation/parent: '+ident)
        current=row.get('position_cad_mm',[0,0,0])
        if current not in (spec['baseline_position_cad_mm'],spec['target_position_cad_mm']):
            raise ValueError('Unknown coordinated frame position: '+ident)
        frame_states[ident]='target' if current==spec['target_position_cad_mm'] else 'baseline'
        row['position_cad_mm']=list(spec['target_position_cad_mm'])
        row['intake_cap_coordination_contract']=contract_digest
        (changed_assemblies if spec['kind']=='assemblies' else changed_occurrences).append(ident)
    anchor=rows['oil-filler-cap'];added=SEAL not in rows
    newseal=rows.get(SEAL,copy.deepcopy(anchor))
    newseal.update(id=SEAL,definition=SEAL,parent=anchor['parent'],position_cad_mm=list(anchor['position_cad_mm']),rotation_cad_deg=list(anchor.get('rotation_cad_deg',[0,0,0])),name='Oil filler cap seal · estimated',function='Illustrates an annular sealing land between the screw cap and cover neck; compression and production section remain unknown.',explode_cad_mm=[0,0,490])
    if added:occurrences.append(newseal)
    rows[SEAL]=newseal;changed_occurrences.append(SEAL)
    newposes=transforms({'mechanism':mechanism,'occurrences':occurrences,'assemblies':assemblies,'definitions':definitions})
    definitions[:]=[d for d in definitions if d['id'] not in CHANGED_IDS]
    for ident,shape in world.items():
        old=olddefs.get(ident,{})
        # Bake before localization, then let shared exporter verify local STEP.
        shape=study.bake(shape,'adapter-world-'+ident)
        local=newposes[ident].inverse()*shape
        name=old.get('name',newseal['name']);function=old.get('function',newseal['function'])
        if ident=='efi-upper-intake':function='A compact estimated plenum distributes air through six curved runners; direct twin-port throttle flange and two-ended runner spread follow Ford comparison images.'
        if ident=='valve-cover':function='Contains rocker oil with one relocated fill opening and a continuous illustrative threaded neck. The previous provisional opening is regenerated closed.'
        define(ident,local,name,function,old.get('system','closures'),old.get('color','#48545f'),
               list(dict.fromkeys(old.get('sources',[])+[SOURCE])),list(dict.fromkeys(old.get('unresolved',[])+GAPS)),old.get('dimension_claims',[]),prepared=True)
        next(d for d in definitions if d['id']==ident)['intake_cap_coordination_contract']=contract_digest
        rows[ident]['name']=name;rows[ident]['function']=function
        if ident not in changed_occurrences:changed_occurrences.append(ident)
    return {'changed_definitions':sorted(CHANGED_IDS),'changed_occurrences':sorted(changed_occurrences),
            'changed_assemblies':changed_assemblies,'new_occurrences':[SEAL] if added else [],'cover_input_state':cover_state,'frame_input_states':frame_states,'frame_contract_sha256':contract_digest,
            'frame_policy':'Existing definition/occurrence frames retained; world candidate converted through inverse final occurrence pose. Three rigid assembly frames and cap/EGR gasket/bolts normalize to explicit absolute target coordinates; reviewed legacy and target states are idempotent.'}
