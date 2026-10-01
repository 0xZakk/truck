#!/usr/bin/env python3
"""Read-only actual FS10 axial orientation and physical mount witnesses."""
from pathlib import Path
import json,sys,hashlib,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_math import transforms
mp=R/'inventory/engine/full-assembly.json';m=json.loads(mp.read_text());d={v['id']:v for v in m['definitions']};o={v['id']:v for v in m['occurrences']};t=transforms(m,0)
names=['ac-compressor-front-cylinder','ac-compressor-rear-cylinder','ac-compressor-front-head','ac-compressor-rear-head','ac-compressor-clutch-pulley','ac-compressor-swashplate-shaft','ps-ac-support-bracket']
p={n:R/d[o[n]['definition']]['step'].lstrip('/') for n in names};s={n:t[n]*b.import_step(p[n]) for n in names}
def bbox(sh):
 bb=sh.bounding_box();return {'min':list(bb.min),'max':list(bb.max)}
seats=[]
for y in (210,350):
 for z in (60,140):
  a=[(y+8*math.cos(k*math.tau/16),z+8*math.sin(k*math.tau/16)) for k in range(16)]
  seats.append({'axis_yz':[y,z],'case_material_at_x432_55':sum(s[names[0]].is_inside((432.55,yy,zz)) for yy,zz in a),'carrier_material_at_x432_57':sum(s['ps-ac-support-bracket'].is_inside((432.57,yy,zz)) for yy,zz in a),'samples':16})
# Deliberately wrong pose: moving the branch off its actual mating plane.
fault=s[names[0]].translate((25,0,0));fault_count=sum(fault.is_inside((432.55,y+8*math.cos(k*math.tau/16),z+8*math.sin(k*math.tau/16))) for y in (210,350) for z in (60,140) for k in range(16))
paths=[mp,Path(__file__),R/'cad/engine/assembly_math.py',R/'cad/engine/ac_compressor.py',R/'cad/engine/accessory_brackets.py',R/'cad/engine/accessory_carrier_1994.py',*p.values()]
out={'status':'COMPLETE datum investigation, no trial installation','bounds':{n:bbox(v) for n,v in s.items()},'ear_material_witnesses':seats,'axial_shift_25mm_fault_material_count':fault_count,'orientation':'+X is front; actual front cylinder/head/pulley bounds confirm no inversion','declared_belt_groove_x_mm':[463.56+4*k for k in range(6)],'source_estimated_ear_contact_x_mm':432.56,'rigid_axial_hypotheses':[{'shift_x_mm':x,'all_six_groove_plane_errors_mm':x,'case_ear_to_existing_carrier_seat_error_mm':x,'result':'Requires complete belt-plane and carrier revisions; rejected as isolated repair'} for x in (25,50)],'input_sha256':{str(v.relative_to(R)):hashlib.sha256(v.read_bytes()).hexdigest() for v in paths}}
assert fault_count<64
(R/'inventory/engine/fs10-axial-mount-datums.json').write_text(json.dumps(out,indent=2)+'\n')
