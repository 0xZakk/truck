"""Read-only chronology of timing-cover versus installed water-pump interfaces."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_math import transforms
from cad_metrics import solid_volume
O=R/'cad/engine/generated/timing-waterpump-cover-datum-audit';O.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def bounds(s):return [list(s.bounding_box().min),list(s.bounding_box().max)]
def norm(s):
 if not s:return None
 ss=list(s.solids());return b.Compound(ss)if ss else None
def metric(s):return solid_volume(s)if s else 0.
def info(s):return {'volume_mm3':metric(s),'bounds_mm':bounds(s)if s else None,'solids':len(s.solids())if s else 0}
mp=R/'inventory/engine/full-assembly.json';st=R/'inventory/engine/corrected-engine-stage.json';m=json.loads(mp.read_text());stage=json.loads(st.read_text());poses=transforms(m);sp=transforms(stage);defs={q['id']:q for q in m['definitions']};sd={q['id']:q for q in stage['definitions']};occ={q['id']:q for q in m['occurrences']}
paths={};neighbors={};pose_rows={}
for n in ['water-pump-housing','water-pump-gasket']:
 p=R/defs[occ[n]['definition']]['step'].lstrip('/');paths[n]=p;neighbors[n]=poses[n]*b.import_step(p)
 assert poses[n]==sp[n];assert defs[n]['step']==sd[n]['step'];pose_rows[n]={'world_bounds_mm':bounds(neighbors[n]),'transform_unchanged':True,'definition_unchanged':True}
variants={'canonical':R/defs['timing-cover']['step'].lstrip('/'),'shell':R/'cad/engine/generated/timing-cover-shell-candidate/timing-cover-shell-candidate.step','front-joint':R/'cad/engine/generated/timing-cover-front-joint-candidate/cover.step','attachment-v2':R/'cad/engine/generated/timing-cover-attachment-v2/cover.step','seal2692':R/'cad/engine/generated/front-seal-2692-candidate/cover.step','seven-main':R/'cad/engine/generated/timing-cover-seven-fastener-candidate/cover.step','pan21':R/'cad/engine/generated/timing-pan21-lateral-candidate/cover.step','serialized-stage':R/sd['timing-cover']['step'].lstrip('/')}
rows={};covers={};witnesses={};data={}
for name,p in variants.items():
 cover=b.import_step(p)
 if name=='canonical':cover=poses['timing-cover']*cover
 if name=='serialized-stage':cover=sp['timing-cover']*cover
 covers[name]=cover;rows[name]={}
 for n,s in neighbors.items():
  q=norm(cover.intersect(s));row=info(q)
  if q:
   try:row['adaptive_volume_mm3']=sum(abs(solid_volume(x,'adaptive'))for x in q.solids())
   except Exception as e:row['adaptive_error']=str(e)
   wp=O/(name+'__'+n+'.step');b.export_step(q,wp);row['witness_step']=str(wp.relative_to(R));row['witness_sha256']=sha(wp);witnesses[name,n]=q
  rows[name][n]=row
 print(name,rows[name],flush=True)
# Intersect whole signed deltas with neighbors: never neighbor subtraction as a repair.
changes={}
for old,new in [('canonical','front-joint'),('front-joint','attachment-v2'),('attachment-v2','seal2692'),('seal2692','seven-main'),('seven-main','pan21')]:
 changes[old+'→'+new]={}
 for sign,a,z in [('added',new,old),('removed',old,new)]:
  q=norm(covers[a].cut(covers[z]));changes[old+'→'+new][sign]={n:info(norm(q.intersect(s)))if q else info(None)for n,s in neighbors.items()}
 print('DELTA',old,new,changes[old+'→'+new],flush=True)
# Actual YZ sections reveal shell/flange/pump ownership; export curves for deterministic plotting.
for name,s in {**neighbors,'cover':covers['pan21'],'old-cover':covers['canonical']}.items():
 for x in [374,376,390,414]:
  cut=b.section(s,b.Plane.YZ.offset(x));lines=[]
  for e in cut.edges():
   pts=np.array([tuple(e.position_at(t))for t in np.linspace(0,1,65)]);lines.append(pts)
  if lines:data[f'{name}_{x}']=np.array(lines)
np.savez_compressed(O/'sections.npz',**data)
inputs=[mp,st,Path(__file__),*paths.values(),*variants.values(),R/'cad/engine/water_pump_joint_candidate.py',R/'cad/engine/timing_cover_shell_candidate.py',R/'cad/engine/timing_cover_front_joint_candidate.py',R/'reference/engine/water-pump-mounting-topology-reviewed.json',R/'reference/engine/timing-cover-registration-review.json']
r={'status':'FAIL actual pump/cover interference; diagnosis only','stage_sha256':sha(st),'pump_poses':pose_rows,'chronology':rows,'changed_regions':changes,'inputs':{str(p.relative_to(R)):sha(p)for p in inputs},'canonical_or_stage_modified':False,'limitations':['No geometry repair, hydraulic interpretation or source-measured dimensional claim.','Shell and front-joint differ in estimated registration; not a pure local edit.']};(R/'inventory/engine/timing-waterpump-cover-datum-audit.json').write_text(json.dumps(r,indent=2)+'\n')
