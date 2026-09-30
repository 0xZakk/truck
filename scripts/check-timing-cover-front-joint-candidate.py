#!/usr/bin/env python3
"""Isolated coordinated joint checks; no canonical acceptance implied."""
from pathlib import Path
import sys,json,hashlib,itertools,time
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'));OUT=ROOT/'cad/engine/generated/timing-cover-front-joint-candidate';OUT.mkdir(parents=True,exist_ok=True)
import build123d as b,trimesh
import timing_cover_front_joint_candidate as c
import oil_pan_joint_v9_candidate as old
from cad_metrics import solid_volume
vol=lambda s:sum(abs(solid_volume(q)) for q in s.solids()) if s else 0
ov=lambda a,d:vol(a.intersect(d))
print('Rebuilding unchanged v9 pan reference',flush=True);ref=b.Pos(0,-12,-96)*old.pan_interface(None)
print('Building coordinated front joint',flush=True);parts,m=c.build(ref)
# Normalize compounds returned by OCCT before using assemblies.
parts={k:c.joined(v) for k,v in parts.items()};export={};preview={};scene=trimesh.Scene()
for i,(key,s) in enumerate(parts.items()):
 print('Export',key,s.is_valid,len(s.solids()),flush=True)
 if not s.is_valid:continue
 b.export_step(s,OUT/(key+'.step'));roundtrip=b.import_step(OUT/(key+'.step'))
 v,f=roundtrip.tessellate(.12,.16);v=np.array([tuple(t) for t in v]);f=np.array(f);mesh=trimesh.Trimesh(v,f);mesh.merge_vertices(digits_vertex=6)
 glb=trimesh.Trimesh(mesh.vertices[:,[0,2,1]]*np.array([1,1,-1])/1000,mesh.faces);glb.export(OUT/(key+'.glb'));scene.add_geometry(glb,node_name=key)
 preview[f'v{i}']=v;preview[f'f{i}']=f;section=s.intersect(b.Pos(380,-100,0)*b.Box(130,400,600));sv,sf=section.tessellate(.12,.16);preview[f'cv{i}']=np.array([tuple(t) for t in sv]);preview[f'cf{i}']=np.array(sf)
 export[key]={'valid':s.is_valid,'solids':len(s.solids()),'mesh_watertight':mesh.is_watertight,'step_delta_mm3':abs(solid_volume(roundtrip,'adaptive')-solid_volume(s,'adaptive')),'default_step_delta_mm3':abs(vol(roundtrip)-vol(s)),'volume_mm3':vol(s),'glb_watertight':glb.is_watertight,'mesh_euler_number':int(mesh.euler_number)}
scene.export(OUT/'candidate.glb');np.savez_compressed(OUT/'preview.npz',**preview)
cover,main,land,rtv,gasket,pan=[parts[k] for k in ['cover','main-gasket','future-block-land','front-terminal-sealant','pan-gasket','pan']]
print('Checking full-area gasket support',flush=True);front=c.clip_x(gasket,c.CUT,500);upper=cover+land+main+rtv
probe_up=c.joined(b.Pos(0,0,.02)*front-front);probe_low=c.joined(b.Pos(0,0,-.02)*front-front)
seats={'upper_missing_mm3':vol(probe_up-upper),'lower_missing_mm3':vol(probe_low-pan),'upper_probe_mm3':vol(probe_up),'lower_probe_mm3':vol(probe_low)}
print('Checking overlaps and protected interfaces',flush=True)
main_low=b.Pos(-.02,0,0)*c.clip_x(main,373,373.02)
main_high=b.Pos(.02,0,0)*c.clip_x(main,373.78,373.8)
seats['main_gasket_land_missing_mm3']=vol(main_low-land)
seats['main_gasket_cover_missing_mm3']=vol(main_high-cover)
wall_reserve=[]
for cam in (c.c.CURRENT_CAM,c.P.cam_yz):
 witness=c.c.cx(86.947,380,390,*cam);wall_reserve.append(vol(witness-m['outer_mask']))

pairs={a+' / '+d:ov(parts[a],parts[d]) for a,d in itertools.combinations(parts,2)}
gears={}
from dataclasses import replace
for name,cam in [('current',c.c.CURRENT_CAM),('proposed',c.P.cam_yz)]:
 env=c.c.gear_envelopes(replace(c.P,cam_yz=cam));gears[name]={'overlap_mm3':[sum(ov(s,e) for s in parts.values()) for e in env],'cover_clearance_mm':[cover.distance_to(e) for e in env]}
seal=c.c.cx(27,410,418)-c.c.cx(21,409,419)
travel_cam=c.c.cx(83.947,378.159375,392.259375,*c.P.cam_yz)
travel_check={'axial_interval_mm':[378.159375,392.259375],'overlap_mm3':sum(ov(s,travel_cam) for s in parts.values()),'cover_clearance_mm':cover.distance_to(travel_cam),'scope':'Proposed cam tip envelope across axial travel[-0.1,0] from timing-core worker; crank remains fixed.'}
fixedseal={'overlap_mm3':sum(ov(s,seal) for s in parts.values()),'outer_seat_missing_mm3':vol((c.c.cx(27.05,410,418)-c.c.cx(27,409,419))-cover)}
clamps=[]
for x,y,head in m['front_stations']:
 z=head+7.6;seat=c.disk(7.5,x,y,head+1.6,head+1.65)-c.disk(4.3,x,y,head,head+2)
 shaft=c.disk(3.96875,x,y,head+1.6,head+22.098)
 bore=c.disk(4.1,x,y,z+.1,z+14.9)
 wall=c.disk(6.2,x,y,z+.1,z+14.9)-c.disk(4.2,x,y,z,z+15)
 owner=land if x<373 else cover
 clamps.append({'station':[x,y,head],'washer_support_missing_mm3':vol(seat-pan),'shaft_obstruction_mm3':sum(ov(s,shaft) for s in parts.values()),'socket_obstruction_mm3':ov(owner,bore),'socket_wall_missing_mm3':vol(wall-owner),'nominal_socket_engagement_mm':14.498,'tip_clearance_mm':.502})
# Continuous front segment, plus two explicit main-gasket terminal pockets.
rtv_probe=b.Pos(0,0,-.02)*c.clip_z(rtv,c.PLANE,c.PLANE+.02)
faults={'removed_front_gasket_volume_mm3':vol(front),'removed_terminal_sealant_upper_support_loss_mm3':vol(probe_up-(cover+land+main)),'terminal_bottom_contact_missing_mm3':vol(rtv_probe-gasket),'terminal_solid_count':len(rtv.solids()),'limit':'Gap/support negative controls; no fluid simulation or compressed-material model.'}
# Removing the front segment must expose both mating faces to an empty seal corridor.
remaining_gasket=c.clip_x(gasket,-500,c.CUT)
faults['removed_front_upper_witness_gap_mm3']=vol(c.joined(b.Pos(0,0,-.04)*probe_up)-(cover+land+main+rtv+pan+remaining_gasket))
faults['removed_front_lower_witness_gap_mm3']=vol(c.joined(b.Pos(0,0,.04)*probe_low)-(cover+land+main+rtv+pan+remaining_gasket))
faults['terminal_contacts']=[{'volume_mm3':vol(q),'lower_missing_mm3':vol(c.joined(b.Pos(0,0,-.02)*c.clip_z(q,c.PLANE,c.PLANE+.02))-gasket)} for q in rtv.solids()]
rear_ref=c.clip_x(ref,-500,c.CUT);rear_new=c.clip_x(pan,-500,c.CUT)
# Read-only current pump/pickup context, bound to manifest and exported inputs.
manifest_path=ROOT/'inventory/engine/full-assembly.json';manifest=json.loads(manifest_path.read_text());assemblies={q['id']:q for q in manifest['assemblies']};defs={q['id']:q for q in manifest['definitions']}
def frame(identifier):
 if identifier not in assemblies:return b.Location()
 q=assemblies[identifier];return frame(q.get('parent'))*b.Pos(*q.get('position_cad_mm',[0,0,0]))*b.Rot(*q.get('rotation_cad_deg',[0,0,0]))
context={};context_inputs={str(manifest_path.relative_to(ROOT)):hashlib.sha256(manifest_path.read_bytes()).hexdigest()}
for name in ['oil-pump-housing','oil-pickup-tube']:
 occ=next(q for q in manifest['occurrences'] if q['id']==name);path=ROOT/defs[occ['definition']]['step'].lstrip('/');context_inputs[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest()
 neighbor=frame(occ['parent'])*b.Pos(*occ['position_cad_mm'])*b.Rot(*occ['rotation_cad_deg'])*b.import_step(path);bb=neighbor.bounding_box();context[name]={'bounds_mm':[tuple(bb.min),tuple(bb.max)],'changed_front_region_x_gap_mm':c.CUT-bb.max.X,'method':'Positive X interval separation proves changed front region cannot intersect this current neighbor; not whole-engine integration.'}
rear={'removed_mm3':vol(rear_ref-rear_new),'added_mm3':vol(rear_new-rear_ref),'all_pan_stations':m['all_stations'],'station_count':len(m['all_stations']),'unchanged_station_count':sum(s in old.STATIONS for s in m['all_stations'])}
topology={'expected_pan_gasket_euler':-50,'actual_pan_gasket_euler':export['pan-gasket']['mesh_euler_number'],'meaning':'One continuous ring, central opening and 25 bolt holes; extra windows rejected.'}
passed=topology['actual_pan_gasket_euler']==topology['expected_pan_gasket_euler'] and len(export)==6 and travel_check['overlap_mm3']<.1 and all(x['valid'] and x['glb_watertight'] and x['mesh_watertight'] and x['step_delta_mm3']<.01 for x in export.values()) and max(seats['upper_missing_mm3'],seats['lower_missing_mm3'])<.1 and max(pairs.values())<.1 and max([v for g in gears.values() for v in g['overlap_mm3']])<.1 and fixedseal['overlap_mm3']<.1 and fixedseal['outer_seat_missing_mm3']<.01 and max(rear['removed_mm3'],rear['added_mm3'])<.1 and rear['station_count']==25 and max(wall_reserve)<.1 and all(v['changed_front_region_x_gap_mm']>0 for v in context.values()) and max(seats['main_gasket_land_missing_mm3'],seats['main_gasket_cover_missing_mm3'])<.1 and faults['removed_front_upper_witness_gap_mm3']>100 and faults['removed_front_lower_witness_gap_mm3']>100 and rear['unchanged_station_count']==20 and faults['terminal_solid_count']==2 and faults['removed_terminal_sealant_upper_support_loss_mm3']>1 and faults['terminal_bottom_contact_missing_mm3']<.01 and max(v for x in clamps for k,v in x.items() if k.endswith('_mm3'))<.1
r={'local_status':'PASS' if passed else 'FAIL','readiness':'ISOLATED ESTIMATED JOINT; NO INSTALLATION','input_sha256':{str(Path(p).relative_to(ROOT)):hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in [__file__,c.__file__,old.__file__,c.c.__file__,c.source.__file__]},'parameters':m['parameters'],'terminal_plane_mm':m['terminal_plane_mm'],'terminal_pocket_height_mm':m['terminal_pocket_height_mm'],'exports':export,'front_seat_support':seats,'gasket_topology':topology,'pair_overlap_mm3':pairs,'gear_envelopes':gears,'cam_axial_travel_check':travel_check,'fixed_seal':fixedseal,'cam_wall_protection_missing_mm3':wall_reserve,'current_neighbor_context':context,'context_input_sha256':context_inputs,'clamp_checks':clamps,'negative_controls':faults,'rear_preservation':rear,'installed_neighbors':'NOT RUN','browser':'NOT RUN','learning':'NOT RUN'}
(ROOT/'inventory/engine/timing-cover-front-joint-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));raise SystemExit(0 if passed else 1)
