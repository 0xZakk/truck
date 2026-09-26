"""Final illustrative IAC closure, applied after attachment reconstruction."""
from pathlib import Path
import hashlib,json
import build123d as b
from OCP.BRepTools import BRepTools
import iac_attachment_integration as attachment
import iac_closure_candidate as closure
ROOT=Path(__file__).resolve().parents[2]
GEOMETRY_IDS={'iac-valve-body','iac-end-plug'}
METADATA_IDS=attachment.CHANGED_IDS-GEOMETRY_IDS
CHANGED_IDS=GEOMETRY_IDS|METADATA_IDS
SOURCE_IDS=['iac-closure-illustrative-study']
SUPERSEDED=attachment.GAPS[2]
CLOSURE_LIMIT='The previous0.1mm end-plug geometric gap is superseded by an illustrative captured metal closure. Factory retention, material/fit, forming process, contact pressure and leak-rate performance remain unknown.'
GAPS=[CLOSURE_LIMIT,'The recessed plug flange and integral formed lip are educational choices; exact1994 images do not distinguish pressed, crimped/staked or threaded closure. No separate elastomer, production interference or service procedure is inferred.']
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def sources():
 p=ROOT/'reference/engine/iac-closure-review.json'
 return {SOURCE_IDS[0]:dict(title='IAC closure review: unresolved factory method and illustrative captured flange',path='/'+str(p.relative_to(ROOT)),sha256=digest(p),url='https://github.com/0xZakk/truck/issues/44')}
def update_metadata(row):
 gaps=[CLOSURE_LIMIT if g==SUPERSEDED else g for g in row.get('unresolved',[])]
 row['unresolved']=list(dict.fromkeys(gaps+GAPS));row['sources']=list(dict.fromkeys(row.get('sources',[])+SOURCE_IDS))
 return row

def install(define,add,group,definitions,occurrences,assemblies,shapes):
 old={d['id']:d for d in definitions};occs={o['id']:o for o in occurrences};frame=attachment.static_frame('idle-air',assemblies)
 local={};conversions={}
 for ident in GEOMETRY_IDS:
  selected=[o for o in occurrences if o['definition']==ident]
  if len(selected)!=1:raise ValueError('Expected one '+ident+' occurrence')
  conversions[ident]=frame.inverse()*attachment.occurrence_frame(selected[0],assemblies)
  expected=b.Pos(-23.5,0,0) if ident=='iac-end-plug' else b.Location()
  if attachment.frame_error(conversions[ident],expected)>1e-6:raise ValueError('Changed closure datum: '+ident)
  shape=shapes[ident] if ident in shapes else b.import_step(ROOT/old[ident]['step'].lstrip('/'))
  local[ident]=conversions[ident]*shape
 parts=closure.build(local['iac-valve-body'])
 definitions[:]=[d for d in definitions if d['id'] not in GEOMETRY_IDS]
 for row in definitions:
  if row['id'] in METADATA_IDS:update_metadata(row)
 for ident in sorted(GEOMETRY_IDS):
  prior=update_metadata(dict(old[ident]));shape=conversions[ident].inverse()*parts[ident];BRepTools.Clean_s(shape.wrapped);shape.tessellate(.03,.08)
  name=prior['name'] if ident=='iac-valve-body' else 'IAC captured end plug · illustrative'
  function=prior['function'] if ident=='iac-valve-body' else 'A recessed metal flange is captured between an integral body lip and shoulder in this illustrative closure. Its inner face preserves the spring seat; actual Ford construction and leak performance remain unknown.'
  define(ident,shape,name,function,prior['system'],prior['color'],prior['sources'],prior['unresolved'],prior.get('dimension_claims',[]),prepared=True)
  for o in occurrences:
   if o['definition']==ident:o.update(name=name,function=function)
 return dict(changed_definitions=sorted(CHANGED_IDS),geometry_definitions=sorted(GEOMETRY_IDS),metadata_only_definitions=sorted(METADATA_IDS),changed_occurrences=sorted(o['id'] for o in occurrences if o['definition'] in GEOMETRY_IDS),adaptation_chain=['base IAC/throttle','iac_attachment_integration.install','iac_closure_integration.install'])
