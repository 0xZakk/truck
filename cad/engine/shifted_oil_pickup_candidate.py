"""Bounded estimated pickup reconnection. Canonical definitions remain untouched."""
import build123d as b
import oil_drive_layout as drive
from timing_block_axis_feature_candidate import DELTA
MASK_X=(54.,200.)
INSERTION_MM=3.
def original_path():
 start=(drive.PUMP_FRAME*b.Vertex(-34,0,5)).center()
 return b.Spline(start,(60,48,-130),(-100,41,-210),(-190,41,-245),tangents=[(-1,0,0),(-1,0,0)])
def build(old_world):
 path=original_path(); t=path.param_at_point((60,48,-130)); splice=path.position_at(t); tangent=path.tangent_at(t)
 start=(b.Pos(*DELTA)*drive.PUMP_FRAME*b.Vertex(-34+INSERTION_MM,0,5)).center()
 bend=start+b.Vector(-5,0,0)
 curve=b.Wire([b.Edge.make_line(start,bend),b.Spline(bend,splice,tangents=[(-1,0,0),tangent])])
 plane=b.Plane(origin=splice,z_dir=tangent)
 tail=old_world.split(plane,keep=b.Keep.TOP)
 head=b.sweep(b.Plane(origin=start,x_dir=(0,1,0),z_dir=(-1,0,0))*(b.Circle(6)-b.Circle(4.8)),path=curve,is_frenet=True)
 q=tail.fuse(head)
 return q,{'tail':tail,'head':head,'path':curve,'splice':splice,'tangent':tangent,'start':start,'parameter':t}
