"""Static pedestal/shim/fulcrum support contacts from saved source-v2 STEP."""
from pathlib import Path
import sys,json,hashlib,importlib.util
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from valve_source_integration import candidate_transforms
OUT=ROOT/'cad/engine/candidates/valve-source-all12';m=json.loads((OUT/'manifest.json').read_text());occ={o['id']:o for o in m['occurrences']};dmap={d['id']:d for d in m['definitions']}
spec=importlib.util.spec_from_file_location('frozen_source_assembly_math',OUT/'baseline/assembly_math.py');authority=importlib.util.module_from_spec(spec);spec.loader.exec_module(authority)
poses=candidate_transforms(m,0,base_transforms=authority.transforms);defs={};hashes={}
def part(oid):
 did=occ[oid]['definition']
 if did not in defs:
  path=ROOT/dmap[did]['step'].lstrip('/');defs[did]=b.import_step(path);hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
 return defs[did].moved(poses[oid])
head=part('cylinder-head');rows=[]
for c in range(1,7):
 for k in ['intake','exhaust']:
  tag=f'c{c}-{k}';shim=part(tag+'-guide');fulcrum=part(tag+'-fulcrum')
  for a,shape1,bid,shape2 in [(tag+'-guide',shim,'cylinder-head',head),(tag+'-guide',shim,tag+'-fulcrum',fulcrum)]:
   rows.append({'a':a,'b':bid,'gap_mm':shape1.distance_to(shape2)})
fail=[r for r in rows if r['gap_mm']>.002];report={'status':'PASS' if not fail else 'FAIL','candidate_manifest_sha256':hashlib.sha256((OUT/'manifest.json').read_bytes()).hexdigest(),'source_step_hashes':hashes,'contacts':rows,'failures':fail};(OUT/'support-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],len(rows),fail);sys.exit(bool(fail))
