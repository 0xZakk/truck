from pathlib import Path
import numpy as np,hashlib,json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
R=Path(__file__).resolve().parents[1];p=R/'reference/engine/pump-cover-candidate-20261003-display-data.npz';d=np.load(p);names=[k[:-10]for k in d if k.endswith('__vertices')]
fig=plt.figure(figsize=(14,10),facecolor='#f8fafb')
panels=[('Rear attachment / four pads + fifth aperture',0,180),('Side / short tower + peripheral inlet',0,90),('Front-quarter exterior surfaces',25,-35),('Actual v4: head / outlet / carrier conflicts',22,145)]
colors={'water-pump-housing':'#89a8ae','heater-pump-return-elbow':'#cfad66','water-pump-impeller':'#7e878f','water-pump-gasket':'#bba27a','water-pump-drive-hub':'#b8814d','water-pump-pulley':'#344966'}
neighbor=['timing-cover','timing-cover-mounting-screw-3','thermactor-engine-bolt-1','alternator-thermactor-common-carrier','coolant-outlet-housing','coolant-outlet-gasket','cylinder-head','head-gasket']
for k,(title,elev,azim)in enumerate(panels):
 ax=fig.add_subplot(2,2,k+1,projection='3d');ax.set_facecolor('#f8fafb');alltris=[];allcolors=[]
 for n in names:
  if k<3 and(n in neighbor or n=='water-pump-pulley'):continue
  vs=d[n+'__vertices'];fs=d[n+'__faces'];tris=vs[fs]
  norm=np.cross(tris[:,1]-tris[:,0],tris[:,2]-tris[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-12)
  light=np.array([.4,-.5,.75]);light/=np.linalg.norm(light);shade=.65+.35*np.abs(norm@light)
  col=np.array(to_rgb(colors.get(n,'#abb2ba'if n not in neighbor else'#c87668')))[None,:]*shade[:,None]
  alltris.append(tris);allcolors.append(col)
 # One collection makes depth ordering work across parts. QC meshes remain unchanged.
 ax.add_collection3d(Poly3DCollection(np.concatenate(alltris),facecolors=np.concatenate(allcolors),edgecolor='none',zsort='average'))
 ax.set(xlim=(345,495),ylim=(-190,65),zlim=(40,465));ax.set_box_aspect((150,255,425));ax.view_init(elev,azim);ax.set_proj_type('ortho');ax.set_axis_off();ax.set_title(title,fontsize=12)
fig.suptitle('Coordinated pump option B · 98.43 mm mounting-to-hub height\nSource-led joint estimate: 14 actual v4 collisions retained',fontsize=17)
fig.text(.5,.018,'Actual exported STEP surfaces · display-only tessellation · no source pixels redistributed · spring internal and omitted',ha='center',fontsize=10)
fig.subplots_adjust(top=.9,bottom=.05,wspace=.01,hspace=.05)
out=R/'reference/engine/pump-cover-candidate-20261003-review.png';fig.savefig(out,dpi=140)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(R/'reference/engine/pump-cover-candidate-20261003-render.json').write_text(json.dumps({'image':str(out.relative_to(R)),'sha256':sha(out),'data_sha256':sha(p),'script_sha256':sha(Path(__file__)),'source_pixels_excluded':True,'scope':'actual exported STEP surfaces with display-only coarse tessellation; full GLB QC unchanged; actual v4 neighbor STEP; useful viewpoints not camera registration'},indent=2)+'\n')
