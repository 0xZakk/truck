"""Idempotent local-frame adapter for explicitly illustrative four plate screws."""
from pathlib import Path
import hashlib
import build123d as b
from OCP.BRepTools import BRepTools
import throttle_plate_fasteners_candidate as candidate
ROOT=Path(__file__).resolve().parents[2]
REPLACED={'throttle-shaft','throttle-plate'}
SCREW='throttle-plate-screw-illustrative'
NEW_IDS={SCREW};CHANGED_IDS=REPLACED|NEW_IDS
POSITIONS={f'throttle-plate-screw-{i}-{j}-illustrative':(0,center+dy,0) for i,center in enumerate([-27,27],1) for j,dy in enumerate([-8,8],1)}
NEW_OCCURRENCES=set(POSITIONS)
SOURCE_ID='throttle-plate-retention-illustrative-study'
GAPS=['Four screws (two per plate) are an explicit educational hypothesis; Ford count, shaft construction and dimensions remain unverified.',
      'Actual helical geometry demonstrates capture and unthreading; pitch, fit, torque, staking/locking, strength and preload are not Ford specifications.',
      'Plate bevels, airflow/idle calibration and production stops remain unresolved.']
DESCRIPTIONS={'throttle-shaft':('Throttle shaft · keyed and plate-retention study','Preserves the keyed linkage end and adds local head pockets, supporting pads and estimated helical receivers for the plates.'),'throttle-plate':('Throttle butterfly plate · retention study','Restricts one air passage and is captured by two explicitly illustrative screws through estimated clearance holes.'),SCREW:('Throttle plate screw · illustrative','One of four hypothesized plate screws; its head seats on the manifold-facing plate surface and a modeled helix captures the shaft receiver.')}
def source():
 p=ROOT/'reference/engine/throttle-plate-fasteners-review.json'
 return {SOURCE_ID:dict(title='Factory limits and illustrative throttle plate retention',path='/reference/engine/throttle-plate-fasteners-review.json',sha256=hashlib.sha256(p.read_bytes()).hexdigest(),url='https://github.com/0xZakk/truck/issues/43')}
def local_bindings(occurrences):
 rows={o['id']:o for o in occurrences};shaft=rows['throttle-shaft'];parent=shaft['parent']
 for oid,pos in [('throttle-shaft',[0,0,0]),('throttle-plate-1',[0,-27,0]),('throttle-plate-2',[0,27,0])]:
  o=rows[oid]
  if o['parent']!=parent or o['position_cad_mm']!=pos or o.get('rotation_cad_deg',[0,0,0])!=[0,0,0]:raise ValueError('Unreviewed local throttle frame: '+oid)
 return parent

def current_gaps(previous):
 # Replace only explicit superseded absence statements; retain all evidence limits.
 substitutions={
 'IAC/TPS studies and bypass passages are present; their exact variants and internal details remain unresolved. Purge ports, linkage, return spring, accelerator bracket and plate screws remain unmodeled. Idealized 0–90 degree motion is not the production stop calibration.':'IAC/TPS, linkage, spring, bracket and plate retention have illustrative studies; exact variants and production details remain unresolved. Purge ports remain unmodeled. Idealized 0–90 degree motion is not production stop calibration.',
 'Spring, shield, cable/socket, plate screws and preset stops absent;0–90 degrees is inherited educational travel.':'Spring, shield and plate screws now have illustrative studies. Actual cable/socket and production stops remain unresolved; 0–90 degrees is educational travel.'}
 return list(dict.fromkeys([substitutions.get(g,g) for g in previous]+GAPS))

def install(define,add,definitions,occurrences,assemblies,shapes):
 old={d['id']:d for d in definitions};parent=local_bindings(occurrences)
 originals={ident:shapes[ident] if ident in shapes else b.import_step(ROOT/old[ident]['step'].lstrip('/')) for ident in REPLACED}
 proposed,_=candidate.parts(originals['throttle-shaft'],originals['throttle-plate'])
 pieces={'throttle-shaft':proposed['throttle-shaft-plate-retention-illustrative'],'throttle-plate':proposed['throttle-plate-drilled-illustrative'],SCREW:candidate.screw()}
 definitions[:]=[d for d in definitions if d['id'] not in CHANGED_IDS]
 occurrences[:]=[o for o in occurrences if o['id'] not in NEW_OCCURRENCES]
 for ident in sorted(CHANGED_IDS):
  prior=old.get(ident,{});name,description=DESCRIPTIONS[ident];shape=pieces[ident]
  BRepTools.Clean_s(shape.wrapped);shape.tessellate(.05,.1)
  define(ident,shape,name,description,prior.get('system','induction'),prior.get('color','#b6bec1'),list(dict.fromkeys(prior.get('sources',[])+[SOURCE_ID])),current_gaps(prior.get('unresolved',[])),prior.get('dimension_claims',[]),prepared=True)
 for o in occurrences:
  if o['definition'] in REPLACED:o.update(name=DESCRIPTIONS[o['definition']][0],function=DESCRIPTIONS[o['definition']][1])
 for oid,pos in POSITIONS.items():add(oid,SCREW,parent,pos,(-80,0,0),name='Throttle plate screw · illustrative')
 return dict(changed_definitions=sorted(CHANGED_IDS),changed_occurrences=sorted(NEW_OCCURRENCES|{'throttle-shaft','throttle-plate-1','throttle-plate-2'}),new_definitions=sorted(NEW_IDS),new_occurrences=sorted(NEW_OCCURRENCES))
