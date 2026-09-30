#!/usr/bin/env python3
"""Isolated world-frame exports and bounded timing-core interfaces."""
from pathlib import Path
import sys,json,hashlib,itertools
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import numpy as np
import trimesh
import timing_core_migration_candidate as c
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-core-migration-candidate';OUT.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def volume(s):return sum(abs(solid_volume(q,'adaptive')) for q in s.solids()) if s else 0.
mp=ROOT/'inventory/engine/full-assembly.json';raw=mp.read_bytes();m=json.loads(raw)
parts,records,paths=c.source_parts(m)
inputs={str(p.relative_to(ROOT)):sha(p) for p in set(paths.values())|{Path(c.__file__),Path(__file__),ROOT/'cad/engine/cad_metrics.py'}}
proofpath=ROOT/'inventory/engine/timing-gear-pair-refinement-validation.json';proof=json.loads(proofpath.read_text())
for key,identifier in [('cam','cam-timing-gear'),('crank','crank-timing-gear')]:assert sha(paths[identifier])==proof['exports'][key]['step_sha256']
checks={};preview={}
for identifier in c.IDS:
 q=parts[identifier];print('export',identifier,flush=True)
 assert q.is_valid and len(q.solids())==1,identifier
 sp=OUT/(identifier+'.step');b.export_step(q,sp);rt=b.import_step(sp);assert rt.is_valid and len(rt.solids())==1
 v,f=q.tessellate(.06,.12);v=np.array([tuple(p) for p in v]);f=np.array(f)
 mesh=trimesh.Trimesh(v[:,[0,2,1]]*[1,1,-1]/1000,f);mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();gp=OUT/(identifier+'.glb');mesh.export(gp)
 loaded=trimesh.load(gp,force='mesh');loaded.merge_vertices(digits_vertex=8)
 assert loaded.is_watertight and loaded.nondegenerate_faces().all() and loaded.unique_faces().all(),identifier
 vv=np.asarray(loaded.vertices)[:,[0,2,1]]*[1,-1,1]*1000;bb=q.bounding_box();err=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))))
 assert err<.15
 ve=abs(volume(q)-volume(rt));assert ve<.001
 checks[identifier]={'valid':True,'solids':1,'watertight':True,'bounds_error_mm':err,'step_volume_error_mm3':ve,'step_sha256':sha(sp),'glb_sha256':sha(gp),'triangles':len(loaded.faces)}
 preview[identifier+'_vertices']=vv;preview[identifier+'_faces']=np.asarray(loaded.faces)
np.savez_compressed(OUT/'render-input.npz',**preview)
(OUT/'exports-checkpoint.json').write_text(json.dumps({'inputs':inputs,'exports':checks},indent=2)+'\n')
def measure(a,d,distance=True):
 print('interface',a,d,flush=True)
 q=parts[a];r=parts[d]
 if distance:
  # Neighbor slab contains every possible overlap with the full shaft;
  # distance after clipping is explicitly local, not global minimum.
  if a in ['camshaft','crankshaft']:
   bb=r.bounding_box();mid=(bb.min.X+bb.max.X)/2
   q=q.intersect(b.Pos(mid,0,0)*b.Box(bb.max.X-bb.min.X+(60 if d=='rear-cam-plug' else 2),600,600))
  for name,which in [(a,'q'),(d,'r')]:
   if name=='cam-timing-gear':
    guard=b.Pos(385.259375,*c.CAM_YZ)*b.Rot(0,90,0)*b.Cylinder(50,30)
    if which=='q':q=q.intersect(guard)
    else:r=r.intersect(guard)
 return {'a':a,'b':d,'overlap_mm3':volume(q.intersect(r)),**({'local_interface_distance_mm':q.distance_to(r)} if distance else {})}
pairs=[('camshaft','cam-timing-gear'),('camshaft','cam-gear-spacer'),('camshaft','cam-thrust-plate'),('camshaft','cam-timing-key'),('camshaft','rear-cam-plug'),('cam-timing-gear','cam-gear-spacer'),('cam-timing-gear','cam-timing-key'),('cam-thrust-plate','cam-gear-spacer'),('crankshaft','crank-timing-gear')]+[('camshaft',f'cam-bearing-{i}') for i in range(1,5)]+[(f'cam-thrust-bolt-{i}',f'cam-thrust-washer-{i}') for i in [1,2]]+[(f'cam-thrust-washer-{i}','cam-thrust-plate') for i in [1,2]]+[(f'cam-thrust-bolt-{i}','cam-timing-gear') for i in [1,2]]
interfaces=[]
for a,d in pairs:
 interfaces.append(measure(a,d))
 (OUT/'interfaces-progress.json').write_text(json.dumps(interfaces,indent=2)+'\n')
# Context is deliberately not migrated; quantify expected rejection separately.
context=[measure('camshaft','block',False),measure('cam-timing-gear','timing-cover',False)]
assert inputs=={p:sha(ROOT/p) for p in inputs},'Bound input changed during check'
report={'status':'CHECKED isolated core; inspect interface results; UNINSTALLED','baseline_manifest_sha256':hashlib.sha256(raw).hexdigest(),'input_sha256':inputs,'refinement_report_sha256':sha(proofpath),'world_translation_mm':c.DELTA,'cam_axis_yz_mm':c.CAM_YZ,'output_frame':'World CAD frame per occurrence; these are not drop-in local definition exports','occurrence_records':records,'exports':checks,'interfaces':interfaces,'expected_unmigrated_context_conflicts':context,'limitations':['No block bore filling or canonical updates','No crank key supplied; refined keyway lacks matched shaft slot/key','Bearing oil feeds, press fits and installed manufacturing dimensions unresolved','Static internal interface scope only; gear phase sweep inherited only by unchanged gear shapes and relative pose, not new shaft/context motion','Browser and CAD valvetrain/distributor adaptation NOT RUN']}
(ROOT/'inventory/engine/timing-core-migration-candidate-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],flush=True)
