"""Actual corrected neighbors and conservative all-angle seven-support bounds."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import timing_cover_seven_fastener_candidate as c
from assembly_math import transforms
import timing_block_support_machining_candidate as journals
newpath=ROOT/'cad/engine/generated/timing-cover-seven-fastener-candidate/block.step';new=b.import_step(newpath);old=b.import_step(c.BLOCK);supports=[c.front.c.cx(c.SUPPORT_RADIUS,c.SUPPORT_BACK,373,y,z)for y,z in c.AXES];paths=[newpath,c.BLOCK,Path(c.__file__),Path(__file__)];errors={};rows=[]
def vol(s):
 if s is None:return 0.
 if isinstance(s,b.ShapeList):return sum(vol(t)for t in s)
 v=0.
 for t in s.solids():
  q=GProp_GProps();e=BRepGProp.VolumeProperties_s(t.wrapped,q,1e-9,True,False)
  if e>1e-7:raise ValueError(e)
  v+=abs(q.Mass())
 return v
def m(k,s):
 try:return vol(s)
 except Exception as e:errors[k]=repr(e);return None
prior=ROOT/'inventory/engine/timing-pan21-lateral-neighbors.json';paths.append(prior);pr=json.loads(prior.read_text());neighbors={}
for row in pr['neighbors']:
 p=ROOT/row['part']
 if p==newpath:continue
 paths.append(p);neighbors[str(p.relative_to(ROOT))]=b.import_step(p)
for n in ['cover','pan','pan-gasket']:
 p=ROOT/'cad/engine/generated/timing-pan21-lateral-candidate'/(n+'.step');paths.append(p);neighbors[str(p.relative_to(ROOT))]=b.import_step(p)
manifest=ROOT/'inventory/engine/full-assembly.json';paths.append(manifest);man=json.loads(manifest.read_text());poses=transforms(man);defs={x['id']:x for x in man['definitions']};occ={x['id']:x for x in man['occurrences']}
for name in ['water-pump-gasket','water-pump-housing','water-pump-impeller','water-pump-shaft','oil-pump-housing','oil-pump-mount-bolt-1','oil-pump-mount-bolt-2']:
 p=ROOT/defs[occ[name]['definition']]['step'].lstrip('/');paths.append(p);s=poses[name]*b.import_step(p)
 if name.startswith('oil-pump'):s=b.Pos(*journals.DELTA)*s
 neighbors[name]=s
for name,s in neighbors.items():
 row={'part':name,'new_overlap_mm3':m(name,new.intersect(s)),'old_overlap_mm3':m(name+'old',old.intersect(s))};rows.append(row);print(row,flush=True)
phase=[]
for path in ['cad/engine/generated/crank-clockwise-candidate/crankshaft.step','cad/engine/generated/cam-clockwise-candidate/camshaft.step','cad/engine/generated/timing-coupled-core-candidate/cam-timing-gear.step','cad/engine/generated/timing-coupled-core-candidate/crank-timing-gear.step']:
 s=neighbors[path];local=s.intersect(b.Pos((c.SUPPORT_BACK+373)/2,0,0)*b.Box(373-c.SUPPORT_BACK,1500,1500));axis=(95.1098209901611,76.08785679212888)if 'cam' in Path(path).name else(0.,0.)
 if local is None or not local.solids():phase.append({'part':path,'proof':'Disjoint changed-stock X slab','all_angle_separated':True});continue
 bb=local.bounding_box();radius=max(math.hypot(y-axis[0],z-axis[1])for y in [bb.min.Y,bb.max.Y]for z in [bb.min.Z,bb.max.Z]);gaps=[]
 for n,stock in enumerate(supports,1):
  sb=stock.bounding_box();dy=max(sb.min.Y-axis[0],0,axis[0]-sb.max.Y);dz=max(sb.min.Z-axis[1],0,axis[1]-sb.max.Z);gaps.append({'station':n,'radial_separation_lower_mm':math.hypot(dy,dz)-radius})
 phase.append({'part':path,'axis_yz':axis,'actual_bbox_corner_radius_upper_mm':radius,'support_bounds':gaps,'all_angle_separated':all(x['radial_separation_lower_mm']>0 for x in gaps)})
r={'neighbors':rows,'phase_independent_changed_stock':phase,'errors':errors,'input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths},'limits':['All-angle separation covers new support envelopes only; old block/crank motion limitations remain','Pump/oil pump poses follow bound manifest and existing documented oil-pump shift','Any inherited static overlap remains explicit; this report does not waive it']};r['gates']={'actual_neighbors_clear':all(x['new_overlap_mm3']is not None and x['new_overlap_mm3']<.1 for x in rows),'changed_stock_all_angle':all(x['all_angle_separated']for x in phase),'metrics_verified':not errors};r['status']='PASS bounded neighbors'if all(r['gates'].values())else'FAIL or NOT VERIFIED bounded neighbors';(ROOT/'inventory/engine/timing-seven-block-neighbors.json').write_text(json.dumps(r,indent=2)+'\n');print(r['gates'],flush=True)
