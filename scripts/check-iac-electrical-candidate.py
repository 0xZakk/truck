#!/usr/bin/env python3
"""Isolated electrical topology witnesses; no resistance/material certification."""
from pathlib import Path
import sys,json,hashlib,itertools,subprocess
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/iac-electrical-candidate'
if '--render' in sys.argv:
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.colors import to_rgb
 from mpl_toolkits.mplot3d.art3d import Poly3DCollection
 a=np.load(OUT/'preview.npz');names=json.loads(str(a['names']));fig=plt.figure(figsize=(14,6))
 colors=['#bb923e','#bfc5ce','#647881','#bf713e','#d4cab4']
 for j in [1,2]:
  ax=fig.add_subplot(1,2,j,projection='3d');triangles=[];facecolors=[]
  for i,k in enumerate(names):
   v=a[f'v{i}'];f=a[f'f{i}'];tri=v[f]
   if j==1 and k in ['iac-connector-cap','iac-coil','iac-coil-carrier-estimated']:tri=tri[tri.mean(1)[:,1]>=0]
   if j==2:
    if k not in ['iac-connector-cap','iac-terminal-control-estimated','iac-terminal-vpwr-estimated']:continue
    tri=tri[tri.mean(1)[:,0]>=74]
   triangles.extend(tri)
   normals=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-12)
   shade=.6+.4*np.abs(normals@np.array([.8,-.4,.4]))
   if j==2 and k=='iac-connector-cap':shade*=np.where(tri.mean(1)[:,0]<78,.65,1)
   facecolors.extend(np.clip(shade[:,None]*np.array(to_rgb(colors[i])),0,1))
  ax.add_collection3d(Poly3DCollection(triangles,facecolors=facecolors,edgecolor='none',alpha=1))
  ax.set(xlim=(24 if j==1 else 74,81),ylim=(-12 if j==1 else -8,12 if j==1 else 8),zlim=(-12 if j==1 else -7,12 if j==1 else 7),xlabel='IAC X mm',ylabel='Y',zlabel='Z');ax.set_box_aspect((57 if j==1 else 7,24 if j==1 else 16,24 if j==1 else 14));ax.view_init(20 if j==1 else 0,-65 if j==1 else 0);ax.set_proj_type('ortho')
  if j==2:ax.set_xticks([]);ax.set_xlabel('')
  ax.set_title('Mesh cutaway: isolated tails to winding envelope' if j==1 else 'Engine-side mouth: control above VPWR')
 fig.suptitle('Estimated electrical construction — key and terminal dimensions unverified; no physical diode claimed');fig.tight_layout();fig.savefig(OUT/'candidate-review.png',dpi=160);raise SystemExit
import build123d as b,trimesh
sys.path.insert(0,str(ROOT/'cad/engine'))
import iac_electrical_candidate as c
import iac_attachment_integration as frames
from assembly_math import transforms
from cad_metrics import solid_volume
M=ROOT/'inventory/engine/full-assembly.json';raw=M.read_bytes();m=json.loads(raw);D={x['id']:x for x in m['definitions']};O={x['id']:x for x in m['occurrences']};A={x['id']:x for x in m['assemblies']};poses=transforms(m);inv=frames.static_frame('idle-air',m['assemblies']).inverse();inputs={}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def track(p):inputs[str(p.relative_to(ROOT))]=sha(p);return p
def load(k):return b.import_step(track(ROOT/D[O[k]['definition']]['step'].lstrip('/'))).moved(inv*poses[k])
def vol(s):return sum(abs(solid_volume(q,'adaptive')) for q in s.solids()) if s else 0.
def overlap(a,d):return vol(a.intersect(d))
def bounds(s):r=s.bounding_box();return np.array([tuple(r.min),tuple(r.max)])
def area(a,d):
 result=0.
 for f in a.faces():
  if f.geom_type!=b.GeomType.PLANE:continue
  for g in d.faces():
   if g.geom_type!=b.GeomType.PLANE or f.distance_to(g)>1e-6:continue
   q=f.intersect(g)
   if q:result+=q.area
 return result
for p in [Path(__file__),Path(c.__file__),ROOT/'reference/engine/iac-electrical-review.json',ROOT/'cad/engine/iac_attachment_integration.py']:track(p)
ledger=json.loads((ROOT/'reference/engine/iac-electrical-review.json').read_text())
for row in ledger['sources']:
 assert sha(ROOT/row['path'])==row['sha256'];track(ROOT/row['path'])
base={k:load(k) for k in O if k.startswith('iac-')};parts=c.build();allparts={**base,**parts};term=[parts[k] for k in c.TERMINALS];coil=parts['iac-coil'];carrier=parts['iac-coil-carrier-estimated'];cap=parts['iac-connector-cap']
collisions=[]
for a,d in itertools.combinations(allparts,2):
 if a not in parts and d not in parts:continue
 v=overlap(allparts[a],allparts[d])
 if v>1e-5:collisions.append(dict(a=a,b=d,volume_mm3=v))
contacts=[area(t,coil) for t in term];gaps={k:[t.distance_to(base[k]) for t in term] for k in ['iac-solenoid-can','iac-armature','iac-pintle']};separation=term[0].distance_to(term[1]);retention=[overlap(b.Pos(dx,0,0)*t,cap) for t in term for dx in [-1,1]]
gauge=c.mating_witness();correct=overlap(gauge,cap)+sum(overlap(gauge,t) for t in term);wrong=overlap(b.Rot(180,0,0)*gauge,cap)
bridge=b.Pos(76,0,0)*b.Box(1,1,4.6);short=[overlap(bridge,t) for t in term];opened=term[0]-b.Pos(32.9,0,0)*b.Box(65.8,30,30);opengap=opened.distance_to(coil)
motion={str(dx):sum(overlap(b.Pos(dx,0,0)*base['iac-armature'],s) for s in parts.values()) for dx in np.linspace(-1,1,5)}
# New solids stay inside the inherited cylindrical case/connector envelope.
# This is containment only, not a claim about absent neighboring parts.
envelope=c.cx(12,24,70)+b.Pos(75,0,0)*b.Box(10,14,12);outside={k:vol(s-envelope) for k,s in parts.items()}
seats=dict(carrier_body_mm2=area(carrier,base['iac-valve-body']),carrier_cap_mm2=area(carrier,cap),coil_carrier_mm2=area(coil,carrier))
# All-occurrence broad phase, scoped to the changed electrical region. Imported
# mesh bounds receive 0.5 mm margin; exact CAD is used for selected collisions.
region=np.array([[23,-13,-13],[81,13,13]]);near={};mesh_boxes={}
for k,o in O.items():
 if k in base:continue
 ident=o['definition'];gp=ROOT/D[ident]['glb'].lstrip('/')
 if ident not in mesh_boxes:
  vv=np.array(trimesh.load(gp,force='mesh').vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000;mesh_boxes[ident]=(vv.min(0),vv.max(0))
 low,high=mesh_boxes[ident];loc=inv*poses[k];vv=np.array([tuple(b.Vertex(*v).moved(loc).center()) for v in itertools.product(*zip(low,high))])
 if np.all(vv.min(0)<=region[1]+.5) and np.all(region[0]<=vv.max(0)+.5):near[k]=load(k);track(gp)
neighbors=[]
for k,s in parts.items():
 for n,t in near.items():
  v=overlap(s,t)
  if v>1e-5:neighbors.append(dict(part=k,neighbor=n,volume_mm3=v))
OUT.mkdir(parents=True,exist_ok=True);exports={};preview={'names':np.array(json.dumps(list(parts)))};scene=trimesh.Scene()
for i,(k,s) in enumerate(parts.items()):
 v,f=s.tessellate(.025,.08);v=np.array([tuple(x) for x in v]);f=np.array(f);preview[f'v{i}']=v;preview[f'f{i}']=f
 sp=OUT/(k+'.step');b.export_step(s,sp);q=b.import_step(sp);mesh=trimesh.Trimesh(v[:,[0,2,1]]*np.array([1,1,-1])/1000,f);mesh.merge_vertices();gp=OUT/(k+'.glb');mesh.export(gp);scene.add_geometry(mesh,node_name=k,geom_name=k)
 vv=np.array(trimesh.load(gp,force='mesh').vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000
 exports[k]=dict(valid=s.is_valid,solids=len(s.solids()),watertight=mesh.is_watertight,step_valid=q.is_valid,step_volume_error_mm3=abs(vol(q)-vol(s)),mesh_bounds_error_mm=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-bounds(s)))))
np.savez_compressed(OUT/'preview.npz',**preview);scene.export(OUT/'candidate.glb')
ancestors=set()
for k in set(base)|set(near):
 p=O[k]['parent']
 while p in A:ancestors.add(p);p=A[p]['parent']
snapshot=dict(definitions={O[k]['definition']:D[O[k]['definition']] for k in set(base)|set(near)},occurrences={k:O[k] for k in set(base)|set(near)},assemblies={k:A[k] for k in ancestors});new=json.loads(M.read_bytes());stable=all({r['id']:r for r in new[kind]}[k]==v for kind,rows in snapshot.items() for k,v in rows.items()) and all(sha(ROOT/p)==h for p,h in inputs.items())
passed=stable and not neighbors and min(seats.values())>1 and not collisions and min(contacts)>.28 and min(x for row in gaps.values() for x in row)>.1 and separation>1 and min(retention)>.1 and correct<1e-5 and wrong>1 and min(short)>.1 and opengap>.2 and max(motion.values())<1e-5 and max(outside.values())<1e-5 and all(r['valid'] and r['solids']==1 and r['watertight'] and r['step_valid'] and r['step_volume_error_mm3']<.001 and r['mesh_bounds_error_mm']<.2 for r in exports.values())
report=dict(status='PASS' if passed else 'FAIL',scope='Educational geometry only; no production connector dimensions, dielectric or resistance certification',baseline_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),manifest_sha256=hashlib.sha256(raw).hexdigest(),input_sha256=inputs,relevant_pose_snapshot=snapshot,relevant_inputs_stable=stable,coil_contact_mm2=contacts,metal_clearance_mm=gaps,terminal_separation_mm=separation,capture_withdrawal_overlap_mm3=retention,key_witness=dict(correct_overlap_mm3=correct,reversed_overlap_mm3=wrong),fault_controls=dict(short_bridge_overlap_mm3=short,open_tail_gap_mm=opengap),armature_motion_overlap_mm3=motion,seats_mm2=seats,neighbor_ids=sorted(near),neighbor_collisions=neighbors,internal_collisions=collisions,outside_existing_envelope_mm3=outside,exports=exports)
report['output_sha256']={str(p.relative_to(ROOT)):sha(p) for p in OUT.iterdir() if p.suffix in ['.step','.glb','.npz']}
(OUT/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['input_sha256','relevant_pose_snapshot']},indent=2));raise SystemExit(0 if passed else 1)
