"""Coherent expanded pan/gasket/block checks after worker exports are frozen."""
from pathlib import Path
import sys,json,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
b.SkipClean.clean=False
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import timing_pan_expanded_seat_v2_contract as seat
import timing_front_block_expanded_seat_v3_candidate as contract
p=argparse.ArgumentParser();p.add_argument('--pan-sha',required=True);p.add_argument('--gasket-sha',required=True);a=p.parse_args()
OUT=ROOT/'cad/engine/generated/timing-front-block-expanded-seat-v3-candidate'
PD=ROOT/'cad/engine/generated/timing-pan-expanded-seat-v2-candidate'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(q):
 if q is None or getattr(q,'wrapped',True) is None:return 0.
 if isinstance(q,b.ShapeList):return sum(vol(s)for s in q)
 total=0.
 for s in q.solids():
  for precision in [1e-9,1e-11,1e-13]:
   props=GProp_GProps();err=BRepGProp.VolumeProperties_s(s.wrapped,props,precision,True,False)
   if err<=1e-7:total+=abs(props.Mass());break
  else:raise ValueError(f'Strict integration failed {err}')
 return total
paths=[OUT/'block.step',PD/'pan.step',PD/'pan-gasket.step',Path(seat.__file__),Path(contract.__file__),Path(__file__)]
assert sha(paths[1])==a.pan_sha and sha(paths[2])==a.gasket_sha
assert sha(paths[3])==contract.SEAT_SHA
block,pan,gasket=[b.import_step(p)for p in paths[:3]]
rows=[]
for name,x,y in [('block-pan',block,pan),('block-gasket',block,gasket),('pan-gasket',pan,gasket)]:
 overlap=x.intersect(y);v=vol(overlap);row={'pair':name,'overlap_mm3':v,'distance_mm':x.distance_to(y)};rows.append(row);print(row,flush=True)
 if v>1e-5:b.export_step(contract.norm(overlap),OUT/(name+'-overlap.step'))
male_path=ROOT/'cad/engine/generated/pan-fastener-thread-candidate/pan-screw.step';paths.append(male_path);male=b.import_step(male_path)
for n in [10,20]:
 placed=b.Pos(*contract.ownership.RELOCATIONS[n])*male
 rows.append({'pair':f'block-male-{n}','overlap_mm3':vol(block.intersect(placed)),'distance_mm':block.distance_to(placed)})
back=seat.clip_x(seat.band(0,.02,'gasket',True),300,365)
under=seat.clip_x(seat.band(-2.02,-2,'gasket',True),300,365)
back_missing=vol(back.cut(block));under_missing=vol(under.cut(pan))
# Actual gasket translated into its supporting owner, normal thickness is not inferred.
# This supplements analytic source witnesses and excludes vertical cut edges at portals.
actual_upper=vol(seat.clip_x(b.Pos(0,0,.01)*gasket,300.01,364.99).cut(gasket).cut(block))
actual_lower=vol(seat.clip_x(b.Pos(0,0,-.01)*gasket,300.01,364.99).cut(gasket).cut(pan))
report={'status':'coherent estimated expanded seat pair','input_sha256':{str(p.relative_to(ROOT)):sha(p)for p in paths},'pairs':rows,'analytic_upper_backing_missing_mm3':back_missing,'analytic_lower_backing_missing_mm3':under_missing,'actual_upper_translation_unbacked_mm3':actual_upper,'actual_lower_translation_unbacked_mm3':actual_lower,'limits':['10mm block backing is estimated, no strength/factory claim','Translation checks include sloped side edges; any nonzero requires localized diagnosis, no automatic threshold relaxation','Whole oil containment and installed/browser acceptance remain open']}
report['gates']={'no_overlap':all(r['overlap_mm3']<1e-5 for r in rows),'analytic_seat_support':back_missing+under_missing<1e-5,'actual_gasket_support':actual_upper+actual_lower<1e-5};report['local_status']='PASS' if all(report['gates'].values())else'FAIL'
(ROOT/'inventory/engine/timing-front-expanded-seat-v3-pair.json').write_text(json.dumps(report,indent=2)+'\n');print(report,flush=True)
