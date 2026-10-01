#!/usr/bin/env python3
"""Section proposal only: dashed paths are estimates, not built geometry."""
from pathlib import Path
import json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
R=Path(__file__).resolve().parents[1];I=R/'cad/engine/generated/timing-cover-attachment-v2';O=R/'cad/engine/generated/timing-pan-access-proposal';O.mkdir(parents=True,exist_ok=True)
a=np.load(I/'preview.npz');names=json.loads((I/'names.json').read_text())
def section(ax,name,y,color,label=None):
 i=names.index(name);t=a['v'+str(i)][a['f'+str(i)]];segs=[]
 for tri in t[(t[:,:,1].min(1)<=y)&(t[:,:,1].max(1)>=y)]:
  hits=[]
  for p,q in zip(tri,np.roll(tri,-1,axis=0)):
   if(p[1]<y<=q[1])or(q[1]<y<=p[1]):hits.append((p+(q-p)*(y-p[1])/(q[1]-p[1]))[[0,2]])
  if len(hits)==2:segs.append(hits)
 ax.add_collection(LineCollection(segs,colors=color,linewidths=1.3,label=label or name))
fig,axes=plt.subplots(2,2,figsize=(15,11))
ax=axes[0,0]
for n,col in [('pan','#999999'),('pan-gasket','#356ea0'),('oil-pan-mounting-screw-23','#a57437'),('oil-pan-mounting-washer-23','#704d29')]:section(ax,n,0,col)
# Oil is left of both front wall surfaces; exterior tool space is right.
ax.fill([350,360,360,374,374,350],[-95,-95,-76,-76,-65.4,-65.4],color='#509dcc',alpha=.10)
ax.plot([378,378,363,363],[-65.4,-80,-80,-95],'--',color='#167a55',lw=2,label='Proposed outer wall / shoulder')
ax.plot([374,374,360,360],[-65.4,-76,-76,-95],'--',color='#167a55',lw=1)
ax.fill_between([379,401],-98,-65.4,color='#eac36c',alpha=.22,label='Estimated 22 mm OD socket corridor')
ax.annotate('Wet oil region',(360,-86));ax.annotate('Dry exterior access',(381,-93),fontsize=9)
ax.set(xlim=(348,406),ylim=(-99,-57),title='A. Actual center section + broad setback proposal',xlabel='X mm',ylabel='Z mm');ax.legend(fontsize=7,loc='upper left');ax.set_aspect('equal')
ax=axes[0,1];ys=np.linspace(-149,213,1200);dimples=np.ones_like(ys)*399
for y0 in [-110,0,180]:
 d=np.abs(ys-y0);w=np.where(d<=13,1,np.where(d<28,(1+np.cos(np.pi*(d-13)/15))/2,0));dimples=np.minimum(dimples,399-21*w)
ax.plot(ys,np.ones_like(ys)*399,color='#999',label='Frozen outer front wall')
ax.plot(ys,np.ones_like(ys)*378,'--',color='#167a55',label='Broad setback: outer X378')
ax.plot(ys,dimples,':',color='#965ab0',lw=2,label='Three local inward recesses')
for y0 in [-110,0,180]:
 ax.add_patch(plt.Circle((y0,390),11,fill=False,color='#a57437'));ax.plot(y0,390,'+',color='#a57437')
ax.text(-140,370,'Wet side');ax.text(-140,405,'Dry side / front')
ax.set(xlim=(-155,219),ylim=(362,411),xlabel='Y mm',ylabel='X mm',title='B. Plan comparison; 22 mm tool envelopes estimated');ax.legend(fontsize=8,loc='lower right');ax.set_aspect('equal')
ax=axes[1,0]
for n,col in [('pan','#999999'),('pan-gasket','#356ea0'),('oil-pan-mounting-screw-10','#a57437'),('oil-pan-mounting-washer-10','#704d29')]:section(ax,n,196,col)
ax.set(xlim=(353,378),ylim=(-41,-22),title='C. Station 10: actual sloping transition conflict',xlabel='X mm',ylabel='Z mm');ax.set_aspect('equal');ax.legend(fontsize=7)
ax=axes[1,1];ax.axis('off');ax.text(0,1,'Preferred next hypothesis: broad setback',fontsize=14,va='top');ax.text(0,.88,'• Simpler continuous wall than three tightly blended dimples.\n• Proposed 4 mm wall: inner X374, outer X378.\n• Preserve complete washer pads and gasket lands above.\n• Join unchanged lower body (inner X360 / outer X363)\n  through the revised shoulder between Z−76 and −80.\n• At center, estimated socket radius 11 mm begins X379:\n  1 mm clearance to proposed dry-side wall.\n• Station 10 needs a separate flat dry-side pad transition.\n\nUnknown / not proved: stamping radii, tool dimensions,\n3D wet-volume continuity, side-wall closure and all minimum\nwall sections. Dashed lines are not accepted geometry.\nRear X≤335 and all fastener axes must remain unchanged.',fontsize=11,va='top',linespacing=1.5)
for ax in axes.flat:
 if ax.axison:ax.grid(alpha=.15)
fig.suptitle('Pan access proposal only — actual frozen mesh with explicitly estimated alternatives',fontsize=15);fig.tight_layout(rect=(0,0,1,.96));fig.savefig(O/'section-proposal.png',dpi=160)
r={'scope':'Unbuilt section proposal; no geometry changes','preferred_hypothesis':'Broad inward front-wall setback, pending root review','estimated_outer_inner_x_mm':[378,374],'estimated_wall_mm':4,'estimated_tool_diameter_mm':22,'center_tool_to_outer_wall_clearance_mm':1,'fixed_front_axes':[[390,-110],[390,0],[390,180]],'actual_lower_body_center_section':{'z_mm':-82,'outer_x_mm':363,'inner_x_mm':360},'station10':'Actual section shows steep transition intersecting head/washer; requires separately shaped pad/transition, not just front wall setback.','minimum_wall_3d':'NOT RUN','oil_volume_continuity':'NOT RUN','full_tool_sweep':'NOT RUN','source_limit':'No source establishes these recess dimensions. Broad wall versus local dimples is an explicit estimated stamping comparison.','input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in [I/'preview.npz',I/'names.json',R/'inventory/engine/timing-cover-attachment-v2-validation.json']}}
(R/'reference/engine/timing-pan-access-proposal.json').write_text(json.dumps(r,indent=2)+'\n')
