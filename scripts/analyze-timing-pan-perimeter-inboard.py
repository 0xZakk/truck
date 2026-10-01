#!/usr/bin/env python3
"""Actual contact mesh route, conservatively measured against all free boundaries."""
from pathlib import Path
import json,hashlib,heapq,sys
import numpy as np
import trimesh
from scipy.spatial import cKDTree
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/timing-pan-perimeter-contact'
variant=sys.argv[1] if len(sys.argv)>1 else 'baseline'
if variant!='baseline':O=O/variant
a=np.load(O/'contact-mesh.npz');m=trimesh.Trimesh(a['vertices'],a['faces'],process=False);v=m.vertices;f=m.faces;c=m.triangles_center
u,ct=np.unique(m.edges_sorted,axis=0,return_counts=True);boundary=u[ct==1]
# Free-boundary samples at <=0.05mm; subtraction below accounts for this approximation.
samples=[];bg={}
for i,j in boundary:
 p,q=v[i],v[j];samples.extend(p+(q-p)*np.linspace(0,1,max(2,int(np.ceil(np.linalg.norm(q-p)/.05))+1))[:,None]);bg.setdefault(int(i),[]).append(int(j));bg.setdefault(int(j),[]).append(int(i))
loops=[];seen=set();wet_vertices=[]
for start in bg:
 if start in seen:continue
 stack=[start];comp=[]
 while stack:
  n=stack.pop()
  if n in seen:continue
  seen.add(n);comp.append(n);stack.extend(bg[n])
 if np.ptp(v[comp,0])>500 and v[comp,0].max()<380:wet_vertices=comp
 ordered=[start];previous=None;current=start
 while True:
  nxt=next((k for k in bg[current] if k!=previous),None)
  if nxt is None or nxt==start:break
  if nxt in ordered:break
  ordered.append(nxt);previous,current=current,nxt
 angles=np.arctan2(v[ordered,1],v[ordered,0]);winding=float((((np.diff(np.r_[angles,angles[0]])+np.pi)%(2*np.pi))-np.pi).sum()/(2*np.pi))
 loops.append({'winding_about_wet_origin':winding,'vertices':len(comp),'bounds_mm':[v[comp].min(0).tolist(),v[comp].max(0).tolist()],'degree_two':all(len(bg[n])==2 for n in comp)})
tree=cKDTree(np.array(samples));adj=m.face_adjacency;mid=v[m.face_adjacency_edges].mean(1)
# Each dual edge travels within two actual contact triangles through their shared edge.
# Sample<=0.25mm: distance is 1-Lipschitz, so subtract half interval + boundary sampling + CAD tessellation allowance.
margin=.125+.05+.025
weights=[]
for (i,j),p in zip(adj,mid):
 points=[]
 for aa,bb in [(c[i],p),(p,c[j])]:points.extend(aa+(bb-aa)*np.linspace(0,1,max(2,int(np.ceil(np.linalg.norm(bb-aa)/.25))+1))[:,None])
 weights.append(max(0,float(tree.query(np.array(points))[0].min())-margin))
g=[[] for _ in c]
for k,((i,j),w) in enumerate(zip(adj,weights)):g[i].append((j,w,k));g[j].append((i,w,k))
anchors=[(0,-130,-34),(-367,0,-53.1),(0,108,-34),(375,0,-61.4)]
wet_tree=cKDTree(v[wet_vertices]);near_wet=wet_tree.query(c)[0]
ids=[int(np.argmin(np.linalg.norm(c-p,axis=1))) for p in anchors]
constraints=[lambda p:p[0]<20 and p[1]<20,lambda p:p[0]<20 and p[1]>-20,lambda p:p[0]>-20 and p[1]>-20,lambda p:p[0]>-20 and p[1]<20]
paths=[];legs=[]
for src,dst,allowed in zip(ids,ids[1:]+ids[:1],constraints):
 capacity=np.full(len(c),np.inf);capacity[src]=0;prev={};heap=[(0,src)]
 while heap:
  val,i=heapq.heappop(heap)
  if val>capacity[i]:continue
  if i==dst:break
  for j,w,k in g[i]:
   if not allowed(c[j]) or w<.5:continue
   # Select the inboard homotopy at retained rear station24; no CAD cut.
   segment_ok=True
   for aa,bb in [(c[i],mid[k]),(mid[k],c[j])]:
    if min(aa[1],bb[1])<=-85<=max(aa[1],bb[1]) and abs(bb[1]-aa[1])>1e-9:
     crossing=aa+(bb-aa)*(-85-aa[1])/(bb[1]-aa[1])
     if crossing[0]<-371:segment_ok=False
   if not segment_ok:continue
   new=val+np.linalg.norm(c[j]-c[i])*(1+near_wet[j]**2)
   if new<capacity[j]:capacity[j]=new;prev[j]=(i,k);heapq.heappush(heap,(new,j))
 if not np.isfinite(capacity[dst]):legs.append({'capacity_mm':float(capacity[dst]),'found':False});continue
 nodes=[dst];edgeids=[]
 while nodes[-1]!=src:
  i,k=prev[nodes[-1]];nodes.append(i);edgeids.append(k)
 nodes.reverse();edgeids.reverse();poly=[c[nodes[0]]]
 for j,k in zip(nodes[1:],edgeids):poly.extend([mid[k],c[j]])
 paths.extend(poly);legs.append({'capacity_mm':float(min(weights[k] for k in edgeids)),'found':True,'route_points':len(poly)})
pts=np.array(paths)
if len(legs)==4 and all(x['found'] for x in legs):
 angle=np.arctan2(pts[:,1],pts[:,0]);delta=(np.diff(np.r_[angle,angle[0]])+np.pi)%(2*np.pi)-np.pi;winding=float(delta.sum()/(2*np.pi));width=2*min(x['capacity_mm'] for x in legs)
else:winding=None;width=0
np.savez_compressed(O/'inboard-route.npz',points=pts)
r={'scope':'Piecewise triangular actual-contact route; tessellation allowance0.025mm. Not full fluid containment or compression proof.','boundary_loops':loops,'boundary_loop_count':len(loops),'contact_surface_euler_characteristic':int(len(v)-len(u)+len(f)),'anchor_face_centers_mm':c[ids].tolist(),'legs':legs,'winding_about_wet_origin':winding,'conservative_contact_route_width_mm':width,'sampling_margin_mm':margin,'status':'PASS bounded finite-width full-perimeter route' if width>0 and abs(abs(winding)-1)<1e-5 else 'FAIL route not demonstrated'}
sys.path.insert(0,str(R/'cad/engine'))
from oil_pan_joint_v9_candidate import STATIONS
from timing_cover_attachment_v2 import RELOCATIONS
holes=[]
for n,xyz in enumerate(STATIONS,1):
 q=RELOCATIONS.get(n,xyz);ang=np.arctan2(pts[:,1]-q[1],pts[:,0]-q[0]);wh=float((((np.diff(np.r_[ang,ang[0]])+np.pi)%(2*np.pi))-np.pi).sum()/(2*np.pi));holes.append({'station':n,'axis_mm':list(q),'route_winding':wh})
wet_windings=[]
for q in v[wet_vertices]:
 ang=np.arctan2(pts[:,1]-q[1],pts[:,0]-q[0]);wet_windings.append(float((((np.diff(np.r_[ang,ang[0]])+np.pi)%(2*np.pi))-np.pi).sum()/(2*np.pi)))
r['wet_boundary_vertices_checked']=len(wet_windings)
r['all_wet_boundary_inside_route']=all(abs(abs(w)-1)<1e-5 for w in wet_windings)
r['all_25_dry_hole_winding']=holes
r['all_holes_outside_route']=all(abs(h['route_winding'])<1e-5 for h in holes)
if not r['all_holes_outside_route'] or not r['all_wet_boundary_inside_route']:r['status']='FAIL dry-hole isolation not demonstrated'
r['input_sha256']={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [Path(__file__),O/'contact-mesh.npz',O/'extraction.json',R/'cad/engine/oil_pan_joint_v9_candidate.py',R/'cad/engine/timing_cover_attachment_v2.py']}
((R/'inventory/engine/timing-pan-perimeter-inboard-review.json') if variant=='baseline' else O/'route-review.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:val for k,val in r.items() if k!='boundary_loops'},indent=2))
