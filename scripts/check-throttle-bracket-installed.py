"""Validate current installed bracket envelopes, not proposed hard-coded test poses.

Checks geometry/placement only. Smooth stud/nut envelopes cannot establish actual
thread flank engagement, anchorage strength, spring/cable sweep or Ford fidelity.
"""
from pathlib import Path
import sys,json,hashlib,importlib.util,itertools
import numpy as np
import build123d as b
import trimesh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
from cad_metrics import solid_volume,step_comparison_shape
MANIFEST=ROOT/'inventory/engine/full-assembly.json'
REPORT=ROOT/'inventory/engine/throttle-bracket-installed-validation.json'
raw=MANIFEST.read_bytes();m=json.loads(raw)
defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};poses=transforms(m)
source=ROOT/'cad/engine/pilot/throttle-bracket/candidate.py'
spec=importlib.util.spec_from_file_location('bracket',source);candidate=importlib.util.module_from_spec(spec);spec.loader.exec_module(candidate)
hashes={str(source.relative_to(ROOT)):hashlib.sha256(source.read_bytes()).hexdigest(),str(Path(__file__).relative_to(ROOT)):hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

def readpath(definition,key):
 p=ROOT/defs[definition][key].lstrip('/')
 hashes[str(p.relative_to(ROOT))]=hashlib.sha256(p.read_bytes()).hexdigest()
 return p

def volume(shape):return sum(solid_volume(s,'adaptive') for s in shape.solids()) if shape else 0.
local={};world={}
def shape(oid):
 if oid not in world:
  did=occ[oid]['definition']
  if did not in local:local[did]=b.import_step(readpath(did,'step'))
  world[oid]=local[did].moved(poses[oid])
 return world[oid]

def area(a,c):
 total=0.
 for fa in a.faces():
  for fc in c.faces():
   q=fa.intersect(fc)
   if q:total+=q.area if hasattr(q,'area') else sum(t.area for t in q)
 return total

def bbox(q):
 bb=q.bounding_box();return np.array([tuple(bb.min),tuple(bb.max)])

def overlaps(a,c,pad=.5):return bool(np.all(a[0]<=c[1]+pad) and np.all(c[0]<=a[1]+pad))

required=['accelerator-cable-bracket','throttle-stud-3','throttle-stud-4','throttle-nut-3','throttle-nut-4']
assert all(k in occ for k in required)
assert 'throttle-bracket-stud-estimated' in defs
for i,z in [(3,464),(4,516)]:
 assert occ[f'throttle-stud-{i}']['definition']=='throttle-bracket-stud-estimated'
 for oid,center in [(f'throttle-stud-{i}',(373,74,z)),(f'throttle-nut-{i}',(383.5,74,z))]:
  assert np.max(np.abs(np.array(tuple(b.Vertex(0,0,0).moved(poses[oid]).center()))-center))<1e-8,oid
  for vector in [(1,0,0),(0,1,0),(0,0,1)]:
   p=np.array(tuple(b.Vertex(*vector).moved(poses[oid]).center()))-center
   assert np.max(np.abs(p-vector))<1e-8,oid
# Opposite pair remains original definition, center and orientation.
for i,z in [(1,464),(2,516)]:
 oid=f'throttle-stud-{i}'
 assert occ[oid]['definition']=='throttle-mount-stud'
 assert occ[oid]['position_cad_mm']==[371,-24,z] and occ[oid].get('rotation_cad_deg',[0,0,0])==[0,0,0]
 q=shape(oid);assert abs(bbox(q)[0,0]-356)<1e-7 and abs(bbox(q)[1,0]-386)<1e-7
 assert occ[f'throttle-nut-{i}']['position_cad_mm']==[381.5,-24,z]

bracket=shape('accelerator-cable-bracket')
expected=step_comparison_shape(candidate.shape())
assert volume(bracket-expected)+volume(expected-bracket)<.02
expected_stud=step_comparison_shape(candidate.mounting_stud_shape())
for oid in ['throttle-stud-3','throttle-stud-4']:
 actual=shape(oid);reference=expected_stud.moved(poses[oid])
 assert volume(actual-reference)+volume(reference-actual)<.02
 assert actual.is_valid and len(actual.solids())==1

# Every occurrence participates in conservative mesh-AABB broad phase. Browser
# meshes use metres and X,Z,-Y; convert into local CAD mm before applying poses.
mesh_bounds={};bounds={};glb_errors={}
for oid,o in occ.items():
 did=o['definition']
 if did not in mesh_bounds:
  mesh=trimesh.load(readpath(did,'glb'),force='mesh')
  v=np.asarray(mesh.vertices)*1000
  cad_v=v[:,[0,2,1]]*np.array([1,-1,1])
  mesh_bounds[did]=np.array([cad_v.min(axis=0),cad_v.max(axis=0)])
 corners=np.array([tuple(b.Vertex(*xyz).moved(poses[oid]).center()) for xyz in itertools.product(*zip(*mesh_bounds[did]))])
 bounds[oid]=np.array([corners.min(axis=0),corners.max(axis=0)])
for oid in required:
 actual=shape(oid);did=occ[oid]['definition']
 err=float(np.max(np.abs(mesh_bounds[did]-bbox(local[did]))));glb_errors[did]=err
 assert err<=.2,(did,err)
 bounds[oid]=bbox(actual)

pairs=[];collisions=[];intentional=[];seen=set()
for oid in required:
 for other in occ:
  key=tuple(sorted((oid,other)))
  if oid==other or key in seen or not overlaps(bounds[oid],bounds[other]):continue
  seen.add(key);a,c=shape(oid),shape(other);q=a.intersect(c);vol=volume(q)
  result={'a':oid,'b':other,'overlap_mm3':vol,'minimum_distance_mm':a.distance_to(c)};pairs.append(result)
  if vol>.1:
   # No blanket hardware exclusions: the only potential intended volume is
   # preserved intake anchorage at the original inward end of these two studs.
   if oid in ('throttle-stud-3','throttle-stud-4') and other=='efi-upper-intake' and bbox(q)[1,0]<=371.+1e-7:
    intentional.append(result|{'reason':'Preserved smooth stud anchorage envelope X356–371 in intake; actual thread strength unverified.'})
   else:collisions.append(result)

def stack(stud,nut):
 sb,nb=bbox(stud),bbox(nut)
 coverage=max(0.,min(sb[1,0],nb[1,0])-max(sb[0,0],nb[0,0]))
 protrusion=sb[1,0]-nb[1,0];contact=area(bracket,nut)
 return {'coverage_mm':coverage,'protrusion_mm':protrusion,'contact_mm2':contact,'pass':coverage>=6.-1e-6 and protrusion>=2.5-1e-6 and contact>1.}
stack_checks=[]
for i in [3,4]:
 stud,nut=shape(f'throttle-stud-{i}'),shape(f'throttle-nut-{i}')
 result=stack(stud,nut);result['radial_clearance_mm']=stud.distance_to(nut)
 assert result['pass'] and .19<=result['radial_clearance_mm']<=.21
 negative=stack(stud,b.Pos(1,0,0)*nut)
 assert not negative['pass'] and negative['contact_mm2']<1e-6
 result['displaced_nut_negative_control']=negative;stack_checks.append(result)
housing_contact=area(bracket,shape('throttle-housing'));assert housing_contact>1.
assert MANIFEST.read_bytes()==raw
assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h for p,h in hashes.items())
report={'status':'PASS' if not collisions else 'FAIL','scope':'Installed estimated mounting envelopes; no certification of real threads, strength, Ford dimensions, cables or return spring. Static occurrence phase only.','manifest_sha256':hashlib.sha256(raw).hexdigest(),'input_hashes':hashes,'broad_phase_occurrences':len(occ),'exact_pairs':pairs,'collisions':collisions,'explicit_intended_anchorage':intentional,'stack_checks':stack_checks,'housing_contact_mm2':housing_contact,'glb_bounds_errors_mm':glb_errors,'unchanged_opposite_studs':'PASS','thresholds':{'overlap_mm3':.1,'broad_phase_padding_mm':.5,'glb_bounds_mm':.2,'nominal_nut_coverage_mm':6.,'protrusion_mm':2.5}}
REPORT.write_text(json.dumps(report,indent=2)+'\n')
assert not collisions,collisions
print('PASS installed throttle bracket:',len(pairs),'exact nearby pairs; actual threaded engagement remains unverified')
