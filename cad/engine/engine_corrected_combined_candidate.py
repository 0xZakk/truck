"""Selected actual candidate assembly, with explicit world/local asset frames."""
from pathlib import Path
import json,math,hashlib
import build123d as b
from assembly_math import transforms
import cam_clockwise_candidate as cam
import engine_clockwise_pose_candidate as motion
from timing_coupled_core_candidate import MOVING,STATIONARY
ROOT=Path(__file__).resolve().parents[2]
MANIFEST=ROOT/'inventory/engine/full-assembly.json'
FIXED_WORLD={'block':'timing-front-block-expanded-seat-v3-candidate/block.step','oil-pan':'timing-pan-expanded-seat-v2-candidate/pan.step','timing-cover':'front-seal-2692-candidate/cover.step'}

def load():
    m=json.loads(MANIFEST.read_text());defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']}
    selected={o['id'] for o in m['occurrences'] if o['parent'].startswith(('rod-group-','piston-group-'))}
    selected|=set(cam.linkage_frames(m))|set(FIXED_WORLD)|{'cylinder-head','head-gasket','valve-cover'}
    paths={key:ROOT/defs[occ[key]['definition']]['step'].lstrip('/') for key in selected}
    for key,p in FIXED_WORLD.items():paths[key]=ROOT/'cad/engine/generated'/p
    for key in ['cylinder-head','head-gasket']:paths[key]=ROOT/'cad/engine/generated/timing-valvetrain-inclined-candidate'/(key+'.step')
    for key in selected:
        if occ[key]['definition']=='rocker-arm':paths[key]=ROOT/'cad/engine/generated/timing-rocker-crest-candidate/rocker-arm.step'
    for key in MOVING|set(STATIONARY)|{'crank-timing-gear'}:paths[key]=ROOT/'cad/engine/generated/timing-coupled-core-candidate'/(key+'.step')
    paths['camshaft']=ROOT/'cad/engine/generated/cam-clockwise-candidate/camshaft.step'
    paths['crankshaft']=ROOT/'cad/engine/generated/crank-clockwise-candidate/crankshaft.step'
    cache={};shapes={}
    for key,p in paths.items():
        if p not in cache:cache[p]=b.import_step(p)
        shapes[key]=cache[p]
    evidence=json.loads((ROOT/'inventory/engine/crank-clockwise-candidate-validation.json').read_text())
    assert hashlib.sha256(paths['crankshaft'].read_bytes()).hexdigest()==evidence['candidate_step_sha256']
    m['_candidate_measured_rest_phases']=[math.degrees(math.atan2(-a['yz'][0],a['yz'][1])) for a in evidence['actual_axes']]
    return m,paths,shapes


def frames(m,q=0,axial=0):
    out=transforms(m,0);groups={a['id']:a for a in m['assemblies']};phases=m['mechanism']['cylinder_phases_deg'];radius=m['mechanism']['stroke_mm']/2;length=m['mechanism']['rod_length_mm']
    for o in m['occurrences']:
        parent=o['parent']
        if parent.startswith(('rod-group-','piston-group-')):
            g=groups[parent];i=int(parent.rsplit('-',1)[1]);kind='rod' if parent.startswith('rod') else 'piston'
            frame=motion.corrected_slider_frames(q,phases[i-1],radius,length,g['position_cad_mm'][0],measured_cad_rest_phase_degrees=m['_candidate_measured_rest_phases'][i-1])[kind]
            out[o['id']]=frame*b.Pos(*o['position_cad_mm'])*b.Rot(*o.get('rotation_cad_deg',[0,0,0]))
    out.update(cam.linkage_frames(m,q,axial))
    for key in MOVING:out[key]=motion.cam_frame(q,axial)
    for key in STATIONARY:out[key]=b.Location()
    out['crankshaft']=motion.crank_frame(q);out['crank-timing-gear']=motion.crank_frame(q)
    for key in FIXED_WORLD:out[key]=b.Location()
    return out


def posed(m,shapes,q=0,axial=0):
    pose=frames(m,q,axial)
    return {key:pose[key]*shape for key,shape in shapes.items()}
