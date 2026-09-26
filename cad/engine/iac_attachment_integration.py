"""Idempotent IAC educational attachment adapter, independent of world translation."""
from pathlib import Path
import hashlib,json
import build123d as b
from OCP.BRepTools import BRepTools
import iac_attachment_candidate as candidate
ROOT=Path(__file__).resolve().parents[2]
REPLACED={'iac-valve-body','iac-gasket','iac-armature','throttle-housing'}
SCREW='iac-mount-screw-estimated';SPRING='iac-return-spring-estimated'
NEW_IDS={SCREW,SPRING};CHANGED_IDS=REPLACED|NEW_IDS
NEW_OCCURRENCES={'iac-mount-screw-1-estimated','iac-mount-screw-2-estimated',SPRING}
SOURCE_IDS=['iac-attachment-factory-1994','iac-attachment-estimated-study']
GAPS=['Two diagonal mounting fasteners follow exact1994 factory topology; dimensions, threads, strength and installed valve identity remain unverified.',
 'The return spring, idealized annular ends and armature contact sleeve are educational construction choices, not verified production internals. No force, preload, rate, duty cycle or valve calibration is simulated.',
 'The existing end plug retains0.1mm radial clearance with unresolved retention/sealing construction; this study is not a leak-tight valve certification.']
DESCRIPTIONS={
 'iac-valve-body':('IAC valve body · attachment study','Two estimated flange ears retain the body over a separate gasket. The inherited bypass chambers and reverse-pintle seat remain open.'),
 'iac-gasket':('IAC mounting gasket · estimated','Seals the modeled two-port flange against the throttle pad, with two diagonal fastener clearances.'),
 'iac-armature':('IAC armature and contact sleeve · study','A contact sleeve links the armature to the stem in this educational construction. Actual swage, press fit or other production joint remains unknown.'),
 'throttle-housing':('Twin-bore throttle housing','Two main air bores and separate bypass passages remain open. Estimated blind receivers mate to the IAC flange screws.'),
 SCREW:('IAC retaining screw · estimated','One of two fasteners clamping the valve and gasket to the throttle pad. Smooth shank and receiver are thread envelopes; tightening capacity is not established.'),
 SPRING:('IAC restoring spring · illustrative','An illustrative compression spring remains seated between the chamber closure and reverse-seated pintle. It explains a possible restoring load path without claiming a production rate or construction.')}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def sources():
 p=ROOT/'reference/engine/iac-attachment-review.json';r=json.loads(p.read_text());factory=next(s for s in r['sources'] if 'Removal%20and%20Replacement' in s['path'])
 return {SOURCE_IDS[0]:dict(title='1994 Ford IAC removal and two-bolt gasket topology',path='/'+factory['path'],sha256=factory['sha256'],url='https://charm.li/Ford/1994/F%20150%202WD%20Pickup%20L6-300%204.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Fuel%20Delivery%20and%20Air%20Induction/Idle%20Speed%2FThrottle%20Actuator%20-%20Electronic/Service%20and%20Repair/Removal%20and%20Replacement/'),SOURCE_IDS[1]:dict(title='IAC attachment study: estimated dimensions and restoring construction',path='/'+str(p.relative_to(ROOT)),sha256=digest(p),url='https://github.com/0xZakk/truck/issues/44')}
def static_frame(parent,assemblies):
 rows={a['id']:a for a in assemblies};chain=[];seen=set()
 while parent in rows:
  if parent in seen:raise ValueError('Cyclic ancestry')
  seen.add(parent);a=rows[parent]
  if a.get('motion'):raise ValueError('IAC attachment requires static ancestry')
  chain.append(a);parent=a['parent']
 frame=b.Location()
 for a in reversed(chain):frame*=b.Pos(*a.get('position_cad_mm',[0,0,0]))*b.Rot(*a.get('rotation_cad_deg',[0,0,0]))
 return frame

def occurrence_frame(o,assemblies):return static_frame(o['parent'],assemblies)*b.Pos(*o['position_cad_mm'])*b.Rot(*o.get('rotation_cad_deg',[0,0,0]))
def frame_error(a,c):return max((b.Vertex(*p).moved(a).center()-b.Vertex(*p).moved(c).center()).length for p in [(0,0,0),(1,0,0),(0,1,0),(0,0,1)])
def install(define,add,group,definitions,occurrences,assemblies,shapes):
 old={d['id']:d for d in definitions};occs={o['id']:o for o in occurrences}
 frame=static_frame('idle-air',assemblies);local={};conversions={}
 for ident in REPLACED:
  selected=[o for o in occurrences if o['definition']==ident]
  if len(selected)!=1:raise ValueError('IAC adapter expects one occurrence of '+ident)
  o=selected[0];conversions[ident]=frame.inverse()*occurrence_frame(o,assemblies)
  expected=b.Pos(-397,-25,-540) if ident=='throttle-housing' else b.Location()
  if frame_error(conversions[ident],expected)>1e-6:raise ValueError('Unreviewed relative IAC datum: '+ident)
  local[ident]=conversions[ident]*(shapes[ident] if ident in shapes else b.import_step(ROOT/old[ident]['step'].lstrip('/')))
 parts=candidate.build(local['iac-valve-body'],local['iac-gasket'],local['throttle-housing'],local['iac-armature'])
 emitted={ident:conversions[ident].inverse()*parts[ident] for ident in REPLACED}
 emitted.update({SCREW:candidate.screw(),SPRING:parts[SPRING]})
 definitions[:]=[d for d in definitions if d['id'] not in CHANGED_IDS]
 occurrences[:]=[o for o in occurrences if o['id'] not in NEW_OCCURRENCES]
 for ident in sorted(CHANGED_IDS):
  shape=emitted[ident];prior=old.get(ident,{})
  # Reuse finer CAD triangulation through the shared exporter.
  BRepTools.Clean_s(shape.wrapped);shape.tessellate(.05,.1)
  name,fn=DESCRIPTIONS[ident]
  gaps=[g for g in prior.get('unresolved',[]) if 'restoring mechanism remain unresolved' not in g]
  define(ident,shape,name,fn,prior.get('system','induction'),prior.get('color','#c6913b' if ident in NEW_IDS else '#95a3a9'),list(dict.fromkeys(prior.get('sources',[])+SOURCE_IDS)),list(dict.fromkeys(gaps+GAPS)),prior.get('dimension_claims',[]),prepared=True)
  # Existing occurrence frames and explode vectors are preserved, descriptions
  # refreshed so stale absent-mechanism language cannot shadow the definition.
  for o in occurrences:
   if o['definition']==ident:o.update(name=name,function=fn)
 for i,(x,y) in enumerate(candidate.BOLTS,1):add(f'iac-mount-screw-{i}-estimated',SCREW,'idle-air',(x,y,0),(0,0,65),name=f'IAC retaining screw {i} · estimated')
 add(SPRING,SPRING,'idle-air',explode=(-75,0,0))
 return dict(changed_definitions=sorted(CHANGED_IDS),changed_occurrences=sorted(NEW_OCCURRENCES|{o['id'] for o in occurrences if o['definition'] in REPLACED}),new_definitions=sorted(NEW_IDS),new_occurrences=sorted(NEW_OCCURRENCES))
