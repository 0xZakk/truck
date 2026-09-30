#!/usr/bin/env python3
"""Exact near-contact phase bracket; no loaded force or continuous-contact claim."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import timing_gear_pair_candidate as c
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-gear-pair-candidate'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
paths=[Path(__file__),Path(c.__file__),ROOT/'cad/engine/cad_metrics.py',OUT/'crank.step',OUT/'cam.step'];inputs={str(p.relative_to(ROOT)):sha(p) for p in paths}
parts={key:b.import_step(OUT/(key+'.step')) for key in ['crank','cam']}
region=b.Pos(0,40.6*math.cos(c.AXIS_ANGLE),40.6*math.sin(c.AXIS_ANGLE))*b.Rot(math.degrees(c.AXIS_ANGLE),0,0)*b.Box(16,14,44)
rows=[]
for theta in [0,180/c.PARAMS['crank_teeth']]:
 a=b.Compound(children=list((b.Rot(theta,0,0)*parts['crank']).intersect(region).solids()))
 for extra in [.07,.08,.09,.10]:
  cam=b.Pos(0,*c.CAM_YZ)*b.Rot(-theta/2+extra,0,0)*parts['cam'];z=b.Compound(children=list(cam.intersect(region).solids()));overlap=vol(a.intersect(z));gap=a.distance_to(z)
  row=dict(crank_degrees=theta,cam_extra_degrees=extra,overlap_mm3=overlap,local_gap_mm=gap);rows.append(row);print(row,flush=True)
assert all(sha(ROOT/p)==h for p,h in inputs.items())
brackets=[]
for theta in sorted({r['crank_degrees'] for r in rows}):
 q=[r for r in rows if r['crank_degrees']==theta];free=[r for r in q if r['overlap_mm3']<1e-5 and r['local_gap_mm']>1e-6];hit=[r for r in q if r['overlap_mm3']>1e-5]
 brackets.append(dict(crank_degrees=theta,contact_bracket_deg=[max(r['cam_extra_degrees'] for r in free),min(r['cam_extra_degrees'] for r in hit)] if free and hit else None))
r=dict(status='PASS finite first-contact bracket' if all(r['contact_bracket_deg'] for r in brackets) else 'FAIL contact bracket not established',input_sha256=inputs,rows=rows,brackets=brackets,limits=['Finite phase bracket at two tooth-period locations, not exact loaded contact phase or continuous surface-contact proof.','No load/stress/backlash service specification claimed; extra cam rotation intentionally explores drive-flank closure.'])
(ROOT/'inventory/engine/timing-gear-contact-diagnostic.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],flush=True)
