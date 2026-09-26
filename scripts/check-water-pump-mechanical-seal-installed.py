"""Compare installed illustrative seal definitions and poses to accepted study."""
from pathlib import Path
import sys,json,hashlib,argparse
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
from cad_metrics import solid_volume,step_comparison_shape
import water_pump_mechanical_seal_candidate as s
ap=argparse.ArgumentParser();ap.add_argument('--candidate-report',type=Path,required=True);ap.add_argument('--manifest',type=Path,default=ROOT/'inventory/engine/full-assembly.json');ap.add_argument('--report',type=Path,default=ROOT/'inventory/engine/water-pump-mechanical-seal-installed-validation.json');a=ap.parse_args();r=json.loads(a.candidate_report.read_text());assert r['status']=='PASS' and r['inputs_unchanged'] and not r['collisions']
expected_module=next(h for p,h in r['input_hashes'].items() if p.endswith('cad/engine/water_pump_mechanical_seal_candidate.py'));assert hashlib.sha256(Path(s.__file__).read_bytes()).hexdigest()==expected_module
for path,digest in r['input_hashes'].items():
 assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,('stale candidate input',path)
raw=a.manifest.read_bytes();assert hashlib.sha256(raw).hexdigest()==r['manifest_sha256'], 'Run candidate checker against this installed manifest first; neighbor transforms may have changed'
m=json.loads(raw);defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};poses=transforms(m);assert 'water-pump-seal' not in occ
hashes={};checks={}
def vol(q):return sum(solid_volume(v,'adaptive') for v in q.solids()) if q else 0
for key,shape in s.components().items():
 path=ROOT/defs[key]['step'].lstrip('/');hashes[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest();actual=b.import_step(path);expected=step_comparison_shape(shape);delta=vol(actual-expected)+vol(expected-actual);assert actual.is_valid and len(actual.solids())==1 and delta<.02,(key,delta);checks[key]=delta
 assert occ[key]['definition']==key and occ[key]['explode_cad_mm']==[s.EXPLODE_X[key],0,0]
 for point in [(0,0,0),(1,0,0),(0,1,0),(0,0,1)]:assert (b.Vertex(*point).moved(poses[key]).center()-b.Vertex(*point).moved(b.Pos(440,-32,170)).center()).length<1e-9,key
assert raw==a.manifest.read_bytes() and all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h for p,h in hashes.items())
a.report.write_text(json.dumps({'status':'PASS','manifest_sha256':hashlib.sha256(raw).hexdigest(),'step_hashes':{str(Path(p).relative_to(ROOT)):h for p,h in hashes.items()},'step_symmetric_difference_mm3':checks,'rigid_poses_checked':6,'scope':'Installed shape/pose/display-offset comparison only. Root must run current full-engine and browser checks.'},indent=2)+'\n');print('PASS installed illustrative mechanical seal')
