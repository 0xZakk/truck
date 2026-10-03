#!/usr/bin/env python3
from pathlib import Path
import sys,importlib.util,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,numpy as np,trimesh
p=ROOT/'cad/engine/intake-joint-candidate-20261003.py';spec=importlib.util.spec_from_file_location('joint_candidate',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
out=ROOT/'cad/engine/generated/intake-joint-candidate-20261003'
shapes={i:b.import_step(out/(i+'.step')) for i in ('efi-lower-intake','efi-upper-intake','efi-upper-intake-gasket')}
def vol(s):return sum(v.volume for v in s.solids()) if s else 0
def difference(a,c):
 if vol(a)<1e-12:return vol(c)
 if vol(c)<1e-12:return vol(a)
 return vol(a-c)+vol(c-a)
r={'scope':'candidate geometry checks only; no installed/motion approval','port_checks':[],'hole_checks':[],'negative_controls':{},'protected_regions':{},'exports':{}}
for i,x in enumerate(m.X,1):
 probe=m.cyl(24.5,356,367,x,-228)
 vals={k:vol(s&probe) for k,s in shapes.items()};r['port_checks'].append({'port':i,'probe_radius_mm':24.5,'intersection_mm3':vals})
for h,(x,y) in m.H.items():
 probe=m.cyl(5.25,350,371.5,x,y);r['hole_checks'].append({'hole':h,'intersection_mm3':{k:vol(s&probe) for k,s in shapes.items()}})
# Face land is compared as thin slabs translated onto one datum, apart from gasket bore allowance.
lo=shapes['efi-lower-intake'];up=shapes['efi-upper-intake'];ga=shapes['efi-upper-intake-gasket']
slab=lambda z:b.Pos(0,-228,z)*b.Box(800,180,.1)
face_l=lo&slab(359.95);face_u=b.Pos(0,0,-1.6)*(up&slab(361.55))
r['unmasked_face_slab_difference_mm3']=difference(face_l,face_u)
face_mask=m.outline(359.9,360.0)
r['face_land_symmetric_difference_mm3']=difference(face_l&face_mask,face_u&face_mask)
r['mating_face_expected_z_mm']=[360,361.5]
r['mating_face_actual_upper_min_z_mm']=up.bounding_box().min.Z
base=m.cyl(24.5,350,371.5,m.X[1],-228)
r['negative_controls']['shifted_port_5mm']=vol(lo&(b.Pos(5,0,0)*base))
r['negative_controls']['blocked_port_added_disc']=vol((lo+m.cyl(26,357,358,m.X[1],-228))&base)
h=m.H['H1'];r['negative_controls']['mirrored_ear_probe']=vol(ga&m.cyl(5.25,359,363,h[0],-456-h[1]))
# Mirrored missing aperture is detectable by center-to-center registration even when outside gasket metal.
r['negative_controls']['mirrored_ear_nearest_hole_distance_mm']=min(((h[0]-x)**2+(-456-h[1]-y)**2)**.5 for x,y in m.H.values())
(out/'interface-checks-partial.json').write_text(json.dumps(r,indent=2)+'\n')
manifest=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in manifest['definitions']}
regions={'head_injector_region':('efi-lower-intake',b.Pos(0,-156,295)*b.Box(800,38,110)),'throttle_seat':('efi-upper-intake',b.Pos(202,25,490)*b.Box(4,124,68)),'egr_seat':('efi-upper-intake',b.Pos(-197,25,514)*b.Box(8,62,28)), 'regulator_vacuum_receiver':('efi-upper-intake',b.Pos(0,-47,460)*b.Box(12,16,12))}
for name,(key,mask) in regions.items():
 oldpath=ROOT/defs[key]['step'].lstrip('/');old=b.import_step(oldpath)
 try:
  error=difference(old&mask,shapes[key]&mask);status='PASS' if error<.1 else 'FAIL'
 except Exception as exc:
  error=None;status='ERROR '+str(exc)
 r['protected_regions'][name]={'status':status,'symmetric_difference_mm3':error,'baseline_sha256':hashlib.sha256(oldpath.read_bytes()).hexdigest(),'scope':'sampled bounded region; does not establish all adjacent clearance'}
for key,s in shapes.items():
 print('Mesh',key,flush=True);vertices,faces=s.tessellate(.07,.08);v=np.array([tuple(p) for p in vertices]);xyz=v[:,[0,2,1]]*np.array([1,1,-1])/1000
 mesh=trimesh.Trimesh(vertices=xyz.astype(np.float32),faces=faces);mesh.update_faces(mesh.area_faces>0);mesh.remove_unreferenced_vertices();mesh.visual.vertex_colors=[175,185,188,255]
 path=out/(key+'.glb');path.write_bytes(trimesh.Scene(mesh).export(file_type='glb'));check=trimesh.load(path,force='mesh');check.merge_vertices(digits_vertex=8)
 vv=np.array(check.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000;box=s.bounding_box();err=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([tuple(box.min),tuple(box.max)]))))
 r['exports'][key]={'watertight':bool(check.is_watertight),'bounds_error_mm':err,'triangles':len(check.faces),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 np.savez_compressed(out/(key+'-mesh.npz'),vertices_cad_mm=vv,faces=check.faces)
r['rail_axis_probes_mm3']={str(x):vol(lo&m.cyl(3.1,339,365,x,-178)) for x in m.MOUNT_X}
r['injector_axis_probes_mm3']=[vol(lo&m.cyl(7.5,278,318,x-25,-163)) for x in m.core.PORTS]
r['status']='REVIEW REQUIRED';(out/'checks.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2),flush=True)
