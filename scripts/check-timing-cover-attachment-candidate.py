#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib,itertools
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,trimesh
from cad_metrics import solid_volume
import timing_cover_attachment_candidate as c
import timing_cover_front_joint_candidate as joint
OUT=ROOT/'cad/engine/generated/timing-cover-attachment-candidate';OUT.mkdir(parents=True,exist_ok=True)
def vol(s):
 if s is None:return 0
 if isinstance(s,b.ShapeList):return sum(vol(q) for q in s)
 if s.wrapped is None:return 0
 return sum(abs(solid_volume(q,'adaptive')) for q in s.solids())
def ov(a,d):
 aa=a.bounding_box();bb=d.bounding_box()
 if any(min(tuple(aa.max)[i],tuple(bb.max)[i])-max(tuple(aa.min)[i],tuple(bb.min)[i])<1e-7 for i in range(3)):return 0
 # Exact local clipping reduces irrelevant remote helical faces before Boolean.
 size=aa.size;box=b.Pos(*aa.center())*b.Box(size.X+.02,size.Y+.02,size.Z+.02)
 local=d.intersect(box)
 if local is None:return 0
 return vol(a.intersect(local))
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
print('Building five threaded socket proposals against frozen joint',flush=True)
parts,occ,defs,changes,original=c.build();m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());assemblies={q['id']:q for q in m['assemblies']};definitions={q['id']:q for q in m['definitions']}
def frame(key):
 if key not in assemblies:return b.Location()
 q=assemblies[key];return frame(q.get('parent'))*b.Pos(*q.get('position_cad_mm',[0,0,0]))*b.Rot(*q.get('rotation_cad_deg',[0,0,0]))
def current(key):
 q=next(q for q in m['occurrences'] if q['id']==key);return frame(q['parent'])*b.Pos(*q['position_cad_mm'])*b.Rot(*q['rotation_cad_deg'])*c.norm(b.import_step(ROOT/definitions[q['definition']]['step'].lstrip('/')))
seal=current('front-seal');hub=current('damper-hub');crank=current('crankshaft')
allgeo={**parts,**occ,'front-seal':seal,'damper-hub':hub};exports={};preview={};scene=trimesh.Scene()
for i,(key,s) in enumerate(allgeo.items()):
 print('Export',key,flush=True);b.export_step(s,OUT/(key+'.step'));back=b.import_step(OUT/(key+'.step'));v,f=back.tessellate(.12,.16);v=np.array([tuple(q) for q in v]);f=np.array(f);mesh=trimesh.Trimesh(v,f);mesh.merge_vertices(digits_vertex=6);g=trimesh.Trimesh(mesh.vertices[:,[0,2,1]]*[1,1,-1]/1000,mesh.faces);g.export(OUT/(key+'.glb'));scene.add_geometry(g,node_name=key);preview['v'+str(i)]=mesh.vertices;preview['f'+str(i)]=mesh.faces
 exports[key]={'valid':s.is_valid,'solids':len(s.solids()),'watertight':mesh.is_watertight,'step_delta_mm3':abs(vol(s)-vol(back))}
scene.export(OUT/'candidate.glb');np.savez_compressed(OUT/'preview.npz',**preview);(OUT/'names.json').write_text(json.dumps(list(allgeo)))
for name in ['screw','washer']:b.export_step(defs[name],OUT/('reusable-pan-'+name+'.step'))
checks=[];regions=[]
for n,pos in c.RELOCATIONS.items():
 print('Check attachment',n,flush=True)
 x,y,z=pos;f=b.Pos(*pos);owner=parts[changes[str(n)]['socket_owner']];bolt=occ[f'oil-pan-mounting-screw-{n}'];washer=occ[f'oil-pan-mounting-washer-{n}'];socket=f*defs['female_teaching_form'];regions.append(f*c.cz(4.18,7.79,22.31))
 head_probe=f*(c.cz(6.3,0,.02)-c.cz(4.15,-1,1));washer_probe=f*(c.cz(7.5,1.6,1.62)-c.cz(4.3,1,2));wall=f*(c.cz(6.2,7.8,22.3)-c.cz(4.18,7.7,22.4))
 checks.append({'stable_screw_id':f'oil-pan-mounting-screw-{n}','stable_washer_id':f'oil-pan-mounting-washer-{n}','proposed_transform':changes[str(n)],'head_washer_support_missing_mm3':vol(head_probe-washer),'washer_pan_support_missing_mm3':vol(washer_probe-parts['pan']),'socket_wall_missing_mm3':vol(wall-owner),'screw_all_joint_overlap_mm3':sum(ov(bolt,q) for q in parts.values()),'washer_all_joint_overlap_mm3':sum(ov(washer,q) for q in parts.values()),'thread_contact_distance_mm':bolt.distance_to(socket),'axial_thread_interval_mm':[z+7.8,z+22.0],'axial_engagement_mm':22.0-7.8,'tip_clearance_mm':.502,'tip_clearance_obstruction_mm3':ov(f*c.cz(3.95,22.098,22.598),owner),'tip_floor_support_missing_mm3':vol(c.norm(f*c.cz(3.95,22.6,22.62)-owner)),'wrong_phase_overlap_mm3':ov(b.Pos(0,0,.3)*bolt,socket),'smooth_original_bore_radial_clearance_mm':4.15-7.9375/2})
(OUT/'attachment-checkpoint.json').write_text(json.dumps({'exports':exports,'five_pan_checks':checks},indent=2)+'\n')
print('Checking bounded material changes and seal',flush=True)
region=b.Compound(children=regions);diff={}
for k in ['cover','future-block-land']:
 added=c.norm(parts[k]-original[k]);removed=c.norm(original[k]-parts[k]);diff[k]={'removed_mm3':vol(removed),'added_outside_socket_regions_mm3':vol(c.norm(added-region)) if vol(added)>1e-9 else 0,'added_mm3':vol(added)}
# Preserve every pan identity and position except explicitly reviewed five pairs.
pan_rows=[q for q in m['occurrences'] if q['id'].startswith('oil-pan-mounting-screw-')];unchanged=[q['id'] for q in pan_rows if int(q['id'].split('-')[-1]) not in c.RELOCATIONS]
# Seal back shoulder uses R24..27 at X410; inside R21 is still a crude lip.
cx=joint.c.cx
radial=cx(27.02,410,418)-cx(27,409,419);rear=cx(27,409.98,410)-cx(24,409,411)
sealcheck={'fixed_bounds_mm':[tuple(seal.bounding_box().min),tuple(seal.bounding_box().max)],'cover_overlap_mm3':ov(seal,parts['cover']),'radial_outer_seat_missing_mm3':vol(radial-parts['cover']),'rear_axial_shoulder_missing_mm3':vol(rear-parts['cover']),'seal_hub_distance_mm':seal.distance_to(hub),'hub_rear_x_mm':hub.bounding_box().min.X,'seal_front_x_mm':seal.bounding_box().max.X,'seal_crank_distance_mm':seal.distance_to(crank),'seal_crank_overlap_mm3':ov(seal,crank),'interpretation':'Existing seal X410..418 and hub rear X419 leave an actual 1 mm axial gap. No hub sealing-track engagement; no damper movement. Seal lip/case/press fit are not reconstructed.'}
coveraxes=[]
for i,q in enumerate(joint.source.HOLES_NORMALIZED,1):
 y,z=joint.c.yz(q,joint.P);coveraxes.append({'proposed_occurrence_id':f'timing-cover-mounting-screw-{i}','head_seat_model_x_mm':415,'axis_yz_mm':[y,z],'cover_through_radius_mm':4.2,'land_smooth_bore_radius_mm':3.3,'land_bore_x_mm':[366,373],'hardware_status':'NOT BUILT: exact applicable thread, length mix, head and washer mapping unknown; seven hole axes do not establish seven identical screws.'})
local_ok=all(e['valid'] and e['watertight'] and e['step_delta_mm3']<.01 for e in exports.values()) and all(max(v for k,v in q.items() if k.endswith('_mm3') and k!='wrong_phase_overlap_mm3')<.1 and q['wrong_phase_overlap_mm3']>.1 for q in checks) and all(q['removed_mm3']<.01 and q['added_outside_socket_regions_mm3']<.01 and q['added_mm3']>1 for q in diff.values())
inputs=[Path(__file__),Path(c.__file__),ROOT/'inventory/engine/full-assembly.json',ROOT/'inventory/engine/timing-cover-front-joint-validation.json',*[c.FROZEN/(q+'.step') for q in c.PARTS],*[ROOT/'cad/engine/generated'/f'{q}.step' for q in ['oil-pan-mounting-screw','oil-pan-mounting-washer','front-seal','damper-hub','crankshaft']]]
r={'status':'BLOCKED: main-cover hardware and seal/hub joint unresolved','five_pan_attachments_local_status':'PASS' if local_ok else 'FAIL','input_sha256':{str(p.relative_to(ROOT)):h(p) for p in inputs},'exports':exports,'five_pan_checks':checks,'modified_material':diff,'pan_station_count':len(pan_rows),'unchanged_pan_screw_ids':unchanged,'main_cover_axes':coveraxes,'front_seal':sealcheck,'thread_limit':'Estimated ideal zero-clearance conjugate of existing male profile. Female material belongs to cover/block casting, not a separate insert. No preload, tolerance class, manufacturing or strength claim.','installed':'NOT RUN','browser':'NOT RUN','learning':'NOT RUN'}
(ROOT/'inventory/engine/timing-cover-attachment-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));raise SystemExit(0 if local_ok else 1)
