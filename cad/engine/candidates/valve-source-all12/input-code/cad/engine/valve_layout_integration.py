"""Composable all12-station hooks; root integration must regenerate and audit.

No file writes on import. Does not replace current solids with baseline snapshots.
Only the cylinder1 isolated candidate is geometrically checked by this subtask.
"""
from copy import deepcopy
import math
import build123d as b
from assembly_math import transforms
from valve_layout_candidate import (head_adapter,cam_adapter,rocker,fulcrum,pushrod,cup,
    revised_valve,solve,VALVE_Y,PIVOT_Y,PIVOT_Z,LIFTER_BODY_Z,PUSHROD_LENGTH)
FIRING_ORDER=[1,5,3,6,2,4]
LIFTER_OFFSETS={'body':0,'plunger-spring':-20.35,'check-retainer':-12.5,'check-spring':-11.7,
 'check-ball':-6.4,'plunger':6,'metering-disc':17.9,'pushrod-cup':20.9,'lock-ring':24}


def station_pairs(manifest):
    occurrences={o['id']:o for o in manifest['occurrences']}
    return [{'cylinder':c,'firing_deg':FIRING_ORDER.index(c)*120,
      'stations':[occurrences[f'c{c}-{kind}-valve']['position_cad_mm'][0] for kind in ['intake','exhaust']]}
      for c in range(1,7)]


def adapt_head_all(head,manifest):
    for pair in station_pairs(manifest):head=head_adapter(head,pair['stations'])
    return head


def adapt_cam_all(cam,manifest):
    for pair in station_pairs(manifest):cam=cam_adapter(cam,pair['stations'],pair['firing_deg'])
    return cam


def replacement_shapes(current_shapes,manifest):
    """Input current_shapes supplies at least head, cam, intake/exhaust valve."""
    return {'cylinder-head':adapt_head_all(current_shapes['cylinder-head'],manifest),
      'camshaft':adapt_cam_all(current_shapes['camshaft'],manifest),
      'rocker-arm':rocker(),'rocker-fulcrum':fulcrum(),'pushrod':pushrod(),
      'lifter-pushrod-cup':cup(),
      'intake-valve':revised_valve(current_shapes['intake-valve'],'intake'),
      'exhaust-valve':revised_valve(current_shapes['exhaust-valve'],'exhaust')}


def annotate_manifest(manifest):
    """Return corrected rest datums + occurrence motion roles; preserve identities.

    Caller must update definition meshes, dimensions, volumes, evidence and claims
    from regenerated shapes. This function alone never installs valid new geometry.
    Reapplying it does not move lifters another12mm.
    """
    result=deepcopy(manifest);occ={o['id']:o for o in result['occurrences']}
    groups={a['id']:a for a in result['assemblies']}
    for pair in station_pairs(result):
        c=pair['cylinder']
        for kind,x in zip(['intake','exhaust'],pair['stations']):
            tag=f'c{c}-{kind}'
            for suffix in ['valve','spring','seal','retainer','keeper-1','keeper-2']:
                o=occ[tag+'-'+suffix];o['position_cad_mm'][1]=VALVE_Y
                if suffix!='seal':o['valvetrain']={'cylinder':c,'kind':kind,'role':'spring' if suffix=='spring' else 'valve'}
            for suffix in ['rocker','fulcrum','rocker-bolt','guide']:
                o=occ[tag+'-'+suffix];o['position_cad_mm'][1]=PIVOT_Y
                if suffix in ['rocker','fulcrum']:o['position_cad_mm'][2]=PIVOT_Z
            occ[tag+'-rocker']['valvetrain']={'cylinder':c,'kind':kind,'role':'rocker'}
            occ[tag+'-rocker']['rotation_cad_deg']=[0,0,0]
            o=occ[tag+'-pushrod'];o['position_cad_mm']=[x,90,(140.9+367.5)/2]
            o['rotation_cad_deg']=[0,0,0];o['valvetrain']={'cylinder':c,'kind':kind,'role':'pushrod'}
            for suffix,z in LIFTER_OFFSETS.items():
                o=occ[tag+'-lifter-'+suffix];o['position_cad_mm'][2]=LIFTER_BODY_Z+z
                o['valvetrain']={'cylinder':c,'kind':kind,'role':'lifter'}
            for suffix in ['valve-assembly','actuation']:
                # Marker exposes engine controls when isolated; no group transform.
                groups[tag+'-'+suffix]['motion']={'type':'valvetrain','cylinder':c,'kind':kind}
    return result


def state(crank_degrees,cylinder,kind):
    if not math.isfinite(crank_degrees) or cylinder not in FIRING_ORDER or kind not in ['intake','exhaust']:
        raise ValueError('Finite angle, cylinder1–6 and intake/exhaust required')
    center=(468 if kind=='intake' else 246)+FIRING_ORDER.index(cylinder)*120
    offset=(crank_degrees-center+360)%720-360;t=offset/135
    q=96/135;k=-math.log(.05/.247)*(1-q*q)/(q*q)
    lift=0 if abs(t)>=1 else .247*25.4*math.exp(-k*t*t/(1-t*t))
    return {'lifter_lift':lift,**solve(lift)}


def apply_valve_transforms(manifest,poses,degrees=0):
    """Apply occurrence motion once, after base hierarchy transforms are resolved.

    Does not call assembly_math.transforms. The shared authority should lazily
    call this at its return boundary when any occurrence has valvetrain metadata.
    """
    for o in manifest['occurrences']:
        metadata=o.get('valvetrain')
        if not metadata:continue
        s=state(degrees,metadata['cylinder'],metadata['kind']);role=metadata['role']
        if role=='lifter':poses[o['id']]*=b.Pos(0,0,s['lifter_lift'])
        elif role=='valve':poses[o['id']]*=b.Pos(0,0,-s['valve_lift'])
        elif role=='rocker':poses[o['id']]*=b.Rot(math.degrees(s['angle']),0,0)
        elif role=='pushrod':
            top,bottom=s['top'],s['bottom'];rotation=-math.degrees(math.atan2(top[0]-bottom[0],top[1]-bottom[1]))
            poses[o['id']]*=b.Pos(0,(top[0]+bottom[0])/2-90,(top[1]+bottom[1])/2-(140.9+367.5)/2)*b.Rot(rotation,0,0)
        elif role!='spring':raise ValueError('Unknown valvetrain role')
    return poses



def moving_transforms(manifest,degrees=0,**other_motion):
    """Compatibility wrapper; refuses to silently return fixed valves pre-wiring."""
    import assembly_math
    if getattr(assembly_math,'VALVETRAIN_TRANSFORMS_VERSION',0)!=1:
        raise RuntimeError('Wire apply_valve_transforms into shared transforms and set VALVETRAIN_TRANSFORMS_VERSION=1 first')
    return assembly_math.transforms(manifest,degrees,**other_motion)


def spring_at_lift(valve_lift):
    """Actual CAD spring deformation for QC; never scale the wire thickness."""
    if not 0<=valve_lift<=10.03300001:raise ValueError('Lift outside candidate envelope')
    height=51-valve_lift;helix=b.Helix(height/6,height,13)
    return b.sweep(b.Plane(origin=helix@0,z_dir=helix%0)*b.Circle(2),path=helix)



def occurrence_shape(occurrence,definition_shape,degrees=0):
    """Local shape before shared transform; deform springs at cylinder cycle phase.

    Required in assembled STEP export and both static and motion CAD checkers.
    Individual definition STEP/GLB remains the uncompressed rest representation.
    The browser uses the equivalent constant-wire parametric helix mesh.
    """
    metadata=occurrence.get('valvetrain')
    if metadata and metadata['role']=='spring':
        s=state(degrees,metadata['cylinder'],metadata['kind'])
        return spring_at_lift(s['valve_lift'])
    return definition_shape
