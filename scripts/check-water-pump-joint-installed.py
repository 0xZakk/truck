"""Compare installed pump candidate against an accepted unchanged pre-joint baseline."""
from pathlib import Path
import argparse,hashlib,json,sys
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from cad_metrics import solid_volume,step_comparison_shape
from assembly_math import transforms
import water_pump_joint_candidate as p
import water_pump_thermactor_foot_candidate as t
parser=argparse.ArgumentParser();parser.add_argument('--baseline-root',type=Path,required=True);args=parser.parse_args();BASE=args.baseline_root.resolve()
r=json.loads((BASE/'inventory/engine/water-pump-joint-candidate-validation.json').read_text());assert r['inputs_unchanged'] and not r['collisions']
rawbase=(BASE/'inventory/engine/full-assembly.json').read_bytes();assert hashlib.sha256(rawbase).hexdigest()==r['manifest_sha256']
for path,digest in r['input_hashes'].items():assert hashlib.sha256((BASE/path).read_bytes()).hexdigest()==digest,path
for path in ('cad/engine/water_pump_joint_candidate.py','cad/engine/water_pump_thermactor_foot_candidate.py','cad/engine/water_pump_gasket_topology_candidate.py'):
 assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==r['input_hashes'][path],path
base=json.loads(rawbase);defs={d['id']:d for d in base['definitions']}
def old(key):
 path=defs[key]['step'].lstrip('/');assert hashlib.sha256((BASE/path).read_bytes()).hexdigest()==r['step_hashes'][path];return b.import_step(BASE/path)
raw=(ROOT/'inventory/engine/full-assembly.json').read_bytes();m=json.loads(raw);ds={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};actual=transforms(m);expected_poses=transforms(p.shifted_manifest(base))
expected={'block':p.block_interface(t.block_interface(old('block'))),'water-pump-housing':p.housing_interface(old('water-pump-housing')),'water-pump-gasket':p.gasket_shape(),'water-pump-shaft':p.shaft_shape(),'water-pump-impeller':p.impeller_interface(old('water-pump-impeller')),'water-pump-mounting-screw':p.screw_shape(),'thermactor-support-bracket':t.support(),'thermactor-engine-bolt-2':t.upper_bolt()}
def vol(s):return sum(solid_volume(q,'adaptive') for q in s.solids()) if s else 0
checks={};frozen={}
for key,s in expected.items():
 path=ROOT/ds[key]['step'].lstrip('/');frozen[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest();a=b.import_step(path);assert a.is_valid and len(a.solids())==1,key
 normalized=step_comparison_shape(s);difference=vol(a-normalized)+vol(normalized-a);assert difference<.02,(key,difference);checks[key]=difference;print('Installed match',key,flush=True)
active={'water-pump-assembly','fan-clutch-assembly'}
while True:
 more=active|{a['id'] for a in base['assemblies'] if a['parent'] in active}
 if more==active:break
 active=more
ids={o['id'] for o in base['occurrences'] if o['parent'] in active or o['id'] in ('heater-pump-return-elbow','thermactor-support-bracket','thermactor-engine-bolt-2')}
for n,(y,z) in enumerate(p.MOUNTING,1):
 key=f'water-pump-mounting-screw-{n}';assert occ[key]['definition']=='water-pump-mounting-screw';expected_poses[key]=b.Pos(*p.PUMP_POSITION)*b.Pos(-51,y,z);ids.add(key)
for key in ids:
 for point in ((0,0,0),(1,0,0),(0,1,0),(0,0,1)):
  a=b.Vertex(*point).moved(actual[key]).center();e=b.Vertex(*point).moved(expected_poses[key]).center();assert (a-e).length<1e-9,(key,point)
assert raw==(ROOT/'inventory/engine/full-assembly.json').read_bytes() and all(hashlib.sha256((ROOT/q).read_bytes()).hexdigest()==h for q,h in frozen.items())
(ROOT/'inventory/engine/water-pump-joint-installed-validation.json').write_text(json.dumps({'manifest_sha256':hashlib.sha256(raw).hexdigest(),'baseline_manifest_sha256':r['manifest_sha256'],'symmetric_difference_mm3':checks,'rigid_poses_checked':len(ids),'step_hashes':frozen,'scope':'Installed definitions and poses; belt path, moving hardware, completeengine and browser checks remain separate.'},indent=2)+'\n');print('PASS installed pump candidate comparison')
