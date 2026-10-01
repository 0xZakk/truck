from pathlib import Path
import json,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1];rp=R/'reference/engine/online-heater-radial-registration.json';r=json.loads(rp.read_text());fig,axs=plt.subplots(2,2,figsize=(12,12))
for ax,(name,v)in zip(axs.flat,r['views'].items()):
 p=R/'reference/engine/online-heater-captures'/v['file'];ax.imshow(plt.imread(p));ax.set_xlim(0,600);ax.set_ylim(600,0)
 for i,point in zip(v['indices'],v['mounts']):ax.plot(*point,'rx',ms=8);ax.text(point[0]+6,point[1]+8,'fifth'if i==4 else'M'+str(i+1),color='red',fontsize=9)
 for key,col in [('root','limegreen'),('tip','blue'),('hub_center','magenta'),('pilot_center','magenta')]:
  if v.get(key):ax.plot(*v[key],'+',color=col,ms=12);ax.text(v[key][0]+6,v[key][1]-5,key,color=col,fontsize=8)
 if name=='side':
  for y in[224,404]:ax.axhline(y,color='orange',ls='--',lw=1)
  ax.plot([192,332],[228,228],color='magenta');ax.text(320,188,'D ≈140px\nminor ≈22px',color='purple')
 ax.set_title(name+(' — overdetermined five-hole fit'if name=='rear'else' — tentative/occluded anchors'if name!='side'else' — independent circle/axis ratio'))
fig.suptitle('GMB125-1810 source landmark audit\nRed IDs are declared correspondences; front/oblique IDs remain tentative',fontsize=14);fig.tight_layout();out=R/'reference/engine/online-heater-radial-registration/landmarks.png';fig.savefig(out,dpi=130)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(R/'reference/engine/online-heater-radial-registration-visual.json').write_text(json.dumps({'image':str(out.relative_to(R)),'sha256':sha(out),'inputs':{str(p.relative_to(R)):sha(p)for p in [rp,Path(__file__),*[R/'reference/engine/online-heater-captures'/v['file']for v in r['views'].values()]]},'redistribution':'Annotated manufacturer images are local review only, not an authorized redistributed artifact.'},indent=2)+'\n')
