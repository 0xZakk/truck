"""Focused unchanged drain/sump and retained shallow-floor controls for V9."""
from pathlib import Path
import sys,json,hashlib
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import oil_pan_joint_v9_candidate as p
from oil_pan import DRAIN_LOCAL,DRAIN_ROTATION
from cad_metrics import solid_volume
paths=[Path(__file__),Path(p.__file__),ROOT/'cad/engine/oil_pan.py',ROOT/'cad/engine/generated/oil-pan.step']
hashes={str(q.relative_to(ROOT)):hashlib.sha256(q.read_bytes()).hexdigest() for q in paths}
old=b.import_step(ROOT/'cad/engine/generated/oil-pan.step');new=p.pan_interface(old)
def vol(s):return sum(solid_volume(q,'adaptive') for q in s.solids()) if s else 0
# Compare original and rebuilt lower rear sump and complete drain-seat vicinity.
zones={'rear_sump_below_shallow_floor':b.Pos(-165,0,-160)*b.Box(450,300,180),'drain_seat':b.Pos(*DRAIN_LOCAL)*b.Box(55,55,55)}
checks={}
for name,zone in zones.items():
 a=old&zone;c=new&zone;delta=vol(a-c)+vol(c-a);assert delta<.02,(name,delta);checks[name]=delta
# The original shallow-floor slab remains closed at representative interior sites.
floor=[]
for x in (100,200,300):
 probe=b.Pos(x,0,-59.5)*b.Cylinder(2,2)
 v=vol(new&probe);assert abs(v-probe.volume)<1e-6,(x,v);floor.append(v)
# Open drain bore is preserved, not sealed by the shell reconstruction.
frame=b.Pos(*DRAIN_LOCAL)*b.Rot(*DRAIN_ROTATION)
probe=frame*(b.Pos(0,0,-4)*b.Cylinder(6.9,20));v=vol(new&probe);assert v<1e-6,v
assert all(hashlib.sha256((ROOT/q).read_bytes()).hexdigest()==h for q,h in hashes.items())
report={'input_hashes':hashes,'inputs_unchanged':True,'preserved_region_symmetric_difference_mm3':checks,'shallow_floor_probe_mm3':floor,'open_drain_probe_mm3':v,'scope':'Preserves lower rear sump and drain neighborhood; valid solid and static pickup clearance audited separately. No production capacity claim.'}
(ROOT/'inventory/engine/oil-pan-v9-preserved-interfaces-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS V9 preserved sump/drain/floor controls')
