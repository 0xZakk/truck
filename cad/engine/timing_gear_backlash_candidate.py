"""Isolated tooth-thinning study; imported generator globals remain unchanged."""
import math
import types
import build123d as b
import timing_gear_pair_candidate as base
import timing_gear_pair_refinement as refinement
import timing_thrust_land_candidate as land
PAIR_PLAY_MM=.0762
EACH_THINNING_MM=PAIR_PLAY_MM/2
PARAMS={**base.PARAMS,'backlash_mm':EACH_THINNING_MM}
CAM_K_RAD_PER_MM=-math.tan(math.radians(PARAMS['helix_angle_deg']))/(PARAMS['transverse_module_mm']*PARAMS['cam_teeth']/2)
GEAR_X=385.259375

def parts():
    original=dict(base.PARAMS)
    env={**base.gear.__globals__,'PARAMS':dict(PARAMS)}
    env['gear']=types.FunctionType(base.gear.__code__,env,base.gear.__name__,base.gear.__defaults__,base.gear.__closure__)
    isolated=types.FunctionType(base.parts.__code__,env,base.parts.__name__,base.parts.__defaults__,base.parts.__closure__)
    out=refinement.parts(isolated())
    out['cam']=land.revise(out['cam'])
    assert base.PARAMS==original and base.PARAMS['backlash_mm']==.12
    return out

def posed(parts,crank_degrees=0,axial_mm=0,coupled=True):
    phase=math.degrees(CAM_K_RAD_PER_MM*axial_mm) if coupled else 0
    return {'crank':b.Rot(crank_degrees,0,0)*parts['crank'],
            'cam':b.Pos(axial_mm,*base.CAM_YZ)*b.Rot(-crank_degrees/2+phase,0,0)*parts['cam']}
