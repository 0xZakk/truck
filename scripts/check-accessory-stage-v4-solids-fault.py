#!/usr/bin/env python3
"""Separate real posed-part fault sensitivity; frozen full audit unchanged."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_clockwise_candidate import transforms,occurrence_shape
from cad_metrics import solid_volume
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mp=R/'inventory/engine/corrected-engine-stage-v4.json';bp=R/'inventory/engine/corrected-engine-stage-v3.json';audit=R/'inventory/engine/accessory-stage-v4-solids.json'
a=json.loads(audit.read_text());assert sha(mp)==a['stage_sha256']
for p,h in a['input_sha256'].items():assert sha(R/p)==h,p
m=json.loads(mp.read_text());base=json.loads(bp.read_text());defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};t=transforms(m,0,0);old=transforms(base,0,0)
n='ac-compressor-front-cylinder';z='timing-cover';paths={k:R/defs[occ[k]['definition']]['step'].lstrip('/') for k in[n,z]}
parts={k:b.import_step(p)for k,p in paths.items()}
# Sole deliberate fault: old v3 cylinder frame, actual frozen v4 cylinder bytes.
wrong=old[n]*occurrence_shape(occ[n],parts[n],0,0);cover=t[z]*occurrence_shape(occ[z],parts[z],0,0)
def bounds(s):
 q=s.bounding_box();return np.array([tuple(q.min),tuple(q.max)])
def matrix(p):
 tr=p.wrapped.Transformation();return [[tr.Value(i,j)for j in range(1,5)]for i in range(1,4)]
extent=np.minimum(bounds(wrong)[1],bounds(cover)[1])-np.maximum(bounds(wrong)[0],bounds(cover)[0]);candidate=not np.any(extent < -2.0)
assert candidate,'fault missed by same 2mm broadphase'
common=wrong.intersect(cover)
if isinstance(common,b.ShapeList):common=b.Compound(common)
v=solid_volume(common)if common else 0.
assert v>.1,'fault missed by actual solid intersection'
wp=R/'cad/engine/generated/accessory-stage-v4-solids/fault-old-ac-front-cylinder__timing-cover.step';b.export_step(common,wp)
report={'status':'PASS fault detected; deliberately wrong pose not an accepted candidate','fault':'Only AC front cylinder restored to v3 world frame; v4 actual asset and timing-cover pose retained','q':0,'axial_mm':0,'pair':[n,z],'correct_v4_frame':matrix(t[n]),'wrong_v3_frame':matrix(old[n]),'wrong_bounds_mm':bounds(wrong).tolist(),'cover_bounds_mm':bounds(cover).tolist(),'broadphase_pair_padding_mm':2.,'broadphase_extent_mm':extent.tolist(),'entered_broadphase':bool(candidate),'threshold_mm3':.1,'overlap_mm3':v,'witness_step':str(wp.relative_to(R)),'witness_sha256':sha(wp),'input_sha256':{str(p.relative_to(R)):sha(p)for p in [mp,bp,audit,Path(__file__),R/'cad/engine/assembly_clockwise_candidate.py',R/'cad/engine/cad_metrics.py',*paths.values()]}}
(R/'inventory/engine/accessory-stage-v4-solids-fault.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],v)
