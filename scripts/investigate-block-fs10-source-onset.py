#!/usr/bin/env python3
"""Frozen block revision chain against unchanged actual FS10 geometry."""
from pathlib import Path
import sys,json,hashlib,math
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_math import transforms
from cad_metrics import solid_volume
import timing_cover_seven_fastener_candidate as seven
from timing_coupled_core_candidate import AXIS
mp=R/'inventory/engine/full-assembly.json';m=json.loads(mp.read_text());occ={o['id']:o for o in m['occurrences']};defs={d['id']:d for d in m['definitions']};poses=transforms(m,0)
ids=['ac-compressor-rear-cylinder','ac-compressor-swashplate-shaft','ac-compressor-piston-5','ac-compressor-shoe-5-rear','ac-compressor-shoe-5-front','ac-compressor-case-bolt-5']
paths={n:R/defs[occ[n]['definition']]['step'].lstrip('/')for n in ids};parts={n:poses[n]*b.import_step(p)for n,p in paths.items()}
stages=[('canonical block',R/defs['block']['step'].lstrip('/'),'full block'),('pre-front combined block',R/'cad/engine/generated/timing-block-combined-candidate/block.step','full block'),('original frontjoint land',R/'cad/engine/generated/timing-cover-front-joint-candidate/future-block-land.step','added land only'),('attachment-v2 land',R/'cad/engine/generated/timing-cover-attachment-v2/future-block-land.step','added land only'),('first frontblock adapter',R/'cad/engine/generated/timing-front-block-adapter-candidate/block.step','full block'),('expanded seat V3',seven.BLOCK,'full block'),('seven support block',R/'cad/engine/generated/timing-cover-seven-fastener-candidate/block.step','full block')]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();inputs={str(p.relative_to(R)):sha(p)for p in [Path(__file__),mp,Path(seven.__file__),R/'cad/engine/assembly_math.py',R/'cad/engine/cad_metrics.py',*paths.values(),*[p for _,p,_ in stages]]};O=R/'cad/engine/generated/block-fs10-source-datum-investigation';O.mkdir(exist_ok=True);rows=[];out=R/'inventory/engine/block-fs10-source-onset.json'
def norm(s):return b.Compound(children=list(s))if isinstance(s,b.ShapeList)else s
for label,p,kind in stages:
 shape=b.import_step(p)
 for name,part in parts.items():
  common=norm(shape.intersect(part));v=solid_volume(common)if common is not None else 0;row={'stage':label,'kind':kind,'neighbor':name,'default_mm3':v}
  if v>.1:
   try:row['adaptive_mm3']=sum(abs(solid_volume(x,'adaptive'))for x in common.solids())
   except Exception as e:row['adaptive_error']=str(e)
   if label=='original frontjoint land':
    w=O/(name+'-first-land-overlap.step');b.export_step(common,w);row['witness']=str(w.relative_to(R));row['witness_sha256']=sha(w)
  rows.append(row);out.write_text(json.dumps({'status':'RUNNING','rows':rows,'input_sha256':inputs},indent=2)+'\n');print(label,name,v,flush=True)
# Constraint illustration only: source-estimated R65 barrel and R8 station6 boss.
y,z=seven.AXES[5];axis=next(a for a in m['assemblies']if a['id']=='ac-compressor')['position_cad_mm'];radial=math.hypot(y-axis[1],z-axis[2]);required=65+seven.SUPPORT_RADIUS
outboard_axis_y=y+math.sqrt(required**2-(axis[2]-z)**2)
# Inboard bolt corridor preserving a6mm estimated wall around R84.947 gear pocket.
pocket_radius=84.947;inner_axis_y=AXIS[0]+math.sqrt((pocket_radius+6+seven.SUPPORT_RADIUS)**2-(z-AXIS[1])**2)
outer_axis_y=axis[1]-math.sqrt((65+seven.SUPPORT_RADIUS)**2-(z-axis[2])**2)
r={'status':'COMPLETE frozen revision onset research; no geometry changes','rows':rows,'station6':{'axis_yz_mm':[y,z],'compressor_axis_xyz_mm':axis,'current_axis_radial_distance_mm':radial,'declared_case_radius_mm':65,'declared_support_radius_mm':seven.SUPPORT_RADIUS,'barrel_support_required_axis_separation_mm':required,'minimum_compressor_y_if_same_z_and_barrel_guard_mm':outboard_axis_y,'required_compressor_y_shift_mm':outboard_axis_y-axis[1],'hypothetical_station6_y_interval_at_fixed_z_mm':[inner_axis_y,outer_axis_y],'hypothetical_station6_inboard_shift_range_mm':[y-outer_axis_y,y-inner_axis_y],'scope':'Zero-margin analytic feasibility only, estimated radius/wall; not whole flange/cover/belt fit or authorized datum change'},'input_sha256':inputs};assert all(sha(R/p)==h for p,h in inputs.items());out.write_text(json.dumps(r,indent=2)+'\n')
