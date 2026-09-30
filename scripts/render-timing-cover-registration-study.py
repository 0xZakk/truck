#!/usr/bin/env python3
"""Plots derived registration data, never embeds licensed source pictures."""
from pathlib import Path
import json,numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/timing-cover-registration-study';a=np.load(O/'registration-preview.npz');r=json.loads((R/'inventory/engine/timing-cover-registration-validation.json').read_text());fit=r['image_fit'];alt=r['estimated_coordinated_alternative'];p=alt['parameters'];fig,axes=plt.subplots(2,2,figsize=(15,11))
ax=axes[0,0];h=a['holes'];back=a['back'];H=a['H'];q=np.c_[h,np.ones(7)]@H.T;q=q[:,:2]/q[:,2,None]
ax.plot(back[:,0],back[:,1],'o-',color='#5681a0',label='Observed seven bosses (002)');ax.scatter(q[:,0],q[:,1],marker='+',s=80,color='#a8573c',label='Projected source hole centers')
for i,(x,y) in enumerate(back):ax.text(x+8,y+8,str(i+1))
ax.invert_yaxis();ax.set_aspect('equal');ax.set_title('Camera fit, not a CAD transform\nReflection and perspective are required');ax.set(xlabel='Photo x (pixels)',ylabel='Photo y (pixels)');ax.legend(fontsize=8)
ax=axes[0,1];q=a['aperture'];c=a['fit'];ax.scatter(q[:,0],q[:,1],s=14,label='Inverse-mapped aperture boundary');ax.add_patch(Circle(c[:2],c[2],fill=False,color='#5681a0'));ax.scatter(c[0],c[1],marker='+',s=100,label='Boundary-fit crank point');ax.scatter(595,955,marker='x',s=60,label='Previous assumed point')
b=np.array(fit['pixel_only_95percent_interval']);ax.add_patch(Rectangle(b[0,:2],*(b[1,:2]-b[0,:2]),facecolor='#a8573c',alpha=.2,label='95% pixel-only interval'));ax.invert_yaxis();ax.set_aspect('equal');ax.set_title('Aperture-based estimate in source-gasket view\nDepth parallax remains an unbounded systematic error');ax.set(xlabel='Source x (reference pixels)',ylabel='Source y (reference pixels)');ax.legend(fontsize=8,loc='upper right')
poly=a['proposed_outline'];ends=a['ends'];theta=np.linspace(-np.pi,0,100);Y=np.r_[-140,-50,np.linspace(-50,50,100),50,116.6];Z=np.r_[-32,-32,-np.sqrt(59.4**2-np.linspace(-50,50,100)**2),-32,-32]
for ax in axes[1]:
 ax.fill(poly[:,0],poly[:,1],color='#bd995b',alpha=.65,label='Same source outline, uniform scale');ax.plot(Y,Z,color='#397eb2',lw=3,label='Current pan seat estimate');ax.scatter([0],[0],marker='+',s=100,color='black',label='Fixed crank axis');ax.plot(ends[:,0],ends[:,1],'s',color='#a8573c',ms=4,label='Required terminal corridor');ax.set_aspect('equal');ax.set(xlabel='Y (model mm)',ylabel='Z (model mm)')
for c,col in [((90,72),'#8060a0'),((95.109821,76.087857),'#47916e')]:
 axes[1,0].add_patch(Circle(c,83.947,fill=False,color=col));axes[1,0].add_patch(Circle(c,86.947,fill=False,color=col,ls='--',alpha=.6))
axes[1,0].add_patch(Circle((0,0),43.18,fill=False,color='black',ls=':'));axes[1,0].set(xlim=(-155,265),ylim=(-80,220));axes[1,0].set_title('Estimated coordinated envelope, not an installed joint\nSolid circles: cam tips; dashed: clearance + wall');axes[1,0].legend(fontsize=7,loc='upper left')
ax=axes[1,1];ax.set(xlim=(-155,220),ylim=(-75,5));ax.scatter([-85,0,85],[-39.6,-67,-39.6],marker='x',color='#397eb2',s=60,label='Current three front bolt stations');ax.set_title('Pan changes required by the estimated envelope\n25 fastener count retained; locations unchanged pending review');ax.legend(fontsize=7,loc='upper center',bbox_to_anchor=(.5,-.35),ncol=2)
for ax in axes.flat:ax.grid(alpha=.2)
fig.suptitle('Source registration and bounded joint feasibility — no canonical geometry changed',fontsize=15);fig.tight_layout();fig.savefig(O/'registration-review.png',dpi=160)
