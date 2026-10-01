#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,collections
R=Path(__file__).resolve().parents[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names=['corrected-stage-changed-neighbors','corrected-stage-overlap-classification','corrected-stage-audit-negative-control','timing-waterpump-cover-datum-audit'];reports={};bindings={};objects={}
for name in names:
 p=R/'inventory/engine'/(name+'.json');r=json.loads(p.read_text());objects[name]=r;reports[str(p.relative_to(R))]=sha(p)
 for key in ['input_sha256','inputs']:
  for path,value in r.get(key,{}).items():
   if isinstance(value,str)and len(value)==64:assert sha(R/path)==value,path;bindings[path]=value
# Frozen original cam/valve law transitive sources are independently still bound.
p=R/'inventory/engine/cam-clockwise-candidate-delivery-validation.json';delivery=json.loads(p.read_text());reports[str(p.relative_to(R))]=sha(p)
for path,value in delivery['transitive_source_sha256'].items():assert sha(R/path)==value,path;bindings[path]=value
a=objects['corrected-stage-changed-neighbors'];c=objects['corrected-stage-overlap-classification'];assert len(a['exact_checks'])==a['broadphase_candidates']==2212 and len(a['conflicts'])==77 and not a['metric_errors'];assert len(c['rows'])==77
assert all(x.get('adaptive_overlap_mm3',0)>.1 for x in a['conflicts'])
for x in c['rows']:
 if 'canonical_q0_overlap'in x:assert x['canonical_q0_overlap']['adaptive_mm3']<=.1 and 'adaptive_error'not in x['canonical_q0_overlap']
for x in a['conflicts']:assert sha(R/x['witness_step'])==x['witness_sha256']
assert objects['corrected-stage-audit-negative-control']['detected_overlap_mm3']>100
r={'status':'FAIL private staged neutral assembly:77 actual overlapping pairs','checked_event_degrees':0,'axial_mm':0,'changed_occurrences':len(a['changed_occurrences']),'unchanged_occurrences':len(a['unchanged_occurrences']),'exact_changed_neighbor_pairs':2212,'bounds_separated_affected_pairs':a['bounds_separated_affected_pairs'],'identical_shape_pose_pairs_reused':a['identical_shape_pose_pairs_reused'],'category_counts':dict(collections.Counter(x['category']for x in c['rows'])),'canonical_comparison_counts':dict(collections.Counter(x['onset']for x in c['rows'])),'converged_positive_overlap_pairs':77,'strict_interior_center_witness_pairs':sum(x['strict_interior_witness']is not None for x in a['conflicts']),'block_source_attribution':c['block_support_attribution'],'open_noncollision_dependencies':a['known_open'],'reports_sha256':reports,'verified_input_sha256':bindings,'checker_sha256':sha(Path(__file__)),'limits':['Static q0 only; prior rod-bolt/block motion failure remains open despite no q0 rod hit','Exact positive overlap does not identify a permissible manufacturing repair','Seals/gaskets/pump circuit/lead reach require interface acceptance beyond collision checks','No canonical or source geometry changed']}
(R/'inventory/engine/corrected-stage-changed-neighbor-summary.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status']);print(r['category_counts'])
