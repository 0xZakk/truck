"""Integration hooks for the independently checked 1994 shared-carrier study.

Root must apply placement/removal hooks as well as build_hardware; calling only
build_hardware would duplicate attachments. No installed builder is modified here.
"""
import accessory_carrier_1994 as c
from tensioner_engine_support import mount_bolt_local

REMOVE_OCCURRENCES={'ps-ac-engine-bracket-bolt-1','ps-ac-engine-bracket-bolt-2'}
TENSIONER_IDS=set(c.tensioner_arm.components())|set(c.tensioner_pulley.components())
PLACEMENT_OVERRIDES={identifier:{'position_cad_mm':list(c.TENSIONER_POSITION),'rotation_cad_deg':[0,90,0]} for identifier in TENSIONER_IDS}


def replacement_definition(identifier,shape):
 if identifier=='ps-ac-support-bracket':return c.carrier()
 if identifier=='tensioner-mounting-bolt':return mount_bolt_local()
 return shape


def build_hardware(api):
 define,add,group=api
 group('carrier-1994-engine-attachments','1994 shared carrier · engine attachments','accessory-support-brackets')
 pieces={k:s for k,s in c.parts().items() if k.startswith('carrier-')}
 for i,(identifier,shape) in enumerate(pieces.items()):
  if identifier=='carrier-front-head-bolt-1':
   name='Shared carrier · front cylinder-head bolt #1';function='Ford Fig4 identifies this front-head clamp point. The smooth bolt and its dimensions remain provisional.';explode=(140,0,0)
  elif identifier=='carrier-side-head-bolt-2':
   name='Shared carrier · side cylinder-head bolt #2';function='Ford Fig4 identifies the head-side clamp point. The external dry boss and smooth bolt fit are a construction study.';explode=(0,140,0)
  else:
   name=identifier.replace('-',' ').title();function='One of the two lower block-side stud/nut clamp stacks shown as nuts #3 in Ford Fig4. Washers, dimensions and smooth thread envelopes remain illustrative.';explode=(0,150+i*18,0)
  define(identifier,shape,name,function,'accessory-drive','#a9afb2',c.SOURCES,c.GAPS)
  add(identifier,identifier,'carrier-1994-engine-attachments',(0,0,0),explode)
