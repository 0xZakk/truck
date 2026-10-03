"""Read-only saved STEP/GLB material/void replay; no CAD regeneration."""
from pathlib import Path
import hashlib,json,math
import numpy as np,trimesh,build123d as b
R=Path(__file__).resolve().parents[1];F=R/'reference/engine/ho2s-specimen-20261003-validation.json';d=json.loads(F.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for p,h in (d['inputs']|d['asset_hashes']).items():assert sha(R/p)==h,p
O=R/'cad/engine/generated/ho2s-specimen-20261003';out={}
def mesh_inside(mesh,point):
 # Signed solid angle over actual closed exported triangles: independent of CAD kernel.
 t=mesh.triangles-np.asarray(point);a,bb,c=t[:,0],t[:,1],t[:,2]
 la=np.linalg.norm(a,axis=1);lb=np.linalg.norm(bb,axis=1);lc=np.linalg.norm(c,axis=1)
 numerator=np.einsum('ij,ij->i',a,np.cross(bb,c))
 denominator=la*lb*lc+np.einsum('ij,ij->i',a,bb)*lc+np.einsum('ij,ij->i',bb,c)*la+np.einsum('ij,ij->i',c,a)*lb
 winding=float(np.sum(2*np.arctan2(numerator,denominator))/(4*np.pi))
 assert min(abs(winding),abs(abs(winding)-1))<.001,winding
 return abs(winding)>.5
for name,key in [('mounting-shell','thread_probes'),('slotted-protective-cap','slot_void_probes')]:
 row=d['regions'][name];s=b.import_step(R/row['step']);g=trimesh.load(R/row['glb'],force='mesh');v=g.vertices[:,[0,2,1]]*[1,-1,1]*1000;m=trimesh.Trimesh(v,g.faces,process=False)
 assert s.is_valid and len(s.solids())==1 and m.is_watertight
 for q in d[key]:
  assert s.is_inside(q['point_mm'])==q['expected']
  assert mesh_inside(m,q['point_mm'])==q['expected'],q
 out[key]={'saved_step':len(d[key]),'actual_glb_solid_angle':len(d[key])}
for filename,key in [('control-smooth-thread.step','thread_probes'),('control-closed-cap.step','slot_void_probes')]:
 s=b.import_step(O/filename);assert any(s.is_inside(q['point_mm'])!=q['expected'] for q in d[key])
out['saved_negative_controls_rejected']=True
mouth=b.import_step(O/'connector-housing.step');blocked=b.import_step(O/'control-blocked-mouth.step')
assert not mouth.is_inside((0,0,43)) and blocked.is_inside((0,0,43))
out['saved_blocked_mouth_rejected']=True
out['inputs']={str(F.relative_to(R)):sha(F),str(Path(__file__).relative_to(R)):sha(Path(__file__))}
out['scope']='Sampled saved STEP and independently classified GLB material/void; not thread gauge, flow simulation or installed fit.'
(R/'reference/engine/ho2s-specimen-20261003-replay.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',out)
