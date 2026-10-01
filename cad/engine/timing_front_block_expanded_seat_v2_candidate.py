"""Estimated shared X300..365 seat trial; frozen predecessors are inputs only."""
from pathlib import Path
import hashlib
import build123d as b
import timing_front_block_adapter_candidate as previous
import timing_pan_expanded_seat_v2_contract as seat
ROOT=previous.ROOT
BASE=previous.BASE
LAND=previous.LAND
FROZEN=ROOT/'cad/engine/generated/timing-front-block-adapter-candidate/block.step'
FROZEN_SHA='661dcdfce65f64ff19aeaeb01c8b4ac46f67379eb37d4f29e80aa4dfad594502'
SEAT_SHA='4fa9d104606158710bb221fcfc71ca5dcddb62bf00243338920e92adb8f9839e'
SUPPORT_HEIGHT=10.
norm=previous.norm
old=previous.old
ownership=previous.ownership

def socket_guards():
 return {n:b.Pos(x,y,-25)*b.Cylinder(10,70) for n,(x,y,z) in ownership.RELOCATIONS.items() if n in (10,20)}

def intended_socket_cavity():
 import pan_fastener_thread_candidate as thread
 female=b.import_step(ROOT/'cad/engine/generated/pan-fastener-thread-candidate/female-test-coupon.step')
 return b.Pos(*ownership.RELOCATIONS[20])*norm(thread.cz(4.15,6.6,22.6).cut(female))

def build():
 assert hashlib.sha256(BASE.read_bytes()).hexdigest()==previous.BASE_SHA
 assert hashlib.sha256(FROZEN.read_bytes()).hexdigest()==FROZEN_SHA
 assert hashlib.sha256(Path(seat.__file__).read_bytes()).hexdigest()==SEAT_SHA
 original=b.import_step(BASE);frozen=b.import_step(FROZEN);land=b.import_step(LAND)
 fills=previous.retired_bore_fills();masks=previous.regions();masks['below-new-seat']=seat.below_mating_seat()
 guards=socket_guards();support=seat.transition_seat_support(SUPPORT_HEIGHT)
 with b.SkipClean():
  for g in guards.values():support=norm(support.cut(g))
  q=original
  for s in fills.values():q=norm(q.fuse(s))
  for s in masks.values():q=norm(q.cut(s))
  q=norm(q.fuse(land));q=norm(q.cut(seat.transition_below_seat()));q=norm(q.fuse(support))
  # Preserve exact existing owner material in the full socket/floor neighborhood.
  for g in guards.values():q=norm(q.cut(g).fuse(frozen.intersect(g)))
  cavity=intended_socket_cavity();q=norm(q.cut(cavity))
 return q,{'socket_cavity':cavity,'original':original,'frozen':frozen,'fills':fills,'masks':masks,'land':land,'support':support,'socket_guards':guards}
