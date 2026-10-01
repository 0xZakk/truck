#!/usr/bin/env python3
"""Reimport actual delivered STEP files before checking linkage contacts."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import timing_valvetrain_inclined_candidate as c
OUT=ROOT/'cad/engine/generated/timing-valvetrain-inclined-candidate'
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']}
keys=['rocker-arm','pushrod','intake-valve','exhaust-valve','lifter-pushrod-cup','rocker-fulcrum']
paths={k:OUT/'rocker-arm.step' if k=='rocker-arm' else ROOT/defs[k]['step'].lstrip('/') for k in keys};sh={k:b.import_step(p) for k,p in paths.items()}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();watch=[Path(__file__),Path(c.__file__),ROOT/'inventory/engine/full-assembly.json']+list(paths.values());inputs={str(p.relative_to(ROOT)):sha(p) for p in watch}
rows=[]
for i,kind,x in c.stations(m):
 tag=f'c{i}-{kind}';center=(468 if kind=='intake' else 246)+[1,5,3,6,2,4].index(i)*120
 for off in [-150,-96,0,96,150]:
  for axial in [0,-.1]:
   theta=(center+off)%720;frames=c.poses(m,theta,axial);s=c.contract.state(theta,i,kind,axial)
   placed={suffix:frames[tag+'-'+suffix]*sh[occ[tag+'-'+suffix]['definition']] for suffix in ['rocker','valve','pushrod','lifter-pushrod-cup','fulcrum']}
   point=b.Vertex(x,s['pad_y'],261+c.v.LENGTHS[kind]-s['valve_lift']);gaps={'pad_valve':max(point.distance_to(placed['rocker']),point.distance_to(placed['valve']))}
   for a,z in [('rocker','pushrod'),('pushrod','lifter-pushrod-cup'),('rocker','fulcrum')]:gaps[a+'__'+z]=placed[a].distance_to(placed[z])
   assert max(gaps.values())<.002,gaps
   rows.append({'id':tag,'theta':theta,'axial':axial,'gaps_mm':gaps,'rod_center_length_error_mm':s['closure_error']})
r={'status':'PASS reimported actual STEP linkage contacts','inputs':inputs,'rows':rows,'source_rod':'Unchanged canonical pushrod STEP, placed by rigid Location only; no dimensional scale operation','limits':['120 event-relative sampled contacts only, no continuous contact proof.','Smooth fastener thread engagement and broader spring/cover/collision sweeps remain separate open gates.']}
assert all(sha(ROOT/p)==h for p,h in inputs.items());(ROOT/'inventory/engine/timing-valvetrain-inclined-export-contacts-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
