"""IAC-local illustrative electrical construction, after attachment and closure."""
from pathlib import Path
import hashlib
import build123d as b
from OCP.BRepTools import BRepTools
import iac_attachment_integration as attachment
import iac_electrical_candidate as candidate
ROOT=Path(__file__).resolve().parents[2]
REPLACED={'iac-connector-cap','iac-coil'}
NEW_IDS={'iac-coil-carrier-estimated',*candidate.TERMINALS}
NEW_OCCURRENCES=NEW_IDS
GEOMETRY_IDS=CHANGED_IDS=REPLACED|NEW_IDS
SOURCE_IDS=['iac-electrical-factory-topology-illustrative-construction']
GAPS=['Exact1994 diagrams support two IAC terminals and a suppression diode in parallel with the winding; no physical diode package or location is modeled.',
 'Connector dimensions, key and mounting clocking, carrier, terminal alloy/plating, embedded shoulders and tail terminations are illustrative. No production molded retention or joint method is identified.',
 'The coil is a winding envelope, not a homogeneous conductor, resolved turns or electrical resistance simulation. No wire-color-to-metal-material inference is made.']
DESCRIPTIONS={
 'iac-connector-cap':('IAC keyed connector cap · illustrative','An estimated asymmetric shroud and embedded terminal shoulders illustrate a two-contact engine-side connector. The component face looks toward -X, control above VPWR; production cavity numbering and clocking remain unknown.'),
 'iac-coil':('IAC winding envelope · illustrative','An annular winding envelope accepts two separate estimated lead tails. The exact1994 circuit includes a parallel suppression diode, represented in explanation only.'),
 'iac-coil-carrier-estimated':('IAC coil insulator · illustrative','An estimated insulating bobbin supports the winding between fixed axial seats and separates it from the armature and metal case.'),
 'iac-terminal-control-estimated':('IAC control terminal and tail · illustrative','The upper contact in the chosen engine-side view joins one winding endpoint. This is the PCM-controlled circuit; its embedded capture and termination method are estimated.'),
 'iac-terminal-vpwr-estimated':('IAC VPWR terminal and tail · illustrative','The lower contact in the chosen engine-side view joins the other winding endpoint. VPWR is the supply node and suppression-diode cathode in the source circuit; package construction is unknown.')}
def sources():
 p=ROOT/'reference/engine/iac-electrical-review.json'
 return {SOURCE_IDS[0]:dict(title='Exact1994 IAC two-terminal circuit and illustrative electrical construction',path='/'+str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),url='https://github.com/0xZakk/truck/issues/44')}
def install(define,add,group,definitions,occurrences,assemblies,shapes):
 old={d['id']:d for d in definitions};frame=attachment.static_frame('idle-air',assemblies)
 if 'iac-closure-illustrative-study' not in old['iac-valve-body'].get('sources',[]):raise ValueError('Apply the reviewed attachment/closure chain before electrical detail')
 for ident in REPLACED:
  rows=[o for o in occurrences if o['definition']==ident]
  if len(rows)!=1 or attachment.frame_error(frame.inverse()*attachment.occurrence_frame(rows[0],assemblies),b.Location())>1e-6:raise ValueError('Unreviewed electrical relative frame: '+ident)
 parts=candidate.build();definitions[:]=[d for d in definitions if d['id'] not in CHANGED_IDS];occurrences[:]=[o for o in occurrences if o['id'] not in NEW_OCCURRENCES]
 for ident in sorted(CHANGED_IDS):
  prior=old.get(ident,{});shape=parts[ident];BRepTools.Clean_s(shape.wrapped);shape.tessellate(.03 if ident=='iac-connector-cap' else .025,.08);name,fn=DESCRIPTIONS[ident]
  define(ident,shape,name,fn,prior.get('system','induction'),prior.get('color','#c8b986' if ident in candidate.TERMINALS else '#9b9b85'),list(dict.fromkeys(prior.get('sources',[])+SOURCE_IDS)),list(dict.fromkeys(prior.get('unresolved',[])+GAPS)),prior.get('dimension_claims',[]),prepared=True)
  for o in occurrences:
   if o['definition']==ident:o.update(name=name,function=fn)
 for ident in sorted(NEW_IDS):add(ident,ident,'idle-air',explode=(80,0,0))
 return dict(changed_definitions=sorted(CHANGED_IDS),geometry_definitions=sorted(GEOMETRY_IDS),changed_occurrences=sorted(CHANGED_IDS),new_definitions=sorted(NEW_IDS),new_occurrences=sorted(NEW_IDS),adaptation_chain=['base IAC/throttle','iac_attachment_integration.install','iac_closure_integration.install','iac_electrical_integration.install'])
