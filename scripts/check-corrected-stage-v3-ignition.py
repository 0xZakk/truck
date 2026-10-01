"""Root replay: guarded composition, installed-frame mesh bounds and audit identity."""
from pathlib import Path
import copy, hashlib, importlib.util, json, sys
import numpy as np, trimesh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from assembly_clockwise_candidate import transforms
sha=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
load=lambda p:json.loads((ROOT/p).read_text())
spec=importlib.util.spec_from_file_location('composer',ROOT/'scripts/compose-corrected-engine-ignition-stage.py')
composer=importlib.util.module_from_spec(spec);spec.loader.exec_module(composer)
v2='inventory/engine/corrected-engine-stage-v2.json';v3='inventory/engine/corrected-engine-stage-v3.json'
pp='inventory/engine/shifted-ignition-lead-integration-proposal.json'
m,p,staged=load(v2),load(pp),load(v3)
replay,assets,counts=composer.compose(m,p,sha(v2));assert replay==staged
controls=[]
for name,edit in [('stale before',lambda q:q['definitions'][0]['before'].update(name='wrong')),
                  ('duplicate row',lambda q:q['definitions'].append(copy.deepcopy(q['definitions'][0]))),
                  ('stale asset',lambda q:q['definitions'][0]['copy_assets']['step'].update(sha256='0'*64)),
                  ('double translation',lambda q:q['occurrences'][0]['after'].update(position_cad_mm=[1,0,0]))]:
 bad=copy.deepcopy(p);edit(bad)
 try:composer.compose(m,bad,sha(v2))
 except ValueError:controls.append(name)
 else:raise AssertionError(name)
inputs={x:sha(x) for x in [v2,v3,pp,'scripts/check-corrected-stage-v3-ignition.py','scripts/compose-corrected-engine-ignition-stage.py','cad/engine/assembly_clockwise_candidate.py']}
for file,key in [('inventory/engine/shifted-ignition-lead-delivery.json','bindings'),('inventory/engine/shifted-ignition-lead-neighbor-validation.json','inputs')]:
 report=load(file);inputs[file]=sha(file)
 for f,h in report[key].items():assert sha(f)==h,f;inputs[f]=h
inputs.update(assets)
poses=transforms(staged,0,0);definitions={d['id']:d for d in staged['definitions']};checks=[]
for update in p['occurrences']:
 o=update['after'];d=definitions[o['definition']]
 sp=d['step'].lstrip('/');gp=d['glb'].lstrip('/')
 shape=b.import_step(ROOT/sp);mesh=trimesh.load(ROOT/gp,force='mesh')
 assert shape.is_valid and len(shape.solids())==1
 assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
 vertices=mesh.vertices[:,[0,2,1]]*[1,-1,1]*1000
 t=poses[o['id']].wrapped.Transformation();rotation=np.array([[t.Value(i,j)for j in range(1,4)]for i in range(1,4)]);offset=np.array([t.Value(i,4)for i in range(1,4)])
 world=vertices@rotation.T+offset;bounds=(poses[o['id']]*shape).bounding_box()
 error=float(np.max(abs(np.array([world.min(0),world.max(0)])-np.array([list(bounds.min),list(bounds.max)]))))
 assert error<.025,(o['id'],error)
 checks.append({'id':o['id'],'world_bounds_error_mm':error})
assert len(checks)==28
assert all(sha(f)==h for f,h in inputs.items())
report={'status':'PASS root ignition stage replay; other engine gates remain open','world_checks':checks,'negative_controls':controls,'bindings':inputs,'visual_review':'Root inspected actual exported route projection and cap-local boot/contact mesh section. This shows coherent endpoints and rings, not factory route certification.','remaining_scope':'No browser or installed acceptance; unrelated cover/block/gasket and source gaps persist.','canonical_modified':False}
(ROOT/'inventory/engine/corrected-stage-v3-ignition-replay.json').write_text(json.dumps(report,indent=2)+'\n')
print(report['status'],len(checks),'parts; max',max(x['world_bounds_error_mm']for x in checks))
