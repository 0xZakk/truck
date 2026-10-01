from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import timing_pan21_lateral_candidate as c
OUT=ROOT/'cad/engine/generated/timing-pan21-lateral-candidate';OUT.mkdir(exist_ok=True)
errors={}
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
parts,d=c.build();print('built',flush=True);r={'validity':{n:{'valid':s.is_valid,'solids':len(s.solids())}for n,s in parts.items()},'checks':{},'measurement_errors':errors};q=r['checks'];cover=parts['cover'];pan=parts['pan'];gasket=parts['pan-gasket']
for n,s in parts.items():
 if s.is_valid and len(s.solids())==1:b.export_step(s,OUT/(n+'.step'))
main1=b.import_step(c.COVER.with_name('main-cover-screw-1.step'));loc=b.Pos(*c.NEW)
wall=loc*(c.owner.cz(6.2,7.8,23.6)-c.owner.cz(4.17,7.7,23.7));floor=loc*c.owner.cz(4.15,22.6,23.6)
for key,s in {'main1_head_cover':cover.intersect(main1),'main1_access_cover':cover.intersect(d['access']),'pan21_male_cover':cover.intersect(d['male']),'pan21_male_pan':pan.intersect(d['male']),'pan21_male_gasket':gasket.intersect(d['male']),'pan21_washer_pan':pan.intersect(d['washer']),'pan21_washer_cover':cover.intersect(d['washer']),'pan21_female_missing':d['female'].cut(cover),'pan21_intended_void_filled':cover.intersect(d['cavity']),'pan21_wall_missing':wall.cut(cover),'pan21_floor_missing':floor.cut(cover),'cover_pan':cover.intersect(pan),'cover_gasket':cover.intersect(gasket),'pan_gasket':pan.intersect(gasket)}.items():q[key]=m(key,s);print(key,q[key],flush=True)
r['initial_status']='PASS'if all(v is not None and v<1e-5 for v in q.values())and all(v['valid']and v['solids']==1 for v in r['validity'].values())else'FAIL'
r['inputs_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [c.COVER,c.PAN,c.GASKET,c.FEMALE,c.MALE,c.WASHER,Path(c.__file__),Path(__file__)]};r['artifacts_sha256']={p.name:hashlib.sha256(p.read_bytes()).hexdigest()for p in OUT.glob('*.step')};r['not_run']=['full25 hardware/contact/BOM, changed-material locality, wet connectivity, moving core neighbors, mesh/render pending initial gates','browser/installation/factory/strength']
(ROOT/'inventory/engine/timing-pan21-lateral-candidate-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['initial_status'])
