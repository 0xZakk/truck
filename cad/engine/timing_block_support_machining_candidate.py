"""Declared 2mm educational journal backing and analytic final bore machining."""
import build123d as b
import timing_block_boolean_topology_candidate as base
DELTA=base.DELTA
JOURNAL_STATIONS=(-334.,-110.,110.,360.5)
BACKING_MM=2.0
WIDTH_MM=22.0

def cutters():
 import full_engine as f
 tunnel=b.Pos(0,90+DELTA[1],72+DELTA[2])*f.cx(f.CAM_BORE_R,f.LENGTH+2)
 guides=[b.Pos(x+dx,90+DELTA[1],150+DELTA[2])*b.Cylinder(f.LIFTER_BORE_R,235) for x in f.CYLINDERS for dx in [-25,25]]
 return tunnel,guides

def backing_shells():
 import full_engine as f
 return {i:b.Pos(x,90+DELTA[1],72+DELTA[2])*(f.cx(f.CAM_BORE_R+BACKING_MM,WIDTH_MM)-f.cx(f.CAM_BORE_R,WIDTH_MM+2)) for i,x in enumerate(JOURNAL_STATIONS,1)}

def build():
 import full_engine as f
 q,edits=base.regenerate();assert q.is_valid
 original=q
 with b.SkipClean():
  shells=backing_shells()
  for shell in shells.values():q=q.fuse(shell)
  supported=q
  tunnel,guides=cutters()
  q=q.cut(tunnel)
  for guide in guides:q=q.cut(guide)
 return q,{'base':original,'supported':supported,'shells':shells,'source_edit_counts':edits}
