#!/usr/bin/env python3
"""Render actual frozen trial STEP and selected actual posed neighbors."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/accessory-psac-carrier';trial=sys.argv[1];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if '--extract' in sys.argv:
 import trimesh
 import build123d as b
 sys.path.insert(0,str(R/'cad/engine'));from assembly_clockwise_candidate import transforms
 mp=R/'inventory/engine/corrected-engine-stage-v3.json';m=json.loads(mp.read_text());t=transforms(m,0,0);ds={d['id']:d for d in m['definitions']};sel=json.loads((R/'inventory/engine/accessory-constrained-layout-step-check.json').read_text());e=json.loads((R/'inventory/engine/accessory-constrained-layout-envelopes.json').read_text());groups={n:g for g,ids in e['moving_occurrence_ownership'].items()for n in ids};tri=[];names=[];inputs={str(mp.relative_to(R)):sha(mp)}
 def add(v,f,name):
  vv=np.asarray(v)[np.asarray(f)];tri.extend(vv);names.extend([name]*len(vv))
 for o in m['occurrences']:
  n=o['id']
  if trial=='tool-access':continue
  if n not in ['timing-cover','water-pump-housing','ps-pump-housing','ps-pump-reservoir','ps-pump-pulley','ac-compressor-front-cylinder','ac-compressor-rear-cylinder','ac-compressor-clutch-pulley','tensioner-spring-cartridge','tensioner-moving-arm','tensioner-pulley-wheel']:continue
  p=R/ds[o['definition']]['glb'].lstrip('/');inputs[str(p.relative_to(R))]=sha(p);mm=trimesh.load(p,force='mesh');v=np.array(mm.vertices)[:,[0,2,1]]*[1,-1,1]*1000;tr=t[n].wrapped.Transformation();a=np.array([[tr.Value(i,j)for j in range(1,5)]for i in range(1,4)]);v=v@a[:,:3].T+a[:,3]
  if n in groups:v[:,1:]+=sel['posedelta_yz_mm'][groups[n]]
  add(v,mm.faces,'accessory'if n in groups else'fixed')
 paths=[O/f'{trial}-carrier.step',*O.glob(f'{trial}*overlap*.step')]
 for p in paths:
  inputs[str(p.relative_to(R))]=sha(p);s=b.import_step(p);v,f=s.tessellate(.15,.3);add([tuple(q)for q in v],f,('carrier'if p.name.endswith('-carrier.step')else('overlap'if 'overlap'in p.name else('accessory'if p.name=='lower-engine-bolt-tool.step'else'fixed'))))
 np.savez_compressed(O/f'{trial}-review.npz',triangles=np.array(tri),names=np.array(names));(O/f'{trial}-render-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
else:
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.collections import PolyCollection
 from matplotlib.colors import to_rgb
 d=np.load(O/f'{trial}-review.npz');vv=d['triangles'];names=d['names'];colors={'fixed':'#a3a9b3','accessory':'#d4ac70','carrier':'#409991','overlap':'#df2448'};normal=np.cross(vv[:,1]-vv[:,0],vv[:,2]-vv[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12);shade=.5+.5*np.abs(normal@np.array([.8,-.3,.5]));rgb=np.array([to_rgb(colors[n])for n in names])*shade[:,None]
 fig,axs=plt.subplots(1,2,figsize=(14,8))
 for ax,basis,depth,title in [(axs[0],np.array([[0,1,0],[0,0,1]]),np.array([1,0,0]),'Front view'),(axs[1],np.array([[-.53,.85,0],[-.32,-.20,.925]]),np.array([.786,.491,.383]),'Oblique view • depth of ribs')]:
  p=vv@basis.T;ix=np.argsort(vv.mean(1)@depth);ax.add_collection(PolyCollection(p[ix],facecolors=rgb[ix],edgecolors='none',rasterized=True));red=names=='overlap';ax.add_collection(PolyCollection(p[red],facecolors='#df2448',edgecolors='none',alpha=.8));ax.autoscale();ax.set_aspect('equal');ax.invert_xaxis();ax.set_title(title);ax.grid(alpha=.12)
 fig.suptitle(f'PS/AC/tensioner carrier {trial} • actual STEP • conditional study',fontsize=16);fig.text(.5,.04,('Teal: carrier    Gold: estimated tool    Gray: separate nominal inlet hypothesis    Red: actual tool overlap' if trial=='tool-access' else 'Teal: carrier    Gold: accessories    Gray: v3 fixed context    Red: failed overlap witnesses')+'\nEstimated load-path prototype; factory silhouette, retention and installed acceptance remain unverified.',ha='center');fig.tight_layout(rect=[0,.10,1,.94]);fig.savefig(O/f'{trial}-review.png',dpi=160)
