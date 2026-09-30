#!/usr/bin/env python3
"""Read-only rejection study: do not trim collision to imply a sealed joint."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import timing_cover_shell_candidate as cover
import timing_cover_joint_candidate as outline
import oil_pan_joint_v9_candidate as pan
from cad_metrics import solid_volume
out=ROOT/'cad/engine/generated/timing-cover-pan-joint-proposal';out.mkdir(parents=True,exist_ok=True)
vol=lambda s:sum(abs(solid_volume(q)) for q in s.solids()) if s else 0
p=cover.Parameters();face,_,_=cover.profiles(p)
main=cover.extrude_x(face,p.block_seat_x,p.gasket_thickness)
for pt in outline.HOLES_NORMALIZED:
 y,z=cover.yz(pt,p);main-=cover.cx(4.2,p.block_seat_x-1,p.block_seat_x+2,y,z)
gasket=pan.gasket_shape();front=gasket.intersect(b.Pos(373,0,-50)*b.Box(16,400,100))
# Terminal regions conservatively include the lowest 12 mm of each open end.
terminals={}
for name,yrange in [('long_leg',(-150,-80)),('short_leg',(130,210))]:
 t=main.intersect(b.Pos(373.4,sum(yrange)/2,-16)*b.Box(2,yrange[1]-yrange[0],24))
 bb=t.bounding_box();terminals[name]={'bounds_mm':[tuple(bb.min),tuple(bb.max)],'distance_to_complete_pan_gasket_mm':t.distance_to(gasket),'contact_overlap_mm3':vol(t.intersect(gasket))}
# A valid terminal join needs a zero-gap seating path, not merely zero overlap.
r={'status':'REJECTED REGISTRATION; NO NEW JOINT GEOMETRY','scope':'Read-only source and current-model terminal comparison','input_sha256':{str(Path(f).relative_to(ROOT)):hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in [__file__,cover.__file__,outline.__file__,pan.__file__]},'parameters':{'cover':p.__dict__,'pan_station_count':len(pan.STATIONS),'front_end':pan.ENDS[0]},'terminal_checks':terminals,'complete_main_gasket_to_pan_gasket_distance_mm':main.distance_to(gasket),'front_gasket_valid':front.is_valid,'joint_contact_proof':'FAIL: separated terminal regions; no continuous main-to-pan sealing junction established','collision_subtraction':'NOT PERFORMED; would not establish seating or terminal continuity','crank_and_seal':'UNCHANGED','installed':'NOT RUN','learning':'NOT RUN','browser':'NOT RUN'}
(ROOT/'inventory/engine/timing-cover-pan-joint-validation.json').write_text(json.dumps(r,indent=2)+'\n')
# Derived CAD only; useful overlay for review without source-photo redistribution.
b.export_step(b.Compound(children=[main,front]),out/'terminal-comparison.step')
import numpy as np
parts=[main,front];data={}
for i,s in enumerate(parts):
 v,f=s.tessellate(.1,.15);data[f'v{i}']=np.array([tuple(t) for t in v]);data[f'f{i}']=np.array(f)
np.savez_compressed(out/'terminal-preview.npz',**data)
print(json.dumps(r,indent=2))
