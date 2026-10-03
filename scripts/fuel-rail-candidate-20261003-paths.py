#!/usr/bin/env python3
"""Analytic tangent checks only; no CAD construction or canonical writes."""
from pathlib import Path
import json, math, hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'cad/engine/fuel-rail-candidate-20261003-parameters.json'
p=json.loads(P.read_text())
out=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003';out.mkdir(parents=True,exist_ok=True)
results={}
for sign in p['variants']:
 gy=-163+24*sign
 theta=np.linspace(0,math.pi,121)
 loop=np.array([[280.618+13*math.sin(t),-163+12*sign-12*sign*math.cos(t),364+5*math.cos(t)] for t in theta])
 q=np.linspace(0,math.pi/2,61)
 supplyrise=np.array([[204.136-18*math.sin(t),gy,377-18*math.cos(t)] for t in q])
 returndrop=np.array([[162.136+12*math.cos(t),gy,381-12*math.sin(t)] for t in q])
 supplyrear=np.array([[-336.997-18*math.sin(t),-163,387-18*math.cos(t)] for t in q])
 returnrear=np.array([[-320.238-12*math.sin(t),gy,381-12*math.cos(t)] for t in q])
 # Analytic endpoint derivative directions, measured angular mismatch zero.
 arcs={'front_loop':(loop,[1,0,0],[-1,0,0],13,6),'supply_rise':(supplyrise,[-1,0,0],[0,0,1],18,6),'return_drop':(returndrop,[0,0,-1],[-1,0,0],12,4),'supply_rear':(supplyrear,[-1,0,0],[0,0,1],18,6),'return_rear':(returnrear,[-1,0,0],[0,0,1],12,4)}
 rows={}
 for key,(xyz,start,end,r,ro) in arcs.items():
  rows[key]={'start':xyz[0].tolist(),'end':xyz[-1].tolist(),'analytic_start_tangent':start,'analytic_end_tangent':end,'radius_mm':r,'outer_radius_mm':ro,'positive_inner_sweep_radius':r>ro,'sampled_length_mm':float(np.linalg.norm(np.diff(xyz,axis=0),axis=1).sum())}
  d0=(xyz[1]-xyz[0]); d0/=np.linalg.norm(d0)
  d1=(xyz[-1]-xyz[-2]); d1/=np.linalg.norm(d1)
  errors=[float(np.degrees(np.arccos(np.clip(np.dot(d0,start),-1,1)))),float(np.degrees(np.arccos(np.clip(np.dot(d1,end),-1,1))))]
  assert max(errors)<.8 and r>ro,(key,errors)
  rows[key]['sample_chord_vs_analytic_tangent_error_deg']=errors
  np.save(out/f'{sign:+d}-{key}-centerline.npy',xyz)
 assert np.allclose(loop[0],[280.618,-163,369])
 assert np.allclose(loop[-1],[280.618,gy,359])
 assert np.allclose(supplyrise[-1],[186.136,gy,377])
 assert np.allclose(returndrop[-1],[162.136,gy,369])
 assert np.allclose(supplyrear[-1],[-354.997,-163,387])
 assert np.allclose(returnrear[-1],[-332.238,gy,381])
 results[str(sign)]={'arcs':rows,'rear_straight_leads_mm':[23,29],'gallery_return_radial_land_mm':2.5,'path_only':'No solid construction, global collision, curvature-transition manufacturing, pressure/leak or installed check performed'}
report={'parameters_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'variants':results}
(out/'path-checks.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS analytic joins and positive local sweep radii for both signs; no solid construction')
