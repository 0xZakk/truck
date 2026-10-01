#!/usr/bin/env python3
"""Read-only endpoint/passage audit for a shifted pump; no source geometry writes."""
import sys,json,hashlib,math
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from assembly_math import transforms
import oil_drive_layout as drive
from timing_block_axis_feature_candidate import DELTA
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());poses=transforms(m)
defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']}
def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def path(i):return defs[occ[i]['definition']]['step'].lstrip('/')
def shape(i):return poses[i]*b.import_step(ROOT/path(i))
def vec(v):return [float(x) for x in v]
def vol(s):return sum(x.volume for x in s.solids())
old=drive.PUMP_FRAME;new=b.Pos(*DELTA)*old
inlet=(old*b.Vertex(-34,0,5)).center();target=(new*b.Vertex(-34,0,5)).center()
pump=shape('oil-pump-housing');tube=shape('oil-pickup-tube');shift=b.Pos(*DELTA)*pump
# Cross section circles independently expose the actual exported tube inlet frame.
edges=[]
for e in tube.edges():
 if e.geom_type==b.GeomType.CIRCLE:
  center=e.arc_center
  edges.append({'radius_mm':e.radius,'center_mm':vec(center),'distance_to_nominal_inlet_mm':(center-inlet).length})
edges.sort(key=lambda r:r['distance_to_nominal_inlet_mm'])
# Known inlet cutter X[-45,-15],R6. A radius4.7 bore probe lies wholly inside intended inlet lumen.
probe=old*b.Pos(-30,0,5)*b.Rot(0,90,0)*b.Cylinder(4.7,12)
newprobe=b.Pos(*DELTA)*probe
blockpath='cad/engine/generated/timing-front-block-expanded-seat-v3-candidate/block.step';block=b.import_step(ROOT/blockpath)
shaftprobe=b.Pos(*DELTA)*drive.GEAR_FRAME*drive.axial_cylinder(7.1,drive.INTERMEDIATE_BOTTOM-1,drive.INTERMEDIATE_TOP-12)
inputs=['inventory/engine/full-assembly.json','cad/engine/oil_drive_layout.py','cad/engine/oil_pump.py','cad/engine/timing_block_axis_feature_candidate.py','scripts/check-shifted-oil-drive-connections.py',blockpath]+[path(i) for i in ['oil-pump-housing','oil-pickup-tube','oil-pickup-bell','oil-pickup-screen']]
d={'status':'AUDIT; shifted external interfaces not accepted','inputs':{p:sha(p) for p in inputs},'delta_mm':list(DELTA),'inlet':{'old_center_mm':vec(inlet),'shifted_center_mm':vec(target),'stale_endpoint_error_mm':(target-inlet).length,'old_axis_world':[-1,0,0],'shifted_axis_world':[-1,0,0],'actual_tube_circular_edges_nearest_inlet':edges[:4]},'actual_CAD':{'old_pump_tube_overlap_mm3':vol(pump.intersect(tube)),'shifted_pump_stale_tube_overlap_mm3':vol(shift.intersect(tube)),'old_pump_tube_distance_mm':pump.distance_to(tube),'shifted_pump_stale_tube_distance_mm':shift.distance_to(tube),'old_inlet_lumen_probe_pump_overlap_mm3':vol(pump.intersect(probe)),'shifted_inlet_lumen_probe_pump_overlap_mm3':vol(shift.intersect(newprobe)),'shifted_shaft_passage_probe_block_overlap_mm3':vol(block.intersect(shaftprobe))},'routing':{'pickup':'Existing estimated tube remains at old endpoint; downstream bell/screen fixed','pump_discharge':'No complete discharge passage defined by pump source; do not reinterpret shaft bore as fluid outlet','block_support':'Frozen moved pump feet provide mechanical mounting only; oil discharge sealing/routing absent'},'limits':['Static endpoint and actual solids audit only','Tube outer radius6 and bore4.8 are estimates','Shaft clearance probe is not whole pump/block interface acceptance','No new geometry or fluid-pressure claim']}
p=ROOT/'inventory/engine/shifted-oil-drive-connection-audit.json';p.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({k:v for k,v in d.items() if k!='inputs'},indent=2))
