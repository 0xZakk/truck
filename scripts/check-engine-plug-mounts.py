"""Check geometric plug/head interfaces, not surveyed production fit."""
from pathlib import Path
import json,sys
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
from plug_mounts import PLUG_Y,PLUG_LOCAL_Z,PLUG_ANGLE,HEAD_WORLD_Z
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());d={x['id']:x for x in m['definitions']};loc=transforms(m)
head=b.import_step(ROOT/d['cylinder-head']['step'].lstrip('/')).moved(loc['cylinder-head'])
assert abs(next(o for o in m['occurrences'] if o['id']=='cylinder-head')['position_cad_mm'][2]-HEAD_WORLD_Z)<1e-9
collisions=[];probes=[]
for i in range(1,7):
 parts=[o for o in m['occurrences'] if o['parent']==f'spark-plug-{i}']
 for o in parts:
  part=b.import_step(ROOT/d[o['definition']]['step'].lstrip('/')).moved(loc[o['id']]);v=head.intersect(part);vol=sum(s.volume for s in v.solids()) if v else 0
  if vol>.1:collisions.append({'part':o['id'],'head_overlap_mm3':vol})
 # A narrow axial path through the modeled bore must open into the firing pocket.
 origin=next(g['position_cad_mm'] for g in m['assemblies'] if g['id']==f'spark-plug-{i}')
 probe=(b.Pos(0,0,-7)*b.Cylinder(.5,22)).moved(b.Pos(*origin)*b.Rot(PLUG_ANGLE,0,0))
 v=head.intersect(probe);vol=sum(s.volume for s in v.solids()) if v else 0
 probes.append({'cylinder':i,'axial_access_blockage_mm3':vol});assert vol<.01
report={'plug_occurrences_checked':54,'head_collisions':collisions,'bore_probes':probes,'verified_production_fit':False,'limits':'Shared provisional mounting datums and simplified bore/seat geometry only; no surveyed casting, thread engagement or coolant-jacket validation.'}
(ROOT/'inventory/engine/plug-mount-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert not collisions
