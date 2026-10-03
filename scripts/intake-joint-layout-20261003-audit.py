#!/usr/bin/env python3
"""Read-only joint correspondence audit. No CAD generation or scale inference."""
from pathlib import Path
import hashlib,json,platform
ROOT=Path(__file__).resolve().parents[1]
PREFIX='intake-joint-layout-20261003'
def digest(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def build():
 inputs=['inventory/engine/full-assembly.json','reference/engine/intake-joint-online-20261003-measurement.json','reference/engine/intake-joint-online-20261003-evidence.json','cad/engine/efi_intake.py','cad/engine/upper_intake_clearance_candidate.py','cad/engine/intake_cap_coordination.py','cad/engine/intake_exterior_integration.py','cad/engine/intake_runner_exterior_candidate.py','cad/engine/intake_runner_exterior_integration.py','cad/engine/fuel_injection.py','cad/engine/intake_locating_dowel.py','reference/engine/intake-cap-frame-contract.json','cad/engine/full_engine.py','cad/engine/manifold_lifting_eye.py','cad/engine/rear_manifold_mounts_desktop_candidate.py','cad/engine/intake_exterior_candidate.py','cad/engine/regulator_vacuum.py','cad/engine/egr.py','docs/onboarding/QUALITY-STANDARD.md','docs/components/intake-runner-exterior-candidate.md','docs/components/intake-support-candidate.md']
 manifest=json.loads((ROOT/inputs[0]).read_text()); rows={o['id']:o for o in manifest['occurrences']}
 measure=json.loads((ROOT/inputs[1]).read_text()); run=next(r for r in measure['runs'] if r['threshold']==210)
 ports=list(reversed(run['port_centers_left_to_right_px'])); front,rear=ports[0],ports[-1]
 dx,dy=rear[0]-front[0],rear[1]-front[1];length=(dx*dx+dy*dy)**.5;u=(dx/length,dy/length);v=(-u[1],u[0])
 def norm(p):return [sum((p[i]-front[i])*a[i] for i in range(2))/length for a in (u,v)]
 holes=sorted((f for f in run['features'] if f['class']=='small_hole'),key=lambda f:norm(f['center_px'])[0])
 features=[{'feature_id':f'P{i}','normalized_uv':norm(p),'row_station_source':s,'runner_number_hypothesis':i,'physical_occurrence':'efi-upper-intake / efi-lower-intake (features, not separate parts)'} for i,(p,s) in enumerate(zip(ports,run['normalized_stations_front_to_rear']),1)]
 holes=[{'feature_id':f'H{i}','normalized_uv':norm(f['center_px']),'pixel_center':f['center_px'],'role':'unresolved aperture'} for i,f in enumerate(holes,1)]
 # Seven longitudinal slots, two with two physical apertures. Do not select a member by convenience.
 slots=[['H1'],['H2'],['H3','H4'],['H5'],['H6','H7'],['H8'],['H9']]
 correspondence=[]
 for i,choices in enumerate(slots,1):
  key=f'efi-upper-stud-{i}';assert key in rows
  correspondence.append({'occurrence_id':key,'definition':rows[key]['definition'],'current_parent':rows[key]['parent'],'current_position_cad_mm':rows[key]['position_cad_mm'],'candidate_hole_ids':choices,'status':'proposed ordering; paired role unresolved' if len(choices)>1 else 'proposed ordering; end and face registration pending'})
 primary=['efi-lower-intake','efi-upper-intake','efi-upper-intake-gasket']
 assert len(holes)==9 and len(features)==6 and all(k in rows for k in primary)
 return {'schema':1,'readiness':'research correction plan; no metric pose approved','baseline_commit':'4f1fe9da2ec177e1ff61668df66ca422e37b0b7c','runtime':platform.python_version(),'inputs_sha256':{p:digest(p) for p in inputs},'coordinate_contract':{'units':'dimensionless until independent metric scale or explicitly approved estimate','origin':'short-gap terminal port center P1; inferred ACT/front end','u':'P1 toward P6; maps to world -X only after end identity review','v':'image-derived +90 degree normal to u; world Y sign unresolved until face registration','normal':'upper/lower joint normal; world +Z is inherited candidate convention','absolute_span_mm':None,'world_origin_mm':None,'gasket_thickness_mm':None,'diameters_mm':None,'old_pitch_is_factory_scale':False},'ports':features,'holes':holes,'stud_correspondence':correspondence,'primary_occurrences':[{k:rows[i].get(k) for k in ('id','definition','parent','position_cad_mm','rotation_cad_deg')} for i in primary],'threshold_ratio_range':[min(r['right_end_gap_over_other_mean'] for r in measure['runs'] if r['topology_valid']),max(r['right_end_gap_over_other_mean'] for r in measure['runs'] if r['topology_valid'])],'uncertainty':'threshold range is extraction repeatability only; uncalibrated photo/perspective, replacement transfer, end/face identification and physical scale remain systematic unknowns','checks':{'feature_counts':'PASS 6 ports, 9 apertures','stable_stud_ids':'PASS 7 existing occurrences; no invented fasteners','metric_scale':'UNKNOWN','paired_hole_roles':'UNKNOWN','CAD_export_installed_motion_browser':'NOT RUN'}}
if __name__=='__main__':
 print(json.dumps(build(),indent=2))
