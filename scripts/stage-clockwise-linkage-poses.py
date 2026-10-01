"""Serialize neutral corrected linkage frames and compare JS deltas with CAD."""
from pathlib import Path
import copy,json,sys,math,hashlib,subprocess
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import cam_clockwise_candidate as cam
from assembly_math import transforms
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=ROOT/'inventory/engine/full-assembly.json';m=json.loads(manifest.read_text())
raw=copy.deepcopy(m)
for o in raw['occurrences']:o.pop('valvetrain',None)
rawposes=transforms(raw,0)
occ={o['id']:o for o in m['occurrences']}
order=[1,5,3,6,2,4]
neutral={}
for cylinder in range(1,7):
 q=order.index(cylinder)*120
 assert all(abs(cam.state(q,cylinder,k)['lifter_lift'])<1e-12 for k in ['intake','exhaust'])
 neutral.update({key:v for key,v in cam.linkage_frames(m,q).items() if key.startswith(f'c{cylinder}-')})
rows=[]
for identity,world in neutral.items():
 old=occ[identity];local=b.Pos(*old['position_cad_mm'])*b.Rot(*old.get('rotation_cad_deg',[0,0,0]))
 parent=rawposes[identity]*local.inverse();newlocal=parent.inverse()*world
 after=copy.deepcopy(old);after['position_cad_mm']=list(newlocal.position);after['rotation_cad_deg']=list(newlocal.orientation)
 if after.get('valvetrain'):after['valvetrain']['model']='clockwise-inclined-v1'
 rows.append({'id':identity,'before':old,'after':after})
# Spring bases are unchanged, but require the coordinated motion revision.
for old in m['occurrences']:
 if (old.get('valvetrain') or {}).get('role')=='spring':
  after=copy.deepcopy(old);after['valvetrain']['model']='clockwise-inclined-v1';rows.append({'id':old['id'],'before':old,'after':after})
patch={'status':'CANDIDATE ONLY; requires corrected assets and new runtime','manifest_sha256':sha(manifest),'occurrences':rows,'canonical_modified':False}
patchpath=ROOT/'inventory/engine/clockwise-linkage-pose-patch.json';patchpath.write_text(json.dumps(patch,indent=2)+'\n')
serialized=json.loads(patchpath.read_text());newraw=copy.deepcopy(m);lookup={o['id']:o for o in newraw['occurrences']}
for row in serialized['occurrences']:
 assert lookup[row['id']]==row['before'] and row['before']['parent']==row['after']['parent']
 lookup[row['id']].clear();lookup[row['id']].update(row['after'])
metadata={key:o.get('valvetrain') for key,o in lookup.items()}
for o in newraw['occurrences']:o.pop('valvetrain',None)
rest=transforms(newraw,0)
queries=[(q,x)for q in [0,55,120,246,468,719]for x in [0,-.1]]
requests=[{'q':q,'x':x,'m':metadata[key],'id':key}for q,x in queries for key in neutral if metadata[key]]
js="import{readFileSync}from'node:fs';import{clockwiseOccurrencePose as pose}from'./viewer/engine-clockwise-motion-candidate.js';console.log(JSON.stringify(JSON.parse(readFileSync(0,'utf8')).map(r=>({...r,p:pose(r.q,r.m,r.x)}))));"
answers=json.loads(subprocess.check_output(['node','--input-type=module','-e',js],input=json.dumps(requests),text=True,cwd=ROOT));answer={(r['q'],r['x'],r['id']):r['p']for r in answers}
def matrix(p):
 t=p.wrapped.Transformation();return np.array([[t.Value(i,j)for j in range(1,5)]for i in range(1,4)])
maximum=0;fault=0;checks=0
for q,x in queries:
 target=cam.linkage_frames(m,q,x)
 for key in neutral:
  pose=rest[key]
  if metadata[key]:
   delta=answer[q,x,key];position=np.array(list(pose.position))+delta['translationEngineCad'];rotation=list(pose.orientation);rotation[0]+=math.degrees(delta['rotationXDeltaRad']);pose=b.Pos(*position)*b.Rot(*rotation)
  error=float(np.max(abs(matrix(pose)-matrix(target[key]))));maximum=max(maximum,error);checks+=1
  if key=='c1-intake-pushrod':fault=max(fault,float(np.max(abs(matrix(b.Pos(0,1,0)*pose)-matrix(target[key])))))
assert maximum<1e-8 and fault>.99
assert sha(manifest)==patch['manifest_sha256']
paths=[manifest,patchpath,Path(__file__),ROOT/'viewer/engine-clockwise-motion-candidate.js',ROOT/'cad/engine/cam_clockwise_candidate.py',ROOT/'cad/engine/assembly_math.py']
report={'status':'PASS numeric serialized linkage stage','occurrence_updates':len(rows),'neutral_linkage_frames':len(neutral),'matrix_checks':checks,'maximum_matrix_error':maximum,'wrong_rest_negative_control_mm':fault,'canonical_modified':False,'bindings':{str(p.relative_to(ROOT)):sha(p)for p in paths},'limitations':['Not loaded by legacy runtime','Requires coordinated candidate geometry','Spring height/mesh acceptance separate','No collision or browser claim']}
(ROOT/'inventory/engine/clockwise-linkage-pose-stage-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
