#!/usr/bin/env python3
"""Read-only interface audit before a PCV vacuum-return connection candidate."""
from pathlib import Path
import hashlib,json,sys,subprocess
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
from cad_metrics import solid_volume
M=ROOT/'inventory/engine/full-assembly.json';m=json.loads(M.read_bytes());D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};poses=transforms(m);inputs={}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(k):
 p=ROOT/D[O[k]['definition']]['step'].lstrip('/');inputs[str(p.relative_to(ROOT))]=sha(p);return poses[k]*b.import_step(p)
def vol(s):return sum(abs(solid_volume(q,'adaptive')) for q in s.solids()) if s else 0.
def tube(r,a,c):
 a=b.Vector(*a);c=b.Vector(*c);return b.Plane(origin=(a+c)*.5,z_dir=c-a)*b.Cylinder(r,(c-a).length)
for p in [Path(__file__),ROOT/'cad/engine/cad_metrics.py',ROOT/'cad/engine/assembly_math.py',ROOT/'reference/engine/pcv-connection-review.json']:inputs[str(p.relative_to(ROOT))]=sha(p)
ledger=json.loads((ROOT/'reference/engine/pcv-connection-review.json').read_text())
for row in ledger['sources']:
 assert sha(ROOT/row['path'])==row['sha256'],row['path'];inputs[row['path']]=row['sha256']
parts={k:load(k) for k in ['pcv-outlet-head','pcv-body','valve-cover','efi-upper-intake','regulator-vacuum-fitting']}
ends={}
for name,z,r in [('lower_large',12,3),('upper_small',24,2.5)]:
 p=tuple(b.Vertex(0,-19,z).moved(poses['pcv-outlet-head']).center());q=tuple(b.Vertex(0,-22,z).moved(poses['pcv-outlet-head']).center());probe=tube(r-.1,p,q);ends[name]=dict(center_world_mm=p,outward_direction=[0,-1,0],model_bore_radius_mm=r,opening_witness_obstruction_mm3=vol(probe.intersect(parts['pcv-outlet-head'])))
# This floor station is a proposed educational datum, NOT an observed port.
# Demonstrate that an interface change would be required, rather than attach a
# hose cosmetically to a blind existing face.
probe=tube(.5,(-100,25,430),(-100,25,465));obstruction=vol(probe.intersect(parts['efi-upper-intake']))
A={a['id']:a for a in m['assemblies']};ancestors=set()
for k in parts:
 parent=O[k]['parent']
 while parent in A:ancestors.add(parent);parent=A[parent]['parent']
snapshot=dict(definitions={O[k]['definition']:D[O[k]['definition']] for k in parts},occurrences={k:O[k] for k in parts},assemblies={k:A[k] for k in ancestors})
report=dict(relevant_snapshot=snapshot,status='AUDIT: no source-identified receiver; arbitrary trial rejected',baseline_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),manifest_sha256=sha(M),input_sha256=inputs,part_bounds_world_mm={k:dict(min=list(s.bounding_box().min),max=list(s.bounding_box().max)) for k,s in parts.items()},pcv_outlet_datums=ends,rejected_receiver_trial=dict(center_world_mm=[-100,25,445],axis=[0,0,1],classification='REJECTED arbitrary feasibility trial; not source-observed or authorized for modeling',radius_half_mm_probe_obstruction_mm3=obstruction,existing_compatible_receiver=False),limits=['No production hose route, diameter, manifold port station, center-branch hardware or secondary outlet use established.','No cover baffle or unused-outlet plug justified by reviewed owner photographs.','No geometry changed; this audit is not pneumatic closure or installed acceptance.'])
assert obstruction>1 and all(row['opening_witness_obstruction_mm3']<1e-5 for row in ends.values())
assert all(sha(ROOT/p)==h for p,h in inputs.items())
new=json.loads(M.read_bytes());assert all({r['id']:r for r in new[kind]}[k]==v for kind,rows in snapshot.items() for k,v in rows.items())
report['relevant_inputs_stable']=True
(ROOT/'inventory/engine/pcv-connection-interface-audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
