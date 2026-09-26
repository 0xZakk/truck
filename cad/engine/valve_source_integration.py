"""All12 occurrence hooks for source-sized candidate, not live integration."""
from copy import deepcopy
import math
import build123d as b
import valve_source_layout as v
from valve_layout_integration import station_pairs,LIFTER_OFFSETS,state as first_state


def state(degrees,cylinder,kind):
    lift=first_state(degrees,cylinder,kind)['lifter_lift']
    return {'lifter_lift':lift,**v.solve(lift,kind)}


def annotate_manifest(manifest):
    result=deepcopy(manifest);occ={o['id']:o for o in result['occurrences']}
    groups={a['id']:a for a in result['assemblies']}
    for pair in station_pairs(result):
      c=pair['cylinder']
      for kind,x in zip(['intake','exhaust'],pair['stations']):
        tag=f'c{c}-{kind}';s=v.solve(0,kind);delta=v.LENGTHS[kind]-109
        for suffix in ['valve','retainer','keeper-1','keeper-2']:
            o=occ[tag+'-'+suffix];o['position_cad_mm']=[x,v.VALVE_Y,261 if suffix=='valve' else 365+delta]
            o['valvetrain']={'cylinder':c,'kind':kind,'role':'valve','model':'source-sized-v2'}
        o=occ[tag+'-spring'];o['definition']=kind+'-spring';o['position_cad_mm']=[x,v.VALVE_Y,363+delta-v.INSTALLED[kind]]
        o['valvetrain']={'cylinder':c,'kind':kind,'role':'spring','model':'source-sized-v2'}
        occ[tag+'-seal']['position_cad_mm']=[x,v.VALVE_Y,363+delta-v.INSTALLED[kind]+4.5]
        for suffix,z in [('rocker',s['pivot_z']),('fulcrum',s['pivot_z']),('rocker-bolt',s['pivot_z']),('guide',s['pivot_z']-18)]:
            occ[tag+'-'+suffix]['position_cad_mm']=[x,v.PIVOT_Y,z]
        o=occ[tag+'-rocker'];o['rotation_cad_deg']=[math.degrees(s['angle']),0,0]
        o['valvetrain']={'cylinder':c,'kind':kind,'role':'rocker','model':'source-sized-v2'}
        top,bottom=s['top'],s['bottom'];o=occ[tag+'-pushrod']
        o['position_cad_mm']=[x,(top[0]+bottom[0])/2,(top[1]+bottom[1])/2]
        o['rotation_cad_deg']=[-math.degrees(math.atan2(top[0]-bottom[0],top[1]-bottom[1])),0,0]
        o['valvetrain']={'cylinder':c,'kind':kind,'role':'pushrod','model':'source-sized-v2'}
        for suffix,z in LIFTER_OFFSETS.items():
            o=occ[tag+'-lifter-'+suffix];o['position_cad_mm']=[x,90,v.LIFTER_DATUM_Z+z]
            o['valvetrain']={'cylinder':c,'kind':kind,'role':'lifter','model':'source-sized-v2'}
        for suffix in ['valve-assembly','actuation']:groups[tag+'-'+suffix]['motion']={'type':'valvetrain','cylinder':c,'kind':kind,'model':'source-sized-v2'}
    result['valvetrain_model']='source-sized-v2'
    return result


def apply_valve_transforms(manifest,poses,degrees=0):
    """No recursive transforms call. Source-sized metadata only; apply exactly once."""
    for o in manifest['occurrences']:
        m=o.get('valvetrain')
        if not m or m.get('model')!='source-sized-v2':continue
        s=state(degrees,m['cylinder'],m['kind']);r=v.solve(0,m['kind']);role=m['role']
        if role=='lifter':poses[o['id']]*=b.Pos(0,0,s['lifter_lift'])
        elif role=='valve':poses[o['id']]*=b.Pos(0,0,-s['valve_lift'])
        elif role=='rocker':poses[o['id']]*=b.Rot(math.degrees(s['angle']-r['angle']),0,0)
        elif role=='pushrod':
            dy=(s['top'][0]+s['bottom'][0]-r['top'][0]-r['bottom'][0])/2
            dz=(s['top'][1]+s['bottom'][1]-r['top'][1]-r['bottom'][1])/2
            def angle(t):return -math.atan2(t['top'][0]-t['bottom'][0],t['top'][1]-t['bottom'][1])
            a0=angle(r);local_y=dy*math.cos(a0)+dz*math.sin(a0);local_z=-dy*math.sin(a0)+dz*math.cos(a0)
            poses[o['id']]*=b.Pos(0,local_y,local_z)*b.Rot(math.degrees(angle(s)-a0),0,0)
        elif role!='spring':raise ValueError(role)
    return poses


def occurrence_shape(o,definition_shape,degrees=0):
    m=o.get('valvetrain')
    if m and m.get('model')=='source-sized-v2' and m['role']=='spring':return v.spring(m['kind'],state(degrees,m['cylinder'],m['kind'])['valve_lift'])
    return definition_shape


def candidate_transforms(manifest,degrees=0,base_transforms=None):
    """Isolated testing only: remove motion metadata before shared base authority.

    Live integration must dispatch apply_valve_transforms once inside its shared
    transform authority, not wrap an already-applied first-stage motion result.
    """
    from assembly_math import transforms
    rest_manifest=deepcopy(manifest)
    for o in rest_manifest['occurrences']:o.pop('valvetrain',None)
    authority=base_transforms or transforms
    return apply_valve_transforms(manifest,authority(rest_manifest,degrees),degrees)


def replacements(current_shapes,manifest):
    head=current_shapes['cylinder-head']
    for pair in station_pairs(manifest):head=v.head_adapter(head,pair['stations'])
    return {'cylinder-head':head,'rocker-arm':v.rocker(),'pushrod':v.pushrod(),
      'lifter-body':v.lifter_body(current_shapes['lifter-body']),'lifter-pushrod-cup':v.lifter_cup(),
      'valve-cover':v.cover(),'valve-seal':v.seal(),
      **{kind+'-valve':v.valve(current_shapes[kind+'-valve'],kind) for kind in v.LENGTHS},
      **{kind+'-spring':v.spring(kind) for kind in v.LENGTHS}}
