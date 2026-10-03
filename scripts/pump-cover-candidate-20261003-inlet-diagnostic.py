from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import pump_cover_candidate_20261003 as c
h=b.import_step(c.O/'water-pump-housing.step');p=c.T*c.inlet(probe=True);hit=c.norm(h.intersect(p));q=c.T.inverse()*hit;port_frame=b.Rot(130,0,0)*b.Pos(0,32,-170)*q
r={'hit_volume_mm3':sum(abs(solid_volume(s,'adaptive'))for s in hit.solids()),'world_bounds':[list(hit.bounding_box().min),list(hit.bounding_box().max)],'unclocked_pump_bounds':[list(q.bounding_box().min),list(q.bounding_box().max)],'inlet_local_bounds':[list(port_frame.bounding_box().min),list(port_frame.bounding_box().max)],'hit_solids':len(hit.solids())};b.export_step(hit,c.O/'inlet-obstruction.step');(R/'reference/engine/pump-cover-candidate-20261003-inlet-diagnostic.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
