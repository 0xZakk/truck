"""Actual frozen neighbors and phase-independent added-boss envelope separation."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import timing_pan21_lateral_candidate as c
OUT=ROOT/'cad/engine/generated/timing-pan21-lateral-candidate';cover=b.import_step(OUT/'cover.step');old=b.import_step(c.COVER);stock=c.stock(c.NEW);paths=[OUT/'cover.step',c.COVER];rows=[];errors={}
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
neighbors=[ROOT/'cad/engine/generated/crank-clockwise-candidate/crankshaft.step',ROOT/'cad/engine/generated/cam-clockwise-candidate/camshaft.step']
neighbors +=[p for p in (ROOT/'cad/engine/generated/timing-coupled-core-candidate').glob('*.step')if p.name!='camshaft.step']
neighbors +=[ROOT/'cad/engine/generated/front-seal-2692-candidate'/n for n in ['damper-hub.step','seal-case-installed.step','seal-elastomer.step','seal-garter-spring.step']]
neighbors +=[c.COVER.with_name('block.step'),ROOT/'cad/engine/generated/timing-cover-attachment-v2/main-gasket.step',ROOT/'cad/engine/generated/timing-cover-attachment-v2/front-terminal-sealant.step']
for p in neighbors:
 q=b.import_step(p);paths.append(p);name=str(p.relative_to(ROOT));row={'part':name,'new_cover_overlap_mm3':m(name,cover.intersect(q)),'old_cover_overlap_mm3':m(name+'old',old.intersect(q)),'new_stock_overlap_mm3':m(name+'stock',stock.intersect(q))};rows.append(row);print(row,flush=True)
# Bound all rotation angles using bbox corners of each actual part clipped to the boss X slab.
phase=[]
for p in neighbors[:2]+[p for p in neighbors if p.name in ['cam-timing-gear.step','crank-timing-gear.step']]:
 q=b.import_step(p);local=q.intersect(b.Pos(390,0,0)*b.Box(20,1500,1500));axis=(95.1098209901611,76.08785679212888)if 'cam' in p.name else(0.,0.)
 if local is None or not local.solids():phase.append({'part':str(p.relative_to(ROOT)),'proof':'Disjoint X slab'});continue
 bb=local.bounding_box();radius=max(math.hypot(y-axis[0],z-axis[1])for y in [bb.min.Y,bb.max.Y]for z in [bb.min.Z,bb.max.Z]);sb=stock.bounding_box();dy=max(sb.min.Y-axis[0],0,axis[0]-sb.max.Y);dz=max(sb.min.Z-axis[1],0,axis[1]-sb.max.Z);lower=math.hypot(dy,dz)
 phase.append({'part':str(p.relative_to(ROOT)),'axis_yz':axis,'actual_bbox_corner_radius_upper_mm':radius,'stock_bbox_radial_lower_mm':lower,'separation_lower_mm':lower-radius,'proof':'Conservative radial enclosure for every X-axis rotation; bounds only local new stock'})
r={'neighbors':rows,'new_stock_continuous_rotation_bounds':phase,'errors':errors,'inputs_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in paths+[Path(__file__),Path(c.__file__)]},'limits':['Actual static contacts plus phase-independent new-stock bounds only; no full-cover all-angle claim','Existing intended seal contacts compared with old cover, not silently counted as collision','Full crank/pan motion clearance belongs to separate current motion reports']};(ROOT/'inventory/engine/timing-pan21-lateral-neighbors.json').write_text(json.dumps(r,indent=2)+'\n')
