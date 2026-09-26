"""Installed inlet comparison against accepted source baseline; no mutations."""
from pathlib import Path
import sys,json,hashlib,argparse
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
from cad_metrics import solid_volume,step_comparison_shape
import water_pump_joint_candidate as p,water_pump_inlet_v3_candidate as n
ap=argparse.ArgumentParser();ap.add_argument('--baseline-root',type=Path,required=True);ap.add_argument('--candidate-report',type=Path,required=True);a=ap.parse_args();BASE=a.baseline_root
report_raw=a.candidate_report.read_bytes();r=json.loads(report_raw);assert r['inputs_unchanged'] and not r['collisions']
base_raw=(BASE/'inventory/engine/full-assembly.json').read_bytes();assert hashlib.sha256(base_raw).hexdigest()==r['manifest_sha256'];base=json.loads(base_raw);ds={d['id']:d for d in base['definitions']}
for path in [Path(p.__file__),Path(n.__file__)]:assert hashlib.sha256(path.read_bytes()).hexdigest()==r['input_hashes'][str(path.relative_to(ROOT))]
old_path=ds['water-pump-housing']['step'].lstrip('/');assert hashlib.sha256((BASE/old_path).read_bytes()).hexdigest()==r['step_hashes'][old_path]
expected=n.housing_interface(p.housing_interface(b.import_step(BASE/old_path)))
raw=(ROOT/'inventory/engine/full-assembly.json').read_bytes();m=json.loads(raw);defs={d['id']:d for d in m['definitions']};path=ROOT/defs['water-pump-housing']['step'].lstrip('/');step_hash=hashlib.sha256(path.read_bytes()).hexdigest();actual=b.import_step(path);assert actual.is_valid and len(actual.solids())==1
expected=step_comparison_shape(expected)
def vol(s):return sum(solid_volume(q,'adaptive') for q in s.solids()) if s else 0
difference=vol(actual-expected)+vol(expected-actual);assert difference<.02,difference
poses=transforms(m);wanted=transforms(p.shifted_manifest(base));ids=['water-pump-housing','water-pump-shaft','water-pump-gasket','water-pump-impeller','water-pump-seal','water-pump-bearing','water-pump-slinger','water-pump-drive-hub','water-pump-pulley','heater-pump-return-elbow']
for key in ids:
 for point in [(0,0,0),(1,0,0),(0,1,0),(0,0,1)]:assert (b.Vertex(*point).moved(poses[key]).center()-b.Vertex(*point).moved(wanted[key]).center()).length<1e-9,key
assert raw==(ROOT/'inventory/engine/full-assembly.json').read_bytes() and step_hash==hashlib.sha256(path.read_bytes()).hexdigest() and report_raw==a.candidate_report.read_bytes()
(ROOT/'inventory/engine/water-pump-inlet-v3-installed-validation.json').write_text(json.dumps({'status':'PASS','manifest_sha256':hashlib.sha256(raw).hexdigest(),'step_sha256':step_hash,'symmetric_difference_mm3':difference,'rigid_poses_checked':ids,'baseline_manifest_sha256':r['manifest_sha256']},indent=2)+'\n');print('PASS installed inlet housing and unchanged component poses')
