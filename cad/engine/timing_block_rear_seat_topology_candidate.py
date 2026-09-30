"""Preserve rear-seat Boolean face topology, without same-domain simplification."""
import build123d as b
from timing_block_rear_seat_repair_candidate import operands,DELTA
import timing_block_fixed_stock_candidate as fixed

def machine_block_seat(block,cam_bore_radius):
 boss,tunnel,seat=operands(cam_bore_radius)
 # build123d _bool_op normally invokes ShapeUpgrade_UnifySameDomain after
 # each Boolean. Retain the exact Boolean result and its separate face wires.
 with b.SkipClean():return (block+boss)-tunnel-seat

def regenerate(delta=DELTA,stage=None,feature_capture=None):
 import full_engine as f
 original=f.machine_block_seat;f.machine_block_seat=machine_block_seat
 try:return fixed.regenerate(delta,stage,feature_capture)
 finally:f.machine_block_seat=original
