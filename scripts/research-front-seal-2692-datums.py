#!/usr/bin/env python3
"""Read-only datum alternatives and preserved-neighbor bounds; no shape exports."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import front_crank_seal_envelope_candidate as seal
import timing_cover_front_joint_candidate as cover
from assembly_math import transforms
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in m['definitions']};frames=transforms(m)
paths={k:ROOT/defs[k]['step'].lstrip('/') for k in ['damper-hub','damper-key','damper-bolt','damper-washer','crankshaft']}
paths['cover']=ROOT/'cad/engine/generated/timing-cover-attachment-v2/cover.step'
paths['crank-gear']=ROOT/'cad/engine/generated/timing-thrust-land-candidate/crank-timing-gear.step'
watch=[Path(__file__),Path(seal.__file__),Path(cover.__file__),ROOT/'inventory/engine/full-assembly.json',ROOT/'reference/engine/front-crank-seal-envelope-review.json',ROOT/'cad/engine/damper.py',ROOT/'cad/engine/damper_attachment.py']+list(paths.values())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();inputs={str(p.relative_to(ROOT)):sha(p) for p in watch}
shapes={k:(b.import_step(p) if k in ['cover','crank-gear'] else frames[k]*b.import_step(p)) for k,p in paths.items()}
bounds={k:[list(q.bounding_box().min),list(q.bounding_box().max)] for k,q in shapes.items()};hubrange=[bounds['damper-hub'][0][0],bounds['damper-hub'][1][0]]
rows=[]
for name,front in [('cover-plane',415),('old-seal-center',414+seal.WIDTH/2),('whole-envelope-on-hub',hubrange[0]+1+seal.WIDTH)]:
 rear=front-seal.WIDTH;rows.append({'name':name,'selected':False,'overall_interval_mm':[rear,front],'possible_hub_axial_overlap_mm':max(0,min(front,hubrange[1])-max(rear,hubrange[0])),'full_envelope_within_existing_hub_axial_interval':rear>=hubrange[0] and front<=hubrange[1]})
lands=[]
for p in cover.source.HOLES_NORMALIZED:
 y,z=cover.c.yz(p,cover.P);lands.append({'axis_yz_mm':[y,z],'R9_land_gap_to_R43_boss_mm':math.hypot(y,z)-9-43})
key_front=444.95
r={'status':'PROPOSED DATUM CONTRACT; no new seal or neighbor CAD','inputs':inputs,'world_bounds_mm':bounds,'alternatives':rows,'mounting_land_bounds':lands,'source_dimensions_mm':{'shaft':seal.SHAFT_DIAMETER,'free_case_OD':seal.CASE_DIAMETER,'housing_bore':seal.HOUSING_BORE,'overall_width':seal.WIDTH,'flange_OD':seal.FLANGE_DIAMETER},'proposed_cover_mask':{'x_mm':[406,434.4112],'radial_mm':[24,43]},'proposed_hub_mask':{'x_mm':[419,435.5],'radial_mm':[seal.SHAFT_DIAMETER/2,27]},'protected_bounds':{'gear_front_to_cover_mask_mm':406-bounds['crank-gear'][1][0],'hub_mask_to_key_cut_rear_mm':key_front-435.5,'remaining_nominal_hub_track_wall_mm':seal.SHAFT_DIAMETER/2-21.05,'nominal_diametral_case_fit_mm':seal.CASE_DIAMETER-seal.HOUSING_BORE},'limits':['Actual hub bore/strength, cover shoulder and lip axial position remain unknown.','All alternatives are unselected pending root coordination.','No OEM or vendor CAD drawings downloaded; independent source-envelope study only.','No geometry/installed support/contact/motion/browser acceptance.']}
assert rows[0]['possible_hub_axial_overlap_mm']==0 and rows[2]['full_envelope_within_existing_hub_axial_interval']
assert min(v['R9_land_gap_to_R43_boss_mm'] for v in lands)>0
assert all(sha(ROOT/p)==h for p,h in inputs.items())
p=ROOT/'inventory/engine/front-seal-2692-datum-research.json';p.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'alternatives':rows,'protected_bounds':r['protected_bounds']},indent=2))
