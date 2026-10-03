from pathlib import Path
import json,math,numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'cad/engine/generated/act-host-estimate-20261002-registration'
report=json.loads((ROOT/'reference/engine/act-host-estimate-20261002-registration.json').read_text())
pts=np.array(list(report['pixel_landmarks'].values()))
# Authored diagram only; no source pixels.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(1,2,figsize=(12,5))
for label,p in zip(('A','B','Boss P','Probe T','Connector C'),pts):
 ax[0].plot(*p,'o');ax[0].annotate(label,p,xytext=(4,5),textcoords='offset points')
for i,j in ((0,1),(2,3),(3,4)):ax[0].plot(pts[[i,j],0],pts[[i,j],1],'-')
ax[0].invert_yaxis();ax[0].set_aspect('equal');ax[0].set_title('Source pixel landmarks (authored reconstruction)');ax[0].set_xlabel('image pixels — no world pose');ax[0].grid(alpha=.2)
for beta in (-60,-30,0,30,60):
 t=math.radians(beta);ax[1].plot([0,math.cos(t)],[0,math.sin(t)],label=f'{beta}°')
ax[1].set_aspect('equal');ax[1].set_title('Different 3D axes, identical projected direction');ax[1].set_xlabel('component along projected sensor direction');ax[1].set_ylabel('unobserved view-depth component');ax[1].legend();ax[1].grid(alpha=.2)
fig.suptitle('ACT registration sensitivity — no installed or clearance claim')
fig.tight_layout();fig.savefig(OUT/'act-host-estimate-20261002-sensitivity.png',dpi=150)
