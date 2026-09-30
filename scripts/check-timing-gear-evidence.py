#!/usr/bin/env python3
"""Read-only source/envelope consistency calculation; not a CAD acceptance gate."""
from pathlib import Path
import hashlib,json,math
ROOT=Path(__file__).resolve().parents[1]
old_center=math.hypot(90,72);cam_z=58;crank_z=29;cam_d=6.610*25.4;crank_d=3.400*25.4
modules={'cam_from_standard_addendum':cam_d/(cam_z+2),'crank_from_standard_addendum':crank_d/(crank_z+2)}
centers={k:v*(cam_z+crank_z)/2 for k,v in modules.items()}
# Independent feasibility design only. Source diameters retained; profile
# addenda, transverse module, pressure angle, width and helix remain estimates.
mt=2.8;beta=25.;center=mt*(cam_z+crank_z)/2;scale=center/old_center
proposed=dict(transverse_module_mm=mt,helix_angle_deg=beta,normal_module_mm=mt*math.cos(math.radians(beta)),transverse_pressure_angle_deg=20,width_mm=14,center_distance_mm=center,cam_axis_yz_mm=[90*scale,72*scale],cam_axis_delta_yz_mm=[90*(scale-1),72*(scale-1)],cam_tip_radius_mm=cam_d/2,crank_tip_radius_mm=crank_d/2,cam_addendum_mm=cam_d/2-mt*cam_z/2,crank_addendum_mm=crank_d/2-mt*crank_z/2,cam_lead_mm=math.pi*mt*cam_z/math.tan(math.radians(beta)),crank_lead_mm=math.pi*mt*crank_z/math.tan(math.radians(beta)))
assert proposed['cam_addendum_mm']>0 and proposed['crank_addendum_mm']>0
assert abs(proposed['cam_lead_mm']/proposed['crank_lead_mm']-2)<1e-12
paths=['reference/engine/timing-gear-evidence/pbm-catalog-2025.pdf','reference/engine/ford-industrial-parts.pdf','reference/engine/timing-gear-evidence/melling-engine-parts-catalog.pdf','reference/engine/timing-gear-evidence/elgin-c2766s.html','reference/engine/timing-gear-evidence/elgin-c2766s-front.jpg']
r=dict(status='PASS arithmetic consistency only; NOT CAD/installation acceptance',script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),sources_sha256={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},source_comparison_diameters_mm=dict(cam=cam_d,crank=crank_d),current_center_mm=old_center,old_center_standard_58_29_tip_diameters_mm=dict(cam=2*old_center/(cam_z+crank_z)*(cam_z+2),crank=2*old_center/(cam_z+crank_z)*(crank_z+2)),standard_unshifted_transverse_modules_mm=modules,standard_unshifted_centers_mm=centers,standard_unshifted_pair_exactly_consistent=False,independent_proposed_estimate=proposed,limits=['Elgin labels gear diameter, not explicit outside/pitch diameter. Treating it as tip diameter is a comparison assumption supported by the product envelope, not an engineering drawing.','Distinct manufacturers: PBM58/29 count and Elgin dimensions are replacement comparisons, not a measured same-specimen engineering specification.','The two published diameters do not imply one exact standard unshifted module; do not average away the discrepancy. Profile shift, tip truncation, rounding and variant remain unresolved.','Helix angle/lead and pressure angle are unmeasured. The proposed25degrees and2.8mm transverse module are independent educational estimates, not source facts.','No CAD has been built or installed by this arithmetic check. Shaft/cover/valvetrain re-registration requires coordinated review.'])
(ROOT/'inventory/engine/timing-gear-evidence-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
