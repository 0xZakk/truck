#!/usr/bin/env python3
"""Watertight ring tessellation of the identical circular sweep, verified against actual STEP."""
import sys,json,math,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import numpy as np,trimesh,build123d as b
import shifted_oil_pickup_candidate as c
from assembly_math import transforms
OUT=ROOT/'cad/engine/generated/shifted-oil-pickup-candidate';m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());poses=transforms(m)
old=poses['oil-pickup-tube']*b.import_step(ROOT/'cad/engine/generated/oil-pickup-tube.step');q=b.import_step(OUT/'oil-pickup-tube-world.step');_,data=c.build(old)
path=b.Wire(list(data['path'].edges())+[c.original_path().trim(data['parameter'],1)])
N=1024;K=64;centers=[];bases=[];vertices=[]
for i in range(N+1):
 t=i/N;center=np.array(tuple(path.position_at(t)));axis=np.array(tuple(path.tangent_at(t)));axis/=np.linalg.norm(axis);u=np.array([0.,1.,0.]);u-=axis*np.dot(u,axis);u/=np.linalg.norm(u);v=np.cross(axis,u);centers.append(center);bases.append((u,v))
 for r in [6.,4.8]:
  vertices.extend(center+r*(np.cos(j*math.tau/K)*u+np.sin(j*math.tau/K)*v) for j in range(K))
faces=[]
def ix(i,side,j):return i*2*K+side*K+j%K
for i in range(N):
 for side in [0,1]:
  for j in range(K):
   a,d,e,f=ix(i,side,j),ix(i,side,j+1),ix(i+1,side,j+1),ix(i+1,side,j)
   faces.extend([(a,d,e),(a,e,f)] if side==0 else [(a,e,d),(a,f,e)])
for i in [0,N]:
 for j in range(K):
  a,d,e,f=ix(i,0,j),ix(i,0,j+1),ix(i,1,j+1),ix(i,1,j)
  faces.extend([(a,e,d),(a,f,e)] if i==0 else [(a,d,e),(a,e,f)])
v=np.array(vertices);loc=poses['oil-pickup-tube'].inverse().wrapped.Transformation();A=np.array([[loc.Value(i,j) for j in range(1,5)] for i in range(1,4)]);local=v@A[:,:3].T+A[:,3]
mesh=trimesh.Trimesh(local[:,[0,2,1]]*[1,1,-1]/1000,np.array(faces),process=False);mesh.fix_normals();gp=OUT/'oil-pickup-tube-parametric.glb';mesh.export(gp);actual=trimesh.load(gp,force='mesh');actual.merge_vertices(digits_vertex=8);assert actual.is_watertight and actual.is_winding_consistent and actual.volume>0
shell=q.shells()[0];errors=[];chords=[]
for i in range(0,N+1,32):
 for side in [0,1]:
  for j in range(0,K,8):errors.append(shell.distance_to(b.Vertex(*v[ix(i,side,j)])))
 print('surface',i,max(errors),flush=True)
for i in range(0,N,32):
 for side in [0,1]:
  for j in range(0,K,8):
   mid=(v[ix(i,side,j)]+v[ix(i+1,side,j+1)])/2;chords.append(shell.distance_to(b.Vertex(*mid)))
control=shell.distance_to(b.Vertex(*(centers[N//2]+6.2*bases[N//2][0])))
rtlocal=b.import_step(OUT/'oil-pickup-tube.step');bb=rtlocal.bounding_box();av=actual.vertices[:,[0,2,1]]*[1,-1,1]*1000;bounds=float(np.max(abs(np.array([av.min(0),av.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))))
assert max(errors)<1e-3 and max(chords)<.02 and bounds<.15 and control>.15
paths=['scripts/mesh-shifted-oil-pickup-parametric.py','cad/engine/shifted_oil_pickup_candidate.py','inventory/engine/full-assembly.json','cad/engine/generated/oil-pickup-tube.step','cad/engine/generated/shifted-oil-pickup-candidate/oil-pickup-tube-world.step','cad/engine/generated/shifted-oil-pickup-candidate/oil-pickup-tube.step','models/engine/oil-pickup-tube.glb']
legacy=trimesh.load(ROOT/paths[-1],force='mesh');legacy.merge_vertices(digits_vertex=8)
r={'status':'PASS bounded parametric mesh; native tessellation failures retained','inputs':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},'artifact':str(gp.relative_to(ROOT)),'sha256':hashlib.sha256(gp.read_bytes()).hexdigest(),'mesh':{'watertight':True,'winding_consistent':True,'positive_volume':True,'triangles':len(actual.faces),'bounds_error_mm':bounds},'construction':{'axial_intervals':N,'angular_segments':K,'outer_radius_mm':6,'inner_radius_mm':4.8,'method':'Explicit annular ring connectivity on exact same source centerline; no hole filling or component geometry changes'},'actual_STEP_shell_checks':{'vertex_sample_count':len(errors),'max_vertex_distance_mm':max(errors),'chord_midpoint_samples':len(chords),'max_chord_distance_mm':max(chords),'radial_fault_0_2mm_distance_mm':control},'canonical_mesh_watertight':bool(legacy.is_watertight),'limits':['Finite actual STEP shell samples and full mesh bounds; not manufacturing tolerance','Native CAD tessellation failures remain in prior diagnostic','No circuit pressure, gasket or bell-retention acceptance']}
(ROOT/'inventory/engine/shifted-oil-pickup-parametric-mesh-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],flush=True)
