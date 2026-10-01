from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import timing_front_block_expanded_seat_candidate as c
b.SkipClean.clean=False
OUT=ROOT/'cad/engine/generated/timing-front-block-expanded-seat-candidate'
rows=[];paths=[]
for name in ['block-pan','block-gasket']:
 p=OUT/(name+'-overlap.step');paths.append(p);q=b.import_step(p)
 for i,s in enumerate(q.solids()):
  bb=s.bounding_box();rows.append({'pair':name,'solid':i,'volume_mm3':abs(solid_volume(s,'adaptive')),'bounds_mm':[list(bb.min),list(bb.max)],'socket_guard_mm3':{n:sum(abs(solid_volume(v,'adaptive'))for v in s.intersect(g).solids())for n,g in c.socket_guards().items()}})
r={'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths+[Path(__file__)]},'overlaps':rows,'status':'Frozen failed pair diagnosis; no geometry change'}
(ROOT/'inventory/engine/timing-front-expanded-seat-overlap-diagnosis.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(rows,indent=2))
