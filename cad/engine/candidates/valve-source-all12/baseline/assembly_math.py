"""CAD-space transforms shared by assembly export and geometric verification."""
import math
import build123d as b
VALVETRAIN_TRANSFORMS_VERSION=1


def compressor_state(motion, degrees, engaged=True):
    role=motion['role']
    if role not in ('pulley','shaft','piston','shoe') or not math.isfinite(degrees):
        raise ValueError('Finite compressor phase and a supported role are required')
    phase=degrees if engaged or role=='pulley' else 0
    if role in ('pulley','shaft'):
        return 0,phase
    cylinder_phase=math.radians(motion['cylinder_phase_deg'])
    amplitude=motion['stroke_amplitude_mm']
    if not math.isfinite(cylinder_phase) or not math.isfinite(amplitude) or amplitude<0:
        raise ValueError('Finite cylinder phase and nonnegative stroke amplitude are required')
    offset=amplitude*(math.cos(cylinder_phase)-math.cos(cylinder_phase-math.radians(phase)))
    return offset,phase if role=='shoe' else 0


def transforms(manifest, degrees=0, throttle_degrees=0, compressor_degrees=0, compressor_engaged=True):
    result={}
    radius=manifest['mechanism']['stroke_mm']/2
    length=manifest['mechanism']['rod_length_mm']
    for a in manifest['assemblies']:
        loc=b.Pos(*a.get('position_cad_mm',[0,0,0]))*b.Rot(*a.get('rotation_cad_deg',[0,0,0]))
        motion=a.get('motion')
        if motion:
            t=math.radians(degrees+motion.get('phase_deg',0))
            jy=-radius*math.sin(t);jz=radius*math.cos(t)
            if motion['type']=='throttle':loc*=b.Rot(0,throttle_degrees,0)
            if motion['type']=='crank':loc*=b.Rot(degrees,0,0)
            if motion['type']=='distributor':loc*=b.Rot(0,0,-degrees/2)
            if motion['type']=='cam':loc*=b.Rot(-degrees/2,0,0)
            if motion['type']=='fs10':
                offset,rotation=compressor_state(motion,compressor_degrees,compressor_engaged)
                loc*=b.Pos(offset,0,0)*b.Rot(rotation,0,0)
            if motion['type']=='rotary':
                axis=motion['axis']
                rotation=degrees*motion['ratio']+motion.get('phase_deg',0)
                if axis not in ('x','y','z') or not math.isfinite(rotation):
                    raise ValueError('Rotary motion requires a CAD axis and finite angle')
                loc*=b.Rot(*(rotation if component==axis else 0 for component in ('x','y','z')))
            if motion['type']=='piston':loc*=b.Pos(0,0,jz+math.sqrt(length**2-jy**2))
            if motion['type']=='rod':loc*=b.Pos(0,jy,jz)*b.Rot(math.degrees(math.asin(jy/length)),0,0)
        result[a['id']]=result.get(a['parent'],b.Location())*loc
    poses = {o['id']:result[o['parent']]*b.Pos(*o['position_cad_mm'])*b.Rot(*o.get('rotation_cad_deg',[0,0,0])) for o in manifest['occurrences']}

    if any(o.get('valvetrain') for o in manifest['occurrences']):
        from valve_layout_integration import apply_valve_transforms
        poses = apply_valve_transforms(manifest,poses,degrees)
    return poses
