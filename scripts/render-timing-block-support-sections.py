#!/usr/bin/env python3
"""Actual four-journal YZ sections plus sampled missing support locations."""
from pathlib import Path
import sys,json,subprocess,numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-block-support-machining-candidate'
if '--extract' in sys.argv:
 sys.path.insert(0,str(ROOT/'cad/engine'))
 import build123d as b
 import full_engine as f
 q=b.import_step(OUT/'block.step');rows=[]
 for x in [-334,-110,110,360.5]:
  sec=b.section(q,section_by=b.Plane.YZ.offset(x));rows.append({'x_mm':x,'curves_yz':[[list(edge.position_at(i/80))[1:] for i in range(81)] for edge in sec.edges()]})
 (OUT/'journal-sections.json').write_text(json.dumps({'rows':rows,'radius_mm':f.CAM_BORE_R+.025}));sys.exit(0)
subprocess.run([str(ROOT/'.venv-cad/bin/python'),str(Path(__file__)),'--extract'],check=True)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
section_data=json.loads((OUT/'journal-sections.json').read_text());rows=section_data['rows'];fig,axes=plt.subplots(2,2,figsize=(12,10));t=np.linspace(0,2*np.pi,361);cy,cz=95.1098209901611,76.08785679212888;radius=section_data['radius_mm']
for i,(ax,row) in enumerate(zip(axes.flat,rows),1):
 for curve in row['curves_yz']:
  p=np.array(curve);ax.plot(p[:,0],p[:,1],color='#444444',linewidth=1)
 ax.plot(cy+radius*np.cos(t),cz+radius*np.sin(t),'--',color='#2277bb',label='support probe radius')
 ax.plot(cy+(radius-.025+2)*np.cos(t),cz+(radius-.025+2)*np.sin(t),color='#258b45',label='declared 2mm backing exterior')
 ax.set_xlim(60,135);ax.set_ylim(40,115);ax.set_aspect('equal');ax.set_title(f'Journal {i}: X{row["x_mm"]} mm');ax.set_xlabel('Y mm');ax.set_ylabel('Z mm');ax.grid(alpha=.2);ax.legend(fontsize=8)
fig.suptitle('Support candidate — actual STEP sections; 2mm backing is an educational estimate',fontsize=14);fig.tight_layout(rect=[0,0,1,.96]);fig.savefig(OUT/'journal-support-sections.png',dpi=150)
