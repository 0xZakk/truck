"""Independent material, passage, preserved datum and STEP checks for inlet."""
from pathlib import Path
import sys,json,hashlib,argparse
import build123d as b
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import water_pump_joint_candidate as p,water_pump_inlet_v2_candidate as n
from cad_metrics import solid_volume
ap=argparse.ArgumentParser();ap.add_argument('--baseline-root',type=Path,required=True);a=ap.parse_args();BASE=a.baseline_root
mp=BASE/'inventory/engine/full-assembly.json';raw=mp.read_bytes();m=json.loads(raw);ds={d['id']:d for d in m['definitions']}
files=[ROOT/'reference/engine/water-pump-inlet-topology-reviewed.json',Path(__file__),Path(p.__file__),Path(n.__file__),ROOT/'cad/engine/cooling_connections.py',ROOT/'cad/engine/water_pump_gasket_topology_candidate.py',ROOT/'cad/engine/cad_metrics.py',ROOT/'reference/engine/water-pump-mounting-topology-reviewed.json'];hashes={str(q):hashlib.sha256(q.read_bytes()).hexdigest() for q in files}
def load(k):
 q=BASE/ds[k]['step'].lstrip('/');hashes[str(q)]=hashlib.sha256(q.read_bytes()).hexdigest();return b.import_step(q)
def volume(s):
 if not s:return 0
 if isinstance(s,b.ShapeList):s=b.Compound(children=list(s))
 return solid_volume(s,'adaptive')
def sym(a,c):return volume(a-c)+volume(c-a)
old=p.housing_interface(load('water-pump-housing'));new=n.housing_interface(old)
assert new.is_valid and len(new.solids())==1
back=b.Pos(-100,0,0)*b.Box(98,400,400) # endsX−51
# Dry-side seal/bearing/nose core must not be opened by the inlet passage.
dry=p.cx(24,11,72)
probe=n.open_probe()+p.cx(2,-54,-19,10,-12)
neck_ring=n.cy(23,118,137)-n.cy(21,117,138)
checks={
 'back_flange_symmetric_difference_mm3':sym(new&back,old&back),
 'dry_nose_material_symmetric_difference_mm3':sym(new&dry,old&dry),
 'open_probe_obstruction_mm3':volume(new&probe),
 'neck_ring_missing_mm3':volume(neck_ring-new),
 'added_neck_volume_mm3':volume(new-old),
 'removed_passage_volume_mm3':volume(old-new),
 'cast_arm_original_contact_mm3':volume(n.outer()&old),
 'probe_solids':len(probe.solids())
}
assert checks['back_flange_symmetric_difference_mm3']<.02,checks
assert checks['dry_nose_material_symmetric_difference_mm3']<.02,checks
assert checks['open_probe_obstruction_mm3']<.02,checks
assert checks['neck_ring_missing_mm3']<.02,checks
assert checks['added_neck_volume_mm3']>1000 and checks['removed_passage_volume_mm3']>100 and checks['cast_arm_original_contact_mm3']>100,checks
assert checks['probe_solids']==1,checks
for key in ['water-pump-seal','water-pump-bearing','water-pump-slinger']:
 checks[key+'_new_cut_contact_mm3']=volume(load(key)&n.passage());assert checks[key+'_new_cut_contact_mm3']<.02,checks
path=Path('/private/tmp/water-pump-inlet-v2-housing.step');b.export_step(new,path);again=b.import_step(path)
checks['step_symmetric_difference_mm3']=sym(new,again);assert again.is_valid and len(again.solids())==1 and checks['step_symmetric_difference_mm3']<.02,checks
# Actual CAD mesh artifacts for assembled and horizontal inlet-axis section.
parts={'housing':new,'impeller':p.impeller_interface(load('water-pump-impeller')),'shaft':p.shaft_shape(),'seal':load('water-pump-seal')}
colors=['#81989c','#c89547','#b3bfc8','#34424b']
for cut in [False,True]:
 arrays={};ids=[];used_colors=[]
 for (key,s),color in zip(parts.items(),colors):
  if cut:s=s&(b.Pos(0,0,-112)*b.Box(500,500,200)) # topZ−12, cut through inlet axis
  if not s:continue
  if isinstance(s,b.ShapeList):s=b.Compound(children=list(s))
  if not s.solids():continue
  vertices,faces=s.tessellate(.35);idx=len(ids);ids.append(key);used_colors.append(color)
  arrays[f'vertices_{idx}']=np.array([[v.X,v.Y,v.Z] for v in vertices]);arrays[f'faces_{idx}']=np.array(faces)
 arrays['metadata']=json.dumps({'parts':ids,'colors':used_colors});np.savez('/private/tmp/water-pump-inlet-v2-'+('cutaway' if cut else 'actual')+'.npz',**arrays)
unchanged=mp.read_bytes()==raw and all(hashlib.sha256(Path(q).read_bytes()).hexdigest()==h for q,h in hashes.items());assert unchanged
report={'baseline_manifest_sha256':hashlib.sha256(raw).hexdigest(),'inputs_unchanged':unchanged,'input_hashes':hashes,'checks':checks,'step_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'limits':n.GAPS,'status':'PASS'}
(ROOT/'inventory/engine/water-pump-inlet-v2-interfaces-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(checks,indent=2));print('PASS inlet interfaces and STEP')
