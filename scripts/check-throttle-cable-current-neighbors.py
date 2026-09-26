"""Bind a completed cable sweep to a later manifest without concealing its scope.

Only a zero-affected-pair addendum can pass here. If any selected geometry or
motion changes, report it and require a focused exact sweep of those pairs.
"""
from pathlib import Path
import sys,json,hashlib,itertools
import numpy as np
import build123d as b
import trimesh
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
REPORT=ROOT/'inventory/engine/throttle-cable-candidate-validation.json'
BASE=ROOT/'cad/engine/generated/iac-closure-integration-stage/full-assembly.json'
CURRENT=ROOT/'inventory/engine/full-assembly.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def overlap(a,z):return bool(np.all(a[0]<z[1]+1e-6) and np.all(z[0]<a[1]+1e-6))
def mapped(points,pose):return np.array([tuple(b.Vertex(*v).moved(pose).center()) for v in points])
r=json.loads(REPORT.read_text());assert r['status']=='PASS' and r['full_sweep']
m=json.loads(CURRENT.read_text());old=json.loads(BASE.read_text());D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};poses=transforms(m);oldposes=transforms(old)
corners=mapped(itertools.product([377,491],[60,126],[450,528]),poses['throttle-housing']);region=np.array([corners.min(0),corners.max(0)])
selected=[];mesh_bounds={};mesh_hashes={};bounds={}
for oid,o in O.items():
 if oid=='accelerator-cable-bracket':continue
 did=o['definition']
 if did not in mesh_bounds:
  p=ROOT/D[did]['glb'].lstrip('/');mesh_hashes[str(p.relative_to(ROOT))]=sha(p);v=np.asarray(trimesh.load(p,force='mesh').vertices)[:,[0,2,1]]*[1,-1,1]*1000;mesh_bounds[did]=np.array([v.min(0),v.max(0)])
 v=mapped(itertools.product(*zip(*mesh_bounds[did])),poses[oid]);bounds[oid]=np.array([v.min(0),v.max(0)])
 if overlap(bounds[oid],region) or o['parent']=='throttle-moving':selected.append(oid)
new_neighbors=sorted(set(selected)-set(r['exact_neighbor_ids']));changed_geometry=[]
for oid in selected:
 path=D[O[oid]['definition']]['step'].lstrip('/')
 if path not in r['input_hashes'] or sha(ROOT/path)!=r['input_hashes'][path]:changed_geometry.append(oid)
# The full candidate includes its proposed bracket derived from this old shape.
bracket_path=D[O['accelerator-cable-bracket']['definition']]['step'].lstrip('/')
if sha(ROOT/bracket_path)!=r['input_hashes'][bracket_path]:changed_geometry.append('accelerator-cable-bracket')
pose_changes=[];probe=[(0,0,0),(1,0,0),(0,1,0),(0,0,1)]
for angle in [row['angle_deg'] for row in r['poses']]:
 p=transforms(m,throttle_degrees=angle);q=transforms(old,throttle_degrees=angle)
 for oid in selected+['throttle-housing','accelerator-cable-bracket']:
  if oid not in q or not np.allclose(mapped(probe,p[oid]),mapped(probe,q[oid]),atol=1e-9,rtol=0):pose_changes.append(dict(angle_deg=angle,occurrence=oid))
affected=bool(new_neighbors or changed_geometry or pose_changes)
review_ids=['iac-coil-carrier-estimated','iac-terminal-control-estimated','iac-terminal-vpwr-estimated','iac-connector-cap','iac-coil','iac-end-plug','iac-valve-body','efi-upper-intake','throttle-housing']
review=[]
for oid in review_ids:
 x=bounds[oid];gap=np.maximum(np.maximum(region[0]-x[1],x[0]-region[1]),0)
 review.append(dict(occurrence=oid,selected=oid in selected,aabb_separation_mm=float(np.linalg.norm(gap)),bounds_mm=x.tolist(),step_sha256=sha(ROOT/D[O[oid]['definition']]['step'].lstrip('/'))))
add=dict(status='FAIL: affected pairs require focused exact sweep' if affected else 'PASS',current_manifest_sha256=sha(CURRENT),current_definition_count=len(D),current_occurrence_count=len(O),baseline_snapshot=str(BASE.relative_to(ROOT)),baseline_snapshot_sha256=sha(BASE),baseline_provenance='Integration lead identified this pre-electrical snapshot; staged electrical before_manifest_sha256 matches it. Original sweep did not hash manifest at load time.',original_checker_manifest_sha256_field_means='Hash read at finish, not at load; do not treat it as original full-manifest provenance.',original_sweep_selected_step_hashes_preserved=True,all_current_occurrences_broad_phased=True,current_selected_neighbors=selected,new_neighbors=new_neighbors,changed_selected_geometry=changed_geometry,pose_changes=pose_changes,reviewed_updated_occurrences=review,additional_exact_pair_evaluations=0,reason='Current selected neighbor set, STEP hashes and all 47 pose transforms are unchanged. New/changed IAC shapes outside the conservative complete cable envelope require no exact pairs.' if not affected else 'Run affected exact pairs before current acceptance.',mesh_input_hashes=mesh_hashes,checker_sha256=sha(Path(__file__)))
r['final_current_neighbor_addendum']=add
REPORT.write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in add.items() if k!='mesh_input_hashes'},indent=2))
raise SystemExit(1 if affected else 0)
