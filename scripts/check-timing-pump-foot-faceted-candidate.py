#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import numpy as np,trimesh
import timing_pump_foot_faceted_candidate as c
import oil_drive_layout as drive
from assembly_math import transforms
from cad_metrics import solid_volume
b.SkipClean.clean=False
OUT=ROOT/'cad/engine/generated/timing-pump-foot-faceted-candidate';OUT.mkdir(exist_ok=True)
OLD=ROOT/'cad/engine/generated/timing-block-support-machining-candidate'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q is not None and getattr(q,'wrapped',True) is not None else 0.
def contact(a,z,other):
 faces=lambda q:[f for f in q.faces() if f.bounding_box().size.Z<1e-6 and abs(f.center().Z-z)<1e-5]
 hits=[x.intersect(y) for x in faces(a) for y in faces(other)]
 return sum(f.area for hit in hits if hit is not None for f in hit.faces())
mp=ROOT/'inventory/engine/full-assembly.json';m=json.loads(mp.read_text());defs={d['id']:d for d in m['definitions']};oc={o['id']:o for o in m['occurrences']};poses=transforms(m);inputs=[mp,Path(__file__),Path(c.__file__),Path(drive.__file__),ROOT/'cad/engine/timing_block_support_machining_candidate.py',OLD/'block.step',ROOT/'inventory/engine/timing-block-support-machining-validation.json',ROOT/'inventory/engine/timing-pump-foot-pan-witnesses.json']
def actual(id,moved=False):
 p=ROOT/defs[oc[id]['definition']]['step'].lstrip('/');inputs.append(p)
 return (b.Pos(*c.DELTA) if moved else b.Pos())*poses[id]*b.import_step(p)
pan=actual('oil-pan');pump=actual('oil-pump-housing',True);bolts=[actual('oil-pump-mount-bolt-'+str(i),True) for i in [1,2]]
if '--from-export' in sys.argv:
 q=b.import_step(OUT/'block.step');data={'supports':[b.Pos(*c.DELTA)*s for s in c.revised_supports()],'old_supports':[b.Pos(*c.DELTA)*s for s in drive.pump_mount_supports()]}
else:q,data=c.build()
print('built',q.is_valid,flush=True)
b.export_step(q,OUT/'block.step');rt=b.import_step(OUT/'block.step')
old=b.import_step(OLD/'block.step');extra=q.cut(old);removed=old.cut(q);oldfeet=b.Compound(children=data['old_supports']);local=(b.Pos(*c.DELTA)*drive.PUMP_FRAME).inverse()
rows=[]
for i,(s,oldfoot,bolt) in enumerate(zip(data['supports'],data['old_supports'],bolts)):
 b.export_step(s,OUT/f'support-{i}.step')
 witness=b.import_step(OLD/f'pump-pan-positive-witness-{i}.step')
 row={'index':i,'valid':s.is_valid,'solids':len(s.solids()),'pan_overlap_mm3':vol(s.intersect(pan)),'pan_distance_mm':s.distance_to(pan),'pump_overlap_mm3':vol(s.intersect(pump)),'bolt_overlap_mm3':vol(s.intersect(bolt)),'pump_seat_contact_mm2':contact(local*s,16,local*pump),'bolt_seat_contact_mm2':contact(local*s,24,local*bolt),'old_witness_volume_mm3':vol(witness),'old_witness_outside_original_support_mm3':vol(witness.cut(oldfoot)),'old_witness_new_overlap_mm3':vol(witness.intersect(s)),'old_witness_outside_pan_mm3':vol(witness.cut(pan)),'support_missing_from_block_mm3':vol(s.cut(q)),'old_support_removed_mm3':vol(oldfoot.cut(s))}
 rows.append(row);print(row,flush=True)
 for name,part in [('pump',pump),('bolt-'+str(i),bolt),('pan',pan)]:b.export_step(part,OUT/(name+'.step'))
mesh_error=None;err=None;mesh=None
try:
 v,f=q.tessellate(.12,.15);v=np.array([tuple(x) for x in v]);mesh=trimesh.Trimesh(v[:,[0,2,1]]*[1,1,-1]/1000,np.asarray(f));mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();mesh.export(OUT/'block.glb');mesh=trimesh.load(OUT/'block.glb',force='mesh');mesh.merge_vertices(digits_vertex=8)
 vv=np.asarray(mesh.vertices)[:,[0,2,1]]*[1,-1,1]*1000;bb=q.bounding_box();err=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([list(bb.min),list(bb.max)]))))
except Exception as exc:
 mesh_error=repr(exc);print('MESH FAIL',mesh_error,flush=True)
r={'mesh_origin':'direct native CAD', 'status':'LOCAL CHECKS; inherited crankgear/front-land FAIL','input_sha256':{str(p.relative_to(ROOT)):sha(p) for p in inputs},'cad_valid':q.is_valid,'solids':len(q.solids()),'step_valid':rt.is_valid,'readback_difference_mm3':vol(q.cut(rt))+vol(rt.cut(q)),'mesh_error':mesh_error,'mesh_watertight':mesh.is_watertight if mesh is not None else False,'mesh_bounds_error_mm':err,'added_material_mm3':vol(extra),'removed_material_mm3':vol(removed),'removed_outside_old_supports_mm3':vol(removed.cut(oldfeet)),'supports':rows,'whole_block_pan_overlap_mm3':vol(q.intersect(pan)),'whole_block_pan_distance_mm':q.distance_to(pan),'actual_pump_pan_overlap_mm3':vol(pump.intersect(pan)),'actual_bolts_pan_overlap_mm3':[vol(x.intersect(pan)) for x in bolts],'estimated_bore_wall_mm':c.FACET_INRADIUS_BOUND_MM-3.2,'estimated_head_edge_margin_mm':c.FACET_INRADIUS_BOUND_MM-5.2,'profile_segments':c.SEGMENTS,'chord_sag_bound_mm':c.CHORD_SAG_BOUND_MM,'inherited_failure':'Crankgear/front-land61.012932mm³ unchanged; no installation','artifacts':{p.name:sha(p) for p in OUT.glob('*') if p.is_file() and p.suffix not in ['.log','.npz']}}
proof=json.loads((ROOT/'inventory/engine/timing-block-support-machining-validation.json').read_text())
for rel,digest in proof['input_sha256'].items():
 assert sha(ROOT/rel)==digest,rel
 r['input_sha256'][rel]=digest
for path in [OLD/f'pump-pan-positive-witness-{i}.step' for i in range(2)]:r['input_sha256'][str(path.relative_to(ROOT))]=sha(path)
# The unchanged column is independently reconstructed from source endpoints.
import math
station=-28;offset=-10
endpoint=(drive.PUMP_FRAME*b.Vertex(station,28,20)).center()+b.Vector(offset,0,0)
start=b.Vector(drive.DRIVE_X-3.5+station+offset,97,-18)
column=b.Solid.make_cylinder(4,(endpoint-start).length,b.Plane(origin=start,z_dir=endpoint-start))
mirror=b.Plane(origin=(drive.DRIVE_X-3.5,0,0),x_dir=(0,1,0),z_dir=(1,0,0))
columns=[b.Pos(*c.DELTA)*v for v in [column,column.mirror(mirror)]]
r['columns_removed_from_old_material_mm3']=[vol(oldfoot.intersect(col).cut(s)) for oldfoot,col,s in zip(data['old_supports'],columns,data['supports'])]
r['gates']={
 'single_valid_block':q.is_valid and len(q.solids())==1 and rt.is_valid,
 'roundtrip':r['readback_difference_mm3']<1e-5,
 'mesh':mesh_error is None and r['mesh_watertight'] and err<.15,
 'localized_material':r['added_material_mm3']<1e-5 and r['removed_outside_old_supports_mm3']<1e-5,
 'facet_seat_margins':r['estimated_bore_wall_mm']>2.29 and r['estimated_head_edge_margin_mm']>.29,
 'columns_unchanged':max(r['columns_removed_from_old_material_mm3'])<1e-5,
 'whole_pan_clearance':r['whole_block_pan_overlap_mm3']<1e-5,
 'pump_and_bolts_clear_pan':r['actual_pump_pan_overlap_mm3']<1e-5 and max(r['actual_bolts_pan_overlap_mm3'])<1e-5,
 'attachments':all(v['valid'] and v['solids']==1 and v['support_missing_from_block_mm3']<1e-5 and v['pan_overlap_mm3']<1e-5 and v['pan_distance_mm']>.5 and v['pump_overlap_mm3']<1e-5 and v['bolt_overlap_mm3']<1e-5 and v['pump_seat_contact_mm2']>1 and v['bolt_seat_contact_mm2']>1 for v in rows),
 'strict_old_witness_negative_controls':all(abs(v['old_witness_volume_mm3']-.008)<1e-7 and v['old_witness_outside_original_support_mm3']<1e-7 and v['old_witness_outside_pan_mm3']<1e-7 and v['old_witness_new_overlap_mm3']<1e-7 for v in rows)}
r['local_status']='PASS' if all(r['gates'].values()) else 'FAIL'
(ROOT/'inventory/engine/timing-pump-foot-faceted-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2),flush=True)

assert all(r['gates'].values()),r['gates']
