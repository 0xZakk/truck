#!/usr/bin/env python3
"""Source-topology constrained placement families; analytic diagnostics, no assets."""
from pathlib import Path
import sys,json,hashlib,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import accessory_belt as base
p=R/'inventory/engine/accessory-common-layout-datums.json';j=json.loads(p.read_text());rows={r['id']:r for r in j['rows']};mapping={'ALT':'alternator-pulley','TENS':'tensioner-pulley-wheel','PS':'ps-pump-pulley','AC':'ac-compressor-clutch-pulley','WP':'water-pump-pulley','AP':'thermactor-pulley'}
nodes=[]
for n in base.PULLEYS:
 n=dict(n)
 if n['id'] in mapping:
  r=rows[mapping[n['id']]];n['center']=r['radial_bbox_center_yz_mm'];bb=r['world_bounds'];n['radius']=max(bb['max'][k]-bb['min'][k] for k in (1,2))/2
 nodes.append(n)
results=[]
for family in ('shared_column','compressor_only_matched_lower_carrier'):
 for dy in (0,25,50,75):
  ns=[dict(n) for n in nodes]
  for n in ns:
   if n['id']=='AC' or(family=='shared_column' and n['id']=='PS'):n['center']=[n['center'][0]+dy,n['center'][1]]
  v={n['id']:n for n in ns};solve=base.solve(ns);sep=math.dist(v['AC']['center'],[251.91680672464793,74.42369033067094]);results.append({'family':family,'delta_y_mm':dy,'centers_yz_mm':{k:n['center'] for k,n in v.items()},'ps_ac_column_angle_from_vertical_deg':math.degrees(math.atan2(v['AC']['center'][0]-v['PS']['center'][0],v['PS']['center'][1]-v['AC']['center'][1])),'estimated_barrel_station6_R8_guard_margin_mm':sep-73,'analytic_cord_route_length_mm':solve['length'],'catalog2491_residual_mm':solve['length']-2491,'wrap_degrees':{a['pulley']:a['wrap_degrees'] for a in solve['arcs']},'source_order_pass':v['PS']['center'][1]>v['TENS']['center'][1]>v['ALT']['center'][1] and v['WP']['center'][1]>v['AC']['center'][1]>0,'scope':'No geometry movement/export. Rigid branch internal fit retained by definition; carrier seats/hoses must be revised separately; exact clearances NOT RUN.'})
inputs=[Path(__file__),p,R/'cad/engine/accessory_belt.py',R/'cad/engine/accessory_belt_profile.py']
r={'status':'COMPLETE proposal-family screen; no candidate selected','sampling_reason':'0/25/50/75mm is an explicitly inferred diagnostic grid, not source measurements or a clearance-optimized chosen pose','source_priority':'Shared column retains schematic near-vertical PS-over-AC relationship; staggered family quantifies that visual departure. Both retain source ordering and shared-carrier topology only if matched support is rebuilt.','belt_limits':'Outside radii treated as path radii plus prior comparison offset; profiles/length/tensioner preload are not verified. No belt geometry installed.','actual_radial_envelope_nodes':nodes,'families':results,'input_sha256':{str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest() for q in inputs}}
(R/'inventory/engine/accessory-common-layout-families.json').write_text(json.dumps(r,indent=2)+'\n')
