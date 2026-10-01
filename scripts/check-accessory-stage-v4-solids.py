#!/usr/bin/env python3
"""Frozen v4 q0 affected-solid audit. No CAD or assembly mutation.

Internal same-group pairs are tested, not silently accepted: byte identity and
relative-frame parity only classify any resulting overlap as inherited at q0.
"""
from pathlib import Path
import hashlib, itertools, json, sys, time
import numpy as np
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_clockwise_candidate import transforms, occurrence_shape
from cad_metrics import solid_volume
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
MP=R/'inventory/engine/corrected-engine-stage-v4.json'
BP=R/'inventory/engine/corrected-engine-stage-v3.json'
CP=R/'inventory/engine/accessory-coordinated-stage-contract.json'
OUT=R/'cad/engine/generated/accessory-stage-v4-solids'
REPORT=R/'inventory/engine/accessory-stage-v4-solids.json'
EXPECTED='9da33ca507e31cf6d906d4ee2c92b87a64ba01db7abea8f14b72f244631f9fe9'

def matrix(p):
 t=p.wrapped.Transformation()
 return np.array([[t.Value(i,j) for j in range(1,5)] for i in range(1,4)]+[[0,0,0,1.]])

def main():
 assert sha(MP)==EXPECTED,'v4 changed'
 c=json.loads(CP.read_text());m=json.loads(MP.read_text());prior=json.loads(BP.read_text())
 assert sha(BP)==c['manifest_sha256']
 inputs={str(p.relative_to(R)):sha(p) for p in [MP,BP,CP,Path(__file__)]}
 for p,h in c['input_sha256'].items():
  assert sha(R/p)==h,p
  inputs[p]=h
 canonical=R/'inventory/engine/full-assembly.json';inputs[str(canonical.relative_to(R))]=sha(canonical)
 groups={n:g for g,ns in c['moving_occurrence_ownership'].items() for n in ns}
 assert len(groups)==sum(map(len,c['moving_occurrence_ownership'].values()))==173
 carriers={x['id'] for x in c['carrier_replacements']};affected=set(groups)|carriers
 occ={x['id']:x for x in m['occurrences']};oldocc={x['id']:x for x in prior['occurrences']}
 defs={x['id']:x for x in m['definitions']};olddefs={x['id']:x for x in prior['definitions']}
 assert set(occ)==set(oldocc) and affected<=set(occ)
 for edit in c['pose_edits']:
  assert next(x for x in prior[edit['table']] if x['id']==edit['id'])==edit['before']
  assert next(x for x in m[edit['table']] if x['id']==edit['id'])==edit['after']
 for x in c['carrier_replacements']:
  for kind,asset in x['replacement_assets'].items():
   assert defs[x['id']][kind].lstrip('/')==asset['path']
   assert sha(R/asset['path'])==asset['sha256']
 paths={k:R/d['step'].lstrip('/') for k,d in defs.items()}
 oldpaths={k:R/d['step'].lstrip('/') for k,d in olddefs.items()}
 for p in set(paths.values())|set(oldpaths.values()):inputs[str(p.relative_to(R))]=sha(p)
 poses=transforms(m,0,0);oldposes=transforms(prior,0,0)
 mats={n:matrix(poses[n]) for n in occ};oldmats={n:matrix(oldposes[n]) for n in occ}
 samebytes={n:sha(paths[o['definition']])==sha(oldpaths[oldocc[n]['definition']]) for n,o in occ.items()}
 for n in occ:
  expected=oldmats[n].copy()
  if n in groups:expected[:3,3]+=c['delta_world_mm'][groups[n]]
  assert np.max(abs(mats[n]-expected))<1e-8,n
  assert samebytes[n] or n in carriers,n
 r={'status':'RUNNING','scope':'q=0 axial=0 compressor=0; 173 moved occurrences plus two replaced carriers versus entire stage; no motion, retention, distance or containment acceptance',
    'threshold_mm3':0.1,'broadphase_padding_mm':2.0,'stage_sha256':EXPECTED,'input_sha256':inputs,
    'affected_occurrences':sorted(affected),'group_ownership':groups,'occurrence_geometry':{},'bounds':{},
    'exact_checks':[],'conflicts':[],'errors':[],
    'internal_classification':'Same STEP hashes and q0 relative matrices classify inherited rigid pairs; every broadphase pair still tested. No assumed internal acceptance.',
    'known_open':c['retained_failures'],'static_only':True}
 OUT.mkdir(exist_ok=True)
 def save():REPORT.write_text(json.dumps(r,indent=2)+'\n')
 save();local={};placed={};bounds={}
 for i,(n,o) in enumerate(occ.items(),1):
  try:
   p=paths[o['definition']]
   if p not in local:local[p]=b.import_step(p)
   shape=poses[n]*occurrence_shape(o,local[p],0,0)
   assert shape.is_valid and len(shape.solids())>0,'invalid/empty posed solid'
   placed[n]=shape;bb=shape.bounding_box();bounds[n]=np.array([tuple(bb.min),tuple(bb.max)])
   r['bounds'][n]=bounds[n].tolist()
   r['occurrence_geometry'][n]={'step':str(p.relative_to(R)),'sha256':sha(p),'matrix':mats[n].tolist(),'solid_count':len(shape.solids())}
  except Exception as e:r['errors'].append({'occurrence':n,'error':repr(e)})
  if i%100==0:print('PLACED',i,'/',len(occ),flush=True);save()
 pairs=[];separated=0;unaffected=0
 for a,z in itertools.combinations(occ,2):
  if not ({a,z}&affected):unaffected+=1;continue
  if a not in bounds or z not in bounds:continue
  extent=np.minimum(bounds[a][1],bounds[z][1])-np.maximum(bounds[a][0],bounds[z][0])
  if np.any(extent < -2.0):separated+=1;continue
  pairs.append((a,z))
 r.update(broadphase_candidates=len(pairs),bounds_separated_affected_pairs=separated,unaffected_pairs_out_of_scope=unaffected)
 save();print('PAIRS',len(pairs),flush=True)
 # Analytical duplicate-solid control verifies the same measurement rejects an overlap.
 cube=b.Box(1,1,1);control=solid_volume(cube.intersect(cube))
 assert control>.1;r['fault_control']={'one_mm_cube_overlap_mm3':control,'detected':True}
 for index,(a,z) in enumerate(pairs,1):
  relerr=float(np.max(abs(np.linalg.inv(mats[a])@mats[z]-np.linalg.inv(oldmats[a])@oldmats[z])))
  invariant=groups.get(a) is not None and groups.get(a)==groups.get(z) and samebytes[a] and samebytes[z] and relerr<1e-8
  row={'a':a,'b':z,'classification':'inherited same-group rigid relation at q0' if invariant else 'fresh affected interface','relative_frame_error':relerr,'same_step_bytes_as_v3':[samebytes[a],samebytes[z]]}
  try:
   common=placed[a].intersect(placed[z])
   if isinstance(common,b.ShapeList):common=b.Compound(common)
   v=solid_volume(common) if common else 0.;row['overlap_mm3']=v
   if common and common.solids() and not common.is_valid:raise ValueError('invalid intersection')
   if v>.1:
    wp=OUT/(a+'__'+z+'.step');b.export_step(common,wp)
    row.update(witness_step=str(wp.relative_to(R)),witness_sha256=sha(wp),overlap_bounds_mm=[list(common.bounding_box().min),list(common.bounding_box().max)])
    r['conflicts'].append(row)
    try:row['adaptive_overlap_mm3']=sum(abs(solid_volume(s,'adaptive')) for s in common.solids())
    except Exception as e:row['adaptive_error']=repr(e);r['errors'].append(row.copy())
    print('OVERLAP',a,z,v,row['classification'],flush=True)
  except Exception as e:row['error']=repr(e);r['errors'].append(row.copy());print('ERROR',a,z,repr(e),flush=True)
  r['exact_checks'].append(row)
  if index%20==0 or 'witness_step' in row:save()
  if index%50==0:print('CHECKED',index,'/',len(pairs),flush=True)
 r['input_changes_after_run']=[p for p,h in inputs.items() if sha(R/p)!=h]
 r['status']='FAIL: overlaps or errors retained' if r['conflicts'] or r['errors'] or r['input_changes_after_run'] else 'PASS bounded affected-solid q0 only'
 r['counts']={'exact':len(r['exact_checks']),'conflicts':len(r['conflicts']),'errors':len(r['errors']),'inherited_rigid_conflicts':sum(x['classification'].startswith('inherited') for x in r['conflicts'])}
 save();print(r['status'],r['counts'],flush=True)
if __name__=='__main__':main()
