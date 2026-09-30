"""Second explicit CSG trial, first distributed-cut attempt preserved."""
import build123d as b
from timing_block_rear_seat_repair_candidate import operands,DELTA
from cad_metrics import solid_volume
import timing_block_fixed_stock_candidate as fixed

def volume(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q is not None and getattr(q,'wrapped',True) is not None else 0.
def machine_block_seat(block,cam_bore_radius):
 boss,tunnel,seat=operands(cam_bore_radius)
 assert volume(block.intersect(tunnel))<1e-5,'Input stock tunnel is not empty'
 # Do not repeat a coincident through-tunnel cut on already bored stock.
 return block.cut(seat).fuse(boss.cut(tunnel).cut(seat))

def regenerate(delta=DELTA,stage=None,feature_capture=None):
 import full_engine as f
 original=f.machine_block_seat;f.machine_block_seat=machine_block_seat
 try:return fixed.regenerate(delta,stage,feature_capture)
 finally:f.machine_block_seat=original
