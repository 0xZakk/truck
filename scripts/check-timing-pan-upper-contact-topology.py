#!/usr/bin/env python3
"""Minimal owner-joined contact topology audit; no path-optimization graph."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import trimesh
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepBuilderAPI import BRepBuilderAPI_Sewing
from timing_cover_attachment_v2 import norm
O=R/'cad/engine/generated/timing-pan-upper-contact';F=R/'cad/engine/generated/timing-cover-attachment-v2'
paths={'gasket':R/'cad/engine/generated/timing-pan-expanded-seat-v2-candidate/pan-gasket.step','block-v3':R/'cad/engine/generated/timing-front-block-expanded-seat-v3-candidate/block.step','cover-2692':R/'cad/engine/generated/front-seal-2692-candidate/cover.step','terminal-sealant':F/'front-terminal-sealant.step'}
g=norm(b.import_step(paths['gasket']));vertical=b.Compound([f for f in g.faces() if abs(f.normal_at().Z)<.05]);faces=[];varea={}
for name in ['block-v3','cover-2692','terminal-sealant']:
 faces.extend(b.import_step(O/(name+'-contact.step')).faces());owner=norm(b.import_step(paths[name]));op=BRepAlgoAPI_Common(vertical.wrapped,b.Compound(list(owner.faces())).wrapped);op.Build();assert op.IsDone();vf=list(b.Compound(op.Shape()).faces());faces.extend(vf);varea[name]=sum(f.area for f in vf)
def audit(faces,label):
 sew=BRepBuilderAPI_Sewing(1e-6)
 for f in faces:sew.Add(f.wrapped)
 sew.Perform();shape=b.Compound(sew.SewedShape());v,f=shape.tessellate(.025,.08);m=trimesh.Trimesh(np.array([tuple(q)for q in v]),np.array(f));m.merge_vertices(digits_vertex=6)
 e,ct=np.unique(m.edges_sorted,axis=0,return_counts=True);bd=e[ct==1];graph={}
 for i,j in bd:graph.setdefault(int(i),[]).append(int(j));graph.setdefault(int(j),[]).append(int(i))
 loops=[];seen=set()
 for start in graph:
  if start in seen:continue
  order=[start];prev=None;cur=start
  while True:
   seen.add(cur);nxt=next((n for n in graph[cur] if n!=prev),None)
   if nxt is None or nxt==start or nxt in order:break
   order.append(nxt);prev,cur=cur,nxt
  pts=m.vertices[order];ang=np.arctan2(pts[:,1],pts[:,0]);w=float((((np.diff(np.r_[ang,ang[0]])+np.pi)%(2*np.pi))-np.pi).sum()/(2*np.pi));loops.append({'bounds_mm':[pts.min(0).tolist(),pts.max(0).tolist()],'degree_two':all(len(graph[n])==2 for n in order),'winding_about_wet_origin':w})
 b.export_step(shape,O/(label+'-surface.step'));np.savez_compressed(O/(label+'-mesh.npz'),vertices=m.vertices,faces=m.faces)
 return {'connected_face_components':len(trimesh.graph.connected_components(m.face_adjacency,nodes=np.arange(len(m.faces)))),'nonmanifold_edges':int(sum(ct>2)),'euler_characteristic':int(len(m.vertices)-len(e)+len(m.faces)),'boundary_loops':loops,'enclosing_boundary_loops':sum(abs(l['winding_about_wet_origin'])>.5 for l in loops)}
r={'baseline':audit(faces,'joined-upper-contact'),'vertical_contact_area_mm2':varea}
# Remove an independent full-width rail swath from contact surface only; fixture, not production geometry.
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut
cut=b.Pos(0,-130,-32)*b.Box(4,30,12);op=BRepAlgoAPI_Cut(b.Compound(faces).wrapped,cut.wrapped);op.Build();assert op.IsDone();r['transverse_fault']=audit(list(b.Compound(op.Shape()).faces()),'fault-upper-contact')
from oil_pan_joint_v9_candidate import STATIONS
from timing_cover_attachment_v2 import RELOCATIONS
matches=[]
for loop in r['baseline']['boundary_loops']:
 lo,hi=np.array(loop['bounds_mm']);center=(lo+hi)/2
 if hi[0]-lo[0]>500:continue
 distance,station=min((float(np.linalg.norm(center[:2]-np.array(RELOCATIONS.get(n,xyz))[:2])),n) for n,xyz in enumerate(STATIONS,1))
 matches.append({'station':station,'center_error_mm':distance})
r['all_25_hole_boundary_matches']=matches
r['all_25_holes_individually_bounded']=sorted(x['station'] for x in matches)==list(range(1,26)) and max(x['center_error_mm'] for x in matches)<.001
r['scope']='Connected annular contact topology only; width measured by local witnesses, no pressure/containment claim'
r['input_sha256']={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [Path(__file__),R/'cad/engine/oil_pan_joint_v9_candidate.py',R/'cad/engine/timing_cover_attachment_v2.py',*paths.values(),*[O/(n+'-contact.step')for n in ['block-v3','cover-2692','terminal-sealant']]]}
(R/'inventory/engine/timing-pan-upper-contact-topology.json').write_text(json.dumps(r,indent=2)+'\n');print({k:{n:v for n,v in val.items() if n!='boundary_loops'} if isinstance(val,dict) else val for k,val in r.items() if k!='input_sha256'})
