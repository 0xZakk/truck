"""Inspect saved native exports. Finite probes are sampled, not a fit certification."""
from pathlib import Path
import json, hashlib, math
import numpy as np
import trimesh
from cadgen import read_step, build123d as bd
from block_core_cup_mps59a import OD, HEIGHT, THICKNESS

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
OUT=ROOT/'cad/engine/generated/text-to-cad-20261003/plugin'
STEP=OUT/'block_core_cup_mps59a.step'
GLB=OUT/'block_core_cup_mps59a.glb'

def bounds(s):
    b=s.bounding_box(); return np.array([tuple(b.min),tuple(b.max)])

def probes(s):
    floor=[(r*math.cos(a),r*math.sin(a),.5) for r in (0,10,23) for a in np.linspace(0,2*math.pi,12,endpoint=False)]
    cavity=[(r*math.cos(a),r*math.sin(a),z) for r in (0,10,24) for z in (2,4,8.2) for a in np.linspace(0,2*math.pi,12,endpoint=False)]
    wall=[((OD/2-.5)*math.cos(a),(OD/2-.5)*math.sin(a),z) for z in (2,4,8.2) for a in np.linspace(0,2*math.pi,24,endpoint=False)]
    return {n:{'passed':sum(bool(s.is_inside(p))==expected for p in pts),'total':len(pts)} for n,pts,expected in [('floor',floor,True),('cavity',cavity,False),('wall',wall,True)]}

def passes(p): return all(x['passed']==x['total'] for x in p.values())
s=read_step(str(STEP))
b=bounds(s)
expected=np.array([[-OD/2,-OD/2,0],[OD/2,OD/2,HEIGHT]])
bd.export_step(s,str(OUT/'roundtrip.step'))
r=read_step(str(OUT/'roundtrip.step'))
m=trimesh.load(GLB,force='mesh',process=False)
raw_vertices=len(m.vertices)
# GLB splits vertices at CAD face normals. Weld coincident positions solely for topology inspection.
m.merge_vertices(merge_norm=True, merge_tex=True, digits_vertex=8)
# Native glTF is expected to be meter Y-up. Explicit inverse of (X,Z,-Y).
mb=np.array([m.vertices[:,0],-m.vertices[:,2],m.vertices[:,1]]).T*1000
converted=np.array([mb.min(axis=0),mb.max(axis=0)])
p=probes(s)
missing=s-bd.Cylinder(24,2,align=(bd.Align.CENTER,bd.Align.CENTER,bd.Align.MIN)).moved(bd.Location((0,0,-.1)))
blocked=s+bd.Cylinder(OD/2-.5,1,align=(bd.Align.CENTER,bd.Align.CENTER,bd.Align.MIN)).moved(bd.Location((0,0,HEIGHT-1)))
controls={'missing_floor':probes(missing),'blocked_opening':probes(blocked)}
report={'step_valid':s.is_valid,'solid_count':len(s.solids()),'volume_mm3':s.volume,'step_bounds_mm':b.tolist(),'dimension_error_mm':float(np.max(abs(b-expected))),'roundtrip_error_mm':float(np.max(abs(bounds(r)-b))),'native_glb_bounds':m.bounds.tolist(),'glb_inverse_converted_bounds_mm':converted.tolist(),'mesh_bounds_error_mm':float(np.max(abs(converted-b))),'mesh':{'raw_vertices':raw_vertices,'weld_digits_meters':8,'vertices':len(m.vertices),'faces':len(m.faces),'watertight':bool(m.is_watertight),'consistent_winding':bool(m.is_winding_consistent),'components':len(trimesh.graph.connected_components(m.face_adjacency, nodes=np.arange(len(m.faces))))},'probes':p,'controls':controls,'control_rejections':{n:not passes(v) for n,v in controls.items()},'tolerance_mm':.025,'sampling':'36 floor,108 cavity,72 wall points; CAD interiors, away from boundaries','hashes':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (STEP,GLB,OUT/'roundtrip.step',Path(__file__),HERE/'block_core_cup_mps59a.py')}}
report['pass']=bool(s.is_valid and len(s.solids())==1 and s.volume>0 and report['dimension_error_mm']<.025 and report['roundtrip_error_mm']<.025 and report['mesh_bounds_error_mm']<.025 and m.is_watertight and m.is_winding_consistent and report['mesh']['components']==1 and passes(p) and all(report['control_rejections'].values()))
(HERE/'report.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert report['pass']
