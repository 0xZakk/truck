#!/usr/bin/env python3
"""Actual world-frame exports, with the whole keyed group posed together."""
from pathlib import Path
import json,hashlib,math
import numpy as np
import trimesh
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/timing-coupled-core-candidate'
proof=ROOT/'inventory/engine/timing-coupled-core-candidate-validation.json';r=json.loads(proof.read_text());moving=set(r['rotating_cam_group']);axis=np.array([0,95.1098209901611,76.08785679212888]);k=-math.tan(math.radians(25))/81.2
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
data={}
for key,e in r['exports'].items():
 p=OUT/(key+'.glb');assert sha(p)==e['glb_sha256'];m=trimesh.load(p,force='mesh');data[key]=(m.vertices[:,[0,2,1]]*[1,-1,1]*1000,m.faces)
fig=plt.figure(figsize=(18,8))
for i,(theta,delta,el,az) in enumerate([(0,0,20,10),(180,-.1,20,10),(180,-.1,10,175)],1):
 ax=fig.add_subplot(1,3,i,projection='3d')
 for key,(v,f) in data.items():
  if i==3 and key in ['camshaft','cam-timing-gear','crank-timing-gear']:continue
  points=v.copy()
  if key in moving or key=='crank-timing-gear':
   angle=math.radians(-theta/2)+k*delta if key in moving else math.radians(theta);co,si=math.cos(angle),math.sin(angle);rot=np.array([[1,0,0],[0,co,-si],[0,si,co]])
   origin=axis if key in moving else np.zeros(3);points=(points-origin)@rot.T+origin
   if key in moving:points[:,0]+=delta
  tri=points[f];tri=tri[tri[:,:,0].min(1)>350]
  if not len(tri):continue
  normals=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);e,a=np.radians([el,az]);eye=np.array([np.cos(e)*np.cos(a),np.cos(e)*np.sin(a),np.sin(e)]);tri=tri[normals@eye>1e-10]
  if not len(tri):continue
  color='#4d9482' if key in moving else '#b09263' if key=='crank-timing-gear' else '#a6acb3'
  ax.add_collection3d(Poly3DCollection(tri,facecolors=color,edgecolor='none',shade=True,antialiased=False))
 ax.set(xlim=(350,405),ylim=(-48,182),zlim=(-48,165));ax.set_box_aspect((55,230,213));ax.view_init(el,az);ax.set_axis_off()
 ax.set_title(['Neutral front core','Crank 180°, cam −89.9671°, axial −0.1 mm','Same coupled pose; gears/shaft hidden'][i-1])
fig.suptitle('Actual modeled timing core — teal: rigid cam group; gray: stationary core; amber: crank gear\nPlate bolts/washers stay fixed. No separate gear-retaining bolt established. Block/cover/linkage acceptance excluded.')
fig.tight_layout();fig.savefig(OUT/'coupled-core-render.png',dpi=150)
(OUT/'render-record.json').write_text(json.dumps(dict(script_sha256=sha(__file__),validation_sha256=sha(proof),mesh_sha256={k:sha(OUT/(k+'.glb')) for k in data},render_sha256=sha(OUT/'coupled-core-render.png')),indent=2)+'\n')
