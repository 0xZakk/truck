#!/usr/bin/env python3
"""Tighten weak strict-order and catalog-edge solutions; no relaxed gates."""
from pathlib import Path
import json,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];source=R/'scripts/accessory-constrained-layout-catalog-solve.py';text=source.read_text();env={'__file__':str(source)};exec(compile(text.split('rng=np.random.default_rng')[0],str(source),'exec'),env)
base=json.loads((R/'inventory/engine/accessory-constrained-layout-catalog-solve.json').read_text());seed=np.array([base['best']['centers_yz_mm'][g]for g in env['groups']]).ravel();original_B=env['B'].copy();old_window=env['length_window']
# Require5mm interior to both sides of assumed length interval. This is a
# numerical robustness reserve, not a Gates manufacturing tolerance.
def robust_window(x):return old_window(x)-5.
env['length_window']=robust_window
rows=[]
for gap in (10.,20.,30.):
 env['B']=original_B.astype(float).copy();env['B'][0]=gap+.286;env['B'][5]=gap-170
 for si,x0 in enumerate([seed,env['prior']]):
  s=env['minimize'](env['objective'],x0,jac=env['gradient'],method='SLSQP',bounds=env['bounds'],constraints={'type':'ineq','fun':env['cons'],'jac':env['jac']},options={'maxiter':650,'ftol':1e-10});c=env['cons'](s.x);order=np.argsort(c)[:8];row={'gap_mm':gap,'seed':si,'success':bool(s.success),'message':str(s.message),'minimum_constraint_mm':float(c.min()),'feasible':bool(c.min()>=-1e-5),'objective':float(s.fun),'centers_yz_mm':{g:s.x[2*i:2*i+2].tolist()for i,g in enumerate(env['groups'])},'effective_interval_mm':[2491-old_window(s.x)[0],2491+old_window(s.x)[1]],'active_or_failed':[{'margin_mm':float(c[i]),'constraint':env['meta'][i]if i<env['count']else {'order_or_length_row':int(i-env['count'])}}for i in order]};rows.append(row);print(gap,si,row['feasible'],row['minimum_constraint_mm'],flush=True)
  if row['feasible']:seed=s.x
out={'status':'COMPLETE robustness screen; no candidate selected','gap_scope':'10/20/30mm are explicit inferred separation hypotheses forPSaboveTENS andWPaboveAC; no dimensions taken from schematic pixels. Extra0.286mm accounts for±5deg75mm arm vertical shift.','length_interior_reserve_mm':5,'length_reserve_scope':'Numerical robustness only, not belt tolerance','rows':rows,'input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [Path(__file__),source,R/'inventory/engine/accessory-constrained-layout-catalog-solve.json',R/'inventory/engine/accessory-constrained-layout-envelopes.json']}}
(R/'inventory/engine/accessory-constrained-layout-order-sensitivity.json').write_text(json.dumps(out,indent=2)+'\n')
