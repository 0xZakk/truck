"""Reviewed rear neck exterior adapter; stable ID/frame, no automatic promotion."""
from pathlib import Path
from functools import lru_cache
import hashlib,json,copy
import build123d as b
from OCP.BRepTools import BRepTools
from assembly_math import transforms
from cad_metrics import solid_volume,support_bounds
ROOT=Path(__file__).resolve().parents[2]
ID='exhaust-rear';CHANGED_IDS={ID};SOURCE_ID='rear-exhaust-neck-study'
OUT=ROOT/'cad/engine/generated/rear-exhaust-neck-candidate'
PROOF=ROOT/'inventory/engine/rear-exhaust-neck-candidate-validation.json'
SUPERSEDED='Retained long outlet neck, thin head lands/bolt arms and end EGR connection still differ visibly from Dorman674-186; dimensions, casting identity, auxiliary ports, threads, sealing and thermal behavior remain unresolved.'
GAPS=['The outlet exterior now blends more broadly into the collector using estimated dimensions; the retained axis, flange and endpoint do not establish production neck length or seat geometry.', 'Thin head lands/bolt arms and the provisional end EGR connection still differ from replacement photographs. Casting identity, auxiliary-port assignments, threads, sealing and thermal behavior remain unresolved.']
TEXT=('Rear exhaust manifold','Collects the three rear exhaust passages and directs them toward the exhaust pipe; a separate connection supplies the EGR tube.')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def difference(a,z):return sum(abs(solid_volume(q,'adaptive')) for s in (a.cut(z),z.cut(a)) if s for q in s.solids())
def source():
 p=PROOF
 return {SOURCE_ID:dict(title='Rear exhaust outlet exterior study and protected interfaces',path='/inventory/engine/rear-exhaust-neck-candidate-validation.json',sha256=sha(p),url='https://github.com/0xZakk/truck/issues/46')}
@lru_cache(maxsize=1)
def fixtures():
 proof=json.loads(PROOF.read_text());assert proof['status']=='PASS isolated candidate; root review pending'
 for p,h in [(OUT/'baseline.step',proof['input_sha256'][str((OUT/'baseline.step').relative_to(ROOT))]),(OUT/'candidate.step',proof['exports']['step'])]:assert sha(p)==h,p
 return b.import_step(OUT/'baseline.step'),b.import_step(OUT/'candidate.step')
def frame(manifest):
 baseline_path=OUT/'baseline-manifest.json'
 proof=json.loads(PROOF.read_text());assert sha(baseline_path)==proof['input_sha256'][str(baseline_path.relative_to(ROOT))],'Changed frozen rear frame baseline'
 baseline=json.loads(baseline_path.read_text())
 manifest=dict(manifest);manifest.setdefault('mechanism',baseline['mechanism'])
 old=next(o for o in baseline['occurrences'] if o['id']==ID);new=next(o for o in manifest['occurrences'] if o['id']==ID)
 for key in ['definition','parent','position_cad_mm','rotation_cad_deg','explode_cad_mm']:
  if old.get(key)!=new.get(key):raise ValueError('Unreviewed rear local frame: '+key)
 if transforms(baseline)[ID].to_tuple()!=transforms(manifest)[ID].to_tuple():raise ValueError('Unreviewed rear ancestor frame')
def install(define,add,definitions,occurrences,assemblies,shapes):
 frame(dict(definitions=definitions,occurrences=occurrences,assemblies=assemblies))
 base,target=fixtures();old=next(d for d in definitions if d['id']==ID);current=shapes.get(ID)
 if current is None:current=b.import_step(ROOT/old['step'].lstrip('/'))
 if min(difference(current,base),difference(current,target))>=.001:raise ValueError('Unreviewed rear geometry')
 order=[d['id'] for d in definitions];definitions[:]=[d for d in definitions if d['id']!=ID]
 # The root-owned exporter also needs rear-only degenerate/duplicate cleanup.
 BRepTools.Clean_s(target.wrapped);target.tessellate(.05,.1)
 superseded='This incremental entry correction retains the old collector and EGR end connection. Both remain unsupported form/routing studies pending joint reconstruction; this is not a completed rear manifold.'
 gaps=[g for g in old['unresolved'] if g not in (superseded,SUPERSEDED)]
 define(ID,target,*TEXT,old['system'],old['color'],list(dict.fromkeys(old['sources']+[SOURCE_ID])),list(dict.fromkeys(gaps+GAPS)),old['dimension_claims'],prepared=True)
 fresh=next(d for d in definitions if d['id']==ID)
 # Preserve extension/provenance metadata absent from define's base schema,
 # while recomputing geometry-dependent dimensions from the new target.
 for key,value in old.items():
  if key not in fresh:fresh[key]=copy.deepcopy(value)
 size=support_bounds(target).size;fresh['model_bounds_mm']=[size.X,size.Y,size.Z]
 shapes[ID]=target;definitions.sort(key=lambda d:order.index(d['id']))
 for o in occurrences:
  if o['id']==ID:o.update(name=TEXT[0],function=TEXT[1])
 return dict(changed_definitions=[ID],changed_occurrences=[ID],new_definitions=[],new_occurrences=[])
