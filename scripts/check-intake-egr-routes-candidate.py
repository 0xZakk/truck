"""Validate proposed EGR flow/export/endpoints; whole-neighbor audit is separate."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
import trimesh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import intake_egr_routes_candidate as candidate
import egr_tube as original
from cad_metrics import solid_volume
from assembly_math import transforms
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=[Path(__file__),Path(candidate.__file__),Path(original.__file__),ROOT/'cad/engine/egr_vacuum_hose.py']
inputs={str(p.relative_to(ROOT)):sha(p) for p in paths}
M=ROOT/'inventory/engine/full-assembly.json';m=json.loads(M.read_text());poses=transforms(m);defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']}
parts=candidate.parts();out=ROOT/'cad/engine/generated/intake-egr-route-study';out.mkdir(exist_ok=True)
def volume(s):return sum(solid_volume(q,'adaptive') for q in s.solids()) if s else 0.
def baked(s,name):
 p=out/(name+'.step');b.export_step(s,p);return b.import_step(p)
checks={};outputs={}
for name,s in parts.items():
 assert s.is_valid and len(s.solids())==1,name
 q=baked(s,name);delta=abs(volume(q)-volume(s));assert q.is_valid and len(q.solids())==1 and delta<max(.001,volume(s)*1e-5),(name,delta)
 v,f=q.tessellate(.12,.1);v=np.asarray([tuple(x) for x in v]);mesh=trimesh.Trimesh(v[:,[0,2,1]]*np.array([1,1,-1])/1000,np.asarray(f));mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();assert mesh.is_watertight,name
 path=out/(name+'.glb');mesh.export(path);bb=q.bounding_box();bound=np.array([tuple(bb.min),tuple(bb.max)]);reopen=trimesh.load(path,force='mesh');vv=np.asarray(reopen.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000;err=float(np.max(np.abs(np.array([vv.min(0),vv.max(0)])-bound)));assert err<.2,(name,err)
 checks[name]={'valid':True,'solids':1,'step_volume_delta_mm3':delta,'mesh_watertight':True,'mesh_bounds_error_mm':err};parts[name]=q
 for p in [out/(name+'.step'),path]:outputs[str(p.relative_to(ROOT))]=sha(p)
route=candidate.route();plane=b.Plane(origin=route@0,z_dir=route%0);probe=b.sweep(plane*b.Circle(original.OUTSIDE_DIAMETER/2-original.WALL-.2),path=route);probe=baked(probe,'flow-probe');blockage=volume(probe&parts['egr-exhaust-tube']);assert blockage<.1,blockage
badprobe=b.sweep(plane*b.Circle(original.OUTSIDE_DIAMETER/2+.2),path=route);badprobe=baked(badprobe,'oversized-probe');blocked=volume(badprobe&parts['egr-exhaust-tube']);assert blocked>100,blocked
source=ROOT/defs[occ['egr-tube-manifold-fitting']['definition']]['step'].lstrip('/');inputs[str(source.relative_to(ROOT))]=sha(source);fitting=baked(poses['egr-tube-manifold-fitting']*b.import_step(source),'fixed-manifold-fitting');gap=parts['egr-exhaust-tube'].distance_to(fitting);hit=volume(parts['egr-exhaust-tube']&fitting);assert gap<.001 and hit<.1,(gap,hit)
oldend=np.array(original.END);newend=np.array(candidate.END);assert np.max(np.abs(newend-oldend-np.array(candidate.DELTA)))<1e-9
assert all(sha(ROOT/p)==h for p,h in inputs.items())
r={'status':'LOCAL_CHECKS_PASS_NEIGHBOR_REVIEW_PENDING','scope':'Isolated estimated fixed-end EGR route with source-supported replacement OD; full coordinated intake neighbors, actual route fidelity, thermal and sealing performance remain separate.','input_hashes':inputs,'output_hashes':outputs,'exports':checks,'egr_delta_mm':candidate.DELTA,'fixed_exhaust_start_mm':original.START,'valve_end_mm':candidate.END,'vacuum_end_mm':candidate.HOSE_END,'tube_centerline_length_mm':route.length,'original_route_centerline_length_mm':original.path().length,'published_replacement_length_mm':17.9*25.4,'length_limit':'Catalog17.9-inch field lacks measurement definition; neither prior nor proposed centerline is proven Ford routing. New route must remain visibly provisional.','flow_probe_intrusion_mm3':blockage,'oversized_probe_negative_mm3':blocked,'fixed_fitting':{'distance_mm':gap,'overlap_mm3':hit},'method':'Collision probes use STEP-roundtripped world solids to avoid nested-placement Boolean anomalies; source/exports guarded.'}
(ROOT/'inventory/engine/intake-egr-routes-candidate-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ('input_hashes','output_hashes')},indent=2))
