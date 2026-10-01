#!/usr/bin/env python3
"""Bounded five-socket proof plus an explicitly separate canonical reuse audit."""
from pathlib import Path
import sys,json,hashlib,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,trimesh
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common,BRepAlgoAPI_Cut
from cad_metrics import solid_volume
import timing_cover_attachment_v2 as c
OUT=ROOT/'cad/engine/generated/timing-cover-attachment-v2';OUT.mkdir(parents=True,exist_ok=True)
def volume(s):
 if s is None or s.wrapped is None:return 0.
 return sum(abs(solid_volume(q,'adaptive')) for q in s.solids())
def operation(kind,a,d):
 if a is None:return None
 if d is None:return a if kind=='cut' else None
 op=(BRepAlgoAPI_Cut if kind=='cut' else BRepAlgoAPI_Common)(a.wrapped,d.wrapped)
 if not op.IsDone():raise RuntimeError(f'{kind} kernel operation failed')
 shape=op.Shape()
 return None if shape.IsNull() else c.norm(b.Compound(shape))
def cut(a,d):return operation('cut',a,d)
def common(a,d):return operation('common',a,d)
def overlap(a,d):
 if a is None or d is None:return 0.
 aa=a.bounding_box();dd=d.bounding_box()
 if any(min(tuple(aa.max)[i],tuple(dd.max)[i])-max(tuple(aa.min)[i],tuple(dd.min)[i])<1e-7 for i in range(3)):return 0.
 size=aa.size;local=common(d,b.Pos(*aa.center())*b.Box(size.X+.04,size.Y+.04,size.Z+.04))
 return volume(common(a,local))
def contact(male,owner):
 # Keep surface results: solid normalization would intentionally discard faces.
 op=BRepAlgoAPI_Common(male.wrapped,b.Compound(list(owner.faces())).wrapped)
 if not op.IsDone():raise RuntimeError('Contact face operation failed')
 s=op.Shape()
 if s.IsNull():return {'total_area_mm2':0.,'flank_area_mm2':0.}
 faces=b.Compound(s).faces()
 return {'total_area_mm2':sum(f.area for f in faces),'flank_area_mm2':sum(f.area for f in faces if .1<abs(f.normal_at().Z)<.99)}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
print('Build five socket candidate',flush=True)
parts,original,occ,defs,owners=c.build()
manifest=ROOT/'inventory/engine/full-assembly.json';m=json.loads(manifest.read_text());assemblies={q['id']:q for q in m['assemblies']};definitions={q['id']:q for q in m['definitions']};rows={q['id']:q for q in m['occurrences']}
def frame(key):
 if key not in assemblies:return b.Location()
 q=assemblies[key];return frame(q.get('parent'))*b.Pos(*q.get('position_cad_mm',[0,0,0]))*b.Rot(*q.get('rotation_cad_deg',[0,0,0]))
def occurrence_frame(q):return frame(q.get('parent'))*b.Pos(*q['position_cad_mm'])*b.Rot(*q['rotation_cad_deg'])
canonical_inputs=set()
def current(key):
 q=rows[key];p=ROOT/definitions[q['definition']]['step'].lstrip('/');canonical_inputs.add(p)
 return occurrence_frame(q)*c.norm(b.import_step(p))
checks=[]
for n,pos in c.RELOCATIONS.items():
 print('Check proposed socket',n,flush=True)
 f=b.Pos(*pos);owner=parts[owners[n]];male=occ[f'oil-pan-mounting-screw-{n}'];washer=occ[f'oil-pan-mounting-washer-{n}']
 local=common(owner,f*c.cz(6.3,7.8,22.3))
 q={'id':f'oil-pan-mounting-screw-{n}','position_cad_mm':pos,'rotation_cad_deg':[0,0,0],'owner':owners[n],
 'head_washer_support_missing_mm3':volume(cut(f*(c.cz(6.3,0,.02)-c.cz(4.15,-1,1)),washer)),
 'washer_pan_support_missing_mm3':volume(cut(f*(c.cz(7.5,1.6,1.62)-c.cz(4.3,1,2)),parts['pan'])),
 'socket_wall_missing_mm3':volume(cut(f*(c.cz(6.2,7.8,22.3)-c.cz(4.18,7.7,22.4)),owner)),
 'male_joint_overlap_mm3':{k:overlap(male,v)for k,v in parts.items()},
 'washer_joint_overlap_mm3':{k:overlap(washer,v)for k,v in parts.items()},
 'flank_contact':contact(male,local),'thread_contact_distance_mm':male.distance_to(local),
 'engagement_interval_world_z_mm':[pos[2]+7.8,pos[2]+22.0],'engagement_mm':14.2,
 'tip_clearance_mm':.502,'tip_void_obstruction_mm3':overlap(f*c.cz(3.95,22.098,22.598),owner),
 'tip_floor_missing_mm3':volume(cut(f*c.cz(3.95,22.6,22.62),owner)),
 'matched_advance_overlap_mm3':overlap(f*b.Pos(0,0,25.4/18/4)*b.Rot(0,0,90)*defs['male'],local),
 'wrong_phase_overlap_mm3':overlap(f*b.Pos(0,0,.3)*defs['male'],local)}
 checks.append(q);(OUT/'five-socket-checkpoint.json').write_text(json.dumps(checks,indent=2)+'\n')
print('Bounded changes and sealing-face preservation',flush=True)
regions=b.Compound([b.Pos(*p)*c.cz(4.18,7.79,22.31)for p in c.RELOCATIONS.values()]);changes={}
for k in c.PARTS:
 added=cut(parts[k],original[k]);removed=cut(original[k],parts[k])
 changes[k]={'removed_mm3':volume(removed),'added_mm3':volume(added),'added_outside_socket_regions_mm3':volume(cut(added,regions))}
print('Export candidate',flush=True)
exports={};preview={};names=[];scene=trimesh.Scene()
for i,(name,s)in enumerate({**parts,**occ}.items()):
 print('Export',name,flush=True);b.export_step(s,OUT/(name+'.step'));back=c.norm(b.import_step(OUT/(name+'.step')))
 v,f=back.tessellate(.08,.12);mesh=trimesh.Trimesh(np.array([tuple(p)for p in v]),np.array(f));mesh.merge_vertices(digits_vertex=6)
 glb=trimesh.Trimesh(mesh.vertices[:,[0,2,1]]*[1,1,-1]/1000,mesh.faces);glb.export(OUT/(name+'.glb'));scene.add_geometry(glb,node_name=name)
 preview['v'+str(i)]=mesh.vertices;preview['f'+str(i)]=mesh.faces;names.append(name)
 exports[name]={'valid':s.is_valid,'roundtrip_valid':back.is_valid,'solids':len(s.solids()),'mesh_watertight':mesh.is_watertight,'step_volume_delta_mm3':abs(volume(s)-volume(back))}
np.savez_compressed(OUT/'preview.npz',**preview);(OUT/'names.json').write_text(json.dumps(names));scene.export(OUT/'candidate.glb')
print('Audit all 25 canonical transforms',flush=True)
block=current('block');pan=current('oil-pan');audit=[]
for n in range(1,26):
 print('Canonical reuse',n,flush=True)
 key=f'oil-pan-mounting-screw-{n}';q=rows[key];f=occurrence_frame(q);male=f*defs['male'];washer=current(f'oil-pan-mounting-washer-{n}')
 bb=male.bounding_box();size=bb.size;local=common(block,b.Pos(*bb.center())*b.Box(size.X+.1,size.Y+.1,size.Z+.1))
 audit.append({'id':key,'unchanged_canonical_transform':{k:q.get(k)for k in ['parent','position_cad_mm','rotation_cad_deg']},'also_unchanged_in_proposed_joint':n not in c.RELOCATIONS,'male_pan_overlap_mm3':overlap(male,pan),'male_block_overlap_mm3':overlap(male,local),'male_washer_overlap_mm3':overlap(male,washer),'head_washer_support_missing_mm3':volume(cut(f*(c.cz(6.3,0,.02)-c.cz(4.15,-1,1)),washer)),'washer_pan_support_missing_mm3':volume(cut(f*(c.cz(7.5,1.6,1.62)-c.cz(4.3,1,2)),pan)),'block_distance_mm':None if local is None else male.distance_to(local),'retention':'Existing smooth socket: no female thread retention proof; no socket alteration in this audit.'})
 (OUT/'canonical-audit-checkpoint.json').write_text(json.dumps(audit,indent=2)+'\n')
local_ok=all(q['flank_contact']['flank_area_mm2']>1 and q['thread_contact_distance_mm']<1e-5 and q['wrong_phase_overlap_mm3']>1 and q['matched_advance_overlap_mm3']<.1 and all(q[k]<.1 for k in ['head_washer_support_missing_mm3','washer_pan_support_missing_mm3','socket_wall_missing_mm3','tip_void_obstruction_mm3','tip_floor_missing_mm3']) and max(q['male_joint_overlap_mm3'].values())<.1 and max(q['washer_joint_overlap_mm3'].values())<.1 for q in checks) and all(q['removed_mm3']<.01 and q['added_outside_socket_regions_mm3']<.01 for q in changes.values()) and all(q['valid']and q['roundtrip_valid']and q['mesh_watertight']and q['step_volume_delta_mm3']<.01 for q in exports.values())
inputs=[Path(__file__),Path(c.__file__),manifest,*canonical_inputs,*[c.FROZEN/(k+'.step')for k in c.PARTS],*[c.MALE/(k+'.step')for k in ['pan-screw','female-test-coupon','existing-pan-washer']],ROOT/'inventory/engine/pan-fastener-thread-validation.json',ROOT/'inventory/engine/timing-cover-front-joint-validation.json']
r={'five_socket_status':'PASS'if local_ok else'FAIL','installation_status':'NOT INSTALLED; main-cover hardware, seal case and canonical socket retention unresolved','five_sockets':checks,'bounded_material_changes':changes,'exports':exports,'canonical_25_reuse_audit':audit,'unchanged_proposed_stations':20,'pan_station_count':25,'female_form':'Ideal zero-clearance conjugate. Estimated profile, no production thread class, preload or strength claim. Female material belongs to future casting, not a physical insert.','input_sha256':{str(p.relative_to(ROOT)):sha(p)for p in inputs},'learning':'NOT RUN','browser':'NOT RUN'}
(ROOT/'inventory/engine/timing-cover-attachment-v2-validation.json').write_text(json.dumps(r,indent=2)+'\n');print('Five sockets:',r['five_socket_status'],flush=True)
raise SystemExit(0 if local_ok else 1)
