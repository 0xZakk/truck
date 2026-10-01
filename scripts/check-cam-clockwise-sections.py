#!/usr/bin/env python3
"""Independent actual BRep sections, point controls and exported-mesh render."""
from pathlib import Path
import sys,json,math,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import numpy as np
from scipy.spatial import cKDTree
import cam_clockwise_candidate as c
OUT=ROOT/'cad/engine/generated/cam-clockwise-candidate'
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())
old=b.Pos(0,-c.AXIS[0],-c.AXIS[1])*b.import_step(c.BASE)
new=b.import_step(OUT/'camshaft-local.step')
replay=c.revise_local(old,m,1)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rotate(points,degrees):
 a=math.radians(degrees);return points@np.array([[math.cos(a),math.sin(a)],[-math.sin(a),math.cos(a)]])
def area(points):return abs(np.sum(points[:,0]*np.roll(points[:,1],-1)-points[:,1]*np.roll(points[:,0],-1)))/2
def boundary_error(a,z):
 # Nearest-vertex-adjacent segments give an upper bound on sampled point distance.
 def one(a,z):
  _,idx=cKDTree(z).query(a,k=4);idx=np.concatenate([idx,(idx-1)%len(z)],axis=1)
  p=z[idx];v=z[(idx+1)%len(z)]-p;d=a[:,None,:]-p
  t=np.clip(np.sum(d*v,axis=2)/np.sum(v*v,axis=2),0,1)
  return float(np.max(np.min(np.linalg.norm(d-t[:,:,None]*v,axis=2),axis=1)))
 return max(one(a,z),one(z,a))
def polygon(shape,x):
 section=b.section(shape,section_by=b.Plane.YZ.offset(x));assert len(section.faces())==1 and len(section.wires())==1
 wire=section.wires()[0]
 pts=np.array([tuple(wire.position_at(i/4096))[1:] for i in range(4096)])
 assert area(pts)>900
 return pts,pts
rows=[];stored=[]
for cylinder,kind,x,phase in c.stations(m):
 p,pp=polygon(old,x);n,nn=polygon(new,x);replay_polygon,_=polygon(replay,x)
 replay_error=boundary_error(p,replay_polygon);assert replay_error<.002
 expected=rotate(p,-2*phase)
 error=boundary_error(expected,n);area_error=abs(area(p)-area(n))
 assert error<.002 and area_error<.02,(cylinder,kind,error,area_error)
 minimum=min(float(np.linalg.norm(p,axis=1).min()),float(np.linalg.norm(n,axis=1).min()));assert minimum>17.99
 # Interior material probes independently cover both edge neighborhoods and radial core.
 count=0
 for shape in [old,new]:
  for dx in [-7.49,0,7.49]:
   for a in range(0,360,15):
    assert shape.is_inside((x+dx,17.89*math.cos(math.radians(a)),17.89*math.sin(math.radians(a))),tolerance=1e-7)
    count+=1
 rows.append(dict(cylinder=cylinder,kind=kind,x_mm=x,section_sample_points=4096,source_replay_boundary_error_mm=replay_error,expected_rigid_phase_rotation_deg=-2*phase,boundary_hausdorff_mm=error,area_difference_mm2=area_error,minimum_core_radius_mm=minimum,strict_core_material_points=count))
 if cylinder==1 and kind=='intake':stored=[pp,nn,x,phase]
 print('Section',cylinder,kind,'PASS',flush=True)
# Entire profile moved incorrectly is detected independently of solid Booleans.
fault=boundary_error(rotate(p,15),n);assert fault>.1
paths=[Path(__file__),Path(c.__file__),c.BASE,OUT/'camshaft-local.step',OUT/'camshaft-local.glb',ROOT/'inventory/engine/cam-clockwise-candidate-build-validation.json']
r=dict(status='PASS independent actual sections and material probes',inputs={str(p.relative_to(ROOT)):sha(p) for p in paths},sections=rows,wrong_phase_boundary_fault_mm=fault,limits=['4096-point actual BRep section polygons approximate continuous boundary; <0.002mm comparison tolerance.','Solid per-station changed-volume diagnostics are not used as acceptance quantities; OCC clipping/subtraction can be unstable at coincident surfaces.','Core strict points supplement exact inset-cylinder containment; no production profile claim.'])
(ROOT/'inventory/engine/cam-clockwise-candidate-section-validation.json').write_text(json.dumps(r,indent=2)+'\n')
# Render actual exported mesh and actual section; no inferred mesh geometry.
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import trimesh
mesh=trimesh.load(OUT/'camshaft-local.glb',force='mesh');vertices=mesh.vertices[:,[0,2,1]]*[1,-1,1]*1000
fig=plt.figure(figsize=(13,8),facecolor='#f6f7f9');ax=fig.add_subplot(211,projection='3d')
collection=Poly3DCollection(vertices[mesh.faces],facecolor='#789daa',edgecolor='none');ax.add_collection3d(collection)
ax.set_xlim(-405,415);ax.set_ylim(-45,45);ax.set_zlim(-45,45);ax.set_box_aspect((9,1,1));ax.view_init(elev=22,azim=-68)
ax.set_title('Actual exported corrected cam mesh · local shaft and keyed ends retained');ax.set_xlabel('X mm');ax.set_ylabel('Y');ax.set_zlabel('Z')
ax=fig.add_subplot(212);pp,nn,x,phase=stored
q=(2*phase-96)%720
def spin(points,degrees):
 a=math.radians(degrees);return points@np.array([[math.cos(a),math.sin(a)],[-math.sin(a),math.cos(a)]])
newposed=spin(nn,q/2);oldposed=spin(pp,-q/2);wrong=spin(pp,q/2)
ax.plot(oldposed[:,0],oldposed[:,1],label='Prior lobe / prior spin',color='#6f7782');ax.plot(newposed[:,0],newposed[:,1],label='Corrected lobe / corrected spin',color='#127a73');ax.plot(wrong[:,0],wrong[:,1],'--',label='Old lobe / corrected spin (fault)',color='#bd4b44')
w=c.tangent(q,1,'intake',0,x);t=[w[1]-c.AXIS[0],w[2]-c.AXIS[1]]
ax.plot([-11.124565,11.124565],[t[1],t[1]],color='#1c2430',lw=3,label='Actual lifter flat-foot plane');ax.scatter(*t,color='#127a73',zorder=5)
ax.set_aspect('equal');ax.set_xlim(-28,28);ax.set_ylim(-25,30);ax.grid(alpha=.2);ax.set_xlabel('Local Y mm');ax.set_ylabel('Local Z mm');ax.legend(loc='lower left',fontsize=8)
ax.set_title('Actual BRep section at X259.48 · intake rising flank, q372° · axial0')
fig.tight_layout();fig.savefig(OUT/'cam-clockwise-mesh-section.png',dpi=160);plt.close(fig)
