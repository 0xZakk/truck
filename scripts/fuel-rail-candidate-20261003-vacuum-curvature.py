from pathlib import Path
import numpy as np,math,json
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003';r={}
for label,sign in [('plus',1),('minus',-1)]:
 p=np.array([(174.136,-163+24*sign,420),(174.136,-163+24*sign,444),(145,(-120 if sign==1 else -170),460),(80,-90,460),(0,-95,460),(0,-75,460)])
 t=np.linspace(0,1,10001)
 def ev(c):
  n=len(c)-1;return sum(math.comb(n,k)*((1-t)**(n-k)*t**k)[:,None]*c[k] for k in range(n+1))
 v=ev(p);d=ev(5*np.diff(p,axis=0));dd=ev(20*np.diff(p,n=2,axis=0));cross=np.linalg.norm(np.cross(d,dd),axis=1);rad=np.linalg.norm(d,axis=1)**3/np.maximum(cross,1e-100);idx=int(np.argmin(rad));bad=rad<=6
 r[label]={'sample_count':len(t),'minimum_sampled_centerline_radius_mm':float(rad[idx]),'t_at_min':float(t[idx]),'point_at_min_mm':v[idx].tolist(),'endpoint_radius_mm':float(rad[-1]),'outer_radius_mm':6,'radius_not_greater_than_outer_count':int(sum(bad)),'bad_t_interval':[float(t[bad][0]),float(t[bad][-1])] if any(bad) else None,'status':'FAIL local swept surface regularity' if any(bad) else 'PASS sampled local criterion; global self-intersection NOT proven'};print(label,r[label])
(OUT/'r5/vacuum-curvature.json').write_text(json.dumps(r,indent=2)+'\n')
