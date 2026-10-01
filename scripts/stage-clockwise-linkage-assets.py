"""Bind three reviewed local assets to the serialized neutral linkage stage."""
from pathlib import Path
import sys,json,hashlib,copy
import numpy as np,trimesh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from assembly_math import transforms
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
M=ROOT/'inventory/engine/full-assembly.json';P=ROOT/'inventory/engine/clockwise-linkage-pose-patch.json'
m=json.loads(M.read_text());patch=json.loads(P.read_text());assert sha(M)==patch['manifest_sha256']
new=copy.deepcopy(m);occ={o['id']:o for o in new['occurrences']}
for row in patch['occurrences']:
 assert occ[row['id']]==row['before'];occ[row['id']].clear();occ[row['id']].update(row['after'])
for o in new['occurrences']:o.pop('valvetrain',None)
poses=transforms(new,0);defs={d['id']:d for d in m['definitions']};rows=[];checks=[]
inputs={str(p.relative_to(ROOT)):sha(p) for p in [M,P,Path(__file__),ROOT/'cad/engine/assembly_math.py']}
for identity,folder in [('cylinder-head','timing-valvetrain-inclined-candidate'),('head-gasket','timing-valvetrain-inclined-candidate'),('rocker-arm','timing-rocker-crest-candidate')]:
 sp=ROOT/'cad/engine/generated'/folder/(identity+'.step');gp=sp.with_suffix('.glb')
 inputs[str(sp.relative_to(ROOT))]=sha(sp);inputs[str(gp.relative_to(ROOT))]=sha(gp)
 shape=b.import_step(sp);mesh=trimesh.load(gp,force='mesh');assert shape.is_valid and len(shape.solids())==1
 assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume>0
 cad=mesh.vertices[:,[0,2,1]]*[1,-1,1]*1000
 for o in m['occurrences']:
  if o['definition']!=identity:continue
  t=poses[o['id']].wrapped.Transformation();rot=np.array([[t.Value(i,j)for j in range(1,4)]for i in range(1,4)]);offset=np.array([t.Value(i,4)for i in range(1,4)]);v=cad@rot.T+offset
  bb=(poses[o['id']]*shape).bounding_box();error=float(np.max(abs(np.array([v.min(0),v.max(0)])-np.array([list(bb.min),list(bb.max)]))))
  assert error<.025;checks.append({'id':o['id'],'world_bounds_error_mm':error})
 after=copy.deepcopy(defs[identity]);after.update(volume_mm3=shape.volume,solid_count=1,triangle_count=len(mesh.faces),geometry_status='provisional')
 rows.append({'id':identity,'before':defs[identity],'after':after,'asset_frame':'Existing definition-local CAD frame; no extra world offset','copy_assets':{'step':{'from':str(sp.relative_to(ROOT)),'to':after['step'].lstrip('/'),'sha256':sha(sp)},'glb':{'from':str(gp.relative_to(ROOT)),'to':after['glb'].lstrip('/'),'sha256':sha(gp)}}})
assert len(checks)==14
out={'status':'CANDIDATE serialized asset proposal; not installed','manifest_sha256':sha(M),'pose_patch_sha256':sha(P),'definitions':rows,'world_mesh_checks':checks,'bindings':inputs,'canonical_modified':False,'limits':['Neutral rest geometry bounds only, not motion collisions','Requires all coordinated lower block/core/drive updates','Geometry remains source-qualified estimates, not OEM-certified','Browser NOT RUN']}
(ROOT/'inventory/engine/clockwise-linkage-asset-patch.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',len(rows),'definition proposals;',len(checks),'rest-world bounds checks; max',max(r['world_bounds_error_mm'] for r in checks))
