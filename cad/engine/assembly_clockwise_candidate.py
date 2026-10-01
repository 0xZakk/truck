"""Opt-in motion adapter for a fully coordinated candidate manifest.

No shared legacy behavior is changed. Caller must stage compatible assets,
neutral poses and physical rest phases before selecting this revision.
"""
import copy,math
import build123d as b
from assembly_math import transforms as legacy_transforms
import cam_clockwise_candidate as cam
from crossed_oil_drive_endplay_candidate import angles,CROSSED_LEAD_RAD_PER_MM
REVISION='clockwise-inclined-v1'


def transforms(manifest,degrees=0,axial_mm=0,throttle_degrees=0,compressor_degrees=0,compressor_engaged=True):
    if manifest.get('motion_revision')!=REVISION:raise ValueError('Explicit coordinated motion revision required')
    ca,da=angles(degrees,axial_mm)
    m=copy.deepcopy(manifest);metadata={}
    for o in m['occurrences']:
        meta=o.pop('valvetrain',None)
        if meta:
            if meta.get('model')!=REVISION:raise ValueError('Mixed valve motion revisions')
            metadata[o['id']]=meta
    for a in m['assemblies']:
        motion=a.get('motion')
        if not motion:continue
        kind=motion['type']
        if kind in ('rod','piston'):
            event=motion.get('phase_deg',0);physical=motion.get('physical_rest_phase_deg')
            if physical is None or abs((physical+event+180)%360-180)>1e-7:raise ValueError('Missing or incompatible physical crank rest phase')
            motion['phase_deg']=physical
        elif kind=='cam':
            if any(abs(v)>1e-9 for v in a.get('rotation_cad_deg',[0,0,0])):raise ValueError('Candidate cam requires unrotated parent-local axis')
            a['position_cad_mm'][0]+=axial_mm
            a['rotation_cad_deg']=[ca-degrees/2,0,0]
        elif kind=='distributor':
            a['motion']={'type':'rotary','axis':'z','ratio':.5,'phase_deg':da+degrees/2}
        elif kind=='rotary':
            ratio=motion['ratio'];motion['ratio']=-ratio
            if a['id'].startswith('oil-pump-'):
                # Driven pair preserves declared signed ratio to distributor.
                motion['phase_deg']=motion.get('phase_deg',0)+(ratio/-.5)*(da+degrees/2)
        elif kind not in ('crank','valvetrain','throttle','fs10'):raise ValueError('Unknown candidate motion type')
    poses=legacy_transforms(m,-degrees,throttle_degrees,compressor_degrees,compressor_engaged)
    for key,meta in metadata.items():
        role=meta['role'];s=cam.state(degrees,meta['cylinder'],meta['kind'],axial_mm);r=cam.state([1,5,3,6,2,4].index(meta['cylinder'])*120,meta['cylinder'],meta['kind'])
        pose=poses[key];position=list(pose.position);rotation=list(pose.orientation)
        if role in ('rocker','pushrod') and abs(rotation[1])+abs(rotation[2])>1e-8:raise ValueError('Linkage requires documented engine-axis neutral frames')
        if role=='lifter':position[2]+=s['lifter_lift']
        elif role=='valve':position[2]-=s['valve_lift']
        elif role=='rocker':rotation[0]+=math.degrees(s['angle']-r['angle'])
        elif role=='pushrod':
            for axis,i in [(1,0),(2,1)]:position[axis]+=(s['top'][i]+s['bottom'][i]-r['top'][i]-r['bottom'][i])/2
            def rodangle(v):return -math.atan2(v['top'][0]-v['bottom'][0],v['top'][1]-v['bottom'][1])
            rotation[0]+=math.degrees(rodangle(s)-rodangle(r))
        elif role!='spring':raise ValueError('Unknown valve role')
        poses[key]=b.Pos(*position)*b.Rot(*rotation)
    return poses


def occurrence_shape(occurrence,shape,degrees=0,axial_mm=0):
    """Actual local spring geometry; never dispatch a new model through legacy law."""
    meta=occurrence.get('valvetrain')
    if not meta:return shape
    if meta.get('model')!=REVISION:raise ValueError('Mixed valve shape revision')
    if meta['role']!='spring':return shape
    angles(degrees,axial_mm)  # Validate the same supported travel contract.
    lift=max(0,cam.state(degrees,meta['cylinder'],meta['kind'],axial_mm)['valve_lift'])
    return _spring(meta['kind'],lift)


from functools import lru_cache
@lru_cache(maxsize=32)
def _spring(kind,lift):
    # Same bounded guard extension already checked in rocker-crest spring study.
    # The actual six-turn sweep/ground-end construction is unchanged.
    import ast,inspect
    import valve_spring_seating_candidate as source
    tree=ast.parse(inspect.getsource(source.spring));count=0
    maximum=max(cam.inclined.H['solve'](.247*25.4,k)['valve_lift'] for k in ['intake','exhaust'])
    for node in ast.walk(tree):
        if isinstance(node,ast.Constant) and node.value==10.0330001:
            node.value=maximum+1e-7;count+=1
    if count!=1:raise ValueError('Spring source guard changed; revalidate geometry authority')
    env=dict(source.spring.__globals__)
    exec(compile(tree,'candidate-spring-guard','exec'),env)
    return env['spring'](kind,lift)
