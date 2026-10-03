"""Actual candidate triangles against frozen authored Carter rear measurements."""
from pathlib import Path
import json,hashlib,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
R=Path(__file__).resolve().parents[1];P='pump-cover-candidate-20261003';source=R/'reference/engine/pump-source-registration-20261003-measurements.json';j=json.loads(source.read_text());datump=R/'reference/engine/pump-cover-joint-20261003-datums.json';d=json.loads(datump.read_text())['options'][1];p=R/f'reference/engine/{P}-display-data.npz';mesh=np.load(p)
s=np.array(d['pump_mounting_axes_yz_mm'])*[-1,1];target=np.array([q['xy']for q in j['source_holes']])[j['best_by_bolts']['permutation']]*[1,-1]
ss=s-s.mean(0);tt=target-target.mean(0);u,_,v=np.linalg.svd(ss.T@tt);rot=u@v;scale=np.sum((ss@rot)*tt)/np.sum(ss**2);off=target.mean(0)-scale*s.mean(0)@rot
project=lambda yz:(scale*(np.array(yz)*[-1,1])@rot+off)*[1,-1]
vertices=mesh['water-pump-housing__vertices'];faces=mesh['water-pump-housing__faces'];tri=project(vertices[:,1:])[faces];rows=[]
for q in j['outline_samples']:
 x=q['x_px'];near=tri[(tri[:,:,0].min(1)<=x)&(tri[:,:,0].max(1)>=x)];hits=[]
 for i,z in [(0,1),(1,2),(2,0)]:
  a,b=near[:,i],near[:,z];ok=(a[:,0]-x)*(b[:,0]-x)<=0;aa=a[ok];bb=b[ok];dd=bb[:,0]-aa[:,0];good=abs(dd)>1e-9;aa=aa[good];bb=bb[good];dd=dd[good];hits.extend((aa[:,1]+(x-aa[:,0])*(bb[:,1]-aa[:,1])/dd).tolist())
 bounds=[float(min(hits)),float(max(hits))]if hits else None;rows.append({'x_px':x,'source_width_px':q['source_width_px_at220'],'source_bounds_px':q['source_threshold_y_bounds'][2],'candidate_bounds_px':bounds,'candidate_width_px':None if bounds is None else bounds[1]-bounds[0]})
fig,ax=plt.subplots(figsize=(9,9));colors=['#c6d8dc','#c8ac74','#86939d']
for n,color in zip(['water-pump-housing','heater-pump-return-elbow','water-pump-impeller'],colors):
 vs=mesh[n+'__vertices'];fs=mesh[n+'__faces'];tris=project(vs[:,1:])[fs];ax.add_collection(PolyCollection(tris,facecolors=color,edgecolors='none',alpha=1))
for q in rows:
 x=q['x_px'];a,b=q['source_bounds_px'];ax.plot([x,x],[a,b],color='#ad432f',linewidth=2)
ax.scatter(*np.array([z['xy']for z in j['source_holes']]).T,color='black',s=12,label='Carter bolt centers');ax.plot([],[],color='#ad432f',label='Authored Carter silhouette widths');ax.plot([],[],color=colors[0],linewidth=8,label='Actual candidate projected housing')
ax.set_xlim(200,1800);ax.set_ylim(1990,0);ax.set_aspect('equal');ax.set_title('Carter rear-pattern registration of actual option B CAD\nBroad inlet-arm mismatch remains; no independent metric camera');ax.set_xlabel('Carter image x / px');ax.set_ylabel('Carter image y / px');ax.legend(loc='upper right',fontsize=8);fig.tight_layout();png=R/f'reference/engine/{P}-source-compare.png';fig.savefig(png,dpi=150);plt.close(fig)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r={'scope':'Actual exported STEP display triangles against frozen authored Carter pixel measurements. No source pixels redistributed.','bolt_rms_px':float(np.sqrt(np.mean(np.sum((scale*s@rot+off-target)**2,axis=1)))),'scale_px_per_estimated_candidate_mm':float(scale),'source_registration':'Proper 2D similarity with current four bolt axes; source fifth/azimuth/source uncertainties preserved in prior frozen report','outline':rows,'verdict':'Source exterior fidelity remains FAIL/open: modeled arm too narrow/short under conditional rear comparison. This candidate tests coordinated joint, not shape acceptance.','limits':['Rear photo projection does not measure actual crosssections or prove depth.','Carter tower/ribs remain underspecified, not production contours.','Clocking is derived from common-face layout; camera roll is fitted separately.'],'inputs':{str(z.relative_to(R)):sha(z)for z in [source,datump,p,Path(__file__)]},'image':{'path':str(png.relative_to(R)),'sha256':sha(png)}};(R/f'reference/engine/{P}-source-compare.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
