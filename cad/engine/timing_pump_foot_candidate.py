"""Isolated estimated narrower pump feet; all source frames/cutters stay fixed."""
import ast, inspect
import build123d as b
import oil_drive_layout as drive
import timing_block_support_machining_candidate as parent
DELTA=parent.DELTA
SEMIMINOR_MM=5.5

def revised_supports():
 tree=ast.parse(inspect.getsource(drive.pump_mount_supports));count=0
 for node in ast.walk(tree):
  if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='Ellipse':
   assert [a.value for a in node.args]==[14,9]
   node.args[1]=ast.Constant(SEMIMINOR_MM);count+=1
 assert count==1
 ns=dict(vars(drive));exec(compile(ast.fix_missing_locations(tree),'<isolated pump foot>','exec'),ns)
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
