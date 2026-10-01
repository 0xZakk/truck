#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,trimesh
from cad_metrics import solid_volume
import pan_fastener_thread_candidate as c
OUT=ROOT/'cad/engine/generated/pan-fastener-thread-candidate';OUT.mkdir(parents=True,exist_ok=True)
def vol(s):
 if s is None:return 0.
 if isinstance(s,b.ShapeList):return sum(vol(q)for q in s)
 if s.wrapped is None:return 0.
 return sum(abs(solid_volume(q,'adaptive'))for q in s.solids())
def mesh(q):
 v,f=q.tessellate(.08,.12);m=trimesh.Trimesh(np.array([tuple(p)for p in v]),np.array(f));m.merge_vertices(digits_vertex=6);return m
def common(a,d):
 from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
 op=BRepAlgoAPI_Common(a.wrapped,d.wrapped);op.Build()
 if not op.IsDone():return {'status':'KERNEL_ERROR','overlap_mm3':None}
 result=op.Shape()
 return {'status':'DONE_NULL_EMPTY' if result.IsNull() else 'DONE','overlap_mm3':0. if result.IsNull() else vol(b.Compound(result))}
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
print('Build reusable male and female coupon',flush=True);male=c.screw();female=c.female(male);washer=c.solid(b.import_step(ROOT/'cad/engine/generated/oil-pan-mounting-washer.step'))
parts={'pan-screw':male,'female-test-coupon':female,'existing-pan-washer':washer};exports={};preview={};scene=trimesh.Scene()
for i,(name,q)in enumerate(parts.items()):
 print('Export',name,flush=True);original=mesh(q);b.export_step(q,OUT/(name+'.step'));roundtrip=b.import_step(OUT/(name+'.step'));m=mesh(roundtrip);g=trimesh.Trimesh(m.vertices[:,[0,2,1]]*[1,1,-1]/1000,m.faces);g.export(OUT/(name+'.glb'));scene.add_geometry(g,node_name=name);preview['v'+str(i)]=m.vertices;preview['f'+str(i)]=m.faces
 exports[name]={'valid':q.is_valid,'roundtrip_valid':roundtrip.is_valid,'solids':len(q.solids()),'raw_mesh_watertight':original.is_watertight,'roundtrip_mesh_watertight':m.is_watertight,'glb_watertight':g.is_watertight,'euler':int(m.euler_number),'roundtrip_volume_delta_mm3':abs(vol(q)-vol(roundtrip)),'bounds_mm':[tuple(q.bounding_box().min),tuple(q.bounding_box().max)]}
scene.export(OUT/'candidate.glb');np.savez_compressed(OUT/'preview.npz',**preview)
print('Matched phases and axial-only negative controls',flush=True);poses=[]
for angle in [-180,-90,0,90,180]:
 z=c.PITCH*angle/360;pose=b.Pos(0,0,z)*b.Rot(0,0,angle)*male;poses.append({'angle_deg':angle,'advance_mm':z,**common(pose,female)})
faults=[{'axial_only_shift_mm':dz,**common(b.Pos(0,0,dz)*male,female)}for dz in [-.3,.3]]
print('Independent deterministic interior-point controls',flush=True);classified=[]
for angle,advance in [(0,0),(90,c.PITCH/4),(0,.3),(0,-.3)]:
 common=0;total=0
 for rad in [3.32,3.55,3.78]:
  for j in range(6):
   theta=math.radians(11+60*j);local_theta=theta-math.radians(angle)
   for k in range(40):
    z=8.13+.093*k;pt=(rad*math.cos(theta),rad*math.sin(theta),z);mp=(rad*math.cos(local_theta),rad*math.sin(local_theta),z-advance);total+=1
    if female.is_inside(pt,tolerance=1e-7) and male.is_inside(mp,tolerance=1e-7):common+=1
 classified.append({'angle_deg':angle,'advance_mm':advance,'samples':total,'common_interior_points':common})
seat=c.cz(6.3,0,.02)-c.cz(4.15,-1,1);head_support=vol(seat-washer);washer_overlap=vol(male.intersect(washer))
legacy=c.solid(b.import_step(ROOT/'cad/engine/generated/oil-pan-mounting-screw.step'));region=b.Pos(0,0,(-5.3+1.6)/2)*b.Box(30,30,6.9);a=male.intersect(region);d=legacy.intersect(region);preserved={'head_and_collar_removed_mm3':vol(d-a),'head_and_collar_added_mm3':vol(a-d)}
vertices=preview['v0'];thread=vertices[vertices[:,2]>1.7+1e-5];major=2*np.max(np.linalg.norm(thread[:,:2],axis=1));bb=male.bounding_box()
nominal={'major_diameter_parameter_mm':c.DIAMETER,'mesh_observed_major_diameter_mm':float(major),'pitch_mm':c.PITCH,'underhead_length_mm':c.LENGTH,'modeled_length_error_mm':abs(bb.max.Z-c.LENGTH),'major_diameter_error_mm':abs(major-c.DIAMETER),'estimated_root_radius_mm':c.ROOT_RADIUS,'estimated_thread_runout_interval_mm':[1.6,1.7],'estimated_crest_width_mm':.2,'estimated_embedded_root_width_mm':2*c.PROFILE_HALF_WIDTH,'estimated_flank_included_angle_deg':60}
manifest_path=ROOT/'inventory/engine/full-assembly.json';manifest=json.loads(manifest_path.read_text());ids=[q['id']for q in manifest['occurrences']if q['definition']=='oil-pan-mounting-screw'];transforms={q['id']:{k:q.get(k)for k in ['parent','position_cad_mm','rotation_cad_deg']}for q in manifest['occurrences']if q['definition']=='oil-pan-mounting-screw'}
passed=all(v['valid']and v['roundtrip_valid']and v['solids']==1 and v['raw_mesh_watertight']and v['roundtrip_mesh_watertight']and v['glb_watertight']and v['roundtrip_volume_delta_mm3']<.01 for v in exports.values()) and all(q['overlap_mm3'] is not None and q['overlap_mm3']<.1 for q in poses) and all(q['overlap_mm3'] is not None and q['overlap_mm3']>1 for q in faults) and classified[0]['common_interior_points']==0 and classified[1]['common_interior_points']==0 and min(q['common_interior_points']for q in classified[2:])>10 and head_support<.01 and washer_overlap<.1 and max(preserved.values())<.01 and nominal['major_diameter_error_mm']<.01 and nominal['modeled_length_error_mm']<.001 and len(ids)==25
inputs=[Path(__file__),Path(c.__file__),manifest_path,ROOT/'cad/engine/generated/oil-pan-mounting-screw.step',ROOT/'cad/engine/generated/oil-pan-mounting-washer.step',ROOT/'reference/engine/ford-oil-pan-hardware-reviewed.json',ROOT/'inventory/engine/timing-cover-attachment-validation.json']
r={'local_status':'PASS'if passed else'FAIL','readiness':'Isolated reusable thread candidate; root review required, not installed','input_sha256':{str(p.relative_to(ROOT)):h(p)for p in inputs},'nominal_and_estimated_dimensions':nominal,'exports':exports,'matched_pose_tests':poses,'wrong_phase_controls':faults,'independent_point_classification':classified,'head_washer_support_missing_mm3':head_support,'male_washer_overlap_mm3':washer_overlap,'preserved_interfaces':preserved,'proposed_reusable_definition':'oil-pan-mounting-screw','existing_occurrence_ids':ids,'unchanged_existing_transforms':transforms,'female_limit':'Test coupon only. Ideal zero-clearance conjugate and estimated thread profile, not manufacturing fit/strength. No cover or land changes in this module.','five_relocated_socket_revalidation':'NOT RUN','all25_station_interfaces':'NOT RUN','installed':'NOT RUN','browser':'NOT RUN','learning':'NOT RUN'}
(ROOT/'inventory/engine/pan-fastener-thread-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));raise SystemExit(0 if passed else 1)
