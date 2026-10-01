#!/usr/bin/env python3
"""Bounded actual-contact surface continuity study; no source geometry changes."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import trimesh
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
from OCP.BRepBuilderAPI import BRepBuilderAPI_Sewing
from timing_cover_attachment_v2 import norm
O=ROOT/'cad/engine/generated/timing-pan-perimeter-contact';F=ROOT/'cad/engine/generated/timing-pan-expanded-seat-v2-candidate'
pan=norm(b.import_step(F/'pan.step'));gasket=norm(b.import_step(F/'pan-gasket.step'))
baseline_pan=pan
base_out=O
for variant in ['baseline','fault-left','fault-front']:
 O=base_out if variant=='baseline' else base_out/variant
 O.mkdir(exist_ok=True)
 pan=baseline_pan
 if variant=='fault-left':pan=norm(pan-(b.Pos(0,-135,-35)*b.Box(4,40,12)))
 if variant=='fault-front':pan=norm(pan-(b.Pos(390,0,-62)*b.Box(100,4,20)))
 gfaces=[f for f in gasket.faces() if f.normal_at().Z<.05]
 q=BRepAlgoAPI_Common(b.Compound(gfaces).wrapped,b.Compound(list(pan.faces())).wrapped);q.Build();assert q.IsDone()
 faces=list(b.Compound(q.Shape()).faces());print('faces',len(faces), 'area',sum(f.area for f in faces),flush=True)
 sew=BRepBuilderAPI_Sewing(1e-6)
 for f in faces:sew.Add(f.wrapped)
 sew.Perform();shape=b.Compound(sew.SewedShape());b.export_step(shape,O/'actual-contact.step')
 v,f=shape.tessellate(.025,.08);mesh=trimesh.Trimesh(np.array([tuple(q)for q in v]),np.array(f));mesh.merge_vertices(digits_vertex=6)
 np.savez_compressed(O/'contact-mesh.npz',vertices=mesh.vertices,faces=mesh.faces)
 print('mesh',len(mesh.vertices),len(mesh.faces),'components',len(trimesh.graph.connected_components(mesh.face_adjacency,nodes=np.arange(len(mesh.faces))),),flush=True)
 edges=mesh.edges_sorted;unique,counts=np.unique(edges,axis=0,return_counts=True);bound=unique[counts==1]
 report={'scope':'Actual lower mating contact surface, no containment claim','contact_faces':len(faces),'contact_area_mm2':sum(f.area for f in faces),'mesh_vertices':len(mesh.vertices),'mesh_faces':len(mesh.faces),'mesh_components':len(trimesh.graph.connected_components(mesh.face_adjacency,nodes=np.arange(len(mesh.faces))),),'boundary_edges':len(bound),'nonmanifold_edges':int(sum(counts>2))}
 report['input_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),F/'pan.step',F/'pan-gasket.step']}
 (O/'extraction.json').write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True)
