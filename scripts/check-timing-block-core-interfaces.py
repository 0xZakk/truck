#!/usr/bin/env python3
"""Read-only fit diagnostics for isolated migrated block and frozen core."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import full_engine as f
import timing_core_migration_candidate as core
from timing_block_axis_feature_candidate import DELTA
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-block-axis-feature-candidate'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bounds(q):
 if not q.solids():return None
 bb=q.bounding_box();return [list(bb.min),list(bb.max)]
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q is not None and getattr(q,'wrapped',True) is not None else 0.
paths={'block':OUT/'block.step','baseline':ROOT/'cad/engine/generated/block.step'}
paths.update({i:ROOT/'cad/engine/generated/timing-thrust-land-candidate'/(i+'.step') for i in core.IDS})
inputs={str(p.relative_to(ROOT)):sha(p) for p in paths.values()};inputs[str(Path(__file__).relative_to(ROOT))]=sha(Path(__file__))
for rel in ['cad/engine/full_engine.py','cad/engine/timing_core_migration_candidate.py','cad/engine/timing_block_axis_feature_candidate.py','cad/engine/oil_drive_layout.py','inventory/engine/timing-block-axis-feature-validation.json']:
 inputs[rel]=sha(ROOT/rel)
parts={k:b.import_step(p) for k,p in paths.items()};block=parts['block'];base=parts['baseline'];rows=[]
for name in core.IDS:
 for travel in ([-.1,0] if name in ['camshaft','cam-timing-gear','cam-gear-spacer','cam-timing-key'] else [0]):
  intersection=block.intersect(b.Pos(travel,0,0)*parts[name]);overlap=vol(intersection);oldpart=parts[name] if name=='crank-timing-gear' else b.Pos(*[-v for v in DELTA])*parts[name];baseline_overlap=vol(base.intersect(b.Pos(travel,0,0)*oldpart));rows.append({'part':name,'travel_mm':travel,'overlap_mm3':overlap,'intersection_bounds_mm':bounds(intersection),'unshifted_same_shape_baseline_overlap_mm3':baseline_overlap,'clear':overlap<1e-5});print(rows[-1],flush=True)
guides=[]
for i,x in enumerate(f.CYLINDERS,1):
 for dx in [-25,25]:
  probe=b.Pos(x+dx,90+DELTA[1],150+DELTA[2])*b.Cylinder(f.LIFTER_BORE_R-.001,235-.002)
  intersection=block.intersect(probe);overlap=vol(intersection);baseline_overlap=vol(base.intersect(b.Pos(*[-v for v in DELTA])*probe));guides.append({'cylinder':i,'x_mm':x+dx,'probe_radius_mm':f.LIFTER_BORE_R-.001,'intrusion_mm3':overlap,'intersection_bounds_mm':bounds(intersection),'baseline_intrusion_mm3':baseline_overlap,'clear':overlap<1e-5});print('guide',guides[-1],flush=True)
seats=[]
for i in range(1,5):
 bearing=parts[f'cam-bearing-{i}'];bb=bearing.bounding_box();x=(bb.min.X+bb.max.X)/2;width=bb.size.X
 shell=f.cx(f.CAM_BORE_R+.05,width)-f.cx(f.CAM_BORE_R+.001,width)
 old=b.Pos(x,90,72)*shell;new=b.Pos(*DELTA)*old
 a=vol(base.intersect(old));d=vol(block.intersect(new));seats.append({'bearing':i,'x_mm':x,'shell_volume_mm3':vol(shell),'baseline_supported_volume_mm3':a,'candidate_supported_volume_mm3':d,'difference_mm3':d-a})
import oil_drive_layout as drive
cutters={'distributor-neck':drive.axial_cylinder(13.149,8.001,109.999),'drive-gear-pocket':drive.axial_cylinder(19.999,-7.999,7.999),'lower-shaft':drive.axial_cylinder(6.199,drive.INTERMEDIATE_TOP-11.999,7.999),'clamp-bolt':b.Pos(0,37,0)*drive.axial_cylinder(4.099,15.001,64.999),'intermediate-shaft':drive.axial_cylinder(7.199,drive.INTERMEDIATE_BOTTOM-1.999,drive.INTERMEDIATE_TOP-11.501)}
drive_probes=[]
for name,cutter in cutters.items():
 old=drive.GEAR_FRAME*cutter;new=b.Pos(*DELTA)*old
 a=vol(base.intersect(old));d=vol(block.intersect(new));drive_probes.append({'name':name,'baseline_intrusion_mm3':a,'candidate_intrusion_mm3':d,'clear':d<1e-5});print('drive',drive_probes[-1],flush=True)
# Unmoved bearing must be detected against the new tunnel/stock.
bad=vol(block.intersect(b.Pos(*[-v for v in DELTA])*parts['cam-bearing-2']))
assert bad>1e-5
assert inputs=={p:sha(ROOT/p) for p in inputs}
r={'status':'PASS sampled core clearances and guide probes' if all(x['clear'] for x in rows+guides+drive_probes) else 'FAIL isolated core or guide fit; inspect reported intrusions','input_sha256':inputs,'block_core_pairs':rows,'lifter_guide_probes':guides,'bearing_support_shells':seats,'connected_drive_cutter_probes':drive_probes,'negative_control_unshifted_bearing_overlap_mm3':bad,'limits':['No canonical installation or factory datum claim','Bearing shell material is a support comparison, not press fit or loading analysis','Axial endpoints only against block; frozen gear pair proofs remain separate and service backlash unresolved','Protected block-feature gates must also pass; a core fit pass cannot override them','Distributor/pump physical fit remains a separate connected-frame validation']}
(ROOT/'inventory/engine/timing-block-core-interface-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
