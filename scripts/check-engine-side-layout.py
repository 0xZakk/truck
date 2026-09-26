"""Check source-supported side relationships, not surveyed installation dimensions."""
from pathlib import Path
import json, sys
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())
poses=transforms(m)
o={p['id']:p for p in m['occurrences']}
def y(id):
    return poses[id].position.Y
checks={
 'cam_opposite_manifold_face':y('camshaft')>0,
 'filter_on_cam_side':y('oil-filter-case')>0,
 'pressure_switch_on_cam_side':y('oil-pressure-body')>0,
 'pump_on_cam_side':y('oil-pump-housing')>0,
}
for i in range(1,7):
 for kind in ('intake','exhaust'):
  tag=f'c{i}-{kind}'
  checks[tag+'-pushrod-on-cam-side']=y(tag+'-pushrod')>0
  checks[tag+'-lifter-on-cam-side']=y(tag+'-lifter-body')>0
  checks[tag+'-rocker-between-pushrod-and-valve']=y(tag+'-valve')<y(tag+'-rocker')<y(tag+'-pushrod')
assert all(checks.values()),[k for k,v in checks.items() if not v]
defs={d['id']:d for d in m['definitions']}
def placed(id):
 return b.import_step(ROOT/defs[o[id]['definition']]['step'].lstrip('/')).moved(poses[id])
block=placed('block');head=placed('cylinder-head')
assert placed('efi-lower-intake').center().Y<0, 'Manifold belongs opposite the cam side'
probes=[]
for i in range(1,7):
 for kind in ('intake','exhaust'):
  center=poses[f'c{i}-{kind}-pushrod'].position
  for label,target,z,h in [('block',block,210,70),('head',head,292,65)]:
   probe=b.Pos(center.X,center.Y,z)*b.Cylinder(3.8,h)
   overlap=target.intersect(probe)
   volume=sum(s.volume for s in overlap.solids()) if overlap else 0
   assert volume<.01,(i,kind,label,volume)
   probes.append(f'{i}-{kind}-{label}')
report={'source':'ford-engine-side-layout','checks':checks,'pushrod_passage_probes':probes,'verified_production_fit':False,
 'limits':'Relative side relationships at reference pose only. Solid clearance, port connectivity and measured datums require separate verification.'}
(ROOT/'inventory/engine/side-layout-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('Side relationships verified:',len(checks),'checks; production fit remains unverified')
