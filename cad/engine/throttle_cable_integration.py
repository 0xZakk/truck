"""Scoped adapter for the explicitly illustrative accelerator cable engine end."""
from pathlib import Path
import hashlib
import build123d as b
from OCP.BRepTools import BRepTools
import throttle_cable_candidate as candidate
ROOT=Path(__file__).resolve().parents[2]
BRACKET='accelerator-cable-bracket'
KINDS={
 'throttle-cable-snap-retainer-illustrative':'fixed',
 'throttle-cable-sheath-stub-illustrative':'fixed',
 'throttle-cable-socket-illustrative':'socket',
 'throttle-cable-swivel-seat-illustrative':'seat',
 'throttle-cable-fixed-guide-illustrative':'guide',
 'throttle-cable-core-illustrative':'core',
 'throttle-cable-compression-spring-illustrative':'compression-spring'}
NEW_IDS=set(KINDS);REPLACED={BRACKET};CHANGED_IDS=NEW_IDS|REPLACED;NEW_OCCURRENCES=NEW_IDS
SOURCE_ID='throttle-cable-engine-end-illustrative-study'
GAPS=['Exact1994 references establish accelerator cable, ball attachment and a distinct cable-end compression spring; owner-installed cable identity is unverified.',
 'Dimensions,24 turns, wire size, internal swivel/guide/terminal retention and bracket revision are educational estimates, not Ford specifications.',
 'No material, preload, spring rate, strength, insertion-flexure or guaranteed vehicle return claim. Full cable route, firewall, pedal and unverified cruise/C6 hardware are excluded.']
TEXT={
 BRACKET:('Accelerator cable bracket · cable clearance study','Retains unchanged mounting, shield and shaft-spring anchors; a proposed distal web/flange revision supports the thicker cable end.'),
 'throttle-cable-snap-retainer-illustrative':('Accelerator cable snap retainer · illustrative','Captured flange and slotted tabs locate the cable assembly through the proposed bracket opening.'),
 'throttle-cable-sheath-stub-illustrative':('Accelerator cable sheath stub · illustrative','A short fixed sheath segment with a captive bead; routing to the firewall and pedal is omitted.'),
 'throttle-cable-socket-illustrative':('Accelerator cable socket and stem · illustrative','Captures the unchanged lever ball and guides the moving cable terminal toward the fixed retainer.'),
 'throttle-cable-swivel-seat-illustrative':('Cable fixed spring seat · illustrative','An estimated captive spherical seat articulates about the stationary retainer.'),
 'throttle-cable-fixed-guide-illustrative':('Cable telescoping guide · illustrative','A captured insert aligns the compression spring as the hollow moving stem slides over it.'),
 'throttle-cable-core-illustrative':('Accelerator cable core and terminal · illustrative','Continuous flexible core joins the captured terminal to a short sheath segment; material feeds through the open cut boundary.'),
 'throttle-cable-compression-spring-illustrative':('Cable-end compression spring · illustrative','A separate spring compresses between cable-end seats; this is distinct from the throttle shaft torsion spring.')}
def source():
 p=ROOT/'reference/engine/throttle-cable-review.json'
 return {SOURCE_ID:dict(title='Exact1994 cable topology, replacement comparison and illustrative engine-end mechanism',path='/reference/engine/throttle-cable-review.json',sha256=hashlib.sha256(p.read_bytes()).hexdigest(),url='https://github.com/0xZakk/truck/issues/43')}
def local_bindings(occurrences):
 rows={o['id']:o for o in occurrences};base=rows[BRACKET]
 if base['parent']!='throttle-assembly' or base['position_cad_mm']!=[0,0,0] or base.get('rotation_cad_deg',[0,0,0])!=[0,0,0]:raise ValueError('Unreviewed bracket local frame')
 for ident in ['throttle-housing','throttle-linkage-shield-estimated','throttle-return-spring-illustrative']:
  o=rows[ident]
  if o['parent']!=base['parent'] or o['position_cad_mm']!=[0,0,0] or o.get('rotation_cad_deg',[0,0,0])!=[0,0,0]:raise ValueError('Unreviewed local anchor: '+ident)
 return base['parent']
def install(define,add,definitions,occurrences,assemblies,shapes):
 parent=local_bindings(occurrences);old={d['id']:d for d in definitions}
 original=shapes.get(BRACKET)
 if original is None:original=b.import_step(ROOT/old[BRACKET]['step'].lstrip('/'))
 pieces=candidate.stationary()|candidate.moving(0)[0]|{BRACKET:candidate.bracket_proposal(original)}
 definitions[:]=[d for d in definitions if d['id'] not in CHANGED_IDS];occurrences[:]=[o for o in occurrences if o['id'] not in NEW_IDS]
 for ident in sorted(CHANGED_IDS):
  prior=old.get(ident,{});name,description=TEXT[ident];q=pieces[ident];BRepTools.Clean_s(q.wrapped);q.tessellate(.05,.1)
  color='#20272d' if KINDS.get(ident) in ['fixed','socket','seat'] else '#b6bec1'
  define(ident,q,name,description,'induction',prior.get('color',color),list(dict.fromkeys(prior.get('sources',[])+[SOURCE_ID])),list(dict.fromkeys(prior.get('unresolved',[])+GAPS)),prior.get('dimension_claims',[]),prepared=True)
 for o in occurrences:
  if o['definition']==BRACKET:o.update(name=TEXT[BRACKET][0],function=TEXT[BRACKET][1])
 for ident,kind in KINDS.items():
  add(ident,ident,parent,(0,0,0),(0,75,0),name=TEXT[ident][0]);occurrences[-1]['throttle_cable']=dict(model='illustrative-cable-v1',kind=kind)
 return dict(changed_definitions=sorted(CHANGED_IDS),changed_occurrences=sorted(CHANGED_IDS),new_definitions=sorted(NEW_IDS),new_occurrences=sorted(NEW_IDS))
