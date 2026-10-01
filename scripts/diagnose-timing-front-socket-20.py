from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import pan_fastener_thread_candidate as thread
import timing_cover_attachment_v2 as joint
b.SkipClean.clean=False
OUT=ROOT/'cad/engine/generated/timing-front-block-expanded-seat-candidate'
def vol(s):return sum(abs(solid_volume(q,'adaptive'))for q in s.solids()) if s is not None else 0.
def bounds(s):
 if s is None or not s.solids():return None
 bb=s.bounding_box();return[list(bb.min),list(bb.max)]
pd=ROOT/'cad/engine/generated/pan-fastener-thread-candidate';male=b.import_step(pd/'pan-screw.step');female=b.import_step(pd/'female-test-coupon.step')
region=thread.cz(4.17,7.8,22.3);cavity=region.cut(female)
paths={'future-land':ROOT/'cad/engine/generated/timing-cover-attachment-v2/future-block-land.step','frozen-adapter':ROOT/'cad/engine/generated/timing-front-block-adapter-candidate/block.step','expanded-adapter':OUT/'block.step'}
rows=[]
for name,p in paths.items():
 shape=b.import_step(p)
 for n in [10,20]:
  loc=b.Pos(*joint.RELOCATIONS[n]);collision=shape.intersect(loc*male);intrusion=shape.intersect(loc*cavity)
  rows.append({'owner':name,'station':n,'male_overlap_mm3':vol(collision),'overlap_bounds_mm':bounds(collision),'intended_cavity_filled_mm3':vol(intrusion),'female_material_missing_mm3':vol((loc*female).cut(shape))})
  if n==20 and name=='expanded-adapter':b.export_step(joint.norm(collision),OUT/'inherited-male20-overlap.step');b.export_step(joint.norm(intrusion),OUT/'inherited-socket20-cavity-fill.step')
paths.update({'male':pd/'pan-screw.step','female':pd/'female-test-coupon.step','script':Path(__file__),'source':Path(thread.__file__)})
r={'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths.values()},'cavity_definition':'Source declared female cylindrical regionR4.17 localZ7.8..22.3 minus source female coupon; no new neighbor carving','results':rows,'status':'DIAGNOSTIC; no model mutation'}
(ROOT/'inventory/engine/timing-front-socket-20-diagnosis.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(rows,indent=2))
