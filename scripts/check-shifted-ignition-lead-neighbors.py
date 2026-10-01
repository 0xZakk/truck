#!/usr/bin/env python3
"""Actual q0/axial0 neighbors of all28 proposed lead definitions in frozen private v2."""
import sys,json,hashlib,itertools
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,numpy as np
from assembly_clockwise_candidate import transforms,occurrence_shape
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/shifted-ignition-lead-candidate';mp=ROOT/'inventory/engine/corrected-engine-stage-v2.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();assert sha(mp)=='9b8253b318e800e18b999a0a74caa749d9525978f2c19bc7286c07bb79a7c100'
m=json.loads(mp.read_text());poses=transforms(m,0,0);defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};selected={p.stem for p in OUT.glob('*.step')};assert len(selected)==28
inputs={str(p.relative_to(ROOT)):sha(p) for p in [mp,Path(__file__),ROOT/'cad/engine/assembly_clockwise_candidate.py',ROOT/'inventory/engine/shifted-ignition-lead-build-validation.json']};parts={};bounds={};placed={}
for i,(key,d) in enumerate(defs.items()):
 p=OUT/(key+'.step') if key in selected else ROOT/d['step'].lstrip('/');inputs[str(p.relative_to(ROOT))]=sha(p);parts[key]=b.import_step(p)
 if i%100==0:print('loaded',i,flush=True)
for key,o in occ.items():
 q=poses[key]*occurrence_shape(o,parts[o['definition']],0,0);placed[key]=q;bb=q.bounding_box();bounds[key]=np.array([tuple(bb.min),tuple(bb.max)])
r={'status':'RUNNING','inputs':inputs,'scope':'All v2 actual q0/axial0 pairs with at least one of28 newlead shapes; all-part BRep bounds then exact actual solid intersections','exact_checks':[],'conflicts':[],'bounds_separated':0}
def save():(ROOT/'inventory/engine/shifted-ignition-lead-neighbor-validation.json').write_text(json.dumps(r,indent=2)+'\n')
for a,z in itertools.combinations(occ,2):
 if a not in selected and z not in selected:continue
 extent=np.minimum(bounds[a][1],bounds[z][1])-np.maximum(bounds[a][0],bounds[z][0])
 if np.any(extent<=0):r['bounds_separated']+=1;continue
 q=placed[a].intersect(placed[z]);v=sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.;row={'a':a,'b':z,'overlap_mm3':v};r['exact_checks'].append(row)
 if v>.1:
  p=OUT/(a+'__'+z+'-conflict.step');b.export_step(q,p);row['witness']=str(p.relative_to(ROOT));row['sha256']=sha(p);r['conflicts'].append(row);print('CONFLICT',row,flush=True)
 if len(r['exact_checks'])%25==0:print('checked',len(r['exact_checks']),flush=True);save()
assert all(sha(ROOT/p)==h for p,h in inputs.items());r['status']='FAIL actual neighbor overlap' if r['conflicts'] else 'PASS affected static neighbors only; no whole-motion/browser claim';save();print(r['status'],flush=True)
