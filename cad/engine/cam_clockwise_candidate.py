"""Isolated lobe phase revision; shaft and dimensional law remain unchanged."""
from pathlib import Path
from types import FunctionType,SimpleNamespace
import json,math
import build123d as b
from valve_motion_candidate import lobe_shape
from valve_layout_integration import station_pairs
import timing_valvetrain_inclined_candidate as inclined
import timing_valvetrain_adapter_candidate as adapter
from timing_axis_kinematic_candidate import cam_lift
from engine_clockwise_pose_candidate import AXIS,K,cam_frame
ROOT=Path(__file__).resolve().parents[2]
PROFILE=ROOT/'cad/engine/candidates/valve-motion/profile.json'
BASE=ROOT/'cad/engine/generated/timing-coupled-core-candidate/camshaft.step'


def stations(manifest):
    return [(p['cylinder'],kind,x,(center+p['firing_deg'])/2)
            for p in station_pairs(manifest)
            for kind,x,center in zip(['intake','exhaust'],p['stations'],[468,246])]


def local_mask(x,radius=26):
    return b.Pos(x,0,0)*b.Rot(0,90,0)*b.Cylinder(radius,15)


def revise_local(local_cam,manifest,phase_sign=-1):
    """Use source interpolated lobe law; +1 replay, -1 candidate, no reflection."""
    if phase_sign not in [-1,1]:raise ValueError('Explicit replay or corrected phase sign required')
    lobe=lobe_shape(json.loads(PROFILE.read_text())['profile'])
    cam=local_cam
    for _,_,x,phase in stations(manifest):
        cut=cam-local_mask(x)
        solids=list(cut) if isinstance(cut,b.ShapeList) else cut.solids()
        replacement=b.Pos(x,0,0)*b.Rot(phase_sign*phase,0,0)*lobe
        fused=replacement.fuse(*solids)
        cam=b.Compound(children=list(fused)) if isinstance(fused,b.ShapeList) else fused
        if len(cam.solids())!=1:raise ValueError(f'Cam disconnected at station {x}')
        cam=cam.solids()[0]
    return cam


def effective_event(q,axial_mm=0):return q+2*math.degrees(K*axial_mm)


def state(q,cylinder,kind,axial_mm=0):
    lift=cam_lift(effective_event(q,axial_mm),cylinder,kind)
    return {'lifter_lift':lift,**inclined.H['solve'](lift,kind)}


def tangent(q,cylinder,kind,axial_mm=0,x=0):
    t=(effective_event(q,axial_mm)-(468 if kind=='intake' else 246)-[1,5,3,6,2,4].index(cylinder)*120+360)%720-360
    u=t/135;lift=cam_lift(effective_event(q,axial_mm),cylinder,kind)
    threshold=96/135;k=-math.log(.05/.247)*(1-threshold**2)/threshold**2
    slope=0 if abs(u)>=1 else lift*(-2*k*u/(1-u*u)**2)/math.radians(67.5)
    return [x+axial_mm,AXIS[0]+slope,AXIS[1]+18+lift]


def linkage_frames(manifest,q=0,axial_mm=0):
    """Only corrected inclined linkage frames. Springs need separate compressed CAD.

    Never return inherited crank/cam poses from the legacy general helper.
    """
    env=dict(adapter.poses.__globals__)
    env.update(P=inclined.P,contract=SimpleNamespace(DELTA=inclined.contract.DELTA,state=state))
    poses=FunctionType(adapter.poses.__code__,env,'clockwise_linkage')(manifest,q,axial_mm)
    roles={'lifter','valve','rocker','pushrod'}
    allowed={o['id'] for o in manifest['occurrences'] if (o.get('valvetrain') or {}).get('role') in roles}
    allowed|={f'c{i}-{k}-{suffix}' for i,k,_,_ in stations(manifest) for suffix in ['fulcrum','guide','rocker-bolt']}
    return {key:poses[key] for key in allowed}
