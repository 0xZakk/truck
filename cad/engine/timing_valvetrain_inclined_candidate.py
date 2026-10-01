"""Root-approved isolated inclined linkage and upper-guide passage candidate."""
from copy import deepcopy
from types import FunctionType,SimpleNamespace
import math
import build123d as b
import timing_valvetrain_inclined_hypothesis as numeric
import timing_valvetrain_adapter_candidate as frozen
import valve_source_layout as v
from assembly_math import transforms
H=numeric.layout(90.)
P={'PIVOT_Y':H['pivot_y'],'PUSHROD_Y':90.,'CUP_Z':H['cup_z'],'rest':H['rest']}
contract=SimpleNamespace(DELTA=numeric.DELTA,state=lambda theta,i,kind,axial=0:numeric.state(H,theta,i,kind,axial))
stations=frozen.stations

def rocker():
 env=dict(v.rocker.__globals__);env.update({k:P[k] for k in ['PIVOT_Y','PUSHROD_Y','CUP_Z']})
 return FunctionType(v.rocker.__code__,env,'inclined_rocker')()

def pedestal_head(old,m):
 env=dict(frozen.head_adapter.__globals__);env['P']=P
 return FunctionType(frozen.head_adapter.__code__,env,'inclined_pedestals')(old,m)

def poses(m,theta=0,axial=0):
 env=dict(frozen.poses.__globals__);env.update(P=P,contract=contract)
 return FunctionType(frozen.poses.__code__,env,'inclined_poses')(m,theta,axial)

def passage(x,zlo=244.,zhi=304.,extra=0.):
 s=H['solve'](0)
 # Explicit horizontal circular sections avoid OCC's near-parallel clipped
 # cylinder false zero. R5 is now exact horizontal radius, conservatively
 # satisfying the same sufficient tube-containment bound used in the study.
 sections=[b.Pos(x,numeric.section_y(s,z)[0],z)*b.Circle(5+extra) for z in [zlo,zhi]]
 inclined=b.loft(sections,ruled=True)
 return inclined.fuse(b.Pos(x,90,(zlo+zhi)/2)*b.Cylinder(6+extra,zhi-zlo)).fuse(b.Pos(x,88,(zlo+zhi)/2)*b.Cylinder(6+extra,zhi-zlo))

def head_adapter(old,m):
 q=pedestal_head(old,m)
 for _,_,x in stations(m):q=q.cut(b.Pos(0,0,-v.HEAD_Z)*passage(x,255.5,304))
 return q

def allowed_regions(m):
 env=dict(frozen.allowed_regions.__globals__);env['P']=P
 masks=list(FunctionType(frozen.allowed_regions.__code__,env)(m).solids())
 masks += [b.Pos(0,0,-v.HEAD_Z)*passage(x,255.5,304) for _,_,x in stations(m)]
 return b.Compound(children=masks)

def gasket_adapter(old_world,m):
 q=old_world
 for _,_,x in stations(m):q=q.cut(passage(x,254,255.5))
 return q

def block_adapter(old_world,m):
 q=old_world
 for _,_,x in stations(m):
  # A 2 mm overlap with existing guide walls establishes connected deck material.
  patch=b.Pos(x,numeric.LOWER_Y,249)*b.Cylinder(13.124565,10)
  patch=patch.cut(passage(x,244,254))
  q=q.fuse(patch).cut(passage(x,244,254))
 return q
