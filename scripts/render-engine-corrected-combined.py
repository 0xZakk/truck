#!/usr/bin/env python3
"""Actual selected combined mesh pose and the retained bolt/block conflict section."""
from pathlib import Path
import sys,json,math,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import numpy as np,trimesh,build123d as b
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from engine_clockwise_pose_candidate import corrected_slider_frames
OUT=ROOT/'cad/engine/generated/engine-corrected-combined-candidate'
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());occ={o['id']:o for o in m['occurrences']};defs={d['id']:d for d in m['definitions']}
layout=json.loads((OUT/'combined-q55-layout.json').read_text());meshpaths=set();triangles=[];colors=[]
for row in layout['parts']:
 key=row['id']
 selected=key in ['crankshaft','camshaft','crank-timing-gear','cam-timing-gear'] or any(key.endswith(s) for s in ['-connecting-rod-1','-rod-cap-1','-piston-1','-rocker','-pushrod','-valve','-lifter-body'])
 if not selected:continue
 p=ROOT/row['source'];gp=p.with_suffix('.glb');offset=np.zeros(3)
 if key=='camshaft':gp=p.with_name('camshaft-local.glb');offset=np.array([0,95.1098209901611,76.08785679212888])
 if not gp.exists():gp=ROOT/defs[occ[key]['definition']]['glb'].lstrip('/')
 meshpaths.add(gp);mesh=trimesh.load(gp,force='mesh');v=mesh.vertices[:,[0,2,1]]*[1,-1,1]*1000+offset
 matrix=np.array(row['matrix_3x4']);v=v@matrix[:,:3].T+matrix[:,3];tri=v[mesh.faces]
 color=np.array([.27,.47,.58]) if key=='crankshaft' else np.array([.16,.54,.46]) if key=='camshaft' else np.array([.76,.50,.27]) if 'piston' in key else np.array([.49,.45,.56]) if 'valve' in key or 'rocker' in key else np.array([.52,.58,.62])
 normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm=np.maximum(np.linalg.norm(normal,axis=1),1e-20);shade=.6+.35*np.abs((normal/norm[:,None])@np.array([.1,-.8,.59]));triangles.append(tri);colors.append(shade[:,None]*color)
tri=np.concatenate(triangles);col=np.concatenate(colors);projection=tri[:,:,[0,2]].copy();projection[:,:,0]+=.12*tri[:,:,1];projection[:,:,1]+=.4*tri[:,:,1];order=np.argsort(tri[:,:,1].mean(1)-.4*tri[:,:,2].mean(1))
fig=plt.figure(figsize=(14,10),facecolor='#f6f7f9');grid=fig.add_gridspec(2,2,height_ratios=[1.2,1])
ax=fig.add_subplot(grid[0,:]);ax.add_collection(PolyCollection(projection[order],facecolors=col[order],edgecolors='none'));ax.autoscale();ax.set_aspect('equal');ax.set_xlabel('Projected shaft X (mm)');ax.set_ylabel('Projected height (mm)');ax.set_title('Actual corrected moving-part meshes · event55° · selected328-part STEP retains fixed neighbors')
blockpath=ROOT/'cad/engine/generated/timing-front-block-expanded-seat-v3-candidate/block.step';boltpath=ROOT/'cad/engine/generated/rod-bolt.step';block=b.import_step(blockpath);bolt=b.import_step(boltpath);frame=corrected_slider_frames(305,0,50.546,157.7,284.48,measured_cad_rest_phase_degrees=0)['rod']*b.Pos(0,-34.5,0);bolt=frame*bolt
ax=fig.add_subplot(grid[1,0])
for shape,color,fill in [(block,'#39434a',False),(bolt,'#b87831',True),(block.intersect(bolt),'#bb3038',True)]:
 section=b.section(shape,section_by=b.Plane.YZ.offset(284.48))
 for wire in section.wires():
  p=np.array([tuple(wire.position_at(i/256))[1:] for i in range(257)])
  if fill:ax.fill(p[:,0],p[:,1],color=color,alpha=.7)
  else:ax.plot(p[:,0],p[:,1],color=color,lw=2)
ax.scatter(-73.3626001126,65.2474860469,color='#9d1725',s=20,zorder=5);ax.set_xlim(-82,-62);ax.set_ylim(54,77);ax.set_aspect('equal');ax.grid(alpha=.2);ax.set_xlabel('World Y (mm)');ax.set_ylabel('World Z (mm)');ax.set_title('Actual c1 bolt/block section · corrected event305°')
ax=fig.add_subplot(grid[1,1]);ax.axis('off');ax.text(.02,.93,'Inherited interference remains',fontsize=18,weight='bold',color='#a22c35');ax.text(.02,.78,'Six bolt/block samples fail: 2.716 mm³ each.\nThe red section contains a strict interior\nmaterial witness, not only touching faces.',fontsize=12,linespacing=1.5);ax.text(.02,.52,'Old canonical geometry produces the same\nconflict at old event55°. The estimated bolt\nhead and R98 crankcase need source review.',fontsize=12,linespacing=1.5);ax.text(.02,.24,'Crank/block/pan sweep bounds pass.\nPiston/valve sampled gap ≥6.737 mm.\nCrossed drive and full-engine acceptance open.',fontsize=12,linespacing=1.5,color='#555d68');fig.tight_layout();p=OUT/'combined-motion-review.png';fig.savefig(p,dpi=150);plt.close(fig)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();files=[Path(__file__),OUT/'combined-q55-layout.json',blockpath,boltpath,ROOT/'inventory/engine/engine-corrected-rod-bolt-conflict-validation.json']+list(meshpaths)
r=dict(status='PASS actual mesh/section render; interference retained',inputs={str(p.relative_to(ROOT)):sha(p) for p in files},render_sha256=sha(p),render=str(p.relative_to(ROOT)),limits=['Projection shows selected moving meshes; full static context lives in named STEP','No visual clearance override of six measured failures'])
(ROOT/'inventory/engine/engine-corrected-combined-render-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
