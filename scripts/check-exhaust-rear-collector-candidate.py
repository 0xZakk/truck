#!/usr/bin/env python3
"""Isolated collector gates; --render uses saved actual exported mesh."""
from pathlib import Path
import json,hashlib,sys,math,itertools,inspect,struct
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'cad/engine/generated/exhaust-rear-collector-candidate'
REPORT=ROOT/'inventory/engine/exhaust-rear-collector-validation.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def render():
 import numpy as np
 import trimesh
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from mpl_toolkits.mplot3d.art3d import Poly3DCollection
 paths=[OUT/'baseline.glb',OUT/'exhaust-rear.glb']
 fig=plt.figure(figsize=(15,11));angles=[(12,-90),(15,90),(65,-70)]
 sources=['front','back','three-quarter']
 for row,(elev,azim) in enumerate(angles):
  ax=fig.add_subplot(3,3,row*3+1);ax.imshow(plt.imread(ROOT/f'reference/engine/dorman-674186-{sources[row]}.jpg'));ax.axis('off');ax.set_title('Dorman674-186 · replacement photograph')
  for col,p in enumerate(paths,2):
   mesh=trimesh.load(p,force='mesh');v=mesh.vertices[:,[0,2,1]]*np.array([1,-1,1])*1000
   ax=fig.add_subplot(3,3,row*3+col,projection='3d');pc=Poly3DCollection(v[mesh.faces],facecolors='#99877a',edgecolors='none');ax.add_collection3d(pc)
   low,high=v.min(0),v.max(0);ax.set_xlim(-315,10);ax.set_ylim(-220,-125);ax.set_zlim(135,330);ax.set_box_aspect([325,95,195]);ax.view_init(elev=elev,azim=azim);ax.set_axis_off();ax.set_title(('Baseline box collector' if col==2 else 'Candidate rounded collector'))
 fig.suptitle('Rear collector exterior only · estimated dimensions; EGR end connection and interfaces retained',fontsize=15)
 fig.tight_layout();fig.savefig(OUT/'source-comparison.png',dpi=135);plt.close(fig)
 # Actual half-mesh section uses triangles whose centroids lie behind Y=-180.
 fig=plt.figure(figsize=(14,5))
 for col,p in enumerate(paths,1):
  mesh=trimesh.load(p,force='mesh');v=mesh.vertices[:,[0,2,1]]*np.array([1,-1,1])*1000;tri=v[mesh.faces];tri=tri[tri[:,:,1].mean(1)<-180]
  ax=fig.add_subplot(1,2,col,projection='3d');ax.add_collection3d(Poly3DCollection(tri,facecolors='#a58d78',edgecolors='none'));ax.set_xlim(-315,10);ax.set_ylim(-220,-125);ax.set_zlim(135,330);ax.set_box_aspect([325,95,195]);ax.view_init(elev=8,azim=90);ax.set_axis_off();ax.set_title('Baseline' if col==1 else 'Candidate · actual exported mesh half-view')
 fig.tight_layout();fig.savefig(OUT/'section-review.png',dpi=150);plt.close(fig)
 (OUT/'render-record.json').write_text(json.dumps(dict(script_sha256=sha(__file__),mesh_sha256={p.name:sha(p) for p in paths},images={p.name:sha(p) for p in [OUT/'source-comparison.png',OUT/'section-review.png']},scope='Actual exported mesh render; half-view is triangle-clipped, not an exact CAD section'),indent=2)+'\n')
 print('Rendered actual meshes and source comparison')

def main():
 import numpy as np
 import build123d as b
 import trimesh
 from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
 sys.path.insert(0,str(ROOT/'cad/engine'))
 import exhaust_rear_collector_candidate as c
 import full_engine as engine
 from assembly_math import transforms
 from cad_metrics import solid_volume,support_bounds
 def vol(s):return sum(abs(solid_volume(q,'adaptive')) for q in s.solids()) if s else 0.
 def common(a,z):
  op=BRepAlgoAPI_Common(a.wrapped,z.wrapped);op.Build();assert op.IsDone()
  return None if op.Shape().IsNull() else b.Compound(op.Shape())
 def overlap(a,z):return vol(common(a,z))
 def difference(a,z):return vol(a-z)+vol(z-a)
 def intersects(a,z):return all(min(tuple(a.max)[i],tuple(z.max)[i])-max(tuple(a.min)[i],tuple(z.min)[i])>1e-7 for i in range(3))
 def bounds(p):
  with p.open('rb') as f:
   magic,version,total,length,kind=struct.unpack('<5I',f.read(20));j=json.loads(f.read(length))
  assert magic==0x46546c67 and version==2 and kind==0x4e4f534a
  if any(any(k in n for k in ['matrix','translation','rotation','scale']) for n in j.get('nodes',[])):
   v=np.asarray(trimesh.load(p,force='mesh').vertices)
  else:
   rows=[j['accessors'][t['attributes']['POSITION']] for m in j['meshes'] for t in m['primitives']];v=np.array([r[k] for r in rows for k in ['min','max']])
  v=v[:,[0,2,1]]*np.array([1,-1,1])*1000
  return v.min(0),v.max(0)
 mp=ROOT/'inventory/engine/full-assembly.json';m=json.loads(mp.read_text());D={d['id']:d for d in m['definitions']};O={o['id']:o for o in m['occurrences']};poses=transforms(m);inv=poses['exhaust-rear'].inverse()
 source_record=json.loads((ROOT/'reference/engine/dorman-674186-profile-reviewed.json').read_text())
 inputs=[Path(__file__),Path(c.__file__),ROOT/'cad/engine/exhaust_front_profile.py',ROOT/'cad/engine/exhaust_rear_entries.py',ROOT/'cad/engine/egr_tube.py',ROOT/'cad/engine/assembly_math.py',ROOT/'cad/engine/cad_metrics.py',OUT/'baseline.step',OUT/'baseline.glb',OUT/'baseline-manifest.json',ROOT/D['exhaust-rear']['step'].lstrip('/')]
 for row in source_record['sources']:
  p=ROOT/row['path'];assert sha(p)==row['sha256'];inputs.append(p)
 input_hash={str(p.relative_to(ROOT)):sha(p) for p in inputs}
 assert sha(OUT/'baseline.step')==sha(ROOT/D['exhaust-rear']['step'].lstrip('/')),'Canonical rear changed; explicitly rebaseline'
 exporter_sha=hashlib.sha256(inspect.getsource(engine.define).encode()).hexdigest()
 baseline=b.import_step(OUT/'baseline.step');shape=c.build(baseline)
 print('Built',shape.is_valid,len(shape.solids()),flush=True);assert shape.is_valid and len(shape.solids())==1
 regions=c.protected_regions();protected={name:difference(common(shape,r),common(baseline,r)) for name,r in regions.items()};print('Protected',protected,flush=True);assert max(protected.values())<.001
 # EGR interface is derived independently from the existing face, bore and
 # complete fitting/end-wall envelopes, not from the protective mask itself.
 face=c.rear.egr_tube.MANIFOLD_FACE
 fitting=c.rear.egr_tube.manifold_fitting(insertion_length=c.rear.FITTING_INSERTION_LENGTH)
 bore=b.Pos(face[0]-1,face[1],face[2])*b.Rot(0,90,0)*b.Cylinder(12.1,17,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))
 true_interface=b.Pos(face[0]+8,face[1],face[2])*b.Box(18,48,48)
 mask=regions['provisional_egr_end'];mb=mask.bounding_box()
 interface_bounds={};margins={}
 for name,part in [('entire_fitting',fitting),('bore',bore),('full_end_wall_and_seat',true_interface)]:
  pb=part.bounding_box();interface_bounds[name]=[list(pb.min),list(pb.max)]
  margins[name]=min(*[tuple(pb.min)[i]-tuple(mb.min)[i] for i in range(3)],*[tuple(mb.max)[i]-tuple(pb.max)[i] for i in range(3)])
  assert margins[name]>=.99,(name,margins[name])
 true_interface_diff=difference(common(shape,true_interface),common(baseline,true_interface));assert true_interface_diff<.001
 bore_hit=overlap(shape,bore);assert bore_hit<.001
 flow=c.flow_witness();assert flow.is_valid and len(flow.solids())==1
 flow_hit=overlap(shape,flow);print('Flow obstruction',flow_hit,flush=True);assert flow_hit<.001
 full_ports={str(x):overlap(shape,c.front.runner_void(x,shrink=.25)) for x in c.rear.PORTS};assert max(full_ports.values())<.001,full_ports
 walls=[];probes=[]
 for x,z,r in c.SECTIONS:
  if x not in [-225,-190,-100,-65]:continue
  for angle in range(0,360,45):
   a=math.radians(angle);probe=b.Pos(x,-180+(r-3)*math.cos(a),z+(r-3)*math.sin(a))*b.Sphere(.5);missing=vol(probe)-overlap(shape,probe);walls.append(dict(x=x,angle=angle,missing_mm3=missing));probes.append(probe)
 print('Wall missing',max(q['missing_mm3'] for q in walls),flush=True);assert max(q['missing_mm3'] for q in walls)<.001
 blocker=b.Pos(-145.688,-180,230)*b.Box(3,8,8);blocked=overlap(shape.fuse(blocker),flow);assert blocked>1
 missingwall=vol(probes[0])-overlap(shape-probes[0],probes[0]);assert missingwall>.4
 shifted=b.Pos(0,.5,0)*shape;shift_diff=difference(common(shifted,regions['head_entries_and_bolt_lands']),common(baseline,regions['head_entries_and_bolt_lands']));assert shift_diff>1
 engine.STEP=OUT;engine.OUT=OUT
 engine.define('exhaust-rear',shape,'Rear collector exterior candidate','Rounded variable-section study; all dimensions estimated.','exhaust','#7c6e63',[],[],[],prepared=True)
 saved=b.import_step(OUT/'exhaust-rear.step');roundtrip=difference(shape,saved);assert roundtrip<.02
 # Isolated refinement after existing exporter: preserve raw output as
 # evidence, clear inherited triangulation, and clean only mesh zero-area/
 # duplicate faces. No hole filling or CAD surface changes are permitted.
 from OCP.BRepTools import BRepTools
 raw_glb=OUT/'standard-export.glb';raw_glb.write_bytes((OUT/'exhaust-rear.glb').read_bytes())
 raw_mesh=trimesh.load(raw_glb,force='mesh');raw_mesh.merge_vertices(digits_vertex=8)
 raw_gate=dict(watertight=bool(raw_mesh.is_watertight),triangles=len(raw_mesh.faces),degenerate_faces=int(sum(~raw_mesh.nondegenerate_faces())),duplicate_faces=int(sum(~raw_mesh.unique_faces())),sha256=sha(raw_glb))
 cad_before=vol(saved);BRepTools.Clean_s(saved.wrapped);v,tri=saved.tessellate(.05,.1)
 refined=trimesh.Trimesh(np.array([tuple(q) for q in v])[:,[0,2,1]]*[1,1,-1]/1000,np.array(tri),process=False)
 refined.merge_vertices();refined.update_faces(refined.nondegenerate_faces());refined.update_faces(refined.unique_faces());refined.remove_unreferenced_vertices()
 refined.visual=trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(baseColorFactor=[124,110,99,255],metallicFactor=.65,roughnessFactor=.38))
 (OUT/'exhaust-rear.glb').write_bytes(trimesh.Scene(refined).export(file_type='glb'))
 assert saved.is_valid and abs(vol(saved)-cad_before)<1e-8
 mesh=trimesh.load(OUT/'exhaust-rear.glb',force='mesh');mesh.merge_vertices(digits_vertex=8)
 mesh_gate=dict(watertight=bool(mesh.is_watertight),degenerate_faces=int(sum(~mesh.nondegenerate_faces())),duplicate_faces=int(sum(~mesh.unique_faces())))
 mesh_pass=mesh_gate['watertight'] and not mesh_gate['degenerate_faces'] and not mesh_gate['duplicate_faces']
 print('Mesh gate',mesh_gate,flush=True)
 vertices=mesh.vertices[:,[0,2,1]]*np.array([1,-1,1])*1000;box=support_bounds(saved);bounds_error=float(np.max(abs(np.array([vertices.min(0),vertices.max(0)])-np.array([tuple(box.min),tuple(box.max)]))));assert bounds_error<.2
 # Scan current occurrence bounds cheaply, then use exact saved STEP comparisons.
 low=np.minimum(np.array(tuple(box.min)),np.array(tuple(baseline.bounding_box().min)))-.5;high=np.maximum(np.array(tuple(box.max)),np.array(tuple(baseline.bounding_box().max)))+.5
 cache={};neighbors={};neighbor_hash={};hits=[];checks=[]
 for key,o in O.items():
  if key=='exhaust-rear':continue
  d=D[o['definition']];gp=ROOT/d['glb'].lstrip('/');sp=ROOT/d['step'].lstrip('/')
  if o['definition'] not in cache:cache[o['definition']]=bounds(gp)
  lo,hi=cache[o['definition']];frame=inv*poses[key];v=np.array([tuple(b.Vertex(*pt).moved(frame).center()) for pt in itertools.product(*zip(lo,hi))])
  if not(np.all(v.min(0)<=high) and np.all(low<=v.max(0))):continue
  neighbor_hash[str(gp.relative_to(ROOT))]=sha(gp);neighbor_hash[str(sp.relative_to(ROOT))]=sha(sp)
  s=b.import_step(sp).moved(frame);neighbors[key]=s
  if not intersects(box,s.bounding_box()):continue
  hit=overlap(saved,s);checks.append(dict(neighbor=key,overlap_mm3=hit));print('Neighbor',key,hit,flush=True)
  if hit>.1:hits.append(checks[-1])
 assert not hits,hits
 # Bind only scoped rows: unrelated concurrent manifest changes are recorded,
 # not silently inherited. Fresh stage or installed check still required later.
 ids=['exhaust-rear']+sorted(neighbors);scope={k:dict(occurrence=O[k],definition=D[O[k]['definition']],world_matrix=poses[k].to_tuple()) for k in ids}
 current=json.loads(mp.read_text());nowO={o['id']:o for o in current['occurrences']};nowD={d['id']:d for d in current['definitions']};nowP=transforms(current)
 assert scope=={k:dict(occurrence=nowO[k],definition=nowD[nowO[k]['definition']],world_matrix=nowP[k].to_tuple()) for k in ids}
 assert input_hash=={str(p.relative_to(ROOT)):sha(p) for p in inputs}
 assert all(sha(ROOT/p)==h for p,h in neighbor_hash.items())
 result=dict(status=('PASS isolated candidate; root review pending' if mesh_pass else 'FAIL export mesh gate; isolated CAD checks only; promotion blocked'),candidate_scope='Rounded collector only; retained EGR end mismatch and all dimension uncertainty',baseline_manifest_sha256=sha(OUT/'baseline-manifest.json'),current_manifest_sha256=sha(mp),input_sha256=input_hash,exporter_define_sha256=exporter_sha,scoped_manifest=scope,neighbor_artifact_sha256=neighbor_hash,valid=True,solid_count=1,protected_difference_mm3=protected,egr_interface=dict(bounds_cad_mm=interface_bounds,mask_margin_mm=margins,independent_difference_mm3=true_interface_diff,bore_obstruction_mm3=bore_hit),flow_obstruction_mm3=flow_hit,branch_obstruction_mm3=full_ports,wall_probes=walls,controls=dict(blocked_flow_mm3=blocked,missing_wall_mm3=missingwall,shifted_interface_mm3=shift_diff),neighbor_checks=checks,spatial_neighbor_ids=sorted(neighbors),roundtrip_difference_mm3=roundtrip,isolated_export=dict(raw_standard_export=raw_gate,linear_mm=.05,angular_radians=.1,cad_volume_change_mm3=vol(saved)-cad_before,triangle_count=len(refined.faces)),mesh=dict(**mesh_gate,triangles=len(mesh.faces),bounds_error_mm=bounds_error),exports={ext:sha(OUT/('exhaust-rear.'+ext)) for ext in ['step','glb']},inputs_stable=True,limits=['Not installed; browser NOT RUN','No production dimensions or factory casting identity','32 wall samples only, not global minimum thickness','Finite flow witness, not CFD or pressure sealing','Source comparison retains unsupported EGR location, old lands and provisional discharge station'])
 REPORT.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],flush=True)
 if not mesh_pass:raise SystemExit(1)

if __name__=='__main__':
 if '--render' in sys.argv:render()
 else:main()
