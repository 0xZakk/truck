#!/usr/bin/env python3
"""Reproduce failed source-preserving export repair without canonical changes."""
from pathlib import Path
import hashlib,json,sys
import build123d as b
import numpy as np
import trimesh
from OCP.BRepTools import BRepTools
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from cad_metrics import solid_volume,support_bounds
OUT=ROOT/'cad/engine/generated/exhaust-rear-collector-candidate'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
p=OUT/'exhaust-rear.step';source_sha=sha(p);s=b.import_step(p);before=solid_volume(s,'adaptive');box=support_bounds(s)
BRepTools.Clean_s(s.wrapped)
v,f=s.tessellate(.05,.1)
mesh=trimesh.Trimesh(np.array([tuple(x) for x in v])[:,[0,2,1]]*[1,1,-1]/1000,np.array(f),process=False)
mesh.merge_vertices();raw=dict(watertight=bool(mesh.is_watertight),faces=len(mesh.faces))
mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices()
out=OUT/'repair-probe.glb';mesh.export(out)
reopened=trimesh.load(out,force='mesh');reopened.merge_vertices(digits_vertex=8)
edges=reopened.edges_unique[np.bincount(reopened.edges_unique_inverse)==1]
edgepoints=reopened.vertices[edges].mean(1)[:,[0,2,1]]*[1,-1,1]*1000
vertices=reopened.vertices[:,[0,2,1]]*[1,-1,1]*1000
err=float(np.max(abs(np.array([vertices.min(0),vertices.max(0)])-np.array([tuple(box.min),tuple(box.max)]))))
assert sha(p)==source_sha and s.is_valid and len(s.solids())==1
assert abs(solid_volume(s,'adaptive')-before)<1e-8
r=dict(status='FAIL repair mesh remains nonwatertight' if not reopened.is_watertight else 'PASS repair mesh',input_step_sha256=source_sha,script_sha256=sha(Path(__file__)),parameters=dict(linear_mm=.05,angular_radians=.1),cad_volume_change_mm3=solid_volume(s,'adaptive')-before,cad_valid=s.is_valid,raw=raw,cleaned_export=dict(watertight=bool(reopened.is_watertight),triangles=len(reopened.faces),degenerate_faces=int(sum(~reopened.nondegenerate_faces())),duplicate_faces=int(sum(~reopened.unique_faces())),boundary_edges=len(edges),boundary_midpoints_cad_mm=([edgepoints.min(0).tolist(),edgepoints.max(0).tolist()] if len(edges) else None),bounds_error_mm=err,sha256=sha(out)),scope='Clean_s removes triangulation cache only; no CAD geometry edits or mesh hole filling. Isolated export probe; complete candidate checks remain required.')
(OUT/'export-repair-report.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status']);sys.exit(0 if reopened.is_watertight else 1)
