#!/usr/bin/env python3
"""Explicit constructed wall, real hardware, seal preservation and estimated access."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,trimesh
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common,BRepAlgoAPI_Cut
import timing_pan_access_candidate as c
import timing_cover_attachment_v2 as v
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-pan-access-candidate';OUT.mkdir(exist_ok=True)
volume_errors=[]
def vol(s):
 if s is None:return 0.
 try:return sum(abs(solid_volume(q,'adaptive'))for q in s.solids())
 except ValueError as e:
  volume_errors.append(str(e));return float('inf') # fail closed, preserve diagnostic

def op(a,d,cut=False):
 if a is None:return None
 if d is None:return a if cut else None
 q=(BRepAlgoAPI_Cut if cut else BRepAlgoAPI_Common)(a.wrapped,d.wrapped)
 if not q.IsDone():raise RuntimeError('Boolean failed')
 return None if q.Shape().IsNull() else c.norm(b.Compound(q.Shape()))
def overlap(a,d):
 if a is None or d is None:return 0.
 aa=a.bounding_box();dd=d.bounding_box()
 if any(min(tuple(aa.max)[i],tuple(dd.max)[i])-max(tuple(aa.min)[i],tuple(dd.min)[i])<1e-7 for i in range(3)):return 0.
 size=aa.size;local=op(d,b.Pos(*aa.center())*b.Box(size.X+.04,size.Y+.04,size.Z+.04))
 return vol(op(a,local))
def missing(a,d):return vol(op(a,d,True))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
print('Build',flush=True);pan,old=c.build();rows=[]
for n,p in v.RELOCATIONS.items():
 print('Hardware',n,flush=True)
 male=c.norm(b.import_step(c.FROZEN/f'oil-pan-mounting-screw-{n}.step'));washer=c.norm(b.import_step(c.FROZEN/f'oil-pan-mounting-washer-{n}.step'))
 # Radius 11 estimate, axial insertion from below; ends at washer underside.
 tool=b.Pos(*p)*v.cz(11,-90,1.6)
 seat=b.Pos(*p)*(v.cz(7.5,1.6,1.62)-v.cz(4.3,1,2))
 rows.append({'station':n,'screw_overlap_mm3':overlap(male,pan),'washer_overlap_mm3':overlap(washer,pan),'seat_missing_mm3':missing(seat,pan),'estimated_tool_overlap_mm3':overlap(tool,pan),'estimated_tool_distance_mm':tool.distance_to(pan)})
 print(rows[-1],flush=True)
print('Preservation',flush=True)
rear=c.box(-1000,335,-500,500,-500,500);flange=c.norm(old.intersect(c.j.front_blank(-6,-2)[0]))
preserve={'rear_removed_mm3':missing(op(old,rear),pan),'rear_added_mm3':missing(op(pan,rear),old),'full_front_flange_removed_mm3':missing(flange,pan)}
seals={k:overlap(pan,c.norm(b.import_step(c.FROZEN/(k+'.step'))))for k in v.PARTS if k!='pan'}
# Full rectangular probes stay within the explicitly estimated wall, away from
# designed apertures and top trim. Shoulder probes span the full joint thickness.
probes={}
for y in [-110,-60,0,60,140,178]:
 probes[f'front_y{y}']=missing(c.box(374,378,y-.1,y+.1,-75,-66),pan)
for x in [355,360,365,370,373]:
 probes[f'side_x{x}']=missing(c.box(x-.1,x+.1,180,184,-74,-40),pan)
for y in [-100,0,100]:
 probes[f'shoulder_y{y}']=missing(c.box(363.1,377.9,y-.1,y+.1,-80,-76),pan)
# Oil-side witness channel crosses shoulder into lower body, with no pan solid.
wet=c.box(345,359,-100,100,-85,-65)
wet_obstruction=overlap(wet,pan)
# Negative controls prove wall and seat probes respond to actual missing material.
bad=op(pan,c.box(374,378,-.2,.2,-75,-66),True)
controls={'missing_front_wall_detected_mm3':missing(c.box(374,378,-.1,.1,-75,-66),bad),'frozen_tool_conflict_mm3':overlap(b.Pos(*v.RELOCATIONS[23])*v.cz(11,-90,1.6),old)}
diagnostics={}
for n in [20,10]:
 hit=op(b.Pos(*v.RELOCATIONS[n])*v.cz(11,-90,1.6),pan)
 diagnostics[str(n)]={'intersection_valid':None if hit is None else hit.is_valid,'nonadaptive_volume_diagnostic_only_mm3':0 if hit is None else hit.volume,'bounds_mm':None if hit is None else [list(hit.bounding_box().min),list(hit.bounding_box().max)]}
diagnostics['wet_probe_frozen_overlap_mm3']=overlap(wet,old)
print('Export',flush=True);b.export_step(pan,OUT/'pan.step');back=c.norm(b.import_step(OUT/'pan.step'))
verts,faces=back.tessellate(.08,.12);mesh=trimesh.Trimesh(np.array([tuple(q)for q in verts]),np.array(faces));mesh.merge_vertices(digits_vertex=6)
np.savez_compressed(OUT/'pan-preview.npz',vertices=mesh.vertices,faces=mesh.faces)
glb=trimesh.Trimesh(mesh.vertices[:,[0,2,1]]*[1,1,-1]/1000,mesh.faces);glb.export(OUT/'pan.glb')
export={'valid':pan.is_valid,'solids':len(pan.solids()),'roundtrip_valid':back.is_valid,'volume_delta_mm3':abs(vol(pan)-vol(back)),'watertight':mesh.is_watertight,'bounds_delta_mm':float(np.max(np.abs(np.array([tuple(pan.bounding_box().min),tuple(pan.bounding_box().max)])-mesh.bounds)))}
inputs=[Path(__file__),Path(c.__file__),ROOT/'inventory/engine/full-assembly.json',ROOT/'inventory/engine/timing-cover-attachment-v2-validation.json',*c.FROZEN.glob('*.step')]
r={'scope':'Uninstalled estimated pan access candidate; no factory or full oil containment acceptance','hardware':rows,'diagnostics':diagnostics,'preservation':preserve,'sealing_neighbor_overlap_mm3':seals,'wall_and_shoulder_missing_mm3':probes,'wet_channel_obstruction_mm3':wet_obstruction,'negative_controls':controls,'export':export,'volume_errors':volume_errors,'wall_coverage':'Explicit full-thickness rectangular samples. Unsampled corner blends and full top-to-bottom closed oil-envelope proof NOT RUN.','tool':'Estimated radius 11 mm axial socket insertion only; ratchet clearance unknown.','all_25_stations':'Five unchanged v2 transforms; twenty rear canonical stations unchanged by rear preservation.','input_sha256':{str(p.relative_to(ROOT)):sha(p)for p in inputs},'browser':'NOT RUN; prior security rejection','installation':'NOT INSTALLED'}
r['local_status']='PASS' if all(q[k]<.1 for q in rows for k in ['screw_overlap_mm3','washer_overlap_mm3','seat_missing_mm3','estimated_tool_overlap_mm3']) and max(preserve.values())<.01 and max(seals.values())<.1 and max(probes.values())<.01 and wet_obstruction<.1 and export['valid'] and export['solids']==1 and export['watertight'] else 'FAIL'
# JSON null preserves unresolved measurements without nonstandard Infinity.
for row in rows:
 for key,value in list(row.items()):
  if isinstance(value,float) and not np.isfinite(value):row[key]=None
r['output_sha256']={str(p.relative_to(ROOT)):sha(p)for p in [OUT/'pan.step',OUT/'pan.glb',OUT/'pan-preview.npz']}
(ROOT/'inventory/engine/timing-pan-access-candidate-validation.json').write_text(json.dumps(r,indent=2,allow_nan=False)+'\n');print(r['local_status'],export,flush=True)
