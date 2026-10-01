from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import timing_front_block_expanded_seat_candidate as c
b.SkipClean.clean=False
OUT=ROOT/'cad/engine/generated/timing-front-block-expanded-seat-candidate';p=OUT/'block.step';block=b.import_step(p)
back=c.seat.clip_x(c.seat.band(0,.02,'gasket',True),300,365);missing=c.norm(back.cut(block));rows=[]
for i,s in enumerate(missing.solids()):
 bb=s.bounding_box();v=abs(solid_volume(s,'adaptive'));row={'index':i,'volume_mm3':v,'bounds_mm':[list(bb.min),list(bb.max)],'inside_socket_guard_mm3':{n:sum(abs(solid_volume(q,'adaptive'))for q in s.intersect(g).solids())for n,g in c.socket_guards().items()}};rows.append(row);b.export_step(s,OUT/f'gasket-backing-missing-{i}.step')
r={'input_sha256':{str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest()for x in [p,Path(c.__file__),Path(c.seat.__file__),Path(__file__)]},'analytic_backing_thickness_mm':.02,'missing':rows,'status':'DIAGNOSTIC; no geometry or threshold changes'}
(ROOT/'inventory/engine/timing-front-expanded-seat-backing-diagnosis.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(rows,indent=2))
