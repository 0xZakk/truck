from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
b.SkipClean.clean=False
import timing_front_block_adapter_candidate as c
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-front-block-adapter-candidate'
def norm(q):return b.Compound(children=list(q)) if isinstance(q,b.ShapeList) else q
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q is not None and getattr(q,'wrapped',True) is not None else 0.
q=b.import_step(OUT/'block.step');old=b.import_step(c.BASE);land=b.import_step(c.LAND);added=norm(q.cut(old));fills=c.retired_bore_fills();mask=b.Compound(children=[land,*fills.values()]);outside=norm(added.cut(mask));rows=[]
for i,s in enumerate(outside.solids()):
 bb=s.bounding_box();rows.append({'index':i,'volume_mm3':vol(s),'bounds_mm':[list(bb.min),list(bb.max)],'valid':s.is_valid});b.export_step(s,OUT/f'outside-addition-mask-{i}.step')
sequential=norm(added.cut(land))
for f in fills.values():
 if sequential is not None and sequential.solids():sequential=norm(sequential.cut(f))
fused=land
for f in fills.values():fused=norm(fused.fuse(f))
fused_outside=norm(added.cut(fused))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r={'input_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [OUT/'block.step',c.BASE,c.LAND,Path(c.__file__),Path(__file__)]},'original_compound_difference_mm3':vol(outside),'regions':rows,'sequential_source_operand_difference_mm3':vol(sequential),'fused_source_operand_difference_mm3':vol(fused_outside),'limits':['Same source operands and strict1e-5mm³ criterion; no expandedmask','Diagnoseoverlappingcompoundoperand behavior beforeacceptance']};(ROOT/'inventory/engine/timing-front-block-material-bounds-diagnosis.json').write_text(json.dumps(r,indent=2)+'\n');print(r,flush=True)
