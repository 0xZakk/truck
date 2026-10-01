#!/usr/bin/env python3
"""Compare found overlaps with actual canonical poses and seven-support source stock."""
from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_math import transforms as canonical_poses
from assembly_clockwise_candidate import transforms as stage_poses
from cad_metrics import solid_volume
import timing_cover_seven_fastener_candidate as seven
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mp=R/'inventory/engine/corrected-engine-stage.json';bp=R/'inventory/engine/full-assembly.json';ap=R/'inventory/engine/corrected-stage-changed-neighbors.json';audit=json.loads(ap.read_text());assert audit['stage_sha256']==sha(mp)
m=json.loads(mp.read_text());base=json.loads(bp.read_text());poses=stage_poses(m,0,0);oldposes=canonical_poses(base,0);occ={o['id']:o for o in m['occurrences']};oldocc={o['id']:o for o in base['occurrences']};defs={d['id']:d for d in m['definitions']};olddefs={d['id']:d for d in base['definitions']};inputs={str(p.relative_to(R)):sha(p)for p in [Path(__file__),mp,bp,ap,Path(seven.__file__),seven.BLOCK]};cache={}
def get(oid,old=False):
 oo=oldocc if old else occ;dd=olddefs if old else defs;pp=oldposes if old else poses;p=R/dd[oo[oid]['definition']]['step'].lstrip('/');inputs[str(p.relative_to(R))]=sha(p)
 if p not in cache:cache[p]=b.import_step(p)
 return pp[oid]*cache[p]
def norm(s):return b.Compound(children=list(s))if isinstance(s,b.ShapeList)else s
def metric(s):
 s=norm(s)
 if s is None:return {'default_mm3':0.,'adaptive_mm3':0.}
 v=solid_volume(s)
 if v<1e-8:return {'default_mm3':v,'adaptive_mm3':0.}
 try:return {'default_mm3':v,'adaptive_mm3':sum(abs(solid_volume(x,'adaptive'))for x in s.solids())}
 except Exception as e:return {'default_mm3':v,'adaptive_error':str(e)}
prior=b.import_step(seven.BLOCK);current=get('block');rows=[];supportrows=[];O=R/'cad/engine/generated/corrected-stage-changed-neighbors';out=R/'inventory/engine/corrected-stage-overlap-classification.json'
def save():out.write_text(json.dumps({'status':'RUNNING','rows':rows,'block_support_attribution':supportrows,'input_sha256':inputs},indent=2)+'\n')
for i,hit in enumerate(audit['conflicts'],1):
 a,z=hit['a'],hit['b'];row={'a':a,'b':z,'current_overlap_mm3':hit['adaptive_overlap_mm3'],'current_witness_step':hit['witness_step']}
 if a in oldocc and z in oldocc:
  baseline=metric(get(a,True).intersect(get(z,True)));row['canonical_q0_overlap']=baseline;row['onset']='new staged geometry/pose relative to canonical q0'if baseline.get('adaptive_mm3',baseline['default_mm3'])<=.1 else'inherited canonical q0 overlap'
 else:row['onset']='new occurrence absent from canonical'
 if a.startswith('distributor-')and z.startswith('ignition-'):row['category']='shifted distributor against unchanged ignition leads'
 elif 'timing-cover-mounting-screw' in a+z:row['category']='new cover hardware external neighbor'
 elif a=='block':row['category']='changed block / FS10'
 elif z in ['front-seal','damper-hub']:row['category']='pending seal and hub integration'
 else:row['category']='changed cover / external neighbor'
 rows.append(row)
 if a=='block':
  neighbor=get(z);p=R/hit['witness_step'];inputs[str(p.relative_to(R))]=sha(p);common=b.import_step(p);oldcommon=norm(prior.intersect(neighbor));added=norm(common.cut(prior));removed=oldcommon.cut(current)if oldcommon else None;retained=common.intersect(prior)
  stock={'a':a,'b':z,'prior_v3_overlap':metric(oldcommon),'current_overlap':metric(common),'retained_prior_stock_overlap':metric(retained),'new_seven_support_overlap':metric(added),'removed_old_overlap':metric(removed),'support_stations':[]}
  for n,(y,zz)in enumerate(seven.AXES,1):
   if not added.solids() or metric(added)['default_mm3']<=1e-7:break
   support=seven.front.c.cx(seven.SUPPORT_RADIUS,seven.SUPPORT_BACK,373,y,zz);v=metric(added.intersect(support))
   if v['default_mm3']>1e-7:stock['support_stations'].append({'station':n,'axis_yz':[y,zz],'overlap':v})
  if metric(added)['default_mm3']>1e-7:
   wp=O/('new-seven-support-stock__'+z+'.step');b.export_step(added,wp);stock['added_stock_witness']=str(wp.relative_to(R));inputs[str(wp.relative_to(R))]=sha(wp)
  supportrows.append(stock)
 save();print(i,a,z,row['onset'],flush=True)
assert all(sha(R/p)==h for p,h in inputs.items())
r={'status':'COMPLETE diagnosis only; no geometry edits','rows':rows,'block_support_attribution':supportrows,'input_sha256':inputs,'limits':['Canonical comparison is q0 only; does not imply dynamic clearance','PriorV3 means before seven-support addition, not factory-correct stock','Waterpump/cover construction-onset detail owned separately by pump worker','Missing gasket/seal/oil route cannot pass a collision audit']};out.write_text(json.dumps(r,indent=2)+'\n')
