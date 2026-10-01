#!/usr/bin/env python3
"""Actual isolated STEP/mesh export and comparison, no source-photo composite."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import numpy as np,trimesh,build123d as b
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from OCP.BRepTools import BRepTools
import timing_valvetrain_inclined_candidate as c
OUT=ROOT/'cad/engine/generated/timing-valvetrain-inclined-candidate'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r={'exports':{},'input_sha256':{}}
for key in ['rocker-arm','cylinder-head','head-gasket','block']:
 p=OUT/(key+'.step');q=b.import_step(p);r['input_sha256'][str(p.relative_to(ROOT))]=sha(p)
 BRepTools.Clean_s(q.wrapped);vertices,faces=q.tessellate(.08,.15)
 cad=np.array([[v.X,v.Y,v.Z] for v in vertices]);web=cad[:,[0,2,1]]*np.array([1,1,-1])/1000
 mesh=trimesh.Trimesh(vertices=web,faces=faces,process=False);mesh.merge_vertices();mesh.update_faces(mesh.nondegenerate_faces());mesh.update_faces(mesh.unique_faces());mesh.remove_unreferenced_vertices()
 path=OUT/(key+'.glb');trimesh.Scene(mesh).export(path);again=trimesh.load(path,force='mesh');bb=q.bounding_box();expected=np.array([[bb.min.X,bb.min.Z,-bb.max.Y],[bb.max.X,bb.max.Z,-bb.min.Y]])/1000
 err=float(np.max(np.abs(again.bounds-expected)))*1000
 r['exports'][key]={'glb_sha256':sha(path),'watertight':bool(again.is_watertight),'triangles':len(again.faces),'maximum_bounds_error_mm':err}
 assert again.is_watertight and err<.2,r['exports'][key]
# Two useful actual-CAD views: old/new rocker and local retained passage section.
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());frames=c.poses(m,318)
fig,axs=plt.subplots(1,2,figsize=(13,7))
def draw(ax,q,color,label,alpha=.55):
 verts,faces=q.tessellate(.15,.2);a=np.array([[v.Y,v.Z] for v in verts]);ax.add_collection(PolyCollection(a[np.array(faces)],facecolor=color,edgecolor='none',alpha=alpha,label=label))
old=b.Pos(259.48,c.v.PIVOT_Y,c.v.rest('intake',c.v.PIVOT_Y)['pivot_z'])*b.import_step(ROOT/'cad/engine/generated/rocker-arm.step')
new=frames['c1-intake-rocker']*b.import_step(OUT/'rocker-arm.step')
draw(axs[0],old,'#527da4','Installed estimated rocker',.25);draw(axs[0],new,'#df9d36','New estimated common rocker',.8)
axs[0].set_xlim(-30,110);axs[0].set_ylim(373,407);axs[0].set_title('Actual rocker solids at rest; common world datums')
head=b.Pos(0,0,255.5)*b.import_step(OUT/'cylinder-head.step');section=head.intersect(b.Pos(259.48,40,320)*b.Box(1,230,200))
draw(axs[1],section,'#718b99','Head section; lower passage adapted',.8)
rod=frames['c1-intake-pushrod']*b.import_step(ROOT/'cad/engine/generated/pushrod.step');draw(axs[1],rod,'#df9d36','Inclined actual pushrod',.85)
draw(axs[1],new,'#df9d36','New rocker',.8)
block=b.import_step(OUT/'block.step');draw(axs[1],block.intersect(b.Pos(259.48,90,249)*b.Box(1,50,20)),'#66806c','Deck backing section',.8)
gasket=b.Pos(0,0,254.75)*b.import_step(OUT/'head-gasket.step');draw(axs[1],gasket.intersect(b.Pos(259.48,90,254.75)*b.Box(1,60,3)),'#b9856c','Actual gasket section',.9)
axs[1].set_xlim(35,112);axs[1].set_ylim(245,407);axs[1].set_title('Cylinder1 intake: bounded lower passage candidate')
for ax in axs:
 ax.set_aspect('equal');ax.set_xlabel('WorldY / mm');ax.set_ylabel('WorldZ / mm');ax.grid(alpha=.15);ax.legend(fontsize=7)
fig.suptitle('Isolated estimated valvetrain adapter — NOT installed / NOT manufacturer shape comparison')
fig.tight_layout();png=OUT/'adapter-comparison.png';fig.savefig(png,dpi=170)
r['render_sha256']=sha(png)
fig2,ax=plt.subplots(figsize=(9,6))
for q,col,label in [(head,'#718b99','Head'),(block,'#66806c','Block deck'),(gasket,'#b9856c','Gasket')]:
 draw(ax,q.intersect(b.Pos(259.48,90,251)*b.Box(.5,40,20)),col,label,.9)
draw(ax,rod,'#df9d36','Actual inclined rod',.8);ax.set_xlim(77,104);ax.set_ylim(242,260);ax.set_aspect('equal');ax.grid(alpha=.2);ax.set_xlabel('WorldY / mm');ax.set_ylabel('WorldZ / mm');ax.set_title('Actual exported stack section — estimated candidate');ax.legend(loc='lower left');fig2.tight_layout();detail=OUT/'lower-stack-section.png';fig2.savefig(detail,dpi=170);r['stack_render_sha256']=sha(detail)
r['status']='PASS watertight bounded exports; candidate remains uninstalled';(ROOT/'inventory/engine/timing-valvetrain-inclined-export-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
