"""Verify actual saved carrier94 geometry against its independently checked candidate."""
import argparse,hashlib,itertools,json,sys
from pathlib import Path
import build123d as cad
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--assembly-root',required=True,type=Path);args=parser.parse_args();ASSEMBLY=args.assembly_root.resolve()
sys.path.insert(0,str(ROOT/'cad/engine'))
import accessory_carrier_1994 as c
from assembly_math import transforms
raw=(ASSEMBLY/'inventory/engine/full-assembly.json').read_bytes();m=json.loads(raw);defs={d['id']:d for d in m['definitions']};occ={o['id']:o for o in m['occurrences']};poses=transforms(m)
source_paths=[Path(c.__file__),ROOT/'cad/engine/accessory_brackets.py',ROOT/'cad/engine/tensioner_arm.py',ROOT/'cad/engine/tensioner_pulley.py',ROOT/'cad/engine/tensioner_engine_support.py',Path(__file__)]
frozen={str(p):p.read_bytes() for p in source_paths};cache={};step_hashes={};failures=[];checks=[]
def volume(shape):return sum(s.volume for s in shape.solids()) if shape else 0

def installed(identifier):
 o=occ[identifier];d=defs[o['definition']];path=ASSEMBLY/d['step'].lstrip('/')
 if path not in cache:
  data=path.read_bytes();step_hashes[str(path)]=hashlib.sha256(data).hexdigest();cache[path]=cad.import_step(path)
 return cache[path].moved(poses[identifier])

def require(condition,message):
 if not condition:failures.append(message);print('FAIL',message,flush=True)

def geometry_error(first,second):return volume(first-second)+volume(second-first)

expected=c.parts();actual={}
for identifier in ('ps-ac-engine-bracket-bolt-1','ps-ac-engine-bracket-bolt-2','tensioner-engine-bracket'):
 require(identifier not in occ,'Obsolete occurrence retained: '+identifier)
for identifier,shape in expected.items():
 if identifier not in occ:require(False,'Missing occurrence: '+identifier);continue
 actual[identifier]=installed(identifier)
 require(actual[identifier].is_valid and len(actual[identifier].solids())==1,'Invalid saved solid: '+identifier)
 delta=geometry_error(actual[identifier],shape);require(delta<=.01,'Saved geometry mismatch: '+identifier+' '+str(delta))
 checks.append({'part':identifier,'symmetric_difference_mm3':delta})
 print('Checked saved geometry',identifier,flush=True)
# A small real displacement must fail the same comparison, not hide behind volume equality.
negative_control=geometry_error(expected['ps-ac-support-bracket'],cad.Pos(.01,0,0)*expected['ps-ac-support-bracket'])
require(negative_control>.01,'Geometry comparator missed0.01mm displacement')
expected_mount=cad.Pos(*c.TENSIONER_POSITION)*cad.Rot(0,90,0)
for identifier in c.tensioner_parts():
 if identifier not in poses:continue
 a=poses[identifier].wrapped.Transformation();b=expected_mount.wrapped.Transformation();delta=max(abs(a.Value(i,j)-b.Value(i,j)) for i in range(1,4) for j in range(1,5))
 require(delta<1e-8,'Tensioner world transform mismatch: '+identifier)
 checks.append({'part':identifier,'transform_max_element_error':delta})
# Validate actual installed receivers without replacing/comparing an entire head
# against the older baseline: unrelated accepted head changes must survive.
boss_material={};probe_results=[]
for identifier,stations,zshift,pad_y,pad_length in [('block',c.BLOCK_STATIONS,0,119.5,31),('cylinder-head',[c.HEAD_SIDE],255.5,117.5,35)]:
 engine=installed(identifier)
 for index,(x,z) in enumerate(stations,1):
  void=c.sideways(4.8,23,x,123,z-zshift).moved(poses[identifier]);floor=c.sideways(4.8,2,x,109,z-zshift).moved(poses[identifier]);pad=c.sideways(14,pad_length,x,pad_y,z-zshift).moved(poses[identifier])
  obstructed=volume(engine.intersect(void));filled=volume(engine.intersect(floor))
  require(obstructed<.01,identifier+' receiver is obstructed')
  require(abs(filled-floor.volume)<.01,identifier+' dry floor is absent')
  material=engine.intersect(pad)
  if material:boss_material[identifier+'-saved-side-boss-'+str(index)]=cad.Compound(material.solids())
  probe_results.append({'part':identifier,'station':index,'obstructed_mm3':obstructed,'floor_volume_mm3':filled,'expected_floor_volume_mm3':floor.volume})
seats=[]
if set(expected)<=set(actual):
 carrier=actual['ps-ac-support-bracket']
 for i in (1,2):
  washer=actual[f'carrier-block-washer-{i}'];nut=actual[f'carrier-block-nut-{i}']
  for name,a,b in [('carrier/washer',carrier,washer),('washer/nut',washer,nut)]:
   distance=a.distance_to(b);require(distance<1e-6,'Unseated '+name+' '+str(i));seats.append({'station':i,'joint':name,'distance_mm':distance})
 for identifier in ('carrier-front-head-bolt-1','carrier-side-head-bolt-2','tensioner-spring-cartridge'):
  distance=carrier.distance_to(actual[identifier]);require(distance<1e-6,'Unseated '+identifier);seats.append({'joint':identifier,'distance_mm':distance})
# Check saved candidates against all current neighbors, including current engine
# definitions. New boss material also gets checked against current internal parts.
bounds={};narrow=0;overlaps=[]
def intersect(a,sa,b,sb):
 global narrow
 for k,s in [(a,sa),(b,sb)]:
  if k not in bounds:bounds[k]=s.bounding_box()
 ba,bb=bounds[a],bounds[b]
 if any(min(getattr(ba.max,v),getattr(bb.max,v))-max(getattr(ba.min,v),getattr(bb.min,v))<=.01 for v in 'XYZ'):return
 narrow+=1;v=volume(sa.intersect(sb))
 if v>.01:overlaps.append({'a':a,'b':b,'volume_mm3':v});print('Overlap',overlaps[-1],flush=True)
for (a,sa),(b,sb) in itertools.combinations(actual.items(),2):intersect(a,sa,b,sb)
for identifier in occ:
 if identifier in actual:continue
 neighbor=installed(identifier)
 for name,shape in {**actual,**boss_material}.items():
  if name.startswith(identifier+'-saved-side-boss-'):continue
  intersect(name,shape,identifier,neighbor)
require(not overlaps,'Saved neighbor intersections detected')
require((ASSEMBLY/'inventory/engine/full-assembly.json').read_bytes()==raw,'Manifest changed during audit')
for path,digest in step_hashes.items():require(hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,'STEP changed: '+path)
for path,data in frozen.items():require(Path(path).read_bytes()==data,'Checker/candidate source changed: '+path)
report={'passed':not failures,'assembly_root':str(ASSEMBLY),'verified_production_fit':False,'manifest_sha256':hashlib.sha256(raw).hexdigest(),'source_sha256':{p:hashlib.sha256(v).hexdigest() for p,v in frozen.items()},'step_sha256':step_hashes,'geometry_and_transform_checks':checks,'geometry_displacement_control_mm3':negative_control,'receiver_probes':probe_results,'joint_seats':seats,'exact_neighbor_intersections':narrow,'overlaps':overlaps,'failures':failures,'limits':c.GAPS}
out=ASSEMBLY/'inventory/engine/accessory-carrier-1994-installed-validation.json';out.write_text(json.dumps(report,indent=2)+'\n');print('RESULT',report['passed'],'checks',narrow,'overlaps',len(overlaps),'report',out,flush=True)
if failures:raise SystemExit(1)
