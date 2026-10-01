#!/usr/bin/env python3
"""Named positive bearing-annulus checks; smooth geometry does not prove preload/threads."""
from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import accessory_psac_carrier_trial1 as src
import accessory_brackets as base
from assembly_clockwise_candidate import transforms
from cad_metrics import solid_volume
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();mp=R/'inventory/engine/corrected-engine-stage-v3.json';ep=R/'inventory/engine/accessory-constrained-layout-envelopes.json';sp=R/'cad/engine/generated/accessory-psac-carrier/trial1-carrier.step';inputs={str(p.relative_to(R)):sha(p)for p in [mp,ep,sp,Path(__file__),Path(src.__file__),R/'cad/engine/assembly_clockwise_candidate.py']};m=json.loads(mp.read_text());t=transforms(m,0,0);ds={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};groups={n:g for g,ids in json.loads(ep.read_text())['moving_occurrence_ownership'].items()for n in ids};cache={'candidate':b.import_step(sp)}
def actual(n):
 if n not in cache:
  p=R/ds[occ[n]['definition']]['step'].lstrip('/');inputs[str(p.relative_to(R))]=sha(p);g=groups.get(n);pose=b.Pos(0,*src.SELECT['posedelta_yz_mm'][g])*t[n]if g else t[n];cache[n]=pose*b.import_step(p)
 return cache[n]
rows=[]
def check(name,axis,face,u,z,ri,ro,low,high):
 if axis=='X':w=base.boss(face-.02,u,z,ro,ri,.02);v=b.Pos(.02,0,0)*w
 else:w=src.old.sideways(ro,.02,u,face-.01,z).cut(src.old.sideways(ri,.04,u,face-.01,z));v=b.Pos(0,.02,0)*w
 rows.append({'name':name,'axis':axis,'face_mm':face,'radii_mm':[ri,ro],'low_owner':low,'high_owner':high,'low_missing_mm3':solid_volume(w.cut(actual(low))),'high_missing_mm3':solid_volume(v.cut(actual(high))),'witness_mm3':solid_volume(w)})
check('front-head clamp','X',385,90,300,5.5,7.8,'candidate','carrier-front-head-bolt-1')
for i,(x,z)in enumerate(src.SIDE):
 if i==2:check('side-head clamp','Y',163,x,z,5.5,8.4,'candidate','carrier-side-head-bolt-2')
 else:
  check('stud washer'+str(i+1),'Y',163,x,z,5.5,11,'candidate','carrier-block-washer-'+str(i+1));check('stud nut'+str(i+1),'Y',165,x,z,5.2,8.4,'carrier-block-washer-'+str(i+1),'carrier-block-nut-'+str(i+1))
for g,ears,ri,ro,prefix in [('PS',src.PS_EARS,4.8,6.7,'ps-bracket-bolt-'),('AC',src.AC_EARS,5.5,7.8,'ac-bracket-bolt-')]:
 for i,(y,z)in enumerate(ears):check(g+' head'+str(i+1),'X',442.56,y,z,ri,ro,'candidate',prefix+str(i+1))
for name,ri,ro,low in [('tensioner arm',8,10.3,'tensioner-moving-arm'),('tensioner sleeve',6,7.9,'tensioner-pivot-sleeve')]:check(name,'X',452.56,*src.PIVOT,ri,ro,low,'tensioner-mounting-bolt')
r={'status':'COMPLETE named bearing annuli only; threads/preload/material/load unverified','rows':rows,'stack_mm':{'front_engine_engagement':14,'side_engine_engagement':20,'side_carrier':28,'side_washer':2,'side_nut':9,'side_stud_tip':2,'PS_ear_insertion':7.8,'AC_ear_insertion':11.8,'accessory_carrier':10,'tensioner_smooth_insertion':14,'tensioner_tip_clearance':2},'inputs':inputs};(R/'inventory/engine/accessory-psac-carrier-clamp-stacks.json').write_text(json.dumps(r,indent=2)+'\n');print(rows)
