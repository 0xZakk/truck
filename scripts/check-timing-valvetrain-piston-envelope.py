#!/usr/bin/env python3
"""Finite-phase conservative CAD Z-envelope check; no continuous claim."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import timing_valvetrain_contract as c
p=ROOT/'inventory/engine/full-assembly.json';m=json.loads(p.read_text());groups={a['id']:a for a in m['assemblies']}
paths=[Path(__file__),Path(c.__file__),p]+[ROOT/f'cad/engine/generated/{k}.step' for k in ['piston','intake-valve','exhaust-valve']]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();inputs={str(p.relative_to(ROOT)):sha(p) for p in paths}
piston=b.import_step(paths[3]);vmin={k:b.import_step(ROOT/f'cad/engine/generated/{k}-valve.step').bounding_box().min.Z for k in ['intake','exhaust']};top=piston.bounding_box().max.Z
R=m['mechanism']['stroke_mm']/2;L=m['mechanism']['rod_length_mm'];rows=[]
for i in range(1,7):
 phase=groups[f'piston-group-{i}']['motion']['phase_deg']
 for kind in ['intake','exhaust']:
  samples=[]
  for axial in [0,-.1]:
   for theta in range(721):
    t=math.radians(theta+phase);y=-R*math.sin(t);pz=R*math.cos(t)+math.sqrt(L*L-y*y)
    s=c.state(theta,i,kind,axial);gap=261-s['valve_lift']+vmin[kind]-pz-top
    samples.append({'crank_degrees':theta,'axial_mm':axial,'z_gap_mm':gap})
  worst=min(samples,key=lambda z:z['z_gap_mm']);rows.append({'id':f'c{i}-{kind}','minimum_sample':worst,'sample_count':len(samples),'down10mm_valve_fault_bound_mm':worst['z_gap_mm']-10})
  assert worst['z_gap_mm']>0 and worst['z_gap_mm']-10<0
r={'status':'PASS sampled conservative valve/piston Z envelopes; continuous motion NOT PROVEN','inputs':inputs,'rows':rows,'coverage':'All12, integer crank0..720 and both axial endpoints; separating entire CAD bounds implies no intersection at those poses','limitations':['No between-sample or intermediate-axial certificate; no production minimum clearance.','Supplied piston/valve geometry and timing remain estimated/replacement hypotheses.','Fault detects failed envelope separation, not exact physical fault overlap.']}
assert all(sha(ROOT/k)==v for k,v in inputs.items());(ROOT/'inventory/engine/timing-valvetrain-piston-envelope-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(min(z['minimum_sample']['z_gap_mm'] for z in rows))
