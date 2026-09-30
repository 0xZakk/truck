#!/usr/bin/env python3
"""Measure proposed interior removals against unchanged carrier socket/seat.
No modified block is constructed or installed. Existing whole-support gate stays failed.
"""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import full_engine as f
from timing_block_fixed_stock_candidate import DELTA
from cad_metrics import solid_volume
path=ROOT/'cad/engine/generated/timing-block-boolean-topology-candidate/block.step';q=b.import_step(path)
def vol(s):return sum(abs(solid_volume(x,'adaptive')) for x in s.solids()) if s is not None and getattr(s,'wrapped',True) is not None else 0.
tunnel=b.Pos(0,90+DELTA[1],72+DELTA[2])*f.cx(f.CAM_BORE_R,f.LENGTH+2)
guides=[b.Pos(x+dx,90+DELTA[1],150+DELTA[2])*b.Cylinder(f.LIFTER_BORE_R,235) for x in f.CYLINDERS for dx in [-25,25]]
rows=[]
with b.SkipClean():
 for x,z in f.carrier94.BLOCK_STATIONS:
  boss=f.carrier94.sideways(14,31,x,119.5,z);socket=f.carrier94.sideways(5.2,25,x,123.5,z)
  pieces=[s for cutter in [tunnel]+guides for s in q.intersect(boss).intersect(cutter).solids()]
  removed=pieces[0].fuse(*pieces[1:]) if len(pieces)>1 else pieces[0]
  socket_guard=f.carrier94.sideways(7.2,29,x,123.5,z)
  seat_guard=f.carrier94.sideways(14,2.1,x,134.05,z)
  bb=removed.bounding_box();rows.append({'station_x_mm':x,'prospective_removed_mm3':vol(removed),'removed_bounds_mm':[list(bb.min),list(bb.max)],'minimum_distance_removed_to_existing_socket_mm':removed.distance_to(socket),'minimum_distance_removed_to_seat_backing_guard_mm':removed.distance_to(seat_guard),'proposed_2mm_socket_wall_guard_removed_mm3':vol(removed.intersect(socket_guard)),'proposed_2mm_seat_backing_guard_removed_mm3':vol(removed.intersect(seat_guard))})
inputs=[path,Path(__file__),ROOT/'cad/engine/accessory_carrier_1994.py',ROOT/'inventory/engine/timing-block-boolean-topology-full.json']
r={'status':'PROPOSAL measurement only; entire-support guard remains failed','input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'source_baseline':{'boss_radius_mm':14,'socket_radius_mm':5.2,'nominal_radial_wall_mm':8.8,'blind_backing_mm':7,'seat_y_mm':135,'evidence_class':'existing provisional CAD, no manufacturer minimum wall evidence'},'proposed_masks':{'socket':'existing radius5.2+2mm; axial111..136 extended2mm each end','mating_face':'entire radius14 footprint at Y135 with2mm backing; Y133..135.1','status':'review proposal only;2mm is an explicit estimate, not production requirement'},'stations':rows,'limits':['Clearance to the socket surface is geometric, not stress/strength qualification','No support material added; no final machining applied','Root must approve any revised physical support contract; prior91 masks remain unchanged']}
(ROOT/'inventory/engine/timing-carrier-machining-proposal.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
