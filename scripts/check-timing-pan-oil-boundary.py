#!/usr/bin/env python3
"""Staged oil-boundary check. Fail closed on rim ambiguity; never alter pan."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from timing_cover_attachment_v2 import norm
OUT=ROOT/'cad/engine/generated/timing-pan-oil-boundary';OUT.mkdir(exist_ok=True)
FROZEN=ROOT/'cad/engine/generated/timing-cover-attachment-v2'
gasket=norm(b.import_step(FROZEN/'pan-gasket.step'))
faces=[]
for i,f in enumerate(gasket.faces()):
 n=f.normal_at();bb=f.bounding_box()
 faces.append({'index':i,'type':str(f.geom_type),'area':f.area,'center':list(f.center()),'normal':list(n),'bounds':[list(bb.min),list(bb.max)],'wires':len(f.wires()),'edges':len(f.edges())})
(OUT/'gasket-faces.json').write_text(json.dumps(faces,indent=2)+'\n')
print(json.dumps([f for f in faces if f['normal'][2]>.1],indent=2))
# Upper face classification is provisional until its loops are verified.
upper=[f for f in gasket.faces() if f.normal_at().Z>.1]
counts={};edges={}
for f in upper:
 for e in f.edges():
  k=hash(e);counts[k]=counts.get(k,0)+1;edges[k]=e
boundary=[edges[k]for k,v in counts.items()if v==1]
wires=b.Wire.combine(boundary,tol=1e-6)
wire_report=[]
for i,w in enumerate(wires):
 bb=w.bounding_box()
 wire_report.append({'index':i,'closed':w.is_closed,'length':w.length,'edges':len(w.edges()),'bounds':[list(bb.min),list(bb.max)],'samples':[list(e.position_at(t/8))for e in w.edges()for t in range(9)]})
(OUT/'rim-loops.json').write_text(json.dumps(wire_report,indent=2)+'\n')
print('LOOPS',[(q['index'],q['closed'],round(q['length'],2),q['bounds'])for q in wire_report])
b.export_step(b.Compound(wires),OUT/'rim-loops.step')
# Every residual loop retains its actual neighboring faces for locatable review.
adjacency=[]
for wi in [12,27,28]:
 for e in wires[wi].edges():
  ff=[]
  for fi,f in enumerate(gasket.faces()):
   if any(e.is_same(q)for q in f.edges()):ff.append({'face':fi,'normal':list(f.normal_at()),'center':list(f.center()),'type':str(f.geom_type)})
  adjacency.append({'loop':wi,'edge_center':list(e.center()),'adjacent_faces':ff})
(OUT/'residual-loop-adjacency.json').write_text(json.dumps(adjacency,indent=2)+'\n')
# The three residual upper-face loops are finite-height radius-8 pad steps.
# Their adjacent vertical faces join upper regions; they are not through-holes.
upper += [list(gasket.faces())[i]for i in [53,329,330]]
counts={};edges={}
for f in upper:
 for e in f.edges():
  k=hash(e);counts[k]=counts.get(k,0)+1;edges[k]=e
wires=b.Wire.combine([edges[k]for k,v in counts.items()if v==1],tol=1e-6)
final=[]
for i,w in enumerate(wires):
 bb=w.bounding_box();final.append({'index':i,'closed':w.is_closed,'length':w.length,'bounds':[list(bb.min),list(bb.max)],'samples':[list(e.position_at(t/8))for e in w.edges()for t in range(9)]})
(OUT/'classified-rim-loops.json').write_text(json.dumps(final,indent=2)+'\n')
print('FINAL LOOPS',len(wires),flush=True)
# Export observed central rim separately, before any temporary fixture generation.
central=[(i,w)for i,w in enumerate(wires)if w.length>1000 and w.bounding_box().max.X<380]
assert len(wires)==27 and len(central)==1 and all(w.is_closed for w in wires)
central_i,central_wire=central[0]
b.export_step(central_wire,OUT/'central-inner-rim.step')
from timing_cover_attachment_v2 import RELOCATIONS
from oil_pan_joint_v9_candidate import STATIONS
import math
mapping=[]
for n,p in enumerate(STATIONS,1):
 p=RELOCATIONS.get(n,p);expected=(p[0],p[1],p[2]+7.6)
 matches=[]
 for i,w in enumerate(wires):
  bb=w.bounding_box();ctr=tuple(bb.center())
  if abs(w.length-2*math.pi*4.3)<1e-5 and math.dist(ctr,expected)<1e-5:matches.append(i)
 mapping.append({'station':n,'expected_upper_center_mm':expected,'matching_loop_indices':matches,'classification':'dry mounting hole; never capped'})
assert all(len(q['matching_loop_indices'])==1 for q in mapping)
(OUT/'dry-hole-classification.json').write_text(json.dumps(mapping,indent=2)+'\n')
# Trial fan roof fixture: observed rim edges meet a declared high interior apex.
# This is a closure instrument, never candidate geometry or a factory contour.
print('Build ruled fan roof trial',flush=True)
roof_parts=[];roof_faces=[];top_edges=[];target=b.Face.make_rect(2000,2000)
for ei,e in enumerate(central_wire.edges()):
 projected=e.scale(.1).project_to_shape(target,direction=(0,0,1))
 assert len(projected)==1
 top=projected[0]
 expected=e.position_at(0)*.1;expected=b.Vector(expected.X,expected.Y,0)
 if (top.position_at(0)-expected).length>(top.position_at(1)-expected).length:top=top.reversed()
 assert (top.position_at(0)-expected).length<1e-5
 top_edges.append(top)
 face=b.Face.make_surface_from_curves(e,top)
 assert face.is_valid
 roof_faces.append(face)
 patch=b.Solid.extrude(face,(0,0,.5))
 if patch.volume<0:patch=b.Solid(patch.wrapped.Reversed())
 roof_parts.append(patch)
 print('Roof ruled patch',ei,flush=True)
top_wires=b.Wire.combine(top_edges,tol=1e-6);assert len(top_wires)==1 and top_wires[0].is_closed
roof_parts.append(b.Solid.extrude(b.Face(top_wires[0]),(0,0,.5)))
roof_faces.append(b.Face(top_wires[0]))
# Sew an explicit closed boundary rather than fusing individual wedge volumes.
faces_for_shell=[]
for f in roof_faces:
 faces_for_shell.extend([f,b.Pos(0,0,.5)*f])
for e in central_wire.edges():faces_for_shell.append(b.Face.make_surface_from_curves(e,b.Pos(0,0,.5)*e))
shell=b.Shell(faces_for_shell)
roof=b.Solid(shell).fix()
b.export_step(roof,OUT/'roof-trial.step')
print('ROOF',roof.is_valid,len(roof.solids()),roof.volume,flush=True)
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common,BRepAlgoAPI_Cut
from cad_metrics import solid_volume
import numpy as np
import trimesh
import oil_pan as source_pan
import timing_pan_access_candidate as candidate

def boolean(a,d,cut=False):
 op=(BRepAlgoAPI_Cut if cut else BRepAlgoAPI_Common)(a.wrapped,d.wrapped)
 if not op.IsDone():raise RuntimeError('Boolean failed')
 return None if op.Shape().IsNull() else norm(b.Compound(op.Shape()))
def volume(s):return 0 if s is None else sum(abs(solid_volume(q,'adaptive'))for q in s.solids())
def overlap(a,d):return volume(boolean(a,d))
def export_mesh(s,name):
 v,f=s.tessellate(.08,.12);m=trimesh.Trimesh(np.array([tuple(q)for q in v]),np.array(f));m.merge_vertices(digits_vertex=6)
 np.savez_compressed(OUT/(name+'.npz'),vertices=m.vertices,faces=m.faces)
 return {'watertight':m.is_watertight,'components':len(m.split(only_watertight=False)),'volume_mm3':m.volume}
assert roof.is_valid and len(roof.solids())==1
pan=norm(b.import_step(ROOT/'cad/engine/generated/timing-pan-access-candidate/pan.step'))
# Upward copy provides a 0.5 mm roof landing on actual gasket footprint.
# It retains every bore, never extends down to hide a pan-wall breach.
collar=b.Pos(0,0,.5)*gasket
b.export_step(collar,OUT/'roof-gasket-collar.step')
roof_pan=overlap(roof,pan);collar_pan=overlap(collar,pan)
print('Fixture pan overlap',roof_pan,collar_pan,flush=True)
frame=b.Pos(0,-12,-96)*b.Pos(*source_pan.DRAIN_LOCAL)*b.Rot(*source_pan.DRAIN_ROTATION)
drain=frame*(b.Pos(0,0,-.25)*b.Cylinder(7.2,.5))
ring=frame*(b.Pos(0,0,-.25)*(b.Cylinder(7.2,.5)-b.Cylinder(7.1,1)))
bore=frame*(b.Pos(0,0,-.25)*b.Cylinder(7.09,.49))
drain_rim_missing=volume(boolean(ring,pan,True));drain_bore_obstruction=overlap(bore,pan)
b.export_step(drain,OUT/'drain-test-cap.step')
roof_mesh=export_mesh(roof,'roof-preview')
witnesses={'main':(0,-7,-100),'rear_sump':(-165,-12,-220),'front_neck':(370,0,-70),'shoulder_above':(355,0,-74),'shoulder_below':(355,0,-82),'rear_join':(330,0,-60)}
dry_witnesses={str(n):(p[0],p[1],p[2]-2.75)for n,p in RELOCATIONS.items()}
box=candidate.box(-450,450,-250,270,-320,100)
def classify(pan_shape,label,include_drain=True,blockage=None):
 print('Void test',label,flush=True)
 void=box
 for step,obstacle in enumerate([pan_shape,gasket,collar,roof]+([drain]if include_drain else [])+([blockage]if blockage else [])):
  void=boolean(void,obstacle,True)
  print('Void subtraction',label,step,'valid',None if void is None else void.is_valid,flush=True)
  if void is None or not void.is_valid:
   if void is not None:b.export_step(void,OUT/(label+'-invalid-step-'+str(step)+'.step'))
   return {'status':'FAIL kernel invalid result; no containment inference','invalid_subtraction_step':step,'all_witnesses_one_enclosed_cavity':False}
 assert void is not None and void.is_valid
 components=[];membership={k:[]for k in witnesses}
 for i,q in enumerate(void.solids()):
  bb=q.bounding_box();lo=list(bb.min);hi=list(bb.max)
  exterior=any(abs(lo[j]-list(box.bounding_box().min)[j])<1e-5 or abs(hi[j]-list(box.bounding_box().max)[j])<1e-5 for j in range(3))
  members=[]
  for key,p in witnesses.items():
   if q.is_inside(p,tolerance=1e-7):membership[key].append(i);members.append(key)
  components.append({'index':i,'exterior':exterior,'witnesses':members,'bounds_mm':[lo,hi]})
 enclosed=[q for q in components if not q['exterior'] and len(q['witnesses'])==len(witnesses)]
 b.export_step(void,OUT/(label+'-voids.step'))
 if enclosed:
  cavity=list(void.solids())[enclosed[0]['index']];b.export_step(cavity,OUT/(label+'-cavity.step'));export_mesh(cavity,label+'-cavity-preview')
 dry_membership={key:[i for i,q in enumerate(void.solids())if q.is_inside(p,tolerance=1e-7)]for key,p in dry_witnesses.items()}
 return {'components':components,'membership':membership,'head_center_membership':dry_membership,'head_centers_mm':dry_witnesses,'all_heads_outside_enclosed_wet_volume':None if not enclosed else all(enclosed[0]['index']not in ids for ids in dry_membership.values()),'all_witnesses_one_enclosed_cavity':len(enclosed)==1}
result={'stage':'fixture and void diagnostic','rim_loops':27,'central_loop_index':central_i,'dry_holes':mapping,'roof_valid':roof.is_valid,'roof_solids':len(roof.solids()),'roof_mesh':roof_mesh,'roof_pan_overlap_mm3':roof_pan,'collar_pan_overlap_mm3':collar_pan,'drain_rim_missing_mm3':drain_rim_missing,'drain_bore_obstruction_mm3':drain_bore_obstruction,'controls':'NOT RUN','containment':'NOT RUN'}
(OUT/'fixture-checkpoint.json').write_text(json.dumps(result,indent=2)+'\n')
if roof_pan<.01 and collar_pan<.01 and drain_rim_missing<.01 and drain_bore_obstruction<.01:
 result['candidate']=classify(pan,'candidate')
 result['frozen']=classify(norm(b.import_step(FROZEN/'pan.step')),'frozen')
 result['containment']='NOT VERIFIED; invalid roof-subtraction result prevents cavity classification and adversarial controls'
 result['checker_status']='FAIL CLOSED' if any('invalid_subtraction_step'in result[k]for k in ['candidate','frozen']) else 'DIAGNOSTIC ONLY; controls pending'
else:result['fixture_status']='FAIL; no containment inference'
result['input_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [Path(__file__),FROZEN/'pan-gasket.step',FROZEN/'pan.step',ROOT/'cad/engine/generated/timing-pan-access-candidate/pan.step']}
(ROOT/'inventory/engine/timing-pan-oil-boundary-validation.json').write_text(json.dumps(result,indent=2)+'\n')
print('DONE',flush=True)
