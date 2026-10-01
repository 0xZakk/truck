#!/usr/bin/env python3
"""Actual source-stage sections; read-only geometry, no trial repair."""
from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
O=R/'cad/engine/generated/block-fs10-source-datum-investigation'
if '--extract' in sys.argv:
 import build123d as b
 from assembly_math import transforms
 m=json.loads((R/'inventory/engine/full-assembly.json').read_text());poses=transforms(m,0);d={x['id']:x for x in m['definitions']};occ={x['id']:x for x in m['occurrences']}
 paths={'original-land':R/'cad/engine/generated/timing-cover-front-joint-candidate/future-block-land.step','seven-block':R/'cad/engine/generated/timing-cover-seven-fastener-candidate/block.step'}
 shapes={n:b.import_step(p) for n,p in paths.items()}
 for n in ('ac-compressor-rear-cylinder','ac-compressor-swashplate-shaft','ac-compressor-piston-5'):
  p=R/d[occ[n]['definition']]['step'].lstrip('/');paths[n]=p;shapes[n]=poses[n]*b.import_step(p)
 curves=[]
 for x in (360,368):
  for name,s in shapes.items():
   sec=b.section(s,section_by=b.Plane(origin=(x,0,0),z_dir=(1,0,0)))
   for e in sec.edges():
    curves.append({'x':x,'name':name,'yz':[[e.position_at(i/120).Y,e.position_at(i/120).Z] for i in range(121)]})
 (O/'sections.json').write_text(json.dumps({'curves':curves,'input_sha256':{str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths.values()}},indent=2)+'\n')
else:
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 dat=json.loads((O/'sections.json').read_text());fig,axes=plt.subplots(1,2,figsize=(13,7));colors={'original-land':'#e99924','seven-block':'#404040','ac-compressor-rear-cylinder':'#1879a8','ac-compressor-swashplate-shaft':'#c93b53','ac-compressor-piston-5':'#2b985a'}
 for ax,x in zip(axes,(360,368)):
  seen=set()
  for row in dat['curves']:
   if row['x']!=x:continue
   n=row['name'];p=row['yz'];ax.plot([v[0] for v in p],[v[1] for v in p],c=colors[n],lw=1.3,label=n if n not in seen else None);seen.add(n)
  ax.scatter([251.9168067],[74.4236903],c='black',marker='+',s=70);ax.annotate('station 6 axis',(251.9168067,74.4236903),xytext=(204,12),arrowprops={'arrowstyle':'->'})
  ax.set(xlim=(195,300),ylim=(0,165),xlabel='Y mm',ylabel='Z mm',title=f'Actual STEP section X={x} mm');ax.set_aspect('equal');ax.grid(alpha=.2);ax.legend(fontsize=7)
 fig.suptitle('Frozen block / FS10 interference: added boss (left), original land (right)\nModel coordinates are estimates; these sections are not a repair proposal')
 fig.tight_layout();fig.savefig(O/'source-onset-sections.png',dpi=160)
