from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
b.SkipClean.clean=False
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-front-block-adapter-candidate'
p=OUT/'block.step';n=ROOT/'cad/engine/generated/timing-cover-attachment-v2/pan.step';q=b.import_step(p);pan=b.import_step(n);hit=q.intersect(pan);rows=[]
for i,s in enumerate(hit.solids()):
 bb=s.bounding_box();row={'index':i,'volume_mm3':abs(solid_volume(s,'adaptive')),'bounds_mm':[list(bb.min),list(bb.max)]};rows.append(row);print(row,flush=True);b.export_step(s,OUT/f'pan-overlap-{i}.step')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r={'status':'FAIL actual pan overlap; no repair performed','input_sha256':{str(x.relative_to(ROOT)):sha(x) for x in [p,n,Path(__file__)]},'regions':rows}
(ROOT/'inventory/engine/timing-front-block-pan-contact-diagnosis.json').write_text(json.dumps(r,indent=2)+'\n')
