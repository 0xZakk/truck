"""Check disjoint composition against both independently exported candidates."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import timing_block_combined_candidate as c
OUT=ROOT/'cad/engine/generated/timing-block-combined-candidate';OUT.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return sum(abs(solid_volume(x,'adaptive'))for x in s.solids())if s else 0.
def diff(a,z):return vol(a.cut(z))+vol(z.cut(a))
paths=[Path(__file__),Path(c.__file__),Path(c.deck.__file__),c.FOOT,c.DECK,ROOT/'inventory/engine/full-assembly.json',ROOT/'inventory/engine/timing-pump-foot-faceted-validation.json',ROOT/'inventory/engine/timing-valvetrain-inclined-delivery-validation.json']
inputs={str(p.relative_to(ROOT)):sha(p)for p in paths}
q,foot=c.build();print('built',q.is_valid,len(q.solids()),flush=True)
deck=b.import_step(c.DECK);slab=b.Pos(0,0,249)*b.Box(2000,2000,10)
metrics={'outside_deck_slab_difference_mm3':diff(q.cut(slab),foot.cut(slab)),'deck_slab_difference_mm3':diff(q.intersect(slab),deck.intersect(slab)),'omitted_deck_negative_control_mm3':diff(foot.intersect(slab),deck.intersect(slab))}
print(metrics,flush=True)
b.export_step(q,OUT/'block.step');rt=b.import_step(OUT/'block.step');metrics['step_roundtrip_difference_mm3']=diff(q,rt)
gates={'one_valid_solid':q.is_valid and len(q.solids())==1 and rt.is_valid,'outside_deck_unchanged':metrics['outside_deck_slab_difference_mm3']<1e-5,'deck_matches':metrics['deck_slab_difference_mm3']<1e-5,'negative_control':metrics['omitted_deck_negative_control_mm3']>1,'roundtrip':metrics['step_roundtrip_difference_mm3']<1e-5}
assert all(sha(ROOT/p)==h for p,h in inputs.items())
r={'status':'PASS local composition'if all(gates.values())else'FAIL','inputs':inputs,'metrics':metrics,'gates':gates,'step_sha256':sha(OUT/'block.step'),'remaining':['Native mesh export NOT RUN','Front crankgear/block/cover unresolved','Broader valve motion separate','Browser NOT RUN','No installation/factory claim']}
(ROOT/'inventory/engine/timing-block-combined-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],flush=True)
assert all(gates.values())
