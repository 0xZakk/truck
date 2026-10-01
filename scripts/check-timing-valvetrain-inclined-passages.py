#!/usr/bin/env python3
"""Exact revised stack support and independent sampled section controls."""
from pathlib import Path
import json,hashlib,sys,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import timing_valvetrain_inclined_candidate as c
OUT=ROOT/'cad/engine/generated/timing-valvetrain-inclined-candidate';OUT.mkdir(parents=True,exist_ok=True)
REPORT=ROOT/'inventory/engine/timing-valvetrain-inclined-passages-validation.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in m['definitions']};frames=c.poses(m)
paths={'block':ROOT/'cad/engine/generated/timing-block-support-machining-candidate/block.step','cylinder-head':OUT/'cylinder-head.step','head-gasket':ROOT/defs['head-gasket']['step'].lstrip('/'),'pushrod':ROOT/defs['pushrod']['step'].lstrip('/')}
assert sha(paths['block'])=='2880d7873e14c8407d40b219d06753be554c069db51da3bdf2ef300724544cfb'
watch=[Path(__file__),Path(c.__file__),ROOT/'cad/engine/timing_valvetrain_inclined_hypothesis.py',ROOT/'inventory/engine/full-assembly.json']+list(paths.values())
r={'status':'RUNNING','inputs':{str(p.relative_to(ROOT)):sha(p) for p in watch},'exports':{},'support':[],'sections':[],'failures':[]}
def save():REPORT.write_text(json.dumps(r,indent=2)+'\n')
save()
oldblock=frames['block']*b.import_step(paths['block']);oldgasket=frames['head-gasket']*b.import_step(paths['head-gasket']);head=frames['cylinder-head']*b.import_step(paths['cylinder-head'])
block=c.block_adapter(oldblock,m);print('block built',block.is_valid,len(block.solids()),flush=True)
gasket=c.gasket_adapter(oldgasket,m);print('gasket built',gasket.is_valid,len(gasket.solids()),flush=True)
blockmask=b.Compound(children=[b.Pos(x,c.numeric.LOWER_Y,249)*b.Cylinder(13.124565,10) for _,_,x in c.stations(m)])
gasketmask=b.Compound(children=[c.passage(x,254,255.5) for _,_,x in c.stations(m)])
r['changes']={'block_removed_outside_mask_mm3':vol(b.Compound(children=list(oldblock.cut(block).solids())).cut(blockmask)),'block_added_outside_mask_mm3':vol(block.cut(oldblock).cut(blockmask)),'gasket_added_mm3':vol(gasket.cut(oldgasket)),'gasket_removed_outside_mask_mm3':vol(b.Compound(children=list(oldgasket.cut(gasket).solids())).cut(gasketmask))}
assert max(r['changes'].values())<1e-5,r['changes']
r['block_removed_inside_mask_mm3']=vol(oldblock.cut(block))
for key,q in [('block',block),('head-gasket',gasket)]:
 assert q.is_valid and len(q.solids())==1
 p=OUT/(key+'.step');b.export_step(frames[key].inverse()*q,p);again=frames[key]*b.import_step(p)
 error=abs(vol(q)-vol(again));assert again.is_valid and len(again.solids())==1 and error<.01
 r['exports'][key]={'sha256':sha(p),'volume_error_mm3':error,'solid_count':len(again.solids()),'valid':again.is_valid}
 if key=='block':block=again
 else:gasket=again
save()
for i,kind,x in c.stations(m):
 tag=f'c{i}-{kind}';row={'id':tag}
 for lo,hi,key,q in [(244.001,253.999,'block',block),(254.001,255.499,'gasket',gasket),(255.501,303.999,'head',head)]:
  probe=c.passage(x,lo,hi)
  overlap=vol(probe.intersect(q))
  row[key+'_passage_probe_overlap_mm3']=overlap
  if overlap>.1:r['failures'].append({'aperture_occupied':tag,'neighbor':key,'overlap_mm3':overlap})
 # Two-mm band around the UNION outline, not around one overlapping circle.
 for z,key,q in [(253.995,'block',block),(254.005,'gasket-bottom',gasket),(255.495,'gasket-top',gasket),(255.505,'head',head)]:
  band=c.passage(x,z-.005,z+.005,2).cut(c.passage(x,z-.015,z+.015))
  row[key]={'probe_mm3':vol(band),'missing_mm3':vol(band.cut(q))}
  if row[key]['missing_mm3']>1e-5:r['failures'].append({'support':tag,'face':key,'missing_mm3':row[key]['missing_mm3']})
 # Independent center-line point grid rejects occupied passage even if OCC
 # Boolean common reports a false zero. Tube interior, not boundary samples.
 # Numeric report separately covers all1442 phases/branch with sufficient bound.
 for theta in [0,90,180,270,360,450,540,630,720]:
  for axial in [0,-.1]:
   state=c.contract.state(theta,i,kind,axial)
   for z,key,q in [(249,'block',block),(254.75,'gasket',gasket),(280,'head',head),(303.9,'head',head),(320,'head',head)]:
    y,half=c.numeric.section_y(state,z)
    for dx,dy in [(0,0),(3,0),(-3,0),(0,3),(0,-3)]:
     if q.is_inside((x+dx,y+dy,z)):
      r['failures'].append({'interior_occupied':tag,'theta':theta,'axial':axial,'z':z,'offset':[dx,dy]})
 r['support'].append(row);print(tag,'support',row,flush=True);save()
# Sensitivity: old R6 lower passage contains strict rod interior at +Y radius3.8.
i,kind,x=c.stations(m)[0];s=c.contract.state(318,i,kind);y,_=c.numeric.section_y(s,254.75)
r['negative_controls']={'old_gasket_contains_tube_interior':oldgasket.is_inside((x,y+3.8,254.75))}
assert r['negative_controls']['old_gasket_contains_tube_interior']
# Old through-guide demonstrably cannot support the new union-outline band.
band=c.passage(x,253.99,254,2).cut(c.passage(x,253.98,254.01))
r['negative_controls']['old_block_missing_support_mm3']=vol(band.cut(oldblock));assert r['negative_controls']['old_block_missing_support_mm3']>.1
assert all(sha(ROOT/p)==h for p,h in r['inputs'].items())
r['status']='FAIL interface gates' if r['failures'] else 'PASS exact scoped stack support and independent sampled interior controls'
r['limits']=['Estimated geometry, no production gasket/fluids-network certification.','Independent interior controls sample tube interior and are not exhaustive; analytic section containment report supplies broader phase coverage.','Browser, full neighbor sweep, fluid flow, staged disassembly and source comparison NOT RUN.','Block one-solid result establishes connectivity, not structural capacity.']
save();print(r['status'],flush=True)
