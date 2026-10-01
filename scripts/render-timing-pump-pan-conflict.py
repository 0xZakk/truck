#!/usr/bin/env python3
from pathlib import Path
import sys,json,subprocess,numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-block-support-machining-candidate'
r=json.loads((ROOT/'inventory/engine/timing-pump-foot-pan-witnesses.json').read_text());z=r['witnesses'][0]['cube_center_mm'][2]
if '--extract' in sys.argv:
 sys.path.insert(0,str(ROOT/'cad/engine'))
 import build123d as b
 import oil_drive_layout as drive
 from assembly_math import transforms
 from timing_block_support_machining_candidate import DELTA
 m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());defs={d['id']:d for d in m['definitions']};o=next(o for o in m['occurrences'] if o['id']=='oil-pan');parts={'fixed pan':transforms(m)['oil-pan']*b.import_step(ROOT/defs[o['definition']]['step'].lstrip('/'))}
 parts.update({f'translated support {i+1}':b.Pos(*DELTA)*s for i,s in enumerate(drive.pump_mount_supports())})
 rows={name:[[list(edge.position_at(i/80))[:2] for i in range(81)] for edge in b.section(q,section_by=b.Plane.XY.offset(z)).edges()] for name,q in parts.items()};(OUT/'pump-pan-section.json').write_text(json.dumps(rows));sys.exit(0)
subprocess.run([str(ROOT/'.venv-cad/bin/python'),str(Path(__file__)),'--extract'],check=True)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(12,5));rows=json.loads((OUT/'pump-pan-section.json').read_text())
for name,curves in rows.items():
 for i,curve in enumerate(curves):
  p=np.array(curve);ax.plot(p[:,0],p[:,1],color='#303030' if name=='fixed pan' else '#c74b29',label=name if i==0 else None)
for i,w in enumerate(r['witnesses']):
 x,y,_=w['cube_center_mm'];ax.plot(x,y,'o',color='#2277bb',label='strict positive interior witnesses' if i==0 else None)
ax.set_xlim(175,275);ax.set_ylim(88,113);ax.set_aspect('equal');ax.grid(alpha=.25);ax.legend(loc='lower center');ax.set_xlabel('X mm');ax.set_ylabel('Y mm');ax.set_title(f'Actual CAD section Z={z:.4f} mm — translated feet cross unchanged pan wall');fig.tight_layout();fig.savefig(OUT/'pump-pan-conflict.png',dpi=150)
