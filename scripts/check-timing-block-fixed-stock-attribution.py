#!/usr/bin/env python3
"""Feature-local ablation and prospective machining audit; never exports a cut block."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import full_engine as f
from cad_metrics import solid_volume
from timing_block_fixed_stock_candidate import DELTA
from timing_block_physical_interface_contract import physical_masks
OUT=ROOT/'cad/engine/generated/timing-block-fixed-stock-candidate'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q is not None and getattr(q,'wrapped',True) is not None else 0.
def comp(q):return b.Compound(children=list(q.solids()))
def bounds(q):
 if not q.solids():return None
 bb=q.bounding_box();return [list(bb.min),list(bb.max)]
paths=[OUT/'block.step',ROOT/'cad/engine/generated/block.step',ROOT/'inventory/engine/timing-block-fixed-stock-validation.json',ROOT/'cad/engine/timing_block_physical_interface_contract.py',ROOT/'cad/engine/timing_block_fixed_stock_candidate.py',ROOT/'cad/engine/full_engine.py',Path(__file__)]
features=['block_interface_shape','filter_block_interface','03-carrier1994']
paths += [OUT/(name+'-'+side+'.step') for name in features for side in ['before','after']]
inputs={str(p.relative_to(ROOT)):sha(p) for p in paths}
q=b.import_step(OUT/'block.step');base=b.import_step(ROOT/'cad/engine/generated/block.step')
tunnel=b.Pos(0,90+DELTA[1],72+DELTA[2])*f.cx(f.CAM_BORE_R,f.LENGTH+2)
guides=b.Compound(children=[b.Pos(x+dx,90+DELTA[1],150+DELTA[2])*b.Cylinder(f.LIFTER_BORE_R,235) for x in f.CYLINDERS for dx in [-25,25]])
cutters={'tunnel':tunnel,'guides':guides};attribution=[]
for name in features:
 before=b.import_step(OUT/(name+'-before.step'));after=b.import_step(OUT/(name+'-after.step'));added=comp(after.cut(before))
 for interface,cutter in cutters.items():
  contribution=added.intersect(cutter);row={'feature':name,'interface':interface,'before_intrusion_mm3':vol(before.intersect(cutter)),'after_intrusion_mm3':vol(after.intersect(cutter)),'net_added_in_interface_mm3':vol(contribution),'net_added_bounds_mm':bounds(contribution),'remaining_in_final_block_mm3':vol(comp(contribution).intersect(q)) if contribution.solids() else 0};attribution.append(row);print('feature',row,flush=True)
# These are proposals measured before any final machining. No cut block is created.
physical,specs=physical_masks();extra=comp(q.cut(base));missing=comp(base.cut(q));guards=[]
for name,mask in physical.items():
 a=vol(extra.intersect(mask));d=vol(missing.intersect(mask));prospective={interface:vol(comp(q.intersect(cutter)).intersect(mask)) for interface,cutter in cutters.items()}
 row={'name':name,'fixed_stock_added_mm3':a,'fixed_stock_removed_mm3':d,'fixed_stock_unchanged':a+d<1e-5,'prospective_final_machining_removal_mm3':prospective,'prospective_safe':sum(prospective.values())<1e-5};guards.append(row);print('guard',row,flush=True)
seats=[]
for i,x in enumerate([-334,-110,110,360.5],1):
 width=22.;radius=f.CAM_BORE_R+.025
 shell=f.cx(f.CAM_BORE_R+.05,width)-f.cx(f.CAM_BORE_R+.001,width)
 old=b.Pos(x,90,72)*shell;new=b.Pos(0,DELTA[1],DELTA[2])*old
 samples=[]
 for sx in [x-10.9,x,x+10.9]:
  missing_angles=[]
  for angle in range(0,360,5):
   rad=math.radians(angle);point=(sx,90+DELTA[1]+radius*math.cos(rad),72+DELTA[2]+radius*math.sin(rad))
   if not q.is_inside(point):missing_angles.append(angle)
  samples.append({'x_mm':sx,'unsupported_sample_angles_deg_from_positive_Y_toward_Z':missing_angles})
 row={'bearing':i,'center_x_mm':x,'shell_volume_mm3':vol(shell),'baseline_supported_mm3':vol(base.intersect(old)),'fixed_stock_supported_mm3':vol(q.intersect(new)),'radial_samples':samples};seats.append(row);print('journal',row,flush=True)
assert inputs=={p:sha(ROOT/p) for p in inputs}
r={'status':'DIAGNOSTIC proposed final machining NOT APPLIED','input_sha256':inputs,'feature_local_ablation':attribution,'physical_mask_contract':specs,'physical_results':guards,'four_journal_support':seats,'limits':['Before/after feature comparison bypasses only that feature on identical incoming stock; not a whole-pipeline alternate regeneration','Original 79 broad guards remain reported separately and are not weakened','Physical 2 mm margins are explicit proposed review guards, not factory wall dimensions','Journal angle sampling at 5 degrees locates deficiencies; shell volumes are exact CAD comparisons, samples are not continuous coverage proof','No new casting support added and no final-machined candidate created']}
(ROOT/'inventory/engine/timing-block-fixed-stock-attribution.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
