"""All actual saved STEP engine neighbors at q0; candidate substitutions in memory only."""
from pathlib import Path
import sys,json,time
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_clockwise_candidate import transforms,occurrence_shape
import waterpump_source_offset_inlet_candidate as c
from cad_metrics import solid_volume
mp=R/'inventory/engine/corrected-engine-stage-v3.json';m=json.loads(mp.read_text());poses=transforms(m,0,0);defs={q['id']:q for q in m['definitions']};inputs={str(mp.relative_to(R)):c.rear.sha(mp),str(Path(__file__).relative_to(R)):c.rear.sha(Path(__file__))}
shapes={};bounds={};sourcepaths={}
def bb(s):return np.array([tuple(s.bounding_box().min),tuple(s.bounding_box().max)])
def vol(s):return sum(abs(solid_volume(q,'adaptive'))for q in s.solids())if s else 0.
variants={k:b.import_step(c.O/(k+'-housing.step'))for k in ['nominal','low-offset','high-offset']};vbb={k:bb(s)for k,s in variants.items()}
for k in variants:
 p=c.O/(k+'-housing.step');inputs[str(p.relative_to(R))]=c.rear.sha(p)
overrides={'timing-cover':c.rear.O/'cover.step','timing-cover-main-gasket':c.rear.O/'main-gasket.step','water-pump-gasket':c.rear.O/'pump-gasket.step'}
rows=[];excluded=[];errors=[];count=0
for o in m['occurrences']:
 key=o['id']
 if key=='water-pump-housing':continue
 if key in overrides:
  p=overrides[key];s=b.import_step(p);inputs[str(p.relative_to(R))]=c.rear.sha(p)
 else:
  p=R/defs[o['definition']]['step'].lstrip('/');inputs[str(p.relative_to(R))]=c.rear.sha(p)
  if p not in shapes:shapes[p]=b.import_step(p)
  # Actual q0 adapter geometry, including deformedsprings; do not reuse legacyshapes.
  s=poses[key]*occurrence_shape(o,shapes[p],0,0)
 box=bb(s);count+=1;tested=False
 for name,housing in variants.items():
  if np.any(np.minimum(box[1],vbb[name][1])-np.maximum(box[0],vbb[name][0])<=0):continue
  tested=True
  try:
   hit=housing.intersect(s);v=vol(hit);row={'variant':name,'neighbor':key,'overlap_mm3':v}
   if v>.1:
    row['bounds_mm']=bb(hit).tolist();wp=c.O/(name+'__'+key+'.step');b.export_step(hit,wp);row['witness']=str(wp.relative_to(R));row['witness_sha256']=c.rear.sha(wp);print('OVERLAP',row,flush=True)
   rows.append(row)
  except Exception as e:errors.append({'variant':name,'neighbor':key,'error':str(e)});print('ERROR',errors[-1],flush=True)
 if not tested:excluded.append(key)
 if count%75==0:print('CHECKED',count,'exact',len(rows),flush=True)
for p in [R/'cad/engine/assembly_clockwise_candidate.py',R/'cad/engine/cam_clockwise_candidate.py',R/'cad/engine/valve_spring_seating_candidate.py',Path(c.__file__)]:inputs[str(p.relative_to(R))]=c.rear.sha(p)
conflicts=[q for q in rows if q['overlap_mm3']>.1];r={'status':'FAIL actual neighbors'if conflicts else'INCONCLUSIVE'if errors else'PASS all-engine staticq0 neighbors','stage_sha256':c.rear.sha(mp),'occurrences_checked':count,'exact_pairs':rows,'bounds_excluded_all_variants':excluded,'conflicts':conflicts,'errors':errors,'substitutions_world_step':{k:str(p.relative_to(R))for k,p in overrides.items()},'inputs':inputs,'limits':['No canonical/stage writes; q0only, no wholeenginecontinuousmotion.','Three offsets are photo-derived sensitivity bounds, not a continuous sweep or manufacturing tolerance.','Unmodeledradiatorhose/fittings excluded byabsence, not claimedclear.']};assert all(c.rear.sha(R/p)==h for p,h in inputs.items());(R/'inventory/engine/waterpump-source-offset-inlet-neighbors.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],len(conflicts),flush=True)
