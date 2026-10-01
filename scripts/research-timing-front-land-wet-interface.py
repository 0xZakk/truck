from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
b.SkipClean.clean=False
from cad_metrics import solid_volume
from assembly_math import transforms
import water_pump_joint_candidate as pump
OUT=ROOT/'cad/engine/generated/timing-front-block-contract-research'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return sum(abs(solid_volume(q,'adaptive')) for q in s.solids()) if s is not None and getattr(s,'wrapped',True) is not None else 0.
def bounds(s):
 if s is None or not s.solids():return None
 bb=s.bounding_box();return [list(bb.min),list(bb.max)]
paths={'block':ROOT/'cad/engine/generated/timing-pump-foot-faceted-candidate/block.step','land':ROOT/'cad/engine/generated/timing-cover-attachment-v2/future-block-land.step'}
inputs={str(p.relative_to(ROOT)):sha(p) for p in paths.values()};parts={k:b.import_step(p) for k,p in paths.items()};land=parts['land'];added=land.cut(parts['block']);added=b.Compound(children=list(added)) if isinstance(added,b.ShapeList) else added
manifest=ROOT/'inventory/engine/full-assembly.json';inputs[str(manifest.relative_to(ROOT))]=sha(manifest);m=json.loads(manifest.read_text());poses=transforms(m);defs={q['id']:q for q in m['definitions']};occ={q['id']:q for q in m['occurrences']}
guards={'pump-chamber-fluid-void':pump.cx(59,359.5,374,-32,170),'pump-fifth-passage-fluid-void':pump.cx(6.5,359.5,374,pump.EXTRA[0]-32,pump.EXTRA[1]+170)}
for name in ['water-pump-gasket','water-pump-housing','water-pump-impeller','water-pump-shaft']:
 p=ROOT/defs[occ[name]['definition']]['step'].lstrip('/');inputs[str(p.relative_to(ROOT))]=sha(p);guards[name]=poses[name]*b.import_step(p)
for i,(y,z) in enumerate(pump.MOUNTING,1):guards[f'pump-blind-socket-{i}']=pump.cx(4.3,356,374,y-32,z+170)
rows=[]
for name,q in guards.items():
 hit=land.intersect(q);row={'name':name,'future_land_overlap_mm3':vol(hit),'new_land_material_overlap_mm3':vol(added.intersect(q)),'overlap_bounds_mm':bounds(hit),'distance_to_land_mm':land.distance_to(q)};rows.append(row);print(row,flush=True)
 if vol(hit)>1e-5:b.export_step(hit,OUT/('land-'+name+'-conflict.step'))
for p in [Path(__file__),Path(pump.__file__),ROOT/'cad/engine/assembly_math.py',ROOT/'cad/engine/cad_metrics.py']:inputs[str(p.relative_to(ROOT))]=sha(p)
r={'status':'RESEARCH ONLY; no land union','input_sha256':inputs,'future_land_new_material_mm3':vol(added),'interfaces':rows,'limits':['Pump chamber is inherited analyticfluidopening, notverifiedhydraulicrouting','Any blocked passage or actual movingpart overlap prohibitsblindfuturelandunion','No blockorcovergeometrymodified']}
assert inputs=={p:sha(ROOT/p) for p in inputs};(ROOT/'inventory/engine/timing-front-land-wet-interface-research.json').write_text(json.dumps(r,indent=2)+'\n')
