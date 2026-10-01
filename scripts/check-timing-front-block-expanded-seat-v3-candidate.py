from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,numpy as np,trimesh
b.SkipClean.clean=False
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import timing_front_block_expanded_seat_v3_candidate as c
import timing_block_axis_feature_candidate as masks
import timing_block_support_machining_candidate as journals
import water_pump_joint_candidate as pump
import cam_retention as retention
from assembly_math import transforms
OUT=ROOT/'cad/engine/generated/timing-front-block-expanded-seat-v3-candidate';OUT.mkdir(exist_ok=True)
refinements=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(q):
 if q is None or getattr(q,'wrapped',True) is None:return 0.
 if isinstance(q,b.ShapeList):return sum(vol(x) for x in q)
 total=0.
 for s in q.solids():
  for precision in [1e-9,1e-11,1e-13]:
   props=GProp_GProps();err=BRepGProp.VolumeProperties_s(s.wrapped,props,precision,True,False)
   if err<=1e-7:
    if precision<1e-9:refinements.append({'requested_precision':precision,'reported_error':err})
    total+=abs(props.Mass());break
  else:raise ValueError(f'Strict volume integration failed: {err}')
 return total
q,d=c.build();print('built',q.is_valid,len(q.solids()),flush=True)
for name,s in [('block',q)]:b.export_step(s,OUT/(name+'.step'))
assert q.is_valid and len(q.solids())==1,'Invalid/disconnected candidate'
old=d['frozen'];added=c.norm(q.cut(old));removed=c.norm(old.cut(q));allowed=[d['socket_cavity'],d['support'],c.previous.regions()['below-new-seat'],d['masks']['below-new-seat']];outside_added=added;outside_removed=removed
for mask in allowed:outside_added=c.norm(outside_added.cut(mask));outside_removed=c.norm(outside_removed.cut(mask))
checks={};guards,spec=masks.protected_masks();guards={k:v for k,v in guards.items() if k.startswith(('main-','water-','accessory-front'))}
for i,s in journals.backing_shells().items():guards[f'cam-bearing-backing-{i}']=s
for i,(x,y,z) in enumerate(c.old.STATIONS,1):
 if i not in c.ownership.RELOCATIONS:guards[f'active-pan-interface-{i}']=b.Pos(x,y)*c.old.cylinder(12,z+7.6,z+25)
for i,(y,z) in enumerate(pump.MOUNTING,1):guards[f'pump-entire-mount-{i}']=pump.cx(10,350,373,y-32,z+170)
guards['pump-chamber-wall']=pump.cx(61,357.5,376,-32,170);guards['pump-fifth-passage-wall']=pump.cx(8.5,357.5,376,pump.EXTRA[0]-32,pump.EXTRA[1]+170)
frame=b.Pos(*journals.DELTA)*retention.MOUNT
guards['cam-thrust-seat-backing']=frame*(b.Pos(0,0,-2)*retention.plate_shape())
for i,x in enumerate(retention.BOLT_STATIONS,1):guards[f'cam-thrust-socket-wall-{i}']=frame*(b.Pos(x,0,-6)*b.Cylinder(6.05,12.2))
guards['deck-244-254']=b.Pos(0,0,249)*b.Box(1500,1000,10)
feet=ROOT/'cad/engine/generated/timing-pump-foot-faceted-candidate'
for i in [0,1]:guards[f'faceted-foot-{i}']=b.import_step(feet/f'support-{i}.step')
guards['rear-through-300']=b.Pos(-600,0,0)*b.Box(1800,1000,1000)
guards['front-from-365']=c.norm((b.Pos(865,0,0)*b.Box(1000,1000,1000)).cut(d['socket_cavity']))
for n,g in d['socket_guards'].items():guards[f'complete-female-socket-{n}-outside-intended-void']=c.norm(c.norm(g.cut(d['socket_cavity'])).cut(c.seat.transition_below_seat()))
rows=[]
for name,g in guards.items():
 a=vol(added.intersect(g));r=vol(removed.intersect(g));row={'name':name,'added_mm3':a,'removed_mm3':r,'unchanged':a+r<1e-5};rows.append(row)
 if not row['unchanged']:print('GUARD',row,flush=True)
print('guards finished',flush=True)
manifest=ROOT/'inventory/engine/full-assembly.json';m=json.loads(manifest.read_text());poses=transforms(m);defs={p['id']:p for p in m['definitions']};occ={p['id']:p for p in m['occurrences']};paths=[c.BASE,c.FROZEN,c.LAND,manifest,*[feet/f'support-{i}.step' for i in [0,1]]]
neighbors={}
for name in ['cover','main-gasket','pan-gasket','pan','front-terminal-sealant']:
 folder='timing-pan-expanded-seat-v2-candidate' if name in ['pan','pan-gasket'] else 'timing-cover-attachment-v2'
 p=ROOT/'cad/engine/generated'/folder/(name+'.step');paths.append(p);neighbors[name]=b.import_step(p)
male_path=ROOT/'cad/engine/generated/pan-fastener-thread-candidate/pan-screw.step';female_path=male_path.parent/'female-test-coupon.step';paths.extend([male_path,female_path]);male=b.import_step(male_path);female=b.Pos(*c.ownership.RELOCATIONS[20])*b.import_step(female_path)
for n in [10,20]:neighbors[f'actual-pan-male-{n}']=b.Pos(*c.ownership.RELOCATIONS[n])*male
for name in ['cam-thrust-plate','cam-thrust-bolt-1','cam-thrust-bolt-2','cam-gear-spacer','camshaft','crank-timing-gear','cam-timing-gear']+[f'cam-bearing-{i}' for i in range(1,5)]:
 p=ROOT/'cad/engine/generated/timing-thrust-land-candidate'/(name+'.step');paths.append(p);neighbors[name]=b.import_step(p)
for name in ['water-pump-gasket','water-pump-housing','water-pump-impeller','water-pump-shaft','oil-pump-housing','oil-pump-mount-bolt-1','oil-pump-mount-bolt-2']:
 p=ROOT/defs[occ[name]['definition']]['step'].lstrip('/');paths.append(p);neighbors[name]=poses[name]*b.import_step(p)
 if name.startswith('oil-pump'):neighbors[name]=b.Pos(*journals.DELTA)*neighbors[name]
pairs=[]
for name,n in neighbors.items():
 row={'name':name,'overlap_mm3':vol(q.intersect(n)),'distance_mm':q.distance_to(n)};row['clear']=row['overlap_mm3']<1e-5;pairs.append(row);print(row,flush=True)
rt=b.import_step(OUT/'block.step');diff=vol(q.cut(rt))+vol(rt.cut(q));mesh_error=None
try:
 v,f=q.tessellate(.12,.15);v=np.array([tuple(p) for p in v]);mesh=trimesh.Trimesh(v[:,[0,2,1]]*[1,1,-1]/1000,np.array(f));mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices();mesh.export(OUT/'block.glb');back=trimesh.load(OUT/'block.glb',force='mesh');back.merge_vertices(digits_vertex=8);vv=np.asarray(back.vertices)[:,[0,2,1]]*[1,-1,1]*1000;bb=q.bounding_box();err=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([list(bb.min),list(bb.max)]))));watertight=back.is_watertight
except Exception as exc:mesh_error=repr(exc);err=None;watertight=False
for mod in list(sys.modules.values()):
 p=Path(getattr(mod,'__file__','') or '')
 if p.is_file() and p.is_relative_to(ROOT/'cad/engine') and p.suffix=='.py':paths.append(p)
paths.append(Path(__file__))
r={'status':'CANDIDATE; scoped gates below','input_sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths},'cad_valid':q.is_valid,'solid_count':len(q.solids()),'step_valid':rt.is_valid,'step_difference_mm3':diff,'mesh_watertight':watertight,'mesh_error':mesh_error,'mesh_bounds_error_mm':err,'added_mm3':vol(added),'removed_mm3':vol(removed),'added_outside_declared_mm3':vol(outside_added),'removed_outside_declared_mm3':vol(outside_removed),'source_female_missing_mm3':vol(female.cut(q)),'support_height_estimate_mm':c.SUPPORT_HEIGHT,'gasket_backing_missing_mm3':vol(c.seat.clip_x(c.seat.band(0,.02,'gasket',True),300,365).cut(q)),'protected_interfaces':rows,'neighbors':pairs,'future_land_missing_mm3':vol(d['land'].cut(q)),'future_land_missing_outside_transition_mm3':vol(c.norm(d['land'].cut(q)).cut(c.seat.transition_below_seat())),'intended_socket_cavity_filled_mm3':vol(q.intersect(d['socket_cavity'])),'quadrature_refinements':refinements,'limits':['Estimated sourceboundary andretired5socket restoration; notfactoryspec','BrowserNOTRUN; no canonicalinstallation','Retention, contact,sealingcontinuity stillrequirefurther scopedreview'],'artifacts':{p.name:sha(p) for p in OUT.glob('*') if p.suffix in ['.step','.glb']}}
r['gates']={'cad':r['cad_valid'] and r['solid_count']==1 and r['step_valid'] and diff<1e-5,'mesh':watertight and err<.15,'bounded_material':r['added_outside_declared_mm3']+r['removed_outside_declared_mm3']<1e-5,'protected':all(x['unchanged'] for x in rows),'neighbors':all(x['clear'] for x in pairs),'land_retained_outside_transition':r['future_land_missing_outside_transition_mm3']<1e-5,'socket_void':r['intended_socket_cavity_filled_mm3']<1e-5 and r['source_female_missing_mm3']<1e-5,'gasket_backing':r['gasket_backing_missing_mm3']<1e-5};r['local_status']='PASS' if all(r['gates'].values()) else 'FAIL'
(ROOT/'inventory/engine/timing-front-block-expanded-seat-v3-validation.json').write_text(json.dumps(r,indent=2)+'\n');print('FINAL',r['gates'],flush=True)
assert all(r['gates'].values()),r['gates']
