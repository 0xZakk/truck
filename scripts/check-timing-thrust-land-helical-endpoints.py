#!/usr/bin/env python3
"""25 tooth-period samples at shifted axial endpoint; zero endpoint inherited."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-thrust-land-candidate'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
def comp(q):return b.Compound(children=list(q.solids()))
proofpath=ROOT/'inventory/engine/timing-gear-pair-candidate-validation.json';refpath=ROOT/'inventory/engine/timing-gear-pair-refinement-validation.json';landpath=ROOT/'inventory/engine/timing-thrust-land-candidate-validation.json'
proof=json.loads(proofpath.read_text());ref=json.loads(refpath.read_text());land=json.loads(landpath.read_text())
assert sha(proofpath)==ref['inherited_sweep']['report_sha256']
assert land['protected_regions']['added_outside_tooth_root_guard_solids']==0
for name in ['cam-timing-gear','crank-timing-gear']:assert sha(OUT/(name+'.step'))==land['exports'][name]['step_sha256']
for name in ['cam','crank']:assert sha(ROOT/f'cad/engine/generated/timing-gear-pair-candidate/{name}.step')==proof['exports'][name]['step_sha256']
# Bind both proof chains. Original whole-engine manifest is historical context;
# this proof reuses only exact frozen paired-gear geometry and its sampled gaps.
for path,h in ref['inputs_sha256'].items():assert sha(ROOT/path)==h,path
watch=[Path(__file__),ROOT/'cad/engine/cad_metrics.py',proofpath,refpath,landpath]+[OUT/(x+'.step') for x in ['cam-timing-gear','crank-timing-gear']]
inputs={str(p.relative_to(ROOT)):sha(p) for p in watch}
axis=(95.1098209901611,76.08785679212888);phi=math.atan2(72,90);gx=385.259375
cam=b.Pos(-gx,-axis[0],-axis[1])*b.import_step(OUT/'cam-timing-gear.step');crank=b.Pos(-gx,0,0)*b.import_step(OUT/'crank-timing-gear.step')
region=b.Pos(0,40.6*math.cos(phi),40.6*math.sin(phi))*b.Rot(math.degrees(phi),0,0)*b.Box(16,14,44)
rows=[]
for old in proof['sweep']:
 theta=old['crank_angle_deg'];a=comp((b.Rot(theta,0,0)*crank).intersect(region));z=comp((b.Pos(-.1,*axis)*b.Rot(-theta/2,0,0)*cam).intersect(region))
 overlap=vol(a.intersect(z));gap=a.distance_to(z)
 assert overlap<1e-5 and gap>1e-6
 # Original refinement only removed material; new annulusR26 lies at least
 #52.62mm from crank tip. Original region gap is therefore a lower bound
 #for the revised neutral pair. X translation commutes with YZ lens clipping
 #and stays inside regionX±8; Lipschitz distance gives all axial values.
 bound=old['engagement_region_surface_gap_mm']-.1
 assert bound>0
 rows.append({'crank_angle_deg':theta,'cam_angle_deg':-theta/2,'axial_mm':-.1,'overlap_mm3':overlap,'local_engagement_gap_mm':gap,'whole_axial_interval_gap_lower_bound_mm_at_this_rotation':bound})
 print(rows[-1],flush=True);(OUT/'helical-progress.json').write_text(json.dumps(rows,indent=2)+'\n')
assert inputs=={p:sha(ROOT/p) for p in inputs}
r={'status':'PASS25rotational samples at both axial endpoints; full axial interval bounded at those rotations; UNINSTALLED','input_sha256':inputs,'endpoint_minus_0_1':rows,'endpoint_zero':{'mode':'inherited frozen original proof plus subtractive refinement and addedR26 material outside engagement','proof_sha256':sha(proofpath),'refinement_sha256':sha(refpath),'land_sha256':sha(landpath),'samples':25,'overlap_limit_mm3':1e-5},'continuous_axial_argument':'At each sampled rotation, original lens-local gap exceeds total0.1mm translation. Translation inX commutes with fixedYZ lens clipping and full geometry remains withinX±8. Subtractive refinement cannot reduce gap; addedR26 annulus lies52.62mm from crank tip. Distance Lipschitz bound establishes no intersection for every axial value[-0.1,0] at these25 rotations.','limits':['25 rotations over one tooth period, not continuous rotation proof','No loaded contact/forces/production backlash claim','Original finite contact-phase brackets ataxial0 are not inherited ataxial−0.1','Full engine context still unmigrated']}
(ROOT/'inventory/engine/timing-thrust-land-helical-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],flush=True)
