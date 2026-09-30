#!/usr/bin/env python3
"""Exact checks of reviewed isolated outlet exterior; no canonical writes."""
from pathlib import Path
import json,hashlib,sys,math,itertools,inspect,struct
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'cad/engine/generated/rear-exhaust-neck-candidate'
REPORT=ROOT/'inventory/engine/rear-exhaust-neck-candidate-validation.json'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
 import numpy as np
 import build123d as b
 import trimesh
 from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
 sys.path.insert(0,str(ROOT/'cad/engine'))
 import rear_exhaust_neck_candidate as c
 import exhaust_rear_collector_candidate as original
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
 inputs=[Path(__file__),Path(c.__file__),Path(original.__file__),ROOT/'cad/engine/exhaust_front_profile.py',ROOT/'cad/engine/exhaust_rear_entries.py',ROOT/'cad/engine/egr_tube.py',ROOT/'cad/engine/assembly_math.py',ROOT/'cad/engine/cad_metrics.py',OUT/'baseline.step',OUT/'baseline.glb',OUT/'baseline-manifest.json',ROOT/D['exhaust-rear']['step'].lstrip('/')]
 for row in source_record['sources']:
  p=ROOT/row['path'];assert sha(p)==row['sha256'];inputs.append(p)
 input_hash={str(p.relative_to(ROOT)):sha(p) for p in inputs}
 assert sha(OUT/'baseline.step')==sha(ROOT/D['exhaust-rear']['step'].lstrip('/')),'Canonical rear changed; explicitly rebaseline'

 baseline=b.import_step(OUT/'baseline.step');shape=c.build(baseline)
 reviewed=b.import_step(OUT/'candidate.step');reviewed_difference=difference(shape,reviewed);assert reviewed_difference<.001
 assert vol(baseline-shape)<.001,'Exterior study removed baseline material'
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
 flow=original.flow_witness();assert flow.is_valid and len(flow.solids())==1
 flow_hit=overlap(shape,flow);print('Flow obstruction',flow_hit,flush=True);assert flow_hit<.001
 full_ports={str(x):overlap(shape,c.front.runner_void(x,shrink=.25)) for x in c.rear.PORTS};assert max(full_ports.values())<.001,full_ports
 # Full original generated gas volumes, rather than only centerline witnesses.
 gas=original.collector(original.WALL).fuse(b.Pos(c.rear.PORTS[1],-180,175)*b.Cylinder(20,86))
 for x in c.rear.PORTS:gas=gas.fuse(c.front.runner_void(x))
 original_gas=gas-baseline
 full_gas_obstruction=overlap(shape,original_gas);assert full_gas_obstruction<.001
 walls=[];probes=[]
 for z,rx,ry in c.SECTIONS:
  if z not in [158.,174.,190.]:continue
  for angle in range(0,360,45):
   a=math.radians(angle);probe=b.Pos(c.rear.PORTS[1]+(rx-2)*math.cos(a),-180+(ry-2)*math.sin(a),z)*b.Sphere(.5)
   missing=vol(probe)-overlap(shape,probe);walls.append(dict(z=z,angle=angle,missing_mm3=missing));probes.append(probe)
 print('Wall missing',max(q['missing_mm3'] for q in walls),flush=True);assert max(q['missing_mm3'] for q in walls)<.001
 blocker=b.Pos(-145.688,-180,230)*b.Box(3,8,8);blocked=overlap(shape.fuse(blocker),flow);assert blocked>1
 missingwall=vol(probes[0])-overlap(shape-probes[0],probes[0]);assert missingwall>.4
 shifted=b.Pos(0,.5,0)*shape;shift_diff=difference(common(shifted,regions['head_entries_and_bolt_lands']),common(baseline,regions['head_entries_and_bolt_lands']));assert shift_diff>1
 # Verify the reviewed exports directly; no shared exporter calls or writes.
 saved=reviewed;roundtrip=difference(shape,saved);assert roundtrip<.02
 mesh=trimesh.load(OUT/'candidate.glb',force='mesh');mesh.merge_vertices(digits_vertex=8)
 mesh_gate=dict(watertight=bool(mesh.is_watertight),degenerate_faces=int(sum(~mesh.nondegenerate_faces())),duplicate_faces=int(sum(~mesh.unique_faces())))
 mesh_pass=mesh_gate['watertight'] and not mesh_gate['degenerate_faces'] and not mesh_gate['duplicate_faces'];assert mesh_pass
 vertices=mesh.vertices[:,[0,2,1]]*np.array([1,-1,1])*1000;box=support_bounds(saved);bounds_error=float(np.max(abs(np.array([vertices.min(0),vertices.max(0)])-np.array([tuple(box.min),tuple(box.max)]))));assert bounds_error<.1
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
 result=dict(status=('PASS isolated candidate; root review pending' if mesh_pass else 'FAIL export mesh gate; isolated CAD checks only; promotion blocked'),candidate_scope='Estimated outlet exterior only; flange and all physical interfaces retained',baseline_manifest_sha256=sha(OUT/'baseline-manifest.json'),current_manifest_sha256=sha(mp),input_sha256=input_hash,scoped_manifest=scope,neighbor_artifact_sha256=neighbor_hash,valid=True,solid_count=1,protected_difference_mm3=protected,egr_interface=dict(bounds_cad_mm=interface_bounds,mask_margin_mm=margins,independent_difference_mm3=true_interface_diff,bore_obstruction_mm3=bore_hit),reviewed_shape_difference_mm3=reviewed_difference,full_original_gas_obstruction_mm3=full_gas_obstruction,baseline_material_removed_mm3=vol(baseline-shape),flow_obstruction_mm3=flow_hit,branch_obstruction_mm3=full_ports,wall_probes=walls,controls=dict(blocked_flow_mm3=blocked,missing_wall_mm3=missingwall,shifted_interface_mm3=shift_diff),neighbor_checks=checks,spatial_neighbor_ids=sorted(neighbors),roundtrip_difference_mm3=roundtrip,isolated_export=dict(linear_mm=.05,angular_radians=.1,scope='Previously reviewed preview export; hashes unchanged'),mesh=dict(**mesh_gate,triangles=len(mesh.faces),bounds_error_mm=bounds_error),exports={ext:sha(OUT/('candidate.'+ext)) for ext in ['step','glb']},inputs_stable=True,limits=['Not installed; browser NOT RUN','No production dimensions or factory casting identity','24 wall samples only, not global minimum thickness','Finite flow witness, not CFD or pressure sealing','Source comparison retains unsupported EGR location, old lands and provisional discharge station'])
 REPORT.write_text(json.dumps(result,indent=2)+'\n');print(result['status'],flush=True)
 if not mesh_pass:raise SystemExit(1)

if __name__=='__main__':main()
