"""Independent clearance-planning hypothesis, not a factory accessory installation."""
import build123d as cad
import accessory_belt as base
from accessory_layout_candidate import LIMITS

GROUPS={'alternator-assembly':'ALT','power-steering-pump-assembly':'PS','ac-compressor':'AC','thermactor-pump-assembly':'AP','tensioner-pulley-assembly':'TENS','tensioner-support-assembly':'TENS'}

def shifts(ac_up=110):
    return {'ALT':(0,-40),'PS':(-90,-60),'AC':(30,ac_up),'AP':(-50,60),'TENS':(-20,20)}

def stations(ac_up=110):
    values=shifts(ac_up);nodes=[dict(n) for n in base.PULLEYS]
    for n in nodes:
        if n['id'] in values:n['center']=tuple(a+c for a,c in zip(n['center'],values[n['id']]))
    return nodes

def matched_ac_up():
    lo,hi=114.,116.
    for _ in range(50):
        mid=(lo+hi)/2
        if base.solve(stations(mid),False)['length']>base.NOMINAL_EFFECTIVE_LENGTH:lo=mid
        else:hi=mid
    return (lo+hi)/2

def belt_shape():
    solution=base.solve(stations(matched_ac_up()))
    span=solution['spans'][0]
    direction=(0,*((span['end'][i]-span['start'][i])/span['length'] for i in range(2)))
    plane=cad.Plane(origin=base.world(span['start']),x_dir=(-1,0,0),z_dir=direction)
    return cad.sweep(plane*cad.Polygon(*base.belt_section_points(),align=None),base.path(solution),is_frenet=False)
