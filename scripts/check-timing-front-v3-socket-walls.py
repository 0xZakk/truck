from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import timing_front_block_expanded_seat_v3_candidate as c
import pan_fastener_thread_candidate as thread
b.SkipClean.clean=False
p=ROOT/'cad/engine/generated/timing-front-block-expanded-seat-v3-candidate/block.step';q=b.import_step(p);source=b.import_step(c.LAND)
def vol(s):return sum(abs(solid_volume(v,'adaptive'))for v in s.solids())if s is not None else 0.
rows=[]
for n in [10,20]:
 loc=b.Pos(*c.ownership.RELOCATIONS[n]);wall=loc*(thread.cz(6.2,7.8,23.6)-thread.cz(4.17,7.7,23.7));floor=loc*thread.cz(4.15,22.6,23.6)
 rows.append({'station':n,'wall_minimum_radial_thickness_mm':2.03,'declared_wall_missing_in_source_mm3':vol(wall.cut(source)),'declared_wall_missing_in_candidate_mm3':vol(wall.cut(q)),'declared_floor_missing_in_source_mm3':vol(floor.cut(source)),'declared_floor_missing_in_candidate_mm3':vol(floor.cut(q))})
r={'input_sha256':{str(v.relative_to(ROOT)):hashlib.sha256(v.read_bytes()).hexdigest()for v in [p,c.LAND,Path(__file__)]},'guards':rows,'scope':'Existing estimated physical annular wall/floor, not strength minimum or factory specification'};r['local_status']='PASS'if all(all(row[k]<1e-5 for k in row if 'missing' in k)for row in rows)else'FAIL'
(ROOT/'inventory/engine/timing-front-v3-socket-walls.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
