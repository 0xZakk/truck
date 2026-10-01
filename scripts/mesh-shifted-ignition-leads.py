#!/usr/bin/env python3
"""Controlled circular sweep meshes plus native connector meshes; no CAD modification."""
import sys,json,math,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,numpy as np,trimesh
import shifted_ignition_lead_candidate as c
OUT=ROOT/'cad/engine/generated/shifted-ignition-lead-candidate';rows=[];inputs={}
def bind(p):inputs[p]=hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
for p in ['scripts/mesh-shifted-ignition-leads.py','cad/engine/shifted_ignition_lead_candidate.py','cad/engine/ignition_leads.py','inventory/engine/shifted-ignition-lead-build-validation.json']:bind(p)
for cyl in [1,2,3,4,5,6,None]:
 prefix=f'ignition-lead-{cyl}' if cyl else 'ignition-coil-lead';path,_,_=c.path_and_contract(cyl);N=1024;K=48;centers=[];bases=[];u=np.array([0.,1.,0.])
 for i in range(N+1):
  center=np.array(tuple(path.position_at(i/N)));axis=np.array(tuple(path.tangent_at(i/N)));axis/=np.linalg.norm(axis);u=u-axis*np.dot(u,axis);u/=np.linalg.norm(u);v=np.cross(axis,u);centers.append(center);bases.append((u.copy(),v))
 for suffix,radii in [('jacket',[3.5,1.05]),('carbon-core',[1.])]:
  ident=prefix+'-'+suffix;sp=OUT/(ident+'.step');bind(str(sp.relative_to(ROOT)));q=b.import_step(sp);verts=[];faces=[];S=len(radii)
  for center,(u,v) in zip(centers,bases):
   for r in radii:verts.extend(center+r*(math.cos(j*math.tau/K)*u+math.sin(j*math.tau/K)*v) for j in range(K))
  def ix(i,s,j):return i*S*K+s*K+j%K
  for i in range(N):
   for side in range(S):
    for j in range(K):
     a,d,e,f=ix(i,side,j),ix(i,side,j+1),ix(i+1,side,j+1),ix(i+1,side,j)
     faces.extend([(a,d,e),(a,e,f)] if side==0 else [(a,e,d),(a,f,e)])
  for i in [0,N]:
   if S==1:
    centeridx=len(verts);verts.append(centers[i])
    for j in range(K):faces.append((centeridx,ix(i,0,j+1),ix(i,0,j)) if i==0 else (centeridx,ix(i,0,j),ix(i,0,j+1)))
   else:
    for j in range(K):
     a,d,e,f=ix(i,0,j),ix(i,0,j+1),ix(i,1,j+1),ix(i,1,j)
     faces.extend([(a,e,d),(a,f,e)] if i==0 else [(a,d,e),(a,e,f)])
  verts=np.array(verts);mesh=trimesh.Trimesh(verts[:,[0,2,1]]*[1,1,-1]/1000,np.array(faces),process=False);mesh.fix_normals();gp=OUT/(ident+'.glb');mesh.export(gp);rt=trimesh.load(gp,force='mesh');rt.merge_vertices(digits_vertex=8);assert rt.is_watertight and rt.is_winding_consistent and rt.volume>0
  shell=q.shells()[0];err=[]
  for i in range(0,N+1,64):
   for side in range(S):
    for j in range(0,K,12):err.append(shell.distance_to(b.Vertex(*verts[ix(i,side,j)])))
  bb=q.bounding_box();vv=rt.vertices[:,[0,2,1]]*[1,-1,1]*1000;be=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))))
  assert max(err)<.001 and be<.15,(ident,max(err),be)
  rows.append({'id':ident,'method':'Explicit circular-ring tessellation on candidate source path; no hole filling','watertight':True,'winding_consistent':True,'positive_volume':True,'triangles':len(rt.faces),'STEP_shell_samples':len(err),'max_sample_distance_mm':max(err),'bounds_error_mm':be,'artifact':str(gp.relative_to(ROOT)),'sha256':hashlib.sha256(gp.read_bytes()).hexdigest()});print(ident,'mesh PASS',max(err),flush=True)
 for suffix in ['cap-boot','cap-contact']:
  ident=prefix+'-'+suffix;sp=OUT/(ident+'.step');bind(str(sp.relative_to(ROOT)));q=b.import_step(sp);v,f=q.tessellate(.10,.12);v=np.array([tuple(x) for x in v]);mesh=trimesh.Trimesh(v[:,[0,2,1]]*[1,1,-1]/1000,np.array(f),process=True);mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();gp=OUT/(ident+'.glb');mesh.export(gp);rt=trimesh.load(gp,force='mesh');rt.merge_vertices(digits_vertex=8);bb=q.bounding_box();vv=rt.vertices[:,[0,2,1]]*[1,-1,1]*1000;be=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))))
  assert rt.is_watertight and rt.is_winding_consistent and rt.volume>0 and be<.15
  rows.append({'id':ident,'method':'Native actual STEP tessellation','watertight':True,'winding_consistent':True,'positive_volume':True,'triangles':len(rt.faces),'bounds_error_mm':be,'artifact':str(gp.relative_to(ROOT)),'sha256':hashlib.sha256(gp.read_bytes()).hexdigest()})
 (ROOT/'inventory/engine/shifted-ignition-lead-mesh-validation.json').write_text(json.dumps({'status':'RUNNING' if cyl is not None else 'PASS 28 scoped meshes','inputs':inputs,'parts':rows,'limits':['Swept cable STEP surface verification sampled; no dielectric/flex simulation']},indent=2)+'\n')
