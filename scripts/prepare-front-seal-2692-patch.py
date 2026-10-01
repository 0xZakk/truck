"""Create seal replacement proposal without editing either live or staged engine."""
from pathlib import Path
import json,hashlib,copy,sys
import numpy as np,trimesh
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_math import transforms
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
M=R/'inventory/engine/full-assembly.json';S=R/'inventory/engine/front-seal-2692-stage-validation.json';m=json.loads(M.read_text());stage=json.loads(S.read_text());defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};poses=transforms(m)
lessons=json.loads((R/'inventory/engine/front-seal-2692-learning-candidate.json').read_text());sources=json.loads((R/'inventory/engine/front-seal-2692-learning-sources.json').read_text())
patch={'scope':'Candidate replacement proposal only; new coordinated cover is preserved','manifest_sha256':sha(M),'definitions':[],'occurrences':[],'assemblies':[],'navigation_aliases':stage['required_navigation_alias'],'learning_additions':lessons,'source_additions':sources,'requirements':['Do not apply before coordinated cover/core/hub installation','Honor explicit removal plus legacy front-seal assembly alias','Old single seal and free-case state must not coexist as installed parts']};checks=[];bindings={str(p.relative_to(R)):sha(p)for p in [M,S,Path(__file__),R/'inventory/engine/front-seal-2692-learning-candidate.json',R/'inventory/engine/front-seal-2692-learning-sources.json']}
assembly=copy.deepcopy(stage['proposed_seal_assembly']);assembly.update(name='Front crankshaft seal · three-part study',function='Stationary case and sealing element surround the rotating damper hub; garter spring supports the lip. Internal construction remains inferred.')
patch['assemblies'].append({'id':assembly['id'],'before':None,'after':assembly})
names={'front-seal-case':'Front seal metal case','front-seal-elastomer':'Front seal elastomer lip','front-seal-garter-spring':'Front seal garter spring'}
colors={'front-seal-case':'#929aa0','front-seal-elastomer':'#353435','front-seal-garter-spring':'#c2c6c9'}
for row in stage['parts']:
 identity=row['id']
 if identity=='timing-cover':continue
 sp=R/row['step'];gp=R/row['glb'];assert sha(sp)==row['step_sha256'] and sha(gp)==row['glb_sha256'];bindings[row['step']]=sha(sp);bindings[row['glb']]=sha(gp)
 shape=b.import_step(sp);mesh=trimesh.load(gp,force='mesh');old=defs.get(identity)
 if old:after=copy.deepcopy(old)
 else:
  after={'id':identity,'name':names[identity],'function':lessons[identity]['summary'],'system':'closures','color':colors[identity],'step':'/cad/engine/generated/'+identity+'.step','glb':'/models/engine/'+identity+'.glb','sources':lessons[identity]['sources'],'dimension_claims':[],'unresolved':[lessons[identity]['limits']]}
 after.update(volume_mm3=shape.volume,solid_count=len(shape.solids()),triangle_count=len(mesh.faces),geometry_status='candidate')
 patch['definitions'].append({'id':identity,'before':old,'after':after,'copy_assets':{k:{'from':row[k],'to':after[k].lstrip('/'),'sha256':row[k+'_sha256']}for k in ['step','glb']}})
 if identity!='damper-hub':
  o=copy.deepcopy(row['proposed_occurrence']);o.update(name=names[identity],function=after['function'],explode_cad_mm=[90+30*len(patch['occurrences']),0,0]);patch['occurrences'].append({'id':identity,'before':None,'after':o})
 pose=poses['damper-hub' if identity=='damper-hub' else 'front-seal'];world=pose*shape;bb=world.bounding_box();t=pose.wrapped.Transformation();rot=np.array([[t.Value(i,j)for j in range(1,4)]for i in range(1,4)]);offset=np.array([t.Value(i,4)for i in range(1,4)]);v=(mesh.vertices[:,[0,2,1]]*[1,-1,1]*1000)@rot.T+offset
 error=float(np.max(abs(np.array([v.min(0),v.max(0)])-np.array([list(bb.min),list(bb.max)]))));assert error<.025
 checks.append({'id':identity,'world_bounds_error_mm':error})
for group,lookup in [('definitions',defs),('occurrences',occ)]:patch[group].append({'id':'front-seal','before':lookup['front-seal'],'after':None})
# The replacement keeps the coordinated cover, whose front seal region is unchanged.
oldpath=R/'cad/engine/generated/front-seal-2692-candidate/cover.step';newpath=R/'cad/engine/generated/timing-pan21-lateral-candidate/cover.step'
old=b.import_step(oldpath);new=b.import_step(newpath)
mask=b.Solid.make_cylinder(43,31,b.Plane(origin=(405,0,0),z_dir=(1,0,0)))
# Clipping both coincident solids first produced a retained invalid Boolean
# witness equal to the entire clipped volume. Fullshape delta first yields
# ten localized pieces, all disjoint from the seal mask even by simple bounds.
proofpath=R/'inventory/engine/front-seal-cover-full-delta-validation.json'
proof=json.loads(proofpath.read_text())
for path,h in proof['bindings'].items():assert sha(R/path)==h,path
for row in proof['rows']:
 for piece in row['parts']:
  lo,hi=piece['bounds_mm']
  nearest=[max(lo[i],0,-hi[i]) for i in [1,2]]
  disjoint=hi[0]<405 or lo[0]>436 or sum(v*v for v in nearest)>43**2
  assert disjoint and piece['seal_region_intersection_mm3']<1e-5
removed=proof['rows'][0]['seal_region_intersection_mm3'];added=proof['rows'][1]['seal_region_intersection_mm3']
bindings[str(proofpath.relative_to(R))]=sha(proofpath)
for path in [oldpath,newpath]:bindings[str(path.relative_to(R))]=sha(path)
P=R/'inventory/engine/front-seal-2692-composition-patch.json';P.write_text(json.dumps(patch,indent=2)+'\n')
report={'status':'PASS bounded seal proposal; not applied','world_mesh_checks':checks,'coordinated_cover_seal_region_removed_mm3':removed,'coordinated_cover_seal_region_added_mm3':added,'deleted_legacy_occurrences':1,'new_physical_seal_parts':3,'canonical_modified':False,'patch_sha256':sha(P),'bindings':bindings,'limits':['Guarded proposal with removals/alias requires future composer support','No full assembly/browser acceptance','Estimated seal internals and datum remain as recorded']}
(R/'inventory/engine/front-seal-2692-composition-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status'],checks,removed,added)
