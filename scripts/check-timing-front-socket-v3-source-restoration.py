from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import timing_front_block_expanded_seat_v3_candidate as c
import pan_fastener_thread_candidate as thread
b.SkipClean.clean=False
OUT=ROOT/'cad/engine/generated/timing-front-block-expanded-seat-v3-candidate'
paths=[OUT/'block.step',c.FROZEN,c.LAND,ROOT/'cad/engine/generated/pan-fastener-thread-candidate/female-test-coupon.step',Path(c.__file__),Path(__file__)]
q,old,source=[b.import_step(p)for p in paths[:3]]
def vol(s):return sum(abs(solid_volume(v,'adaptive'))for v in s.solids()) if s is not None else 0.
def cut(a,z):return c.norm(a.cut(z)) if a is not None else None
def common(a,z):return c.norm(a.intersect(z)) if a is not None else None
loc=b.Pos(*c.ownership.RELOCATIONS[20]);female=loc*b.import_step(paths[3]);cavity=c.intended_socket_cavity();floor=loc*thread.cz(4.15,22.6,23.6);domain=loc*thread.cz(4.15,6.6,23.6)
r={'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths},'old_intended_void_fill_mm3':vol(old.intersect(cavity)),'new_intended_void_fill_mm3':vol(q.intersect(cavity)),'source_intended_void_fill_mm3':vol(source.intersect(cavity)),'source_female_missing_mm3':vol(female.cut(q)),'floor_material_difference_from_source_mm3':vol(q.intersect(floor).cut(source))+vol(source.intersect(floor).cut(q)),'complete_bore_floor_material_difference_from_source_mm3':vol(q.intersect(domain).cut(source))+vol(source.intersect(domain).cut(q)),'unchanged_outside_cavity_and_belowseat_in_socket_neighborhood_mm3':vol(cut(cut(common(cut(q,old),c.socket_guards()[20]),cavity),c.seat.transition_below_seat()))+vol(cut(cut(common(cut(old,q),c.socket_guards()[20]),cavity),c.seat.transition_below_seat()))}
r['gates']={'old_union_negative_control':r['old_intended_void_fill_mm3']>100,'intended_void_restored':r['new_intended_void_fill_mm3']<1e-5,'female_and_floor_retained':r['source_female_missing_mm3']+r['floor_material_difference_from_source_mm3']<1e-5,'bore_matches_intended_source':r['complete_bore_floor_material_difference_from_source_mm3']<1e-5,'bounded_socket_repair':r['unchanged_outside_cavity_and_belowseat_in_socket_neighborhood_mm3']<1e-5};r['local_status']='PASS' if all(r['gates'].values())else'FAIL'
(ROOT/'inventory/engine/timing-front-socket-v3-source-restoration.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
