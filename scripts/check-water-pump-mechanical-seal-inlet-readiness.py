"""Generic seal candidate: contacts, fluid separation, all neighbors, STEP."""
from pathlib import Path
import sys,json,hashlib,itertools,math
import build123d as b
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
from valve_layout_integration import occurrence_shape
from cad_metrics import solid_volume
import water_pump_mechanical_seal_candidate as s
from water_pump_joint_candidate import cx
ACCEPTED=Path('/private/tmp/truck-seal-inlet-baseline-2032a3da');BASE=Path('/private/tmp/truck-desktop-pan-v9-baseline-6b11c0f8')
mp=ACCEPTED/'full-assembly.json';raw=mp.read_bytes();m=json.loads(raw);defs={d['id']:d for d in m['definitions']};poses=transforms(m)
files=[ACCEPTED/'freeze-provenance.json',ROOT/'cad/engine/assembly_math.py',Path(__file__),Path(s.__file__),ROOT/'cad/engine/water_pump_joint_candidate.py',ROOT/'cad/engine/valve_layout_integration.py',ROOT/'cad/engine/valve_layout_candidate.py',ROOT/'cad/engine/cad_metrics.py',ROOT/'reference/engine/water-pump-internal-construction-reviewed.json'];hashes={str(q):hashlib.sha256(q.read_bytes()).hexdigest() for q in files};cache={}
def load(key):
 if key not in cache:
  path=ACCEPTED/(key+'.step')
  if not path.exists():path=BASE/defs[key]['step'].lstrip('/')
  hashes[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest();cache[key]=b.import_step(path)
 return cache[key]
def compound(q):return b.Compound(children=list(q)) if isinstance(q,b.ShapeList) else q
def vol(q):return sum(solid_volume(x,'adaptive') for x in q.solids()) if q else 0
def broad(a,c):return all(min(getattr(a.max,k),getattr(c.max,k))-max(getattr(a.min,k),getattr(c.min,k))>.001 for k in 'XYZ')
parts=s.components()
for k,v in parts.items():assert v.is_valid and len(v.solids())==1,(k,len(v.solids()))
print('Seal solids valid',len(parts),flush=True)
contacts={}
for a,c in [('stationary-face','rotating-face'),('stationary-face','bellows'),('stationary-face','spring'),('spring','carrier'),('bellows','carrier'),('rotating-face','shaft-collar')]:
 ka,kc='water-pump-seal-'+a,'water-pump-seal-'+c
 contacts[a+'/'+c]=parts[ka].distance_to(parts[kc]);assert contacts[a+'/'+c]<1e-7,(a,c,contacts[a+'/'+c])
contacts['carrier/housing']=parts['water-pump-seal-carrier'].distance_to(load('water-pump-housing'))
contacts['shaft-collar/shaft']=parts['water-pump-seal-shaft-collar'].distance_to(load('water-pump-shaft'))
assert max(contacts.values())<1e-7,contacts
# Face-contact area from two plane sections, not just proximity.
def plane_faces(shape,x):return [f for f in shape.faces() if f.bounding_box().size.X<1e-6 and abs(f.center().X-x)<1e-6]
f1=plane_faces(parts['water-pump-seal-stationary-face'],13.5);f2=plane_faces(parts['water-pump-seal-rotating-face'],13.5)
face_area=sum(compound(a&c).area for a in f1 for c in f2 if a&c)
assert abs(face_area-math.pi*(18**2-11**2))<.01,face_area
# Topological fluid test: partition a local cylinder by actual housing/shaft/seal
# material. Wet inlet sample and dry leakage-space sample must belong to distinct
# connected solids. This uses ideal touching faces, not a physical film model.
void=cx(30,10,22)-load('water-pump-housing')-load('water-pump-shaft')
for part in parts.values():void=compound(void)-part
void=compound(void);wet=b.Pos(10.5,20,0)*b.Sphere(.1);dry=b.Pos(21.5,8.5,0)*b.Sphere(.1)
wet_ids=[i for i,v in enumerate(void.solids()) if vol(v&wet)>.004];dry_ids=[i for i,v in enumerate(void.solids()) if vol(v&dry)>.004]
assert len(wet_ids)==len(dry_ids)==1 and wet_ids!=dry_ids,(wet_ids,dry_ids)
print('Contacts and wet/dry partition passed',flush=True)
frame=poses['water-pump-seal'];world={k:frame*v for k,v in parts.items()};neighbors={o['id']:poses[o['id']]*occurrence_shape(o,load(o['definition'])) for o in m['occurrences'] if o['id']!='water-pump-seal'};bounds={k:v.bounding_box(optimal=False) for k,v in {**world,**neighbors}.items()};checks=0;fail=[]
for a,v in world.items():
 for c,t in neighbors.items():
  if broad(bounds[a],bounds[c]):
   checks+=1;amount=vol(v&t)
   if amount>.02:fail.append([a,c,amount]);print('Collision',a,c,amount,flush=True)
for (a,v),(c,t) in itertools.combinations(parts.items(),2):
 checks+=1;amount=vol(v&t)
 if amount>.02:fail.append([a,c,amount])
print('Neighbors checked',checks,flush=True)
# Selected pump-study explosion samples preserve axial ordering; this is a
# display sequence, not a removal procedure or whole-engine explosion claim.
motion_checks=0
pump_occ=[o for o in m['occurrences'] if o['parent']=='water-pump-assembly' and o['id']!='water-pump-seal']
for fraction in [.05,.1,.25,.5,.75,1]:
 moved={k:frame*b.Pos(s.EXPLODE_X[k]*fraction,0,0)*v for k,v in parts.items()}
 other={o['id']:b.Pos(*[fraction*q for q in o.get('explode_cad_mm',[0,0,0])])*neighbors[o['id']] for o in pump_occ}
 bb={k:v.bounding_box(optimal=False) for k,v in {**moved,**other}.items()}
 pairs=list(itertools.combinations(moved.items(),2))+[(aa,cc) for aa in moved.items() for cc in other.items()]
 for (a,v),(c,t) in pairs:
  if broad(bb[a],bb[c]):
   motion_checks+=1;amount=vol(v&t)
   if amount>.02:fail.append(['explode',fraction,a,c,amount])
print('Pump-study explosion checked',motion_checks,flush=True)

step_checks={};out=Path('/private/tmp/water-pump-mechanical-seal-step');out.mkdir(exist_ok=True)
for key,part in parts.items():
 path=out/(key+'.step');b.export_step(part,path);again=b.import_step(path);delta=vol(part-again)+vol(again-part);assert again.is_valid and len(again.solids())==1 and delta<.02,(key,delta);step_checks[key]=delta
# Actual meshes for whole seal and upper-half cutaway.
colors=[s.LABELS[k][2] for k in parts]
for cut in [False,True]:
 arrays={};ids=[];used=[]
 for (key,part),color in zip(parts.items(),colors):
  if cut:part=compound(part&(b.Pos(0,0,-25)*b.Box(200,100,50)))
  if not part:continue
  v,f=part.tessellate(.08);i=len(ids);ids.append(key);used.append(color);arrays[f'vertices_{i}']=np.array([[q.X,q.Y,q.Z] for q in v]);arrays[f'faces_{i}']=np.array(f)
 arrays['metadata']=json.dumps({'parts':ids,'colors':used});np.savez('/private/tmp/water-pump-mechanical-seal-'+('cutaway' if cut else 'actual')+'.npz',**arrays)
unchanged=raw==mp.read_bytes() and all(hashlib.sha256(Path(q).read_bytes()).hexdigest()==h for q,h in hashes.items());report={'status':'PASS' if unchanged and not fail else 'FAIL','manifest_sha256':hashlib.sha256(raw).hexdigest(),'inputs_unchanged':unchanged,'input_hashes':hashes,'neighbor_checks':checks,'pump_study_explode_checks':motion_checks,'collisions':fail,'contact_distances_mm':contacts,'face_contact_area_mm2':face_area,'fluid_partition':{'void_solids':len(void.solids()),'wet_component':wet_ids,'dry_component':dry_ids,'ideal_zero_gap_faces':True},'step_symmetric_difference_mm3':step_checks,'limits':s.GAPS};(ROOT/'inventory/engine/water-pump-mechanical-seal-inlet-readiness-validation.json').write_text(json.dumps(report,indent=2)+'\n');assert unchanged and not fail,fail;print('PASS illustrative seal candidate',flush=True)
