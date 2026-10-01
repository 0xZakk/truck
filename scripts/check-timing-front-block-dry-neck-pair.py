from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
b.SkipClean.clean=False
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-front-block-adapter-candidate'
paths=[OUT/'block.step',ROOT/'cad/engine/generated/timing-pan-dry-neck-candidate/pan.step'];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(paths[1])=='b519c1e37e6cacec5ed2326d92264c61ce7dd7f9f1a40eec7a57afeca1eb0caf'
a,d=[b.import_step(p) for p in paths];hit=a.intersect(d);v=sum(abs(solid_volume(s,'adaptive')) for s in hit.solids()) if hit is not None else 0.;rows=[]
if hit is not None:
 for i,s in enumerate(hit.solids()):
  bb=s.bounding_box();rows.append({'bounds_mm':[list(bb.min),list(bb.max)],'volume_mm3':abs(solid_volume(s,'adaptive'))});b.export_step(s,OUT/f'dry-neck-overlap-{i}.step')
r={'status':'PASS static block/dry-neck clearance' if v<1e-5 else 'FAIL block/dry-neck overlap','input_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [*paths,Path(__file__),ROOT/'inventory/engine/timing-pan-dry-neck-candidate-validation.json']},'overlap_mm3':v,'distance_mm':a.distance_to(d),'regions':rows,'limits':['Frozen v2pan failure retained separately','Static paironly; no sealing or wholeassembly acceptance']};(ROOT/'inventory/engine/timing-front-block-dry-neck-pair.json').write_text(json.dumps(r,indent=2)+'\n');print(r,flush=True)
