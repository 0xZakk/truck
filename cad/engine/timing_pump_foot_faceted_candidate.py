"""Separate estimated inscribed 128-segment foot profile; analytic failure frozen."""
import ast, inspect, math
import build123d as b
import oil_drive_layout as drive
import timing_block_support_machining_candidate as parent
DELTA=parent.DELTA
SEMIMINOR_MM=5.5
SEGMENTS=128
CHORD_SAG_BOUND_MM=14*(1-math.cos(math.pi/SEGMENTS))
FACET_INRADIUS_BOUND_MM=5.5*math.cos(math.pi/SEGMENTS)

def revised_supports():
 tree=ast.parse(inspect.getsource(drive.pump_mount_supports));count=0
 for node in ast.walk(tree):
  if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='Ellipse':
   assert [a.value for a in node.args]==[14,9]
   node.func=ast.Name(id='foot_profile',ctx=ast.Load());node.args=[];count+=1
 assert count==1
 ns=dict(vars(drive));ns['foot_profile']=lambda:b.Polygon(*[(14*math.cos(2*math.pi*i/SEGMENTS),5.5*math.sin(2*math.pi*i/SEGMENTS)) for i in range(SEGMENTS)],align=None);exec(compile(ast.fix_missing_locations(tree),'<isolated pump foot>','exec'),ns)
 return ns['pump_mount_supports']()

def build():
 old=drive.pump_mount_supports
 # Materialize before replacement so source inspection always sees original function.
 revised=revised_supports()
 drive.pump_mount_supports=lambda:revised
 try:q,data=parent.build()
 finally:drive.pump_mount_supports=old
 data['supports']=[b.Pos(*DELTA)*s for s in revised]
 data['old_supports']=[b.Pos(*DELTA)*s for s in old()]
 return q,data
