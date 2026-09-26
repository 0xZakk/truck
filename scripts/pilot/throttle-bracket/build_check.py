from pathlib import Path
import sys,json,hashlib,importlib.util
import build123d as b
import numpy as np
import trimesh
R=Path(__file__).resolve().parents[3]; C=R/'cad/engine/pilot/throttle-bracket'; I=R/'inventory/engine/pilot/throttle-bracket'; REF=I; REF.mkdir(parents=True,exist_ok=True)
spec=importlib.util.spec_from_file_location('candidate',C/'candidate.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
s=m.shape(); b.export_step(s,C/'accelerator-cable-bracket.step')
v,f=s.tessellate(.12,.15);mesh=trimesh.Trimesh(np.array([tuple(x) for x in v]),np.array(f));mesh.visual.face_colors=[135,146,151,255];mesh.export(C/'accelerator-cable-bracket.glb')
BASE=R; M=BASE/'cad/engine/generated'
checks=[];context={}
def pair(id,n):
 common=s.intersect(n); vol=common.volume if common else 0
 checks.append(dict(id=id,distance_mm=s.distance_to(n),overlap_mm3=vol));context[id]=n
for name in ['throttle-housing','throttle-gasket','iac-valve-body','tps-housing','efi-upper-intake']:
 p=M/(name+'.step')
 if p.exists():
  pose={'iac-valve-body':(397,25,540),'tps-housing':(394,-44,490)}.get(name,(0,0,0));pair(name,b.Pos(*pose)*b.import_step(p))
for z in m.PARAMS['mount_z']:
 pair('stud-'+str(z),b.Pos(373,74,z)*m.mounting_stud_shape())
 pair('baseline-nut-'+str(z),b.Pos(381.5,74,z)*b.import_step(M/'throttle-mount-nut.step'))
 pair('candidate-shifted-nut-'+str(z),b.Pos(383.5,74,z)*b.import_step(M/'throttle-mount-nut.step'))
for angle in [0,45,90]:
 for y in [-27,27]:
  pair(f'plate-{y}-angle-{angle}',b.Pos(394,25,490)*b.Rot(0,angle,0)*b.Pos(0,y,0)*b.import_step(M/'throttle-plate.step'))
pair('throttle-shaft',b.Pos(394,25,490)*b.import_step(M/'throttle-shaft.step'))
# Real face contact area, not only zero minimum distance.
housing=context['throttle-housing']; contact=[]
for a in s.faces():
 for c in housing.faces():
  common=a.intersect(c)
  if common:contact.append(sum(q.area for q in common))
arrays={};meta=[]
for name,obj in {'bracket':s,**context}.items():
 vv,ff=obj.tessellate(.3,.25);i=len(meta);arrays[f'v{i}']=np.array([tuple(v) for v in vv]);arrays[f'f{i}']=np.array(ff);meta.append(name)
arrays['metadata']=np.array(json.dumps(meta));np.savez_compressed(REF/'preview.npz',**arrays)
report=dict(status='candidate-not-production-accepted',valid=s.is_valid,solids=len(s.solids()),volume_mm3=s.volume,bounds_mm=[list(s.bounding_box().min),list(s.bounding_box().max)],mesh_watertight=mesh.is_watertight,checks=checks,housing_coplanar_contact_area_mm2=sum(contact),params=m.PARAMS,source_dimension_count=0,baseline_datum_count=5,limitations=m.GAPS,input_hashes={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [C/'candidate.py',Path(__file__),BASE/'inventory/engine/full-assembly.json']})
# A nominal envelope check is not a thread-strength or tapped-anchorage check.
def contact_area(a,c):
 return sum((common.area if hasattr(common,"area") else sum(q.area for q in common)) for fa in a.faces() for fc in c.faces() if (common:=fa.intersect(fc)))
def stack_check(stud,nut):
 sb,nb=stud.bounding_box(),nut.bounding_box()
 engagement=max(0.,min(sb.max.X,nb.max.X)-max(sb.min.X,nb.min.X))
 protrusion=sb.max.X-nb.max.X
 contact=contact_area(s,nut)
 return dict(nominal_axial_overlap_mm=engagement,protrusion_mm=protrusion,contact_area_mm2=contact,
             pass_envelope=engagement>=6.-1e-6 and protrusion>=2.5-1e-6 and contact>1.)
stacks=[]
for z in m.PARAMS['mount_z']:
 stud=context['stud-'+str(z)];nut=context['candidate-shifted-nut-'+str(z)]
 good=stack_check(stud,nut)
 old=stack_check(b.Pos(371,74,z)*b.import_step(M/'throttle-mount-stud.step'),nut)
 floating=stack_check(stud,b.Pos(1,0,0)*nut)
 good['stud_nut_radial_clearance_mm']=stud.distance_to(nut)
 extension=b.Pos(388,74,z)*b.Rot(0,90,0)*b.Cylinder(4,4)
 good['new_exposed_segment_neighbor_overlap_mm3']={}
 for name in ['throttle-housing','throttle-gasket','iac-valve-body','tps-housing','efi-upper-intake']:
  common=extension.intersect(context[name]);vol=common.volume if common else 0.
  good['new_exposed_segment_neighbor_overlap_mm3'][name]=vol
  assert vol<=.1
 good['negative_controls']={'old_short_stud':old,'floating_nut':floating}
 assert good['pass_envelope'] and not old['pass_envelope'] and not floating['pass_envelope']
 assert good['stud_nut_radial_clearance_mm']>=.19
 stacks.append(good)
roundtrip=b.import_step(C/'accelerator-cable-bracket.step')
loaded=trimesh.load(C/'accelerator-cable-bracket.glb',force='mesh')
assert abs(roundtrip.volume-s.volume)<.001
assert np.max(np.abs(loaded.bounds-mesh.bounds))<.001
assert s.is_valid and len(s.solids())==1 and mesh.is_watertight
assert all(c['overlap_mm3']<=.1 for c in checks if not c['id'].startswith('baseline-nut-'))
assert sum(contact)>1.
stud=m.mounting_stud_shape();b.export_step(stud,C/'bracket-mount-stud-estimated.step')
vv,ff=stud.tessellate(.12,.15);trimesh.Trimesh(np.array([tuple(v) for v in vv]),np.array(ff)).export(C/'bracket-mount-stud-estimated.glb')
report.update(mounting_stack=stacks,stack_parameters=m.STACK,step_roundtrip_volume_error_mm3=abs(roundtrip.volume-s.volume),glb_bounds_error_mm=float(np.max(np.abs(loaded.bounds-mesh.bounds))),
              envelope_gate='PASS',actual_thread_strength_and_intake_anchorage='NOT RUN: threads, materials and engagement depth unknown')
for p in list(M.glob('throttle*.step'))+[M/(n+'.step') for n in ['iac-valve-body','tps-housing','efi-upper-intake']]:
 report['input_hashes'][str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
report['output_hashes']={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in C.glob('*.glb')}
(I/'validation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report,indent=2))
