#!/usr/bin/env python3
"""Fresh v2 seal/hub/gasket delta checks; v1 failures remain open."""
from pathlib import Path
import sys,json,hashlib,itertools,time
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_clockwise_candidate import transforms,occurrence_shape
from cad_metrics import solid_volume
O=R/'cad/engine/generated/corrected-stage-v2-sealing-neighbors';O.mkdir(exist_ok=True)
REPORT=R/'inventory/engine/corrected-stage-v2-sealing-neighbors.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mp=R/'inventory/engine/corrected-engine-stage-v2.json';bp=R/'inventory/engine/corrected-engine-stage.json';m=json.loads(mp.read_text());base=json.loads(bp.read_text());poses=transforms(m,0,0);priorposes=transforms(base,0,0)
occ={x['id']:x for x in m['occurrences']};oldocc={x['id']:x for x in base['occurrences']};defs={d['id']:d for d in m['definitions']};olddefs={d['id']:d for d in base['definitions']}
inputs={str(p.relative_to(R)):sha(p)for p in [mp,bp,Path(__file__),R/'cad/engine/assembly_clockwise_candidate.py',R/'cad/engine/assembly_math.py',R/'cad/engine/cam_clockwise_candidate.py',R/'cad/engine/crossed_oil_drive_endplay_candidate.py',R/'cad/engine/timing_coupled_core_candidate.py',R/'cad/engine/cad_metrics.py',R/'cad/engine/valve_spring_seating_candidate.py']}
paths={k:R/d['step'].lstrip('/')for k,d in defs.items()};oldpaths={k:R/d['step'].lstrip('/')for k,d in olddefs.items()}
for p in set(paths.values())|set(oldpaths.values()):inputs[str(p.relative_to(R))]=sha(p)
def matrix(p):
 t=p.wrapped.Transformation();return np.array([[t.Value(i,j)for j in range(1,5)]for i in range(1,4)])
changed={};unchanged=[]
for key,o in occ.items():
 if key not in oldocc:changed[key]={'new_occurrence':True};continue
 old=oldocc[key];shapechange=inputs[str(paths[o['definition']].relative_to(R))]!=inputs[str(oldpaths[old['definition']].relative_to(R))];error=float(np.max(abs(matrix(poses[key])-matrix(priorposes[key]))))
 if shapechange or error>1e-9:changed[key]={'shape_changed':shapechange,'matrix_difference':error,'deformed_spring':o.get('valvetrain',{}).get('role')=='spring'}
 else:unchanged.append(key)
reuse=R/'inventory/engine/corrected-stage-changed-neighbor-summary.json';rr=json.loads(reuse.read_text())
inputs[str(reuse.relative_to(R))]=sha(reuse)
r={'status':'RUNNING','stage_sha256':inputs[str(mp.relative_to(R))],'scope':'q=0 axial=0, all actual saved STEP broadphase pairs with at least one changed shape/pose; no intentional-fit whitelist','changed_occurrences':changed,'unchanged_occurrences':unchanged,'unchanged_reuse':{'report':str(reuse.relative_to(R)),'sha256':sha(reuse),'scope':'V1 diagnostic only: unchanged pairs retain known failures; this is not whole-stage acceptance'},'spring_geometry':'Same corrected q0 deformation in both stages; not an independent spring re-audit','input_sha256':inputs,'exact_checks':[],'conflicts':[],'metric_errors':[],'known_open':m['integration_stage']['open'],'canonical_modified':False}
def save():REPORT.write_text(json.dumps(r,indent=2)+'\n')
save();parts={};placed={};bounds={}
for i,(key,path)in enumerate(paths.items(),1):
 parts[key]=b.import_step(path)
 if i%50==0:print('Loaded',i,'/',len(paths),flush=True)
for key,o in occ.items():
 placed[key]=poses[key]*occurrence_shape(o,parts[o['definition']],0,0);bb=placed[key].bounding_box();bounds[key]=np.array([tuple(bb.min),tuple(bb.max)])
pairs=[];separated=0;reused=0
for a,z in itertools.combinations(occ,2):
 if a not in changed and z not in changed:reused+=1;continue
 extent=np.minimum(bounds[a][1],bounds[z][1])-np.maximum(bounds[a][0],bounds[z][0])
 if np.any(extent<=0):separated+=1;continue
 pairs.append((a,z))
r['removed_occurrences']=sorted(set(oldocc)-set(occ));r['known_v1_failure_pairs']=77
r.update(broadphase_candidates=len(pairs),bounds_separated_affected_pairs=separated,identical_shape_pose_pairs_reused=reused);save();print('PAIRCOUNT',len(pairs),'changed',len(changed),flush=True)
for index,(a,z)in enumerate(pairs,1):
 row={'a':a,'b':z,'actual_deformed_spring_pair':any(occ[k].get('valvetrain',{}).get('role')=='spring'for k in[a,z])}
 try:
  common=placed[a].intersect(placed[z]);v=solid_volume(common)if common else 0.;row['default_overlap_mm3']=v
  if v>.1:
   try:row['adaptive_overlap_mm3']=sum(abs(solid_volume(s,'adaptive'))for s in common.solids())
   except Exception as e:row['adaptive_metric_error']=str(e);r['metric_errors'].append(row)
   bb=common.bounding_box();row['overlap_conservative_bounds_mm']=[list(bb.min),list(bb.max)]
   witness=None
   for s in common.solids():
    point=tuple(s.center())
    if placed[a].is_inside(point,tolerance=1e-7)and placed[z].is_inside(point,tolerance=1e-7):witness=point;break
   row['strict_interior_witness']=witness
   wp=O/(a+'__'+z+'.step');b.export_step(common,wp);row['witness_step']=str(wp.relative_to(R));row['witness_sha256']=sha(wp);r['conflicts'].append(row);print('OVERLAP',a,z,v,flush=True)
 except Exception as e:row['error']=str(e);r['metric_errors'].append(row);print('ERROR',a,z,str(e),flush=True)
 r['exact_checks'].append(row)
 if index%20==0 or 'witness_step'in row:save()
 if index%50==0:print('CHECKED',index,'/',len(pairs),'conflicts',len(r['conflicts']),flush=True)
assert all(sha(R/p)==h for p,h in inputs.items())
r['status']='FAIL overlaps found; incomplete private stage'if r['conflicts']else('INCONCLUSIVE metric errors remain'if r['metric_errors']else'PASS v2 changed-neighbor delta only; unrelated v1 failures remain');save();print(r['status'],flush=True)
