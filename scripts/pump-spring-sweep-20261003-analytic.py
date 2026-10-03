"""Analytic circular helix tube, clipped by explicit axial planes; no native mesh repair."""
from pathlib import Path
import numpy as np,trimesh,json,math,hashlib
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/pump-spring-sweep-20261003';O.mkdir(exist_ok=True)
N,M=1024,256;radius,wire,pitch=15.5,.4,1.4;h=pitch/(2*np.pi);length=np.hypot(radius,h);phi=np.arange(M)*2*np.pi/M
start=(15.5-14.95-wire*radius/length*np.sin(phi))/h;end=(20-14.95-wire*radius/length*np.sin(phi))/h
u=np.linspace(0,1,N+1)[:,None];theta=start[None,:]+u*(end-start)[None,:];c,s=np.cos(theta),np.sin(theta);cp,sp=np.cos(phi)[None,:],np.sin(phi)[None,:]
x=391.43+14.95+h*theta+wire*radius/length*sp;y=-32+radius*s+wire*(-s*cp-h/length*c*sp);z=170-radius*c+wire*(c*cp-h/length*s*sp)
v=np.stack([x,y,z],axis=-1).reshape(-1,3);faces=[]
for i in range(N):
 for j in range(M):
  k=(j+1)%M;a=i*M+j;b=(i+1)*M+j;c0=(i+1)*M+k;d=i*M+k
  faces.extend([(a,c0,b),(a,d,c0)])
def triangulate_loop(points):
 # Ear clipping of the analytically generated simple planar trim loop.
 area=np.sum(points[:,0]*np.roll(points[:,1],-1)-points[:,1]*np.roll(points[:,0],-1))/2
 indices=list(range(len(points))) if area>0 else list(reversed(range(len(points))));out=[]
 def cross(a,b):return a[0]*b[1]-a[1]*b[0]
 while len(indices)>3:
  found=False
  for k in range(len(indices)):
   a,b,c=indices[k-1],indices[k],indices[(k+1)%len(indices)];pa,pb,pc=points[[a,b,c]]
   if cross(pb-pa,pc-pb)<=1e-12:continue
   other=[i for i in indices if i not in (a,b,c)];q=points[other]
   inside=((pb[0]-pa[0])*(q[:,1]-pa[1])-(pb[1]-pa[1])*(q[:,0]-pa[0])>=-1e-12)&((pc[0]-pb[0])*(q[:,1]-pb[1])-(pc[1]-pb[1])*(q[:,0]-pb[0])>=-1e-12)&((pa[0]-pc[0])*(q[:,1]-pc[1])-(pa[1]-pc[1])*(q[:,0]-pc[0])>=-1e-12)
   if np.any(inside):continue
   out.append((a,b,c));indices.pop(k);found=True;break
  if not found:raise RuntimeError('Non-simple or numerically unresolved analytic cap; do not fill arbitrarily')
 out.append(tuple(indices));return out
for base,reverse in [(0,True),(N*M,False)]:
 for a,b,c in triangulate_loop(v[base:base+M,1:]):faces.append((base+a,base+c,base+b) if reverse else(base+a,base+b,base+c))
m=trimesh.Trimesh(v,np.asarray(faces),process=False);gp=O/'spring-analytic.glb';trimesh.Trimesh(v[:,[0,2,1]]*[1,1,-1]/1000,m.faces,process=False).export(gp);g=trimesh.load(gp,force='mesh');gv=g.vertices[:,[0,2,1]]*[1,-1,1]*1000
np.savez_compressed(O/'analytic.npz',vertices=v,faces=m.faces)
r={'construction':'analytic Frenet tube with exact axial clipping and ear-clipped planar caps','parameters':{'radius':radius,'wire_radius':wire,'pitch':pitch,'clip_X':[406.93,411.43],'longitudinal_intervals':N,'circumferential_intervals':M},'native_watertight':m.is_watertight,'native_winding':m.is_winding_consistent,'volume_mm3':float(m.volume),'area_mm2':float(m.area),'glb_watertight':g.is_watertight,'glb_winding':g.is_winding_consistent,'components':len(g.split()),'bounds_mm':[gv.min(0).tolist(),gv.max(0).tolist()],'faces':len(m.faces),'sha256':hashlib.sha256(gp.read_bytes()).hexdigest(),'status':'Geometry generated; STEP distance and interface review pending','installed':False}
(R/'reference/engine/pump-spring-sweep-20261003-analytic.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
