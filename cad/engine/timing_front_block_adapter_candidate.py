"""Estimated coordinated front block; isolated, no canonical writes."""
from pathlib import Path
import hashlib
import build123d as b
import timing_front_block_contract as front
import timing_front_pan_transition_contract as transition
import timing_cover_attachment_v2 as ownership
import oil_pan_joint_v9_candidate as old
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'cad/engine/generated/timing-block-combined-candidate/block.step'
BASE_SHA='72773d2ce6793180ff828d3d8ddf089daea3d85b738962084d335ca4a17c1a36'
LAND=ROOT/'cad/engine/generated/timing-cover-attachment-v2/future-block-land.step'
def norm(q):return b.Compound(children=list(q)) if isinstance(q,b.ShapeList) else q

def regions():
 q=front.proposed_regions()
 return {'main-plane':q['main-plane-only'],'lower-band':q['source-upper-band-supplement'],'below-new-seat':transition.below_new_front_seat()}

def retired_bore_fills():
 return {n:b.Pos(x,y)*old.cylinder(4.15,z+7.6,min(z+old.LENGTH+1,z+25)) for n,(x,y,z) in enumerate(old.STATIONS,1) if n in ownership.RELOCATIONS}

def build():
 assert hashlib.sha256(BASE.read_bytes()).hexdigest()==BASE_SHA
 original=b.import_step(BASE);q=original;fills=retired_bore_fills();masks=regions();land=b.import_step(LAND)
 with b.SkipClean():
  for s in fills.values():q=norm(q.fuse(s))
  filled=q
  for s in masks.values():q=norm(q.cut(s))
  cut=q
  q=norm(q.fuse(land))
 return q,{'original':original,'filled':filled,'cut':cut,'fills':fills,'masks':masks,'land':land}
