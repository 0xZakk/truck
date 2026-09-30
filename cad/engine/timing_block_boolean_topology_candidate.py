"""Retain exact Boolean topology from rear-seat through downstream adapters."""
import build123d as b
import timing_block_fixed_stock_candidate as fixed
DELTA=fixed.DELTA

def regenerate(delta=DELTA,stage=None,feature_capture=None):
 import full_engine as f
 original=f.machine_block_seat;previous=b.SkipClean.clean
 def seat(block,radius):
  # Later same-domain simplification recreates the invalid nested tunnel wire.
  # Preserve native Boolean topology through the remaining ordered adapters.
  b.SkipClean.clean=False
  return original(block,radius)
 f.machine_block_seat=seat
 try:return fixed.regenerate(delta,stage,feature_capture)
 finally:
  f.machine_block_seat=original;b.SkipClean.clean=previous
