"""Rotor-only photo-compared detail after the existing oil-drive adaptation."""
from pathlib import Path
import hashlib
import build123d as b
from OCP.BRepTools import BRepTools
import distributor_center_contact_candidate as candidate
ROOT=Path(__file__).resolve().parents[2]
REPLACED={'distributor-rotor','distributor-rotor-contact'}
NEW='distributor-rotor-center-leaf'
IDS=REPLACED|{NEW}
SOURCE='distributor-center-contact-photo-study'
GAPS=[
 'Exact1994 manual identifies rotor blade and spring; current Ford DR375A photo supports a raised folded leaf, open molded collar and captured outer pad. Current replacement revisions may differ from original1994 production.',
 'Leaf thickness, bend/recess dimensions, stake geometry and material properties are inferred. Geometric contact does not establish elastic preload, pressure, electrical resistance or durability.',
 'Cap central-contact envelope is unchanged: material, hidden retention and actual coil-feed construction remain unresolved. No cap coil spring is inferred.',
 'Preserved shaft seat and peripheral tip are inherited educational estimates, not verified Ford dimensions or ignition calibration.'
]
DESCRIPTIONS={
 'distributor-rotor':('Distributor rotor insulator · source-compared study','An estimated molded collar and recess surround the raised center leaf; an illustrative integral stake captures the outer conductor. Shaft seating follows the existing model.'),
 'distributor-rotor-contact':('Distributor rotor outer conductor · estimated','The captured outer conductor connects the raised center leaf to the existing peripheral tip. Electrical material and exact captured-joint construction remain unverified.'),
 NEW:('Distributor rotor center leaf · estimated','A separate curved metal leaf contacts the cap center-contact envelope and the outer conductor while rotating with the rotor. Source-supported topology; dimensions, spring preload and alloy remain inferred.')
}
def volume(s):return sum(x.volume for x in s.solids()) if s else 0.
def difference(a,z):return volume(a-z)+volume(z-a)
def sources():
 p=ROOT/'reference/engine/distributor-center-contact-review.json'
 return {SOURCE:dict(title='Exact1994 rotor spring and Ford DR375A contact construction comparison',path='/'+str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),url='https://www.ford.com/product/distributor-rotor-p4000075990')}
def install(define,add,group,definitions,occurrences,assemblies,shapes):
 old={d['id']:d for d in definitions};rows={o['id']:o for o in occurrences}
 base=candidate.baseline_parts();target=candidate.parts();recognized={}
 # A rigid move of the entire distributor is safe. Relative rotor frames are
 # not silently normalized, nor may this adapter undo a source/interface edit.
 for ident in IDS:
  if ident not in old:
   if ident==NEW:continue
   raise ValueError('Missing distributor baseline '+ident)
  row=rows.get(ident,{})
  if row.get('definition')!=ident or row.get('parent')!='distributor-rotation' or any(abs(x)>1e-9 for x in row.get('position_cad_mm',[0,0,0])+row.get('rotation_cad_deg',[0,0,0])):
   raise ValueError('Unreviewed distributor relative frame '+ident)
  current=shapes.get(ident)
  if current is None:current=b.import_step(ROOT/old[ident]['step'].lstrip('/'))
  err=difference(current,target[ident]);prior=difference(current,base[ident]) if ident in base else float('inf')
  if min(err,prior)>=.01:raise ValueError('Unreviewed distributor rotor geometry '+ident)
  recognized[ident]='refined' if err<.01 else 'baseline'
 definitions[:]=[d for d in definitions if d['id'] not in IDS]
 occurrences[:]=[o for o in occurrences if o['id']!=NEW]
 for ident in sorted(IDS):
  prior=old.get(ident,{});shape=target[ident];BRepTools.Clean_s(shape.wrapped);shape.tessellate(.025,.1)
  name,fn=DESCRIPTIONS[ident]
  define(ident,shape,name,fn,prior.get('system','ignition'),prior.get('color','#cad0d4'),list(dict.fromkeys(prior.get('sources',[])+[SOURCE])),list(dict.fromkeys(prior.get('unresolved',[])+GAPS)),prior.get('dimension_claims',[]),prepared=True)
  result=next(d for d in definitions if d['id']==ident);size=shape.bounding_box().size;result['model_bounds_mm']=[size.X,size.Y,size.Z]
  for o in occurrences:
   if o['definition']==ident:o.update(name=name,function=fn)
 add(NEW,NEW,'distributor-rotation',explode=(0,0,225))
 return dict(changed_definitions=sorted(IDS),new_definitions=[NEW],changed_occurrences=sorted(IDS),frame_changes=False,recognized_inputs=recognized)
