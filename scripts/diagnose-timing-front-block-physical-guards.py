from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
b.SkipClean.clean=False
from cad_metrics import solid_volume
from assembly_math import transforms
import accessory_brackets as accessory
import water_pump_joint_candidate as pump
OUT=ROOT/'cad/engine/generated/timing-front-block-adapter-candidate'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q is not None and getattr(q,'wrapped',True) is not None else 0.
def norm(q):return b.Compound(children=list(q)) if isinstance(q,b.ShapeList) else q
def bounds(q):
 if q is None or not q.solids():return None
 bb=q.bounding_box();return [list(bb.min),list(bb.max)]
paths=[OUT/'block.step',ROOT/'cad/engine/generated/timing-block-combined-candidate/block.step'];q=b.import_step(paths[0]);old=b.import_step(paths[1]);added=norm(q.cut(old));removed=norm(old.cut(q));rows=[]
physical={'accessory-entire-radius12-boss':accessory.axial(12,24,(361,90,220)),'accessory-radius5.2-socket':accessory.axial(5.2,17,(365.5,90,220)),'pump-actual-radius59-fluid-opening':pump.cx(59,359.5,374,-32,170),'pump-actual-fifth-passage':pump.cx(6.5,359.5,374,pump.EXTRA[0]-32,pump.EXTRA[1]+170)}
mf=ROOT/'inventory/engine/full-assembly.json';m=json.loads(mf.read_text());poses=transforms(m);occ={v['id']:v for v in m['occurrences']};defs={v['id']:v for v in m['definitions']};paths.append(mf)
for name in ['water-pump-gasket','water-pump-housing','power-steering-ac-bracket']:
 if name not in occ:continue
 p=ROOT/defs[occ[name]['definition']]['step'].lstrip('/');paths.append(p);n=poses[name]*b.import_step(p);physical['actual-'+name]=n
 if name=='water-pump-gasket':physical['actual-pump-gasket-2mm-rear-backing']=b.Pos(-2,0,0)*n
for name,p in physical.items():
 a=vol(added.intersect(p));d=vol(removed.intersect(p));row={'name':name,'added_mm3':a,'removed_mm3':d,'candidate_overlap_mm3':vol(q.intersect(p)),'changed_bounds_mm':bounds(added.intersect(p))};rows.append(row);print(row,flush=True)
broad={
'accessory-broad-addition':added.intersect(accessory.axial(13,26,(361,90,220))),
'pump-chamber-wall-addition':added.intersect(pump.cx(61,357.5,376,-32,170))}
broadrows=[]
for name,p in broad.items():
 item={'name':name,'volume_mm3':vol(p),'bounds_mm':bounds(p),'distance_actual_accessory_boss_mm':p.distance_to(physical['accessory-entire-radius12-boss']),'distance_actual_pump_fluid_opening_mm':p.distance_to(physical['pump-actual-radius59-fluid-opening'])};broadrows.append(item);print(item,flush=True)
 if p.solids():b.export_step(p,OUT/(name+'.step'))
for mod in [accessory,pump]:paths.append(Path(mod.__file__))
paths.append(Path(__file__));r={'status':'SUPPLEMENTAL PHYSICAL DIAGNOSIS; original broadguard failures retained','input_sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths},'physical_interfaces':rows,'broad_changed_regions':broadrows,'limits':['No threshold changed','Addedmaterial in broadguard remains explicitly reported','Dry/strength/production clearance not established by modeldistance']}
(ROOT/'inventory/engine/timing-front-block-physical-guard-diagnosis.json').write_text(json.dumps(r,indent=2)+'\n')
