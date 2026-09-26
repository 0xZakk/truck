"""Uninstalled layout experiment; nominal-length constraint is not factory evidence.

Keep the lower accessories fixed to avoid the previously rejected compressor
movement into the timing cover. Move the two upper accessory bodies and tensioner
as a bounded hypothesis. Existing brackets MUST NOT be silently reused.
"""
import math
import build123d as cad
import accessory_belt as base

LIMITS = [
    'Outside pulley radius is only a diagnostic proxy for effective radius; matching 2491 mm does not verify Gates K060980 installation.',
    'Upper-accessory relocation is a numerical hypothesis, not a measured Ford station. No production geometry is changed by this module.',
    'Original support brackets, engine feet and belt-side hose/pipe connections cannot be retained after relocation. New supports require independent design and validation.',
    'Tensioner arm is a provisional 75 mm construction study; unrestricted rotation is diagnostic only and is not allowed physical travel.',
    'No spring force, wrap traction, belt elasticity, accessory load or operating clearance has been verified.',
]


def stations(shift=0, arm_degrees=0):
    nodes = [dict(n) for n in base.PULLEYS]
    for n in nodes:
        y,z=n['center']
        if n['id']=='ALT': n['center']=(y+shift,z-shift)
        elif n['id']=='PS': n['center']=(y-shift,z-shift)
        elif n['id']=='TENS':
            angle=math.radians(arm_degrees)
            n['center']=(-75+75*math.cos(angle),435-shift+75*math.sin(angle))
    return nodes


def nominal_shift():
    lo,hi=0.,100.
    for _ in range(60):
        mid=(lo+hi)/2
        if base.solve(stations(mid),cord_path=False)['length']>base.NOMINAL_EFFECTIVE_LENGTH:lo=mid
        else:hi=mid
    return (lo+hi)/2


def belt_shape(shift,arm_degrees=0):
    solution=base.solve(stations(shift,arm_degrees))
    span=solution['spans'][0]
    direction=(0,*( (span['end'][i]-span['start'][i])/span['length'] for i in range(2)))
    plane=cad.Plane(origin=base.world(span['start']),x_dir=(-1,0,0),z_dir=direction)
    section=plane*cad.Polygon(*base.belt_section_points(),align=None)
    return cad.sweep(section,base.path(solution),is_frenet=False)


def displacement(assembly_id,shift):
    if assembly_id=='alternator-assembly': return (0,shift,-shift)
    if assembly_id=='power-steering-pump-assembly':return (0,-shift,-shift)
    if assembly_id in ('tensioner-pulley-assembly','tensioner-support-assembly'):return (0,0,-shift)
    return None


def diagnosis():
    baseline=base.solve(cord_path=False)
    relaxed=base.solve([n for n in base.PULLEYS if n['id']!='TENS'],cord_path=False)
    samples=[]
    for degrees in range(3600):
        s=base.solve(stations(0,degrees/10),cord_path=False)
        samples.append(s['length'])
    sensitivity=[]
    for index,node in enumerate(base.PULLEYS):
        result={'pulley':node['id']}
        for axis in range(2):
            lengths=[]
            for sign in (-1,1):
                nodes=[dict(n) for n in base.PULLEYS]
                center=list(nodes[index]['center']);center[axis]+=sign*.01
                nodes[index]['center']=tuple(center)
                lengths.append(base.solve(nodes,False)['length'])
            result['d_length_d_'+('y','z')[axis]]=(lengths[1]-lengths[0])/.02
        sensitivity.append(result)
    return {
        'baseline_outside_radius_length_mm':baseline['length'],
        'catalog_effective_length_mm':base.NOMINAL_EFFECTIVE_LENGTH,
        'tensioner_removed_relaxed_route_length_mm':relaxed['length'],
        'relaxed_route_residual_mm':relaxed['length']-base.NOMINAL_EFFECTIVE_LENGTH,
        'full_circle_3600_sample_minimum_mm':min(samples),
        'full_circle_3600_sample_maximum_mm':max(samples),
        'tensioner_removed_is_diagnostic_not_proposed_routing':True,
        'center_sensitivity':sensitivity,
        'candidate_shift_mm':nominal_shift(),
        'limits':LIMITS,
    }
