"""Independent placed outlet/head joint candidate against a frozen full engine."""
import argparse,hashlib,json,sys,tempfile
from pathlib import Path
import build123d as cad
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import coolant_outlet_head_candidate as candidate
p=argparse.ArgumentParser();p.add_argument('--assembly-root',type=Path,required=True);p.add_argument('--installed',action='store_true');a=p.parse_args()
sys.path.insert(0,str(a.assembly_root/'cad/engine'))
from assembly_math import transforms
from valve_layout_integration import occurrence_shape
mp=a.assembly_root/'inventory/engine/full-assembly.json';raw=mp.read_bytes();m=json.loads(raw);poses=transforms(m)
defs={d['id']:d for d in m['definitions']};parts=candidate.parts();cache={};fixed={};changed={};hashes={};installed_checks=[]
source_bytes=Path(candidate.__file__).read_bytes()
def vol(s):return sum(x.volume for x in s.solids()) if s else 0
def difference(sa,sb):return vol(sa-sb)+vol(sb-sa)
mount=cad.Pos(*candidate.POSITION)
for o in m['occurrences']:
 d=o['definition'];identifier=o['id']
 if d not in cache:
  path=a.assembly_root/defs[d]['step'].lstrip('/');hashes[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest();cache[d]=cad.import_step(path)
 shape=occurrence_shape(o,cache[d]).moved(poses[identifier])
 if identifier=='cylinder-head':changed[identifier]=candidate.head_interface(cache[d]).moved(poses[identifier])
 elif d in parts:
  if d=='heater-supply-ect-elbow':changed[identifier]=parts[d]
  elif d=='thermostat-piston':changed[identifier]=mount*cad.Pos(*candidate.THERMOSTAT_POSITION)*parts[d]
  elif d=='coolant-outlet-bolt':
   index=int(identifier.rsplit('-',1)[1])-1;y,z=candidate.HOLES[index]
   changed[identifier]=mount*cad.Pos(0,y,z)*parts[d]
  else:changed[identifier]=mount*parts[d]
 elif o['parent']=='thermostat-assembly':changed[identifier]=mount*cad.Pos(*candidate.THERMOSTAT_POSITION)*cache[d]
 elif o['parent']=='engine-coolant-temperature-assembly':changed[identifier]=cad.Pos(*candidate.ect_position(identifier))*cache[d]
 else:fixed[identifier]=shape
 if a.installed and identifier in changed:
  delta=difference(shape,changed[identifier])
  assert delta<.01,(identifier,'saved geometry/pose differs from candidate',delta)
  installed_checks.append({'id':identifier,'difference_mm3':delta})
  changed[identifier]=shape
print('Loaded',len(changed),'changed parts',len(fixed),'neighbors',flush=True)
roundtrips=[]
with tempfile.TemporaryDirectory(prefix='truck-outlet-head-') as tmp:
 for identifier,shape in changed.items():
  assert shape.is_valid and len(shape.solids())==1,(identifier,len(shape.solids()))
  path=Path(tmp)/(identifier+'.step');cad.export_step(shape,path);r=cad.import_step(path)
  assert r.is_valid and len(r.solids())==1
  assert abs(r.volume-shape.volume)<max(.01,shape.volume*1e-6)
  roundtrips.append(identifier)
allparts={**fixed,**changed};boxes={k:s.bounding_box() for k,s in allparts.items()};checks=0;hits=[]
def check(i,j):
 global checks
 bi,bj=boxes[i],boxes[j]
 if any(min(getattr(bi.max,v),getattr(bj.max,v))-max(getattr(bi.min,v),getattr(bj.min,v))<=.01 for v in 'XYZ'):return
 checks+=1;overlap=vol(allparts[i].intersect(allparts[j]))
 if overlap>.01:
  hits.append({'a':i,'b':j,'volume_mm3':overlap});print('OVERLAP',hits[-1],flush=True)
for i in changed:
 for j in fixed:check(i,j)
keys=list(changed)
for n,i in enumerate(keys):
 for j in keys[n+1:]:check(i,j)
joints=[]
for i,j in [('cylinder-head','coolant-outlet-gasket'),('coolant-outlet-housing','coolant-outlet-gasket'),('cylinder-head','thermostat-frame'),('coolant-outlet-housing','coolant-outlet-bolt-1'),('coolant-outlet-housing','coolant-outlet-bolt-2'),('thermostat-frame','thermostat-piston'),('coolant-outlet-housing','heater-supply-ect-elbow'),('heater-supply-ect-elbow','engine-coolant-temperature-body')]:
 distance=changed[i].distance_to(changed[j]);joints.append({'a':i,'b':j,'distance_mm':distance})
 if distance>1e-6:hits.append({'joint_gap':joints[-1]})
head=changed['cylinder-head'];probes=[]
for name,xyz,metal in [('main-receiver',(350,0,295),False),('secondary-receiver',(360,-42,295),False),('main-rear-floor',(336.5,0,295),True),('main-upper-wall',(345,0,324),True),('rocker-space-above-pocket',(345,0,330),False)]:
 probe=cad.Pos(*xyz)*cad.Box(.5,.5,.5);fraction=vol(head.intersect(probe))/probe.volume
 passed=fraction>.999 if metal else fraction<1e-6
 probes.append({'name':name,'material_fraction':fraction,'expected_metal':metal,'passed':passed})
 if not passed:hits.append({'probe':probes[-1]})
flow_checks=[]
for name,probe in candidate.flow_probes().items():
 obstruction=0
 for identifier,s in changed.items():obstruction+=vol(s.intersect(probe))
 passed=obstruction<1e-6;flow_checks.append({'name':name,'obstruction_mm3':obstruction,'passed':passed})
 if not passed:hits.append({'flow_probe':flow_checks[-1]})
assert candidate.SUPPLY_ENDPOINT==(488,-57,335),'Vehicle boundary changed'
plug=candidate.axial(7,1,(400,-42,295))
flow_negative=vol(plug.intersect(candidate.flow_probes()['outlet-secondary-to-supply']))
assert flow_negative>.01,'Blocked-flow negative control was not detected'
gasket=changed['coolant-outlet-gasket'];negative=vol((cad.Pos(-.2,0,0)*gasket).intersect(head))
assert negative>.01,('penetration negative control',negative)
withdrawal=(cad.Pos(2,0,0)*gasket).distance_to(head);assert withdrawal>1
local=candidate.head_interface(cache['cylinder-head']);again=candidate.head_interface(local)
idempotence=vol(local-again)+vol(again-local);assert idempotence<.01,idempotence
assert mp.read_bytes()==raw,'Manifest changed during audit'
assert Path(candidate.__file__).read_bytes()==source_bytes,'Candidate changed during audit'
for path,digest in hashes.items():assert hashlib.sha256(Path(path).read_bytes()).hexdigest()==digest,path
report={'status':'rejected' if hits else ('installed-static-pass' if a.installed else 'candidate-static-pass'),'production_fit':False,'manifest_sha256':hashlib.sha256(raw).hexdigest(),'candidate_sha256':hashlib.sha256(source_bytes).hexdigest(),'changed_parts':keys,'roundtrips':roundtrips,'exact_intersection_checks':checks,'failures':hits,'joints':joints,'probes':probes,'flow_probes':flow_checks,'unchanged_supply_endpoint':candidate.SUPPLY_ENDPOINT,'head_adapter_idempotence_mm3':idempotence,'negative_controls':{'gasket_penetration_mm3':negative,'gasket_withdrawal_gap_mm':withdrawal,'closed_flow_obstruction_mm3':flow_negative},'limits':candidate.GAPS,'input_step_sha256':hashes,'installed_geometry_pose_checks':installed_checks}
out=(a.assembly_root if a.installed else ROOT)/('inventory/engine/coolant-outlet-head-installed-validation.json' if a.installed else 'inventory/engine/coolant-outlet-head-candidate-validation.json');out.write_text(json.dumps(report,indent=2)+'\n')
print('RESULT',report['status'],'checks',checks,'failures',len(hits),flush=True)
