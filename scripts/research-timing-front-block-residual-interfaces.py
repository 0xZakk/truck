from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
b.SkipClean.clean=False
import timing_front_block_contract as contract
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-front-block-contract-research'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return sum(abs(solid_volume(q,'adaptive')) for q in s.solids()) if s is not None and getattr(s,'wrapped',True) is not None else 0.
def norm(s):return b.Compound(children=[]) if s is None else b.Compound(children=list(s)) if isinstance(s,b.ShapeList) else s
def bounds(s):
 if s is None or not s.solids():return None
 bb=s.bounding_box();return [list(bb.min),list(bb.max)]
p=ROOT/'cad/engine/generated/timing-pump-foot-faceted-candidate/block.step';block=b.import_step(p);inputs={str(p.relative_to(ROOT)):sha(p)};regions=contract.proposed_regions();rows=[]
for name in ['cover','main-gasket','pan-gasket','front-terminal-sealant','future-block-land']:
 p=ROOT/'cad/engine/generated/timing-cover-attachment-v2'/(name+'.step');inputs[str(p.relative_to(ROOT))]=sha(p);neighbor=b.import_step(p);shared=norm(block.intersect(neighbor));remaining=norm(shared.cut(regions['main-plane-only'])) if shared.solids() else shared;remaining=norm(remaining.cut(regions['source-upper-band-supplement'])) if remaining.solids() else remaining;row={'name':name,'original_overlap_mm3':vol(shared),'overlap_remaining_after_proposed_region_removal_mm3':vol(remaining),'remaining_bounds_mm':bounds(remaining)};rows.append(row);print(row,flush=True)
 if vol(remaining)>1e-5:b.export_step(remaining,OUT/('remaining-'+name+'-overlap.step'))
for p in [Path(__file__),Path(contract.__file__)]:inputs[str(p.relative_to(ROOT))]=sha(p)
r={'status':'RESEARCH conditional witness differences only; no blockcandidate','input_sha256':inputs,'interfaces':rows,'limits':['No native block cut performed','Futureland is intendedblockmaterial; its overlap is attachment not collision','Gasket or sealant residuals forbid calling the proposed regionmask a completeadapter']}
(ROOT/'inventory/engine/timing-front-block-residual-interface-research.json').write_text(json.dumps(r,indent=2)+'\n')
