#!/usr/bin/env python3
"""Sample internal centerlines; this is not an airflow/minimum-section proof."""
from pathlib import Path
import importlib.util,sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
p=ROOT/'cad/engine/intake-joint-candidate-20261003.py';spec=importlib.util.spec_from_file_location('joint_candidate',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
out=ROOT/'cad/engine/generated/intake-joint-candidate-20261003';lo=b.import_step(out/'efi-lower-intake.step');up=b.import_step(out/'efi-upper-intake.step');rows=[]
for i,(old,new) in enumerate(zip(m.core.PORTS,m.X),1):
 pts=[(old-25,-140.5,277.5),(old-25,-183,277.5),(old,-228,315),(old,-228,355)];a,c=m.split(pts,.65);c[-2]=b.Vector(new,-228,c[-2].Z);c[-1]=b.Vector(new,-228,355)
 paths=[b.Bezier(*a),b.Bezier(*c)];terminal=-150+(old+m.core.PORTS[0])/(2*m.core.PORTS[0])*300;upper=b.Bezier((new,-228,366.5),(new,-228,490),(terminal,-145,490),(terminal,-20,490))
 blocked_lower=[(segment,j) for segment,path in enumerate(paths) for j in range(1,100) if lo.is_inside(path@(j/100))];blocked_upper=[j for j in range(1,100) if up.is_inside(upper@(j/100))]
 rows.append({'runner':i,'lower_samples':198,'upper_samples':99,'lower_material_hits':blocked_lower,'upper_material_hits':blocked_upper})
r={'status':'PASS sampled centerlines' if not any(x['lower_material_hits'] or x['upper_material_hits'] for x in rows) else 'FAIL sampled centerlines','rows':rows,'limits':'Does not establish minimum section, wall thickness or continuous off-axis passage clearance.'};(out/'passages.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
