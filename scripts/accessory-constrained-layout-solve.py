#!/usr/bin/env python3
"""Coupled constrained centers; no catalog-length optimization or asset edits."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
from scipy.optimize import minimize
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import accessory_belt as belt
p=R/'inventory/engine/accessory-constrained-layout-envelopes.json';j=json.loads(p.read_text());groups=['ALT','AP','PS','AC','TENS'];index={g:i for i,g in enumerate(groups)};prior=np.array([j['current_centers_yz_mm'][g] for g in groups]).ravel();reserve=1.
ns=[];cs=[];grows=[];hrows=[];starts=[];meta=[]
payload=R/j['obstacle_file'];assert hashlib.sha256(payload.read_bytes()).hexdigest()==j['obstacle_sha256']
for row in json.loads(payload.read_text()):
 v=np.array(row['polygon']);delta=np.roll(v,-1,axis=0)-v;n=np.c_[delta[:,1],-delta[:,0]];n/=np.linalg.norm(n,axis=1)[:,None];c=np.sum(n*v,axis=1);starts.append(len(ns));ns.extend(n);cs.extend(c);grows.extend([index[row['group']]]*len(n));hrows.extend([index[row['other_group']] if 'other_group'in row else -1]*len(n));meta.append({k:v for k,v in row.items() if k!='polygon'})
N=np.array(ns);C=np.array(cs);G=np.array(grows);H=np.array(hrows);starts=np.array(starts);ends=np.r_[starts[1:],len(N)];count=len(starts)
def margins(x):
 q=x.reshape(-1,2);v=np.sum(N*(q[G]-np.where((H>=0)[:,None],q[np.maximum(H,0)],0)),axis=1)-C;return np.maximum.reduceat(v,starts)-reserve
# Exact linear source-order constraints: gap1mm is numerical strict ordering.
A=[];B=[]
def order(g,axis,h=None,otheraxis=None,constant=0):
 a=np.zeros(10);a[2*index[g]+axis]=1
 if h:a[2*index[h]+(axis if otheraxis is None else otheraxis)]-=1
 A.append(a);B.append(constant+1)
order('PS',1,'TENS');order('TENS',1,'ALT');order('ALT',1,'AP');order('AP',1,constant=0);order('AC',1,constant=0)
# AC below fixedWP170; TENS inboard ofPS.
a=np.zeros(10);a[2*index['AC']+1]=-1;A.append(a);B.append(-169);order('PS',0,'TENS')
A=np.array(A);B=np.array(B)
def cons(x):return np.r_[margins(x),A@x-B]
def jac(x):
 q=x.reshape(-1,2);v=np.sum(N*(q[G]-np.where((H>=0)[:,None],q[np.maximum(H,0)],0)),axis=1)-C;chosen=np.array([a+np.argmax(v[a:z])for a,z in zip(starts,ends)]);out=np.zeros((count,10));i=np.arange(count);out[i,2*G[chosen]]=N[chosen,0];out[i,2*G[chosen]+1]=N[chosen,1];mask=H[chosen]>=0;ii=i[mask];hh=H[chosen][mask];out[ii,2*hh]-=N[chosen][mask,0];out[ii,2*hh+1]-=N[chosen][mask,1];return np.r_[out,A]
def objective(x):
 d=(x-prior)/100;column=(x[2*index['PS']]-x[2*index['AC']])/100;return float(d@d+column*column)
def gradient(x):
 g=2*(x-prior)/10000;column=2*(x[4]-x[6])/10000;g[4]+=column;g[6]-=column;return g
bounds=[(-500,-80),(180,450),(-450,-70),(20,220),(120,500),(220,520),(120,500),(20,169),(20,350),(180,480)]
rng=np.random.default_rng(32034);seeds=[prior,prior+np.array([-75,0,-75,0,75,30,75,0,0,30])]
for k in range(6):seeds.append(np.array([rng.uniform(a,z)for a,z in bounds]))
runs=[];report=R/'inventory/engine/accessory-constrained-layout-solve.json'
for k,seed in enumerate(seeds):
 s=minimize(objective,seed,jac=gradient,method='SLSQP',bounds=bounds,constraints={'type':'ineq','fun':cons,'jac':jac},options={'maxiter':450,'ftol':1e-10});c=cons(s.x);bad=np.argsort(c)[:12];row={'seed':k,'solver_success':bool(s.success),'message':str(s.message),'objective':float(s.fun),'minimum_constraint_mm':float(c.min()),'numerically_feasible':bool(c.min()>=-1e-5),'centers_yz_mm':{g:s.x[2*i:2*i+2].tolist()for i,g in enumerate(groups)},'active_or_failed_constraints':[{'margin_mm':float(c[i]),'constraint':meta[i] if i<count else {'ordering_row':int(i-count)}}for i in bad]};runs.append(row);report.write_text(json.dumps({'status':'RUNNING','runs':runs},indent=2)+'\n');print(k,row['numerically_feasible'],row['objective'],row['minimum_constraint_mm'],flush=True)
valid=[r for r in runs if r['numerically_feasible']];best=min(valid,key=lambda r:r['objective'])if valid else None
if best:
 nodes=[dict(n) for n in json.loads((R/'inventory/engine/accessory-common-layout-families.json').read_text())['actual_radial_envelope_nodes']]
 for n in nodes:
  if n['id'] in best['centers_yz_mm']:n['center']=best['centers_yz_mm'][n['id']]
 b=belt.solve(nodes);best['cord_route_length_mm']=b['length'];best['catalog_effective2491_residual_mm']=b['length']-2491;best['wrap_degrees']={v['pulley']:v['wrap_degrees']for v in b['arcs']};best['delta_from_weak_prior_mm']={g:(np.array(best['centers_yz_mm'][g])-np.array(j['current_centers_yz_mm'][g])).tolist()for g in groups}
inputs=[Path(__file__),p,payload,R/'cad/engine/accessory_belt.py',R/'cad/engine/accessory_belt_profile.py',R/'inventory/engine/accessory-common-layout-families.json']
out={'status':'NUMERICAL ENVELOPE FEASIBLE; exactSTEP/support/belt acceptance pending'if best else 'NO FEASIBLE POINT FOUND; not proof of physical impossibility','reserve_mm':reserve,'domains':{g:bounds[2*i:2*i+2]for i,g in enumerate(groups)},'objective':'sum squaredYZ deviations/100mm from weak priors + squaredPS-ACcolumn offset/100mm; no length target','best':best,'runs':runs,'limits':['Conservative axial slab convex hulls, staticq0','Carrier solids deliberately need matched reconstruction; no unsupported seat accepted','Outside envelope/cord/effective mismatch retained','Unverified factory dimensions; not installed'],'input_sha256':{str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest()for q in inputs}}
report.write_text(json.dumps(out,indent=2)+'\n')
