"""Compare installed source-v2 solids/poses with the accepted predecessor delta."""
from pathlib import Path
import argparse,json,sys,hashlib
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
from cad_metrics import solid_volume,step_comparison_shape
from valve_source_integration import replacements,annotate_manifest,candidate_transforms
from valve_source_definition_adapter import replacement
import valve_source_layout as v
p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path,required=True);a=p.parse_args()
raw=(ROOT/'inventory/engine/full-assembly.json').read_bytes();m=json.loads(raw);assert m['valvetrain_model']=='source-sized-v2'
base=json.loads((a.baseline/'manifest.json').read_text());ds={d['id']:d for d in m['definitions']}
inputs={k:b.import_step(a.baseline/(k+'.step')) for k in ['cylinder-head','lifter-body','intake-valve','exhaust-valve']}
expected=replacements(inputs,base);rows=[];hashes={}
def vol(s):return sum(solid_volume(q,'adaptive') for q in s.solids()) if s else 0
for key,wanted in expected.items():
 path=ROOT/ds[key]['step'].lstrip('/');hashes[key]=hashlib.sha256(path.read_bytes()).hexdigest();actual=b.import_step(path)
 wanted=step_comparison_shape(wanted);delta=vol(actual-wanted)+vol(wanted-actual)
 assert delta<.02,(key,delta)
 repeated=replacement(key,actual,m);idempotence=vol(actual-repeated)+vol(repeated-actual)
 assert idempotence<.02,(key,'refresh drift',idempotence)
 rows.append({'part':key,'symmetric_difference_mm3':delta,'adapter_idempotence_mm3':idempotence})
 print('PASS installed',key,flush=True)
expected_manifest=annotate_manifest(base);count=0
for angle in [0,45,90,135,180,225,246,270,315,333,342,360,405,450,468,495,540,585,630,675,720]:
 actual=transforms(m,angle);wanted=candidate_transforms(expected_manifest,angle)
 for o in m['occurrences']:
  if not o.get('valvetrain'):continue
  for point in [(0,0,0),(1,0,0),(0,1,0),(0,0,1)]:
   difference=(b.Vertex(*point).moved(actual[o['id']]).center()-b.Vertex(*point).moved(wanted[o['id']]).center()).length
   assert difference<1e-8,(angle,o['id'],difference);count+=1
assert raw==(ROOT/'inventory/engine/full-assembly.json').read_bytes()
assert all(hashlib.sha256((ROOT/ds[k]['step'].lstrip('/')).read_bytes()).hexdigest()==h for k,h in hashes.items())
report={'status':'PASS','manifest_sha256':hashlib.sha256(raw).hexdigest(),'parts':rows,'pose_basis_comparisons':count,'step_sha256':hashes,'scope':'Installed delta versus predecessor, persistent adapter idempotence and phase placement; does not prove factory contours or installed part identity.'}
(ROOT/'inventory/engine/valve-source-installed-desktop-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',count,'pose basis comparisons',flush=True)
