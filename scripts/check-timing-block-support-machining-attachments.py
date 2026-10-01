#!/usr/bin/env python3
"""Actual fixed hardware, source-defined support walls, and pan8 diagnosis."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
b.SkipClean.clean=False
import full_engine as f
import timing_block_support_machining_candidate as c
from assembly_math import transforms
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-block-support-machining-candidate'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q is not None and getattr(q,'wrapped',True) is not None else 0.
def comp(q):return b.Compound(children=list(q.solids()))
def bounds(q):
 if not q.solids():return None
 bb=q.bounding_box();return [list(bb.min),list(bb.max)]
manifestpath=ROOT/'inventory/engine/full-assembly.json';manifest=json.loads(manifestpath.read_text());defs={d['id']:d for d in manifest['definitions']};occ={o['id']:o for o in manifest['occurrences']};poses=transforms(manifest)
paths={'candidate':OUT/'block.step','base':OUT/'base.step','canonical':ROOT/'cad/engine/generated/block.step'}
ids=['ps-ac-support-bracket','carrier-block-stud-1','carrier-block-stud-2','oil-pan','oil-pan-molded-gasket','oil-pan-mounting-screw-8','oil-pan-mounting-washer-8','crankshaft']
for name in ids:paths[name]=ROOT/defs[occ[name]['definition']]['step'].lstrip('/')
inputs={str(p.relative_to(ROOT)):sha(p) for p in paths.values()}
for p in [Path(__file__),manifestpath,Path(c.__file__),ROOT/'inventory/engine/timing-block-support-machining-validation.json']:inputs[str(p.relative_to(ROOT))]=sha(p)
parts={name:(poses[name]*b.import_step(path) if name in ids else b.import_step(path)) for name,path in paths.items()};q=parts['candidate'];base=parts['base'];canonical=parts['canonical'];removed=comp(base.cut(q));added=comp(q.cut(canonical));missing=comp(canonical.cut(q))
neighbor=[]
for name in ids:
 a=vol(canonical.intersect(parts[name]));error=None
 try:d=vol(q.intersect(parts[name]))
 except ValueError as exc:d=None;error=str(exc)
 try:new_material_overlap=vol(added.intersect(parts[name]))
 except ValueError as exc:new_material_overlap=None;error=(error or '')+'; added material: '+str(exc)
 neighbor.append({'part':name,'baseline_overlap_mm3':a,'candidate_overlap_mm3':d,'candidate_integration_error':error,'added_material_overlap_mm3':new_material_overlap,'inferred_overlap_upper_bound_mm3':a+new_material_overlap if new_material_overlap is not None else None,'no_new_overlap':new_material_overlap is not None and new_material_overlap<1e-5,'proof':'Any new intersection is contained in (candidate minus canonical) intersect neighbor; removals cannot create overlap'});print('neighbor',neighbor[-1],flush=True)
def contact_area(a,d,y):
 fs=[face for face in a.faces() if face.bounding_box().size.Y<1e-6 and abs(face.bounding_box().min.Y-y)<1e-5]
 gs=[face for face in d.faces() if face.bounding_box().size.Y<1e-6 and abs(face.bounding_box().min.Y-y)<1e-5]
 return sum(sum(z.area for z in inter.faces()) for face in fs for other in gs if (inter:=face.intersect(other)) is not None)
carriers=[]
for i,(x,z) in enumerate(f.carrier94.BLOCK_STATIONS,1):
 boss=f.carrier94.sideways(14,31,x,119.5,z);socket=f.carrier94.sideways(5.2,25,x,123.5,z);rem=comp(removed.intersect(boss));seatguard=f.carrier94.sideways(14,2.1,x,134.05,z);seat_change=vol(added.intersect(seatguard))+vol(missing.intersect(seatguard));stock=comp(q.intersect(boss));clip=b.Pos(x,135,z)*b.Box(34,4,34)
 old_area=contact_area(canonical.intersect(clip),parts['ps-ac-support-bracket'].intersect(clip),135);new_area=contact_area(q.intersect(clip),parts['ps-ac-support-bracket'].intersect(clip),135)
 distance=rem.distance_to(socket);carriers.append({'station':i,'x_mm':x,'removed_mm3':vol(rem),'min_removed_to_socket_mm':distance,'minimum_5mm_pass':distance>=5,'seat_backing_changed_mm3':seat_change,'support_region_solid_count':len(stock.solids()),'block_solid_count':len(q.solids()),'baseline_carrier_face_contact_mm2':old_area,'candidate_carrier_face_contact_mm2':new_area,'contact_preserved':old_area>0 and abs(old_area-new_area)<1e-5});print('carrier',carriers[-1],flush=True)
# Exact source pan8 support, not the older oversized probe.
x,y,z=f.pan_joint.STATIONS[7];boss=b.Pos(x,y)*f.pan_joint.cylinder(10,z+7.6,z+25);bore=b.Pos(x,y)*f.pan_joint.cylinder(4.15,z+6.6,z+f.pan_joint.LENGTH+1);broad=b.Pos(x,y,z+17)*b.Cylinder(12,26);tiny=comp(added.intersect(broad));actual_change=vol(added.intersect(boss))+vol(missing.intersect(boss));fault=comp(canonical.intersect(boss)).cut(b.Pos(x,y)*f.pan_joint.cylinder(4.65,z+7.6,z+25));fault_removed=vol(comp(canonical.intersect(boss)).cut(fault))
pan={'station':[x,y,z],'original_radius12_guard_added_mm3':vol(tiny),'added_bounds_mm':bounds(tiny),'actual_radius10_boss_change_mm3':actual_change,'distance_added_to_actual_boss_mm':tiny.distance_to(boss),'distance_added_to_socket_bore_mm':tiny.distance_to(bore),'source_boss_z_range':[z+7.6,z+25],'source_bore_radius_mm':4.15,'oversize_bore_negative_control_removed_mm3':fault_removed,'physical_interface_pass':actual_change<1e-5 and fault_removed>1e-5};print('pan8',pan,flush=True)
# Any rigid crankshaft rotation stays inside its verified coaxial cylinder.
crank=[];radial_floor=math.hypot(90+c.DELTA[1],72+c.DELTA[2])-(f.CAM_BORE_R+c.BACKING_MM);bound_radius=radial_floor-.1
for i,x in enumerate(c.JOURNAL_STATIONS,1):
 clip=b.Pos(x,0,0)*b.Box(c.WIDTH_MM,1000,1000);shaft=comp(parts['crankshaft'].intersect(clip));outside=vol(shaft.cut(b.Pos(x,0,0)*f.cx(bound_radius,c.WIDTH_MM+.02)));crank.append({'journal':i,'x_mm':x,'support_min_radius_about_crank_mm':radial_floor,'crank_containing_radius_mm':bound_radius,'crank_material_outside_cylinder_mm3':outside,'conservative_all_rotation_clearance_mm':.1 if outside<1e-5 else None})
assert inputs=={p:sha(ROOT/p) for p in inputs}
r={'status':'PASS declared fixed attachments and pan8 physical diagnosis' if all(n['no_new_overlap'] for n in neighbor) and all(a['minimum_5mm_pass'] and a['seat_backing_changed_mm3']<1e-5 and a['contact_preserved'] and a['support_region_solid_count']==1 for a in carriers) and pan['physical_interface_pass'] and all(a['crank_material_outside_cylinder_mm3']<1e-5 for a in crank) else 'FAIL one or more attachment gates','input_sha256':inputs,'neighbors':neighbor,'carrier_supports':carriers,'pan_socket8':pan,'crank_rotation_envelopes':crank,'limits':['5mm carrier criterion and2mm backing are geometric educational criteria, not production strength evidence','Original radius12 pan guard remains a measured historical change, not a zero result or tolerance waiver','Crank envelope covers rigid crankshaft only; no full valvetrain/rod/piston motion acceptance','No front land union or canonical installation']}
(ROOT/'inventory/engine/timing-block-support-machining-attachments.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],flush=True)
