#!/usr/bin/env python3
"""Actual v3 meshes in proposed frames; illustrative cord path is separate."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/accessory-constrained-layout';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((R/'inventory/engine/accessory-constrained-layout-step-check.json').read_text());e=json.loads((R/'inventory/engine/accessory-constrained-layout-envelopes.json').read_text());centers=s['selection']['centers_yz_mm'];groups={n:g for g,ids in e['moving_occurrence_ownership'].items()for n in ids};colors={'ALT':'#e9ae48','AP':'#53bfa5','PS':'#72a9e2','AC':'#df886e','TENS':'#bd8cdf','fixed':'#909ba8'}
if '--extract' in sys.argv:
 import trimesh
 sys.path.insert(0,str(R/'cad/engine'))
 from assembly_clockwise_candidate import transforms
 import accessory_belt as belt
 mp=R/'inventory/engine/corrected-engine-stage-v3.json';assert sha(mp)==e['stage_sha256'];m=json.loads(mp.read_text());t=transforms(m,0,0);ds={d['id']:d for d in m['definitions']};polys=[];rgb=[];depth=[];shades=[];inputs={str(mp.relative_to(R)):sha(mp)}
 # External visible context only; exact checker retains all neighbors.
 fixed={'engine-block','timing-cover','water-pump-housing','water-pump-pulley','crank-pulley','crankshaft-pulley','cylinder-head'}
 for o in m['occurrences']:
  n=o['id'];g=groups.get(n)
  if not g and n not in fixed:continue
  p=R/ds[o['definition']]['glb'].lstrip('/');inputs[str(p.relative_to(R))]=sha(p);mm=trimesh.load(p,force='mesh');v=np.asarray(mm.vertices)[:,[0,2,1]]*[1,-1,1]*1000;tr=t[n].wrapped.Transformation();a=np.array([[tr.Value(i,j)for j in range(1,5)]for i in range(1,4)]);v=v@a[:,:3].T+a[:,3]
  if g:v[:,1:]+=s['posedelta_yz_mm'][g]
  vv=v[np.asarray(mm.faces)];vv=vv[np.max(vv[:,:,0],axis=1)>250];normal=np.cross(vv[:,1]-vv[:,0],vv[:,2]-vv[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12);shades.extend(.45+.55*np.abs(normal@np.array([.8,-.35,.48])));polys.extend(vv[:,:,1:]);depth.extend(vv[:,:,0].mean(1));rgb.extend([g or 'fixed']*len(vv))
 idx=np.argsort(depth);np.savez_compressed(O/'review-mesh.npz',triangles=np.array(polys)[idx],groups=np.array(rgb)[idx],shades=np.array(shades)[idx])
 nodes=json.loads((R/'inventory/engine/accessory-common-layout-families.json').read_text())['actual_radial_envelope_nodes']
 for n in nodes:
  if n['id'] in centers:n['center']=centers[n['id']]
 sol=belt.solve(nodes);(O/'review-route.json').write_text(json.dumps(sol,indent=2)+'\n');(O/'review-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
else:
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.collections import PolyCollection
 from matplotlib.colors import to_rgb
 from matplotlib.patches import Circle
 d=np.load(O/'review-mesh.npz');fig,axs=plt.subplots(1,2,figsize=(15,8));ax=axs[0];ax.add_collection(PolyCollection(d['triangles'],facecolors=[np.array(to_rgb(colors[g]))*v for g,v in zip(d['groups'],d['shades'])],edgecolors='none',linewidths=0,rasterized=True));ax.set_title('Actual meshes • proposed q0 frames\nTwo replacement carriers are absent')
 route=json.loads((O/'review-route.json').read_text());ax=axs[1]
 for n in route['nodes']:
  y,z=n['center'];ax.add_patch(Circle((y,z),n['radius'],color=colors.get(n['id'],'#909ba8'),alpha=.5));ax.text(y,z,n['id'],ha='center',va='center',weight='bold')
 for sp in route['spans']:
  a,b=sp['start'],sp['end'];ax.plot([a[0],b[0]],[a[1],b[1]],color='#26364a',lw=2)
 for arc in route['arcs']:
  n=next(n for n in route['nodes']if n['id']==arc['pulley']);c=np.array(n['center']);a=np.array(arc['start'])-c;theta=np.arctan2(a[1],a[0]);sweep=-np.radians(arc['wrap_degrees'])*arc['side'];angles=theta+np.linspace(0,sweep,80);v=c+arc['path_radius']*np.c_[np.cos(angles),np.sin(angles)];ax.plot(v[:,0],v[:,1],color='#26364a',lw=2)
 for g,pt in centers.items():
  old=e['current_centers_yz_mm'][g];ax.plot(*old,'x',color=colors[g]);ax.annotate('',xy=pt,xytext=old,arrowprops={'arrowstyle':'->','color':colors[g],'lw':1})
 ax.set_title('Outside pulley envelopes + illustrative cord route\nCrosses = inherited weak center priors')
 for ax in axs:ax.set_aspect('equal');ax.set_xlim(-430,440);ax.set_ylim(-110,510);ax.invert_xaxis();ax.set_xlabel('Engine Y (mm) • front view');ax.set_ylabel('Z (mm)');ax.grid(alpha=.15)
 fig.suptitle('Inferred coupled layout — feasibility proposal, not production or installed acceptance',fontsize=16)
 fig.text(.5,.045,'Qualified effective interval 2486–2516 mm includes 2491 mm catalog comparison.\nProfile offsets and ±5° tensioner range are inferred; supports, belt solids, hoses and working range remain unverified.',ha='center',fontsize=11)
 fig.tight_layout(rect=[0,.10,1,.94]);fig.savefig(O/'review.png',dpi=180);plt.close(fig)
