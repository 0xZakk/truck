"""Scoped educational stop adapter; retains current housing/lever IDs and local frames."""
from pathlib import Path
import hashlib,json
from functools import lru_cache
from cad_metrics import solid_volume
import build123d as b
from OCP.BRepTools import BRepTools
import throttle_stop_candidate as candidate
ROOT=Path(__file__).resolve().parents[2]
REPLACED={'throttle-housing','throttle-lever-estimated'}
SCREW='throttle-idle-stop-screw-illustrative'
NEW_IDS={SCREW};NEW_OCCURRENCES={SCREW};CHANGED_IDS=REPLACED|NEW_IDS
SOURCE_ID='throttle-stop-illustrative-study'
GAPS=['Factory material supports an external plate-stop screw contacting a lever pad and a preset wide-open stop. The rounded boss, thread, lever lands and WOT lug are illustrative constructions with estimated dimensions.', 'The inherited 0–90 degree demonstration is not Ford stop calibration. Screw locking, torque, strength, preload, idle airflow and exact production WOT contact remain unverified.']
TEXT={'throttle-housing':('Throttle body · illustrative mechanical stops','Twin-bore body with an estimated threaded idle-stop boss and a fixed WOT contact lug.'),'throttle-lever-estimated':('Throttle lever · illustrative stop lands','Preserves the keyed hub, spring hook and cable ball interfaces while adding idle and WOT contact lands.'),SCREW:('Throttle plate-stop screw · illustrative','A modeled helix retains the external stop screw; its tip meets the lever pad at the educational closed endpoint.')}
def source():
 p=ROOT/'reference/engine/throttle-stop-review.json'
 return {SOURCE_ID:dict(title='Factory stop topology and illustrative mechanical stop study',path='/reference/engine/throttle-stop-review.json',sha256=hashlib.sha256(p.read_bytes()).hexdigest(),url='https://github.com/0xZakk/truck/issues/43')}
def local_bindings(occurrences):
 rows={o['id']:o for o in occurrences}
 for ident,parent in [('throttle-housing','throttle-assembly'),('throttle-lever-estimated','throttle-moving')]:
  o=rows[ident]
  if o['parent']!=parent or o['position_cad_mm']!=[0,0,0] or o.get('rotation_cad_deg',[0,0,0])!=[0,0,0]:raise ValueError('Unreviewed local stop frame: '+ident)
 return 'throttle-assembly'
TARGET_NAMES={'throttle-housing':'throttle-housing-stop-proposal','throttle-lever-estimated':'throttle-lever-stop-proposal',SCREW:SCREW}
def difference(a,z):
 return sum(abs(solid_volume(q,'adaptive')) for shape in (a.cut(z),z.cut(a)) if shape for q in shape.solids())
@lru_cache(maxsize=1)
def fixtures():
 proof=json.loads((ROOT/'inventory/engine/throttle-stop-candidate-validation.json').read_text());assert proof['status']=='PASS' and proof['full_sweep']
 base={};target={}
 for ident in REPLACED:
  p=ROOT/'cad/engine/generated/throttle-stop-baseline'/(ident+'.step')
  assert hashlib.sha256(p.read_bytes()).hexdigest()==proof['input_hashes']['cad/engine/generated/'+ident+'.step']
  base[ident]=b.import_step(p)
 for ident,name in TARGET_NAMES.items():
  p=ROOT/'cad/engine/generated/throttle-stop-candidate'/(name+'.step')
  assert hashlib.sha256(p.read_bytes()).hexdigest()==proof['output_hashes'][str(p.relative_to(ROOT))]
  target[ident]=b.import_step(p)
 return base,target

def install(define,add,definitions,occurrences,assemblies,shapes):
 parent=local_bindings(occurrences);old={d['id']:d for d in definitions};base,pieces=fixtures()
 # Recognize either reviewed baseline or installed target independently for each
 # replaced part, including partial refreshes. Never add features twice.
 for ident in REPLACED:
  current=shapes.get(ident)
  if current is None:current=b.import_step(ROOT/old[ident]['step'].lstrip('/'))
  if difference(current,base[ident])>=1e-5 and difference(current,pieces[ident])>=1e-5:raise ValueError('Unreviewed stop geometry: '+ident)
 order=[d['id'] for d in definitions]
 definitions[:]=[d for d in definitions if d['id'] not in CHANGED_IDS];occurrences[:]=[o for o in occurrences if o['id']!=SCREW]
 for ident in sorted(CHANGED_IDS):
  prior=old.get(ident,{});shape=pieces[ident];BRepTools.Clean_s(shape.wrapped);shape.tessellate(.05,.1);name,description=TEXT[ident]
  define(ident,shape,name,description,prior.get('system','induction'),prior.get('color','#bca369'),list(dict.fromkeys(prior.get('sources',[])+[SOURCE_ID])),list(dict.fromkeys(prior.get('unresolved',[])+GAPS)),prior.get('dimension_claims',[]),prepared=True)
  shapes[ident]=shape
 index={key:i for i,key in enumerate(order)};definitions.sort(key=lambda d:index.get(d['id'],len(index)))
 for o in occurrences:
  if o['definition'] in REPLACED:o.update(name=TEXT[o['definition']][0],function=TEXT[o['definition']][1])
 add(SCREW,SCREW,parent,(0,0,0),(-50,40,0),name=TEXT[SCREW][0])
 return dict(changed_definitions=sorted(CHANGED_IDS),changed_occurrences=sorted(CHANGED_IDS),new_definitions=[SCREW],new_occurrences=[SCREW])
