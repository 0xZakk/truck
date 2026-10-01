#!/usr/bin/env python3
"""Bounded section, positive-radius path, hardware and source-tool checks."""
from pathlib import Path
import sys,json,hashlib,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,trimesh
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common,BRepAlgoAPI_Cut
from cad_metrics import solid_volume
import timing_pan_dry_neck_candidate as c
from timing_cover_attachment_v2 import RELOCATIONS,cz
OUT=ROOT/'cad/engine/generated/timing-pan-dry-neck-candidate';OUT.mkdir(exist_ok=True)
def op(a,d,cut=False):
 if a is None:return None
 q=(BRepAlgoAPI_Cut if cut else BRepAlgoAPI_Common)(a.wrapped,d.wrapped)
 if not q.IsDone():raise RuntimeError('Boolean failed')
 return None if q.Shape().IsNull() else c.norm(b.Compound(q.Shape()))
def vol(s):return 0 if s is None else sum(abs(solid_volume(q,'adaptive'))for q in s.solids())
def overlap(a,d):
 aa=a.bounding_box();local=op(d,b.Pos(*aa.center())*b.Box(aa.size.X+.04,aa.size.Y+.04,aa.size.Z+.04))
 return 0 if local is None else vol(op(a,local))
def tube(a,d,r):
 a=b.Vector(a);d=b.Vector(d)-a
 return b.Solid.make_cylinder(r,d.length,b.Plane(origin=a,z_dir=d))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
print('Build',flush=True);pan,old=c.build()
ledger=ROOT/'reference/engine/tekton-shd03013-access-review.json';spec=json.loads(ledger.read_text())['nominal_mm'];rows=[]
ends={20:(365.5,-110,-34.85),10:(365.5,170,-34.85),21:(370,-110,-34.85),22:(370,170,-34.85),23:(370,0,-69.75)}
breaches={20:(364.5,366.5,-124,-116,-36,-33),10:(364.5,366.5,179,185,-36,-33),21:(373,379,-111,-109,-36,-33),22:(373,379,171,176,-36,-33),23:(373,379,-1,1,-71,-68)}
for n,p in RELOCATIONS.items():
 print('Station',n,flush=True)
 male=c.norm(b.import_step(c.FROZEN/f'oil-pan-mounting-screw-{n}.step'));washer=c.norm(b.import_step(c.FROZEN/f'oil-pan-mounting-washer-{n}.step'))
 seat=b.Pos(*p)*(cz(7.5,1.6,1.62)-cz(4.3,1,2))
 tool=b.Pos(*p)*cz(spec['outside_diameter']/2,-90-spec['overall_length'],0)
 start=(p[0],p[1],p[2]-2.75);path=tube(start,ends[n],.25)
 breach=c.box(*breaches[n]);bad=op(pan,breach,True)
 row={'station':n,'screw_overlap_mm3':overlap(male,pan),'washer_overlap_mm3':overlap(washer,pan),'seat_missing_mm3':vol(op(seat,pan,True)),'nominal_tool_overlap_mm3':overlap(tool,pan),'nominal_tool_distance_mm':tool.distance_to(pan),'head_to_wet_witness_start_mm':start,'wet_witness_end_mm':ends[n],'path_radius_mm':.25,'wall_blocks_path_mm3':overlap(path,pan),'breached_wall_path_overlap_mm3':overlap(path,bad),'head_center_in_pan':pan.is_inside(start,tolerance=1e-7)}
 wet_link=tube(ends[n],(370,0,-70),.25)
 row['wet_endpoint_to_front_neck_obstruction_mm3']=overlap(wet_link,pan)
 rows.append(row);print(row,flush=True)
 b.export_step(path,OUT/f'station{n}-dry-wet-path.step')
 b.export_step(tool,OUT/f'station{n}-nominal-tool.step')
wet_points=[(370,0,-70),(350,0,-70),(350,0,-82),(330,0,-90),(0,-7,-100)]
wet=[]
for i,(a,d)in enumerate(zip(wet_points,wet_points[1:])):
 path=tube(a,d,1);mid=(b.Vector(a)+b.Vector(d))*.5;block=b.Pos(*tuple(mid))*b.Box(4,4,4)
 wet.append({'start_mm':a,'end_mm':d,'radius_mm':1,'pan_obstruction_mm3':overlap(path,pan),'deliberate_block_overlap_mm3':overlap(path,block)})
 b.export_step(path,OUT/f'wet-path-{i}.step')
# Replay the same station20 head-to-neck witness that exposed the prior failure.
prior_path=tube((365.5,-132,-34.85),(370,0,-70),.25)
prior_pan_path=ROOT/'cad/engine/generated/timing-pan-access-candidate/pan.step'
prior_pan=c.norm(b.import_step(prior_pan_path))
prior_replay={'previous_pan_overlap_mm3':overlap(prior_path,prior_pan),'new_pan_overlap_mm3':overlap(prior_path,pan)}
print('Preservation and sections',flush=True)
rear=c.box(-1000,335,-500,500,-500,500);flange=op(old,c.joint.front_blank(-6,-2)[0]);preserve={'rear_removed_mm3':vol(op(op(old,rear),pan,True)),'rear_added_mm3':vol(op(op(pan,rear),old,True)),'full_front_flange_removed_mm3':vol(op(flange,pan,True))}
neighbors={k:overlap(pan,c.norm(b.import_step(c.FROZEN/(k+'.step'))))for k in ['cover','main-gasket','future-block-land','front-terminal-sealant','pan-gasket']}
sections=[]
for z in [-70,-78,-82,-100,-160,-240]:
 s=b.section(pan,b.Plane.XY.offset(z));q={'z_mm':z,'faces':len(s.faces()),'wires_per_face':[len(f.wires())for f in s.faces()],'valid':s.is_valid}
 if len(s.faces())==1 and len(s.faces()[0].wires())==2:
  ordered=sorted(s.faces()[0].wires(),key=lambda w:b.Face(w).area,reverse=True)
  outer_volume=b.Solid.extrude(b.Face(ordered[0]),(0,0,.02));inner_volume=b.Solid.extrude(b.Face(ordered[1]),(0,0,.02))
  q['all_five_axes_outside_outer_contour']=all(not outer_volume.is_inside((p[0],p[1],z+.01),tolerance=1e-7)for p in RELOCATIONS.values())
  xy=(370,0)if z==-70 else ((350,0)if z>=-100 else(-165,-12))
  q['wet_xy_witness_mm']=xy;q['wet_xy_inside_inner_contour']=inner_volume.is_inside((*xy,z+.01),tolerance=1e-7)
 sections.append(q);b.export_step(s,OUT/f'section-z{z}.step');print(q,flush=True)
# Section-breach control away from roof/flange: the front wall at Z-70.
bad=op(pan,c.box(373,379,-1,1,-71,-69),True);bs=b.section(bad,b.Plane.XY.offset(-70));section_control={'z_mm':-70,'faces':len(bs.faces()),'wires_per_face':[len(f.wires())for f in bs.faces()]}
print('Export',flush=True);b.export_step(pan,OUT/'pan.step');back=c.norm(b.import_step(OUT/'pan.step'));v,f=back.tessellate(.08,.12);mesh=trimesh.Trimesh(np.array([tuple(q)for q in v]),np.array(f));mesh.merge_vertices(digits_vertex=6);np.savez_compressed(OUT/'pan-preview.npz',vertices=mesh.vertices,faces=mesh.faces);trimesh.Trimesh(mesh.vertices[:,[0,2,1]]*[1,1,-1]/1000,mesh.faces).export(OUT/'pan.glb')
export={'valid':pan.is_valid,'solids':len(pan.solids()),'roundtrip_valid':back.is_valid,'roundtrip_volume_delta_mm3':abs(vol(pan)-vol(back)),'watertight':mesh.is_watertight,'mesh_components':len(mesh.split(only_watertight=False))}
loaded=trimesh.load(OUT/'pan.glb',force='mesh');verts_mm=loaded.vertices[:,[0,2,1]]*[1,-1,1]*1000
export['glb_to_mesh_bounds_delta_mm']=float(np.max(np.abs(np.array([verts_mm.min(axis=0),verts_mm.max(axis=0)])-mesh.bounds)))
export['cad_to_mesh_bounds_delta_mm']=float(np.max(np.abs(np.array([tuple(pan.bounding_box().min),tuple(pan.bounding_box().max)])-mesh.bounds)))
inputs=[prior_pan_path,Path(__file__),Path(c.__file__),ledger,ROOT/'inventory/engine/full-assembly.json',*c.FROZEN.glob('*.step')]
r={'scope':'Uninstalled analytic dry-neck candidate. Local separation, paths and selected-plane topology only; full oil containment NOT VERIFIED.','hardware_tool_and_separation':rows,'wet_connectivity_paths':wet,'prior_station20_witness_replay':prior_replay,'preservation':preserve,'seal_neighbor_overlaps_mm3':neighbors,'sections':sections,'prior_straight_path_failure':'Preserved first-straight-path-validation.json: straight tube clips shoulder by1.511111mm³; bent route uses actual opening without changing geometry.','section_breach_control':section_control,'export':export,'outer_xy_mm':c.OUTER,'inner_xy_mm':c.INNER,'all_25_stations':'Five frozen revised transforms;20 rear stations preserved with rear material. No station changes.','tool_scope':'TEKTON nominal OD17.526 length48.26, mouthZ0,90mm axial approach; no tolerance/ratchet/full-vehicle claim. PriorR11 failure unchanged.','containment':'NOT VERIFIED; no global roof Boolean used','browser':'NOT RUN','input_sha256':{str(p.relative_to(ROOT)):sha(p)for p in inputs},'output_sha256':{str(p.relative_to(ROOT)):sha(p)for p in [OUT/'pan.step',OUT/'pan.glb',OUT/'pan-preview.npz']}}
r['local_status']='PASS bounded gates' if all(q[k]<.1 for q in rows for k in ['screw_overlap_mm3','washer_overlap_mm3','seat_missing_mm3','nominal_tool_overlap_mm3','breached_wall_path_overlap_mm3','wet_endpoint_to_front_neck_obstruction_mm3']) and all(q['wall_blocks_path_mm3']>.1 and q['nominal_tool_distance_mm']>0 for q in rows) and all(q['pan_obstruction_mm3']<.01 and q['deliberate_block_overlap_mm3']>.1 for q in wet) and all(q.get('all_five_axes_outside_outer_contour') and q.get('wet_xy_inside_inner_contour')for q in sections) and section_control['wires_per_face']==[1] and prior_replay['previous_pan_overlap_mm3']<.01 and prior_replay['new_pan_overlap_mm3']>.1 and max(preserve.values())<.01 and max(neighbors.values())<.1 and all(q['seat_missing_mm3']<.01 and not q['head_center_in_pan']for q in rows) and export['valid'] and export['solids']==1 and export['watertight'] and export['mesh_components']==1 and export['roundtrip_valid'] and export['roundtrip_volume_delta_mm3']<.01 and export['glb_to_mesh_bounds_delta_mm']<.01 and export['cad_to_mesh_bounds_delta_mm']<.01 else 'FAIL or unresolved bounded gates'
(ROOT/'inventory/engine/timing-pan-dry-neck-candidate-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['local_status'],flush=True)
