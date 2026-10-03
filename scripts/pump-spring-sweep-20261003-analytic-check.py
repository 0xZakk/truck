from pathlib import Path
import json,hashlib,numpy as np,trimesh,build123d as b
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/pump-spring-sweep-20261003';gp=O/'spring-analytic.glb';g=trimesh.load(gp,force='mesh');v=g.vertices[:,[0,2,1]]*[1,-1,1]*1000;m=trimesh.Trimesh(v,g.faces,process=False);step=R/'cad/engine/generated/pump-functional-20261003/water-pump-seal-spring.step';s=b.import_step(step);shell=s.shells()[0];rng=np.random.default_rng(20261003);ids=rng.choice(len(m.faces),400,replace=False);caps=np.where(abs(m.face_normals[:,0])>.99999)[0];ids=np.unique(np.r_[ids,rng.choice(caps,min(100,len(caps)),replace=False)]);points=m.triangles_center[ids];distances=[]
for i,p in enumerate(points):
 distances.append(float(b.Vertex(*p).distance_to(shell)))
 if i%100==0:print('sample',i,flush=True)
bound=np.array([[406.93,-47.9,154.1],[411.43,-16.1,185.9]]);err=float(abs(m.bounds-bound).max());mass=GProp_GProps();e=BRepGProp.VolumePropertiesGK_s(s.wrapped,mass,1e-8,True,True)
# Known tube point at theta=10, inward normal, and radially perturbed bad surface.
theta=10;h=1.4/(2*np.pi);center=np.array([406.38+h*theta,-32+15.5*np.sin(theta),170-15.5*np.cos(theta)]);normal=np.array([0,-np.sin(theta),np.cos(theta)]);good=float(b.Vertex(*(center+.4*normal)).distance_to(shell));bad=float(b.Vertex(*(center+.6*normal)).distance_to(shell))
r={'step_sha256':hashlib.sha256(step.read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(gp.read_bytes()).hexdigest(),'samples':len(points),'surface_max_mm':max(distances),'surface_distances_mm':distances,'bounds_error_mm':err,'bounds_and_sample_gate_mm':.025,'watertight':g.is_watertight,'winding':g.is_winding_consistent,'components':len(g.split()),'mesh_volume_mm3':float(m.volume),'adaptive_cad_volume_mm3':mass.Mass(),'adaptive_relative_error_estimate':e,'volume_difference_fraction':float(abs(m.volume-mass.Mass())/mass.Mass()),'good_analytic_point_distance_mm':good,'bad_wire_radius_control_distance_mm':bad,'finite_scope_only':True,'installed':False}
r['status']='PASS finite analytic surface/export checks' if max(distances)<=.025 and err<=.025 and good<=.025 and bad>.025 and g.is_watertight and g.is_winding_consistent and len(g.split())==1 else 'FAIL'
(R/'reference/engine/pump-spring-sweep-20261003-analytic-check.json').write_text(json.dumps(r,indent=2)+'\n');print({k:v for k,v in r.items() if k!='surface_distances_mm'})
