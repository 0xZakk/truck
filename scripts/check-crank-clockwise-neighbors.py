"""Sample actual corrected crank against frozen block and pan; no installation."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import engine_clockwise_pose_candidate as motion
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
files={'crank':ROOT/'cad/engine/generated/crank-clockwise-candidate/crankshaft.step','block':ROOT/'cad/engine/generated/timing-front-block-expanded-seat-v3-candidate/block.step','pan':ROOT/'cad/engine/generated/timing-pan-expanded-seat-v2-candidate/pan.step'}
q={k:b.import_step(p) for k,p in files.items()}
paths=[*files.values(),Path(__file__),Path(motion.__file__),ROOT/'cad/engine/cad_metrics.py']
r={'status':'RUNNING','input_sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths},'samples':[],'scope':'24 static phases over one revolution, only named block/pan; not continuous or all-engine motion'}
out=ROOT/'inventory/engine/crank-clockwise-neighbors.json'
def save():out.write_text(json.dumps(r,indent=2)+'\n')
def vol(s):return sum(abs(solid_volume(x,'adaptive')) for x in s.solids()) if s else 0.
save()
for angle in range(0,360,15):
 moving=motion.crank_frame(angle)*q['crank']
 for name in ['block','pan']:
  overlap=vol(moving.intersect(q[name]));r['samples'].append({'event_deg':angle,'neighbor':name,'overlap_mm3':overlap});save();print(angle,name,overlap,flush=True)
  if overlap>.1:
   r['status']='FAIL actual sampled interference';save();raise SystemExit(1)
fault=vol((b.Pos(0,0,100)*q['crank']).intersect(q['block']));assert fault>100
r['negative_control_shift_up100_overlap_mm3']=fault
assert all(sha(ROOT/p)==h for p,h in r['input_sha256'].items())
r['status']='PASS 48 sampled block/pan pairs; broader continuous motion pending';save();print(r['status'],flush=True)
