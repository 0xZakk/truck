from pathlib import Path
import numpy as np,math,json
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'reference/engine';r={};fig,ax=plt.subplots(1,2,figsize=(12,5))
for a,(label,sign) in zip(ax,[('plus',1),('minus',-1)]):
 rows={}
 for name,control3 in [('r5_failed',(80,-90,460)),('proposed_C2',(0,-115,460))]:
  p=np.array([(174.136,-163+24*sign,420),(174.136,-163+24*sign,444),(145,(-120 if sign==1 else -170),460),control3,(0,-95,460),(0,-75,460)]);t=np.linspace(0,1,10001)
  def ev(c):
   n=len(c)-1;return sum(math.comb(n,k)*((1-t)**(n-k)*t**k)[:,None]*c[k] for k in range(n+1))
  v=ev(p);d=ev(5*np.diff(p,axis=0));dd=ev(20*np.diff(p,n=2,axis=0));cross=np.linalg.norm(np.cross(d,dd),axis=1);rad=np.linalg.norm(d,axis=1)**3/np.maximum(cross,1e-100);k=int(np.argmin(rad));rows[name]={'controls_mm':p.tolist(),'sampled_min_radius_mm':float(rad[k]),'t_at_min':float(t[k]),'endpoint_second_derivative':dd[-1].tolist(),'sampled_r_le_6_count':int(sum(rad<=6))};a.plot(v[:,0],v[:,1],label=name);a.scatter(p[:,0],p[:,1],s=15)
 a.plot([0,0],[-75,-55],'k-',lw=3,label='Fixed straight socket');a.set(title=label+' top projection',xlabel='X mm',ylabel='Y mm');a.legend(fontsize=8);a.set_aspect('equal');a.grid(alpha=.2);r[label]=rows
report={'status':'ROOT REVIEW REQUIRED BEFORE CAD','purpose':'Remove local sweep fold by zero endpoint curvature, without neighbor-driven routing','outer_radius_mm':6,'inner_radius_mm':4.1,'socket_unchanged':[[0,-75,460],[0,-55,460]],'sole_control_change':{'from':[80,-90,460],'to':[0,-115,460]},'sampling':10001,'variants':r,'evidence':'Geometric estimate; C2 Bezier endpoint from last three collinear equally spaced controls. No factory route or forming limit claim. Global self-intersection/export/context still required.'}
(OUT/'fuel-rail-candidate-20261003-vacuum-path-proposal.json').write_text(json.dumps(report,indent=2)+'\n');fig.suptitle('Proposed curvature regularization; endpoints unchanged, no clash optimization');fig.tight_layout();fig.savefig(OUT/'fuel-rail-candidate-20261003-vacuum-path-proposal.png',dpi=160)
