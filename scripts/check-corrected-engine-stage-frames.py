"""Check the real composed manifest with opt-in runtime and staged contracts."""
from pathlib import Path
import sys,json,hashlib,math
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_clockwise_candidate import transforms
from crossed_oil_drive_endplay_candidate import angles
from cam_clockwise_candidate import linkage_frames
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
M=R/'inventory/engine/corrected-engine-stage.json';m=json.loads(M.read_text());base=json.loads((R/'inventory/engine/full-assembly.json').read_text());neutral=transforms(m)
occ={o['id']:o for o in m['occurrences']};groups={a['id']:a for a in m['assemblies']}
def mat(p):
 t=p.wrapped.Transformation();return np.array([[t.Value(i,j)for j in range(1,5)]for i in range(1,4)])
core=json.loads((R/'inventory/engine/timing-core-drive-stage-review.json').read_text());errors=[]
for row in core['core_parts']:errors.append(float(np.max(abs(mat(neutral[row['occurrence']])-np.array(row['target_world_matrix'])))))
maximum=max(errors);checks=len(errors);branchchecks=0
for q in [0,55,120,246,468,719]:
 for x in [0,-.1]:
  pose=transforms(m,q,x)
  for key,want in linkage_frames(base,q,x).items():maximum=max(maximum,float(np.max(abs(mat(pose[key])-mat(want)))));checks+=1
  for o in m['occurrences']:
   group=groups[o['parent']];motion=group.get('motion') or {}
   if group['id']!='distributor-rotation' and not (group['id'].startswith('oil-pump-') and motion.get('type')=='rotary'):continue
   local=b.Pos(*o['position_cad_mm'])*b.Rot(*o.get('rotation_cad_deg',[0,0,0]));parent=neutral[o['id']]*local.inverse()
   distributor=angles(q,x)[1];angle=distributor if group['id']=='distributor-rotation' else distributor*motion['ratio']/-.5
   want=parent*b.Rot(0,0,angle)*local
   maximum=max(maximum,float(np.max(abs(mat(pose[o['id']])-mat(want)))));checks+=1;branchchecks+=1
assert maximum<1e-8,(maximum,checks)
paths=[M,Path(__file__),R/'cad/engine/assembly_clockwise_candidate.py',R/'inventory/engine/timing-core-drive-stage-review.json',R/'inventory/engine/clockwise-linkage-pose-patch.json']
report={'status':'PASS composed manifest motion matrices; geometry gaps remain','occurrences':len(neutral),'matrix_checks':checks,'branch_checks':branchchecks,'maximum_matrix_error':maximum,'bindings':{str(p.relative_to(R)):sha(p)for p in paths},'limits':m['integration_stage']['open']}
(R/'inventory/engine/corrected-engine-stage-frame-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],checks,branchchecks,maximum)
