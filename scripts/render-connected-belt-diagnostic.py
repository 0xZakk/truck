"""Planar plot of existing assumed stations; no fitted replacement geometry."""
import json,math
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Rectangle
ROOT=Path(__file__).resolve().parents[1]
r=json.loads((ROOT/'inventory/engine/connected-outlet-pump-belt-validation.json').read_text());s=r['solution']
fig,ax=plt.subplots(figsize=(11,8))
for n in s['nodes']:
 ax.add_patch(Circle(n['center'],n['radius'],facecolor='#d4e3ee',edgecolor='#34506a'))
 ax.text(*n['center'],n['id'],ha='center',va='center',fontweight='bold')
for span in s['spans']:
 ax.plot([span['start'][0],span['end'][0]],[span['start'][1],span['end'][1]],color='#3e677f',lw=3)
for arc,n in zip(s['arcs'],s['nodes']):
 a=math.atan2(arc['start'][1]-n['center'][1],arc['start'][0]-n['center'][0]);w=math.radians(arc['wrap_degrees']);angles=[a-n['side']*w*i/120 for i in range(121)]
 ax.plot([n['center'][0]+arc['path_radius']*math.cos(q) for q in angles],[n['center'][1]+arc['path_radius']*math.sin(q) for q in angles],color='#3e677f',lw=3)
ax.scatter([0,-42],[295,295],color='#b43730',marker='x',s=110)
ax.annotate('Outlet + heater supply interfere\nwith this unaccepted belt route',xy=(0,315),xytext=(-350,530),arrowprops={'arrowstyle':'->','color':'#b43730'},color='#8d2b25')
ax.text(-400,-155,f"Outside-radius loop: {r['outside_radius_loop_mm']:.1f} mm  |  Illustrative cord: {r['illustrative_cord_path_mm']:.1f} mm\nCatalog comparison: 2491 mm (effective gauge not established)\nAll station coordinates remain provisional; this plot is a diagnostic, not a factory drawing.",fontsize=10)
ax.set(xlim=(-430,440),ylim=(-180,580),xlabel='Model lateral Y (mm)',ylabel='Model vertical Z (mm)',title='Current accessory layout still cannot accept a belt')
ax.set_aspect('equal');ax.grid(alpha=.2);fig.tight_layout()
fig.savefig(ROOT/'reference/engine/connected-belt-diagnostic.png',dpi=160)
