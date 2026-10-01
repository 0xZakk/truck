"""Bounded estimated rocker/head adapter; frozen inputs, no installed writes."""
from copy import deepcopy
from types import FunctionType
import math
import build123d as b
import valve_source_layout as v
import timing_valvetrain_contract as contract
from assembly_math import transforms
P=contract.PROPOSED

def rocker():
    env=dict(v.rocker.__globals__)
    env.update({k:P[k] for k in ['PIVOT_Y','PUSHROD_Y','CUP_Z']})
    return FunctionType(v.rocker.__code__,env,'isolated_common_rocker')()

def stations(m):
    return [(i,k,next(o for o in m['occurrences'] if o['id']==f'c{i}-{k}-valve')['position_cad_mm'][0]) for i in range(1,7) for k in ['intake','exhaust']]

def allowed_regions(m):
    regions=[]
    for _,kind,x in stations(m):
        for y in [v.PIVOT_Y,P['PIVOT_Y']]:regions.append(b.Pos(x,y,(48.5+140)/2)*b.Cylinder(12.1,140-48.5))
        # Passage scope withheld: lower deck and cover ledge need coordination.
    return b.Compound(children=regions)

def head_adapter(old,m):
    head=old
    for _,kind,x in stations(m):
        top=P['rest'](kind,P['PIVOT_Y'])['pivot_z']-20-v.HEAD_Z
        head=head.cut(b.Pos(x,v.PIVOT_Y,(48.5+140)/2)*b.Cylinder(12.01,140-48.5))
        head=head.fuse(b.Pos(x,P['PIVOT_Y'],(48.5+top)/2)*b.Cylinder(12,top-48.5))
        head=head.cut(b.Pos(x,P['PIVOT_Y'],top-14.5)*b.Cylinder(4.6,43))
        # Preserve every existing passage and valve-cover support ledge.
    return head

def poses(m,theta=0,axial=0):
    rest=deepcopy(m)
    for o in rest['occurrences']:o.pop('valvetrain',None)
    out=transforms(rest,theta);occ={o['id']:o for o in m['occurrences']}
    for i,kind,x in stations(m):
        tag=f'c{i}-{kind}';s=contract.state(theta,i,kind,axial);zero=P['rest'](kind,P['PIVOT_Y'])
        for o in m['occurrences']:
            if not o['id'].startswith(tag+'-'):continue
            oid=o['id'];meta=o.get('valvetrain',{});role=meta.get('role')
            if role=='lifter':out[oid]=b.Pos(0,*contract.DELTA)*b.Pos(0,0,s['lifter_lift'])*out[oid]
            elif role=='valve':out[oid]=b.Pos(0,0,-s['valve_lift'])*out[oid]
            elif role=='rocker':out[oid]=b.Pos(x,P['PIVOT_Y'],zero['pivot_z'])*b.Rot(math.degrees(s['angle']),0,0)
            elif role=='pushrod':
                top,bottom=s['top'],s['bottom'];a=-math.degrees(math.atan2(top[0]-bottom[0],top[1]-bottom[1]))
                out[oid]=b.Pos(x,(top[0]+bottom[0])/2,(top[1]+bottom[1])/2)*b.Rot(a,0,0)
        for suffix,z in [('fulcrum',zero['pivot_z']),('rocker-bolt',zero['pivot_z']),('guide',zero['pivot_z']-18)]:out[tag+'-'+suffix]=b.Pos(x,P['PIVOT_Y'],z)
    return out
