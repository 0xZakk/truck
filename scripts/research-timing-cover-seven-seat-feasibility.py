"""Read-only annular support map; no adopted hardware dimensions or CAD edits."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import timing_cover_front_joint_candidate as f
b.SkipClean.clean=False
paths=[ROOT/'cad/engine/generated/timing-front-block-expanded-seat-v3-candidate/block.step',ROOT/'cad/engine/generated/front-seal-2692-candidate/cover.step',Path(__file__),Path(f.__file__),Path(f.source.__file__)]
block,cover=[b.import_step(p)for p in paths[:2]]
def vol(q):return sum(abs(solid_volume(s,'adaptive'))for s in q.solids())if q is not None else 0.
def probe(owner,x,y,z,lo,hi):
 ring=f.c.cx(hi,x-.02,x,y,z)-f.c.cx(lo,x-.03,x+.01,y,z)
 try:return {'missing_mm3':vol(ring.cut(owner)),'complete_volume_mm3':math.pi*(hi*hi-lo*lo)*.02}
 except Exception as e:return {'measurement_error':repr(e)}
rows=[]
for n,p in enumerate(f.source.HOLES_NORMALIZED,1):
 y,z=f.c.yz(p,f.P);row={'station':n,'axis_yz_mm':[y,z],'head_support_R4_2_to_9':{str(x):probe(cover,x,y,z,4.2,9)for x in [377.8,379.8,383.8,387.8,391.8,415.]},'block_wall_R4_2_to_6_2':{str(x):probe(block,x,y,z,4.2,6.2)for x in [354.,358.,362.,366.,370.,373.]}}
 rows.append(row);print(n,'done',flush=True)
r={'status':'RESEARCH; no hardware or seat selected','input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths},'probe_thickness_mm':.02,'probes_are_estimates_not_specifications':True,'stations':rows,'limits':['Annular material samples do not establish load capacity or socket threading','Existing rear plane373, cover rear373.8 and pocketfloor366 are model estimates','No cutter, union, export or canonical model mutation performed','CurrentX415 uniform seats remain unverified']}
(ROOT/'inventory/engine/timing-cover-seven-seat-feasibility.json').write_text(json.dumps(r,indent=2)+'\n')
