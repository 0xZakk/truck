#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from timing_cover_attachment_v2 import norm
O=R/'cad/engine/generated/timing-pan-upper-contact';F=R/'cad/engine/generated/timing-cover-attachment-v2'
paths={'gasket':R/'cad/engine/generated/timing-pan-expanded-seat-v2-candidate/pan-gasket.step','block':R/'cad/engine/generated/timing-front-block-expanded-seat-v3-candidate/block.step','cover':R/'cad/engine/generated/front-seal-2692-candidate/cover.step','main-gasket':F/'main-gasket.step','sealant':F/'front-terminal-sealant.step'}
q={n:norm(b.import_step(p)) for n,p in paths.items()}
def common_area(a,bshape):
 op=BRepAlgoAPI_Common(a.wrapped,b.Compound(list(bshape.faces())).wrapped);op.Build();assert op.IsDone();return sum(f.area for f in b.Compound(op.Shape()).faces())
def sheet(x0,x1,y0,y1,z):return b.Face(b.Wire.make_polygon([(x0,y0,z),(x1,y0,z),(x1,y1,z),(x0,y1,z)],close=True))
witnesses={'left-full-width':sheet(-1,1,-141,-130,-32),'right-backed-strip':sheet(-1,1,106,108,-32),'lifted-right-fault':sheet(-1,1,106,108,-31.9)}
from oil_pan_joint_v9_candidate import STATIONS
for station,(x,y,z) in enumerate(STATIONS,1):
 if station in range(11,20):witnesses['left-inboard-pad-'+str(station)]=sheet(x-.1,x+.1,-126.6,-124.1,-32)
w=[]
for n,s in witnesses.items():
 row={'name':n,'area_mm2':s.area,'gasket_contact_mm2':common_area(s,q['gasket']),'owner_contact_mm2':{name:common_area(s,v)for name,v in q.items()if name!='gasket'},'distance_to_block_mm':s.distance_to(q['block'])};w.append(row);b.export_step(s,O/(n+'.step'))
# Actual source planes provide readable physical geometry, not a contact graph.
for axis,coord in [('X',0),('X',-376),('X',373.4)]:
 for name,shape in q.items():
  sec=b.section(shape,b.Plane.YZ.offset(coord));lines=[]
  for edge in sec.edges():lines.append([list(edge.position_at(i/80))for i in range(81)])
  (O/f'{name}-section-{coord}.json').write_text(json.dumps(lines))
transitions={}
for name in ['block','cover','main-gasket']:
 transitions[name]={'sealant_shared_face_area_mm2':common_area(b.Compound(list(q['sealant'].faces())),q[name]),'sealant_distance_mm':q['sealant'].distance_to(q[name])}
report={'full_width_gap_witnesses':w,'front_terminal_owner_transitions':transitions,'scope':'Exact face contact and distance; no pressure or containment claim','input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [Path(__file__),*paths.values()]}}
(R/'inventory/engine/timing-pan-upper-contact-diagnostic.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
