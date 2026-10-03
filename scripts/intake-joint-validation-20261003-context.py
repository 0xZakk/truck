#!/usr/bin/env python3
"""Whole-scene static successor audit. Preserves frozen candidate and installed files."""
from pathlib import Path
import sys,json,hashlib,time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,numpy as np
from assembly_math import transforms
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.TopAbs import TopAbs_SOLID,TopAbs_FACE
from OCP.TopExp import TopExp_Explorer
from OCP.TopoDS import TopoDS
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
OUT=ROOT/'cad/engine/generated/intake-joint-validation-20261003';OUT.mkdir(exist_ok=True)
CAND=ROOT/'cad/engine/generated/intake-joint-candidate-20261003'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def bounds(s):
 box=s.bounding_box();return np.array(tuple(box.min)),np.array(tuple(box.max))
def world_bounds(bb,pose):
 lo,hi=bb;pts=np.array([tuple(b.Vertex(x,y,z).moved(pose).center()) for x in (lo[0],hi[0]) for y in (lo[1],hi[1]) for z in (lo[2],hi[2])]);return pts.min(0),pts.max(0)
def gap(a,c):return float(np.linalg.norm(np.maximum(np.maximum(a[0]-c[1],c[0]-a[1]),0)))
def common(a,c):
 op=BRepAlgoAPI_Common(a.wrapped,c.wrapped);op.Build();done=op.IsDone()
 if not done:raise ValueError('OCC Common IsDone false')
 result=op.Shape()
 if result.IsNull():raise ValueError('OCC Common null result despite IsDone; unresolved')
 if not BRepCheck_Analyzer(result).IsValid():raise ValueError('OCC Common invalid topology')
 exp=TopExp_Explorer(result,TopAbs_SOLID);count=0;vol=0
 while exp.More():
  solid=TopoDS.Solid_s(exp.Current());props=GProp_GProps();BRepGProp.VolumeProperties_s(solid,props);vol+=abs(props.Mass());count+=1;exp.Next()
 faces=TopExp_Explorer(result,TopAbs_FACE);face_count=0
 while faces.More():face_count+=1;faces.Next()
 return {'IsDone':True,'null':False,'valid':True,'solid_count':count,'face_count':face_count,'overlap_mm3':vol}
mp=ROOT/'inventory/engine/full-assembly.json';m=json.loads(mp.read_text());defs={d['id']:d for d in m['definitions']};poses=transforms(m)
changed=['efi-lower-intake','efi-upper-intake','efi-upper-intake-gasket'];studs={r['id']:r for r in json.loads((CAND/'build.json').read_text())['stud_hypotheses']}
inputs={mp,CAND/'build.json',ROOT/'cad/engine/intake-joint-candidate-20261003-delivery.json',ROOT/'cad/engine/assembly_math.py',Path(__file__)}|{ROOT/d['step'].lstrip('/') for d in defs.values()}|{CAND/(i+'.step') for i in changed}
before={str(p.relative_to(ROOT)):sha(p) for p in inputs};candidate={i:b.import_step(CAND/(i+'.step')) for i in changed};cb={i:bounds(s) for i,s in candidate.items()};local_bounds={};cache={};rows=[];invalid=[];start=time.time()
def check(part,ident,shape,bb,placement):
 distance=gap(cb[part],bb);row={'part':part,'neighbor':ident,'placement':placement,'aabb_distance_lower_mm':distance}
 if distance>1e-7:row['status']='DISJOINT CAD BOUNDS'
 else:
  print('Exact',part,ident,placement,flush=True)
  try:
   row.update(common(candidate[part],shape));row['status']='OVERLAP' if row['overlap_mm3']>.1 else 'NO VOLUME ABOVE0.1mm3'
  except Exception as e:row.update(status='ERROR',error=str(e))
 rows.append(row)
def save(complete=False):
 report={'status':'COMPLETE STATIC DIAGNOSTIC' if complete else 'PARTIAL RUNNING','definitions':len(defs),'occurrences':len(m['occurrences']),'elapsed_seconds':time.time()-start,'input_sha256_before':before,'rows':rows,'invalid_neighbor_definitions':invalid,'limits':['Static only. No whole motion/removal/fastening acceptance.','Seven studs tested at both current and proposed positions; hypotheses do not resolve paired-hole roles.','Exact overlap volumes use standard OCC mass properties; numerical convention0.1mm3 is not manufacturing clearance.']}
 if complete:
  after={str(p.relative_to(ROOT)):sha(p) for p in inputs};report['input_sha256_after']=after;report['input_guard_pass']=before==after;report['summary']={s:sum(r['status']==s for r in rows) for s in sorted({r['status'] for r in rows})};report['failures']=[r for r in rows if r['status'] in ['ERROR','OVERLAP']]
 (OUT/'context.json').write_text(json.dumps(report,indent=2)+'\n')
for index,o in enumerate(m['occurrences']):
 ident=o['id'];did=o['definition']
 if ident in changed:continue
 if did not in local_bounds:
  local=b.import_step(ROOT/defs[did]['step'].lstrip('/'));local_bounds[did]=bounds(local)
  if not local.is_valid:invalid.append(did)
 else:local=cache.get(did)
 bb=world_bounds(local_bounds[did],poses[ident]);needs=any(gap(bb,z)<=1e-7 for z in cb.values()) or ident in studs
 if needs:
  if local is None:local=b.import_step(ROOT/defs[did]['step'].lstrip('/'))
  cache[did]=local;shape=poses[ident]*local
 else:shape=None
 for part in changed:check(part,ident,shape,bb,'installed')
 if ident in studs:
  row=studs[ident];pose=b.Pos(*row['position_cad_mm'])*b.Rot(*row['rotation_cad_deg']);shape=pose*local;box=world_bounds(local_bounds[did],pose)
  for part in changed:check(part,ident,shape,box,'proposed unresolved hypothesis')
 if index%50==0:print('Progress',index,'/',len(m['occurrences']),'rows',len(rows),flush=True);save()
for i,part in enumerate(changed):
 for other in changed[i+1:]:check(part,other,candidate[other],cb[other],'coordinated candidate')
save(True);print('Complete',len(rows),'pairs',time.time()-start,flush=True)
