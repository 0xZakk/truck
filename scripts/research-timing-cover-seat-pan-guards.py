"""Read-only proposed access envelope against frozen pan socket material."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import timing_cover_front_joint_candidate as f
import timing_cover_attachment_v2 as joint
import pan_fastener_thread_candidate as thread
b.SkipClean.clean=False
paths=[ROOT/'cad/engine/generated/front-seal-2692-candidate/cover.step',ROOT/'cad/engine/generated/pan-fastener-thread-candidate/female-test-coupon.step',Path(__file__)]
cover,female=[b.import_step(p)for p in paths[:2]]
def vol(q):return sum(abs(solid_volume(s,'adaptive'))for s in q.solids())if q is not None else 0.
rows=[]
for n,p in enumerate(f.source.HOLES_NORMALIZED,1):
 y,z=f.c.yz(p,f.P);pocket=f.c.cx(10.5,379.8,435,y,z);head=f.c.cx(8.75,379.8,385.1,y,z)
 for k in [21,22,23]:
  loc=b.Pos(*joint.RELOCATIONS[k]);wall=loc*(thread.cz(6.2,7.8,23.6)-thread.cz(4.17,7.7,23.7));floor=loc*thread.cz(4.15,22.6,23.6)
  vals={'main_station':n,'pan_station':k,'access_envelope_female_overlap_mm3':vol(pocket.intersect(loc*female)),'access_envelope_wall_overlap_mm3':vol(pocket.intersect(wall)),'access_envelope_floor_overlap_mm3':vol(pocket.intersect(floor)),'estimated_round_head_cover_overlap_mm3':vol(head.intersect(cover))}
  if any(vals[key]>1e-5 for key in vals if key.endswith('mm3')):rows.append(vals)
report={'status':'READ-ONLY feasibility; round head and tool envelopes are estimates, not actual hardware','input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths},'access_radius_estimate_mm':10.5,'seat_x_estimate_mm':379.8,'head_radius_height_estimate_mm':[8.75,5.3],'conflicts':rows,'limits':['Current head envelope also intersects the unmodified cover bosses slated for recess; that field alone is not a neighbor failure','Protected female/floor/wall overlap cannot be removed as generic access clearance']}
(ROOT/'inventory/engine/timing-cover-seat-pan-guards.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(rows,indent=2))
