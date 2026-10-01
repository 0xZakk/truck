#!/usr/bin/env python3
"""Render actual delivered GLBs; verify closure, orientation and positive volume."""
from pathlib import Path
import json,hashlib
import numpy as np,trimesh
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.colors import to_rgb
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/front-seal-2692-candidate';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names=['cover','damper-hub','seal-case-installed','seal-elastomer','seal-garter-spring'];meshes={};r={'inputs':{},'meshes':{}}
for n in names:
 p=OUT/(n+'.glb');m=trimesh.load(p,force='mesh');assert m.is_watertight and m.is_winding_consistent and m.volume>0,n
 r['inputs'][str(p.relative_to(ROOT))]=sha(p);r['meshes'][n]={'watertight':True,'winding_consistent':True,'positive_signed_volume_mm3':float(m.volume)*1e9,'triangles':len(m.faces)}
 m.vertices=m.vertices[:,[0,2,1]]*np.array([1,-1,1])*1000;meshes[n]=m
camera=np.array([.8,-1,.6]);camera/=np.linalg.norm(camera);right=np.cross([0,0,1],camera);right/=np.linalg.norm(right);up=np.cross(camera,right);basis=np.array([right,up,camera]).T
colors={'seal-case-installed':'#d5a850','seal-elastomer':'#544c56','seal-garter-spring':'#e88455'}
def draw(ax,items):
 tris=[];cols=[]
 for n,offset in items:
  m=meshes[n];v=m.vertices+np.array([offset,0,0]);t=v[m.faces];normal=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1)[:,None],1e-12);visible=normal@camera>1e-9;t=t[visible];normal=normal[visible];light=.35+.65*np.clip(normal@camera,0,1);rgb=np.array(to_rgb(colors[n]));cols.append(light[:,None]*rgb);tris.append(t@basis)
 tris=np.concatenate(tris);cols=np.concatenate(cols);order=np.argsort(tris[:,:,2].mean(axis=1));ax.add_collection(PolyCollection(tris[order,:,:2],facecolors=cols[order],edgecolors='none',rasterized=True));p=tris[:,:,:2].reshape(-1,2);lo=p.min(axis=0);hi=p.max(axis=0);pad=np.max(hi-lo)*.05;ax.set_xlim(lo[0]-pad,hi[0]+pad);ax.set_ylim(lo[1]-pad,hi[1]+pad);ax.set_aspect('equal');ax.axis('off')
fig=plt.figure(figsize=(14,9));grid=fig.add_gridspec(2,3,height_ratios=[1.3,1]);ax=fig.add_subplot(grid[0,:]);draw(ax,[('seal-case-installed',0),('seal-elastomer',40),('seal-garter-spring',77)]);ax.set_title('Exploded source-envelope candidate: case → elastomer → separate closed garter spring\nDisplay-only X offsets of 0 / 40 / 77 mm; installed geometry remains unchanged')
for i,(n,title) in enumerate([('seal-case-installed','Nominal fitted case with flange and return'),('seal-elastomer','Bonded element, lip and open groove'),('seal-garter-spring','96 illustrative windings; continuous closure')]):
 ax=fig.add_subplot(grid[1,i]);draw(ax,[(n,0)]);ax.set_title(title,fontsize=10)
fig.suptitle('Actual delivered GLB geometry — internals are estimates, not exact National2692 anatomy',fontsize=14);fig.tight_layout();p=OUT/'seal-internals-exploded.png';fig.savefig(p,dpi=180);r['render']={'path':str(p.relative_to(ROOT)),'sha256':sha(p)};r['inputs'][str(Path(__file__).relative_to(ROOT))]=sha(Path(__file__));r['status']='PASS actual GLB watertightness, winding and positive volume; exploded rendering generated';(ROOT/'inventory/engine/front-seal-2692-exploded-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
