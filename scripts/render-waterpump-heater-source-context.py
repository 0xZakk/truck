from pathlib import Path
import sys,json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/waterpump-heater-source-candidate'
if '--extract'in sys.argv:
 sys.path.insert(0,str(R/'cad/engine'));import build123d as b,trimesh
 from assembly_clockwise_candidate import transforms,occurrence_shape
 mp=R/'inventory/engine/corrected-engine-stage-v3.json';m=json.loads(mp.read_text());poses=transforms(m,0,0);defs={x['id']:x for x in m['definitions']};data={};inputs=[mp]
 for key in ['cylinder-head','fuel-supply-rail','exhaust-front','front-manifold-lifting-eye']:
  o=next(x for x in m['occurrences']if x['id']==key);p=R/defs[o['definition']]['step'].lstrip('/');s=poses[key]*occurrence_shape(o,b.import_step(p),0,0);v,f=s.tessellate(.15,.2);data[key+'_v']=np.array([tuple(x)for x in v]);data[key+'_f']=np.array(f);inputs.append(p)
 for key in ['housing','tube']:
  p=O/(key+'.glb');g=trimesh.load(p,force='mesh');data[key+'_v']=g.vertices[:,[0,2,1]]*[1,-1,1]*1000;data[key+'_f']=g.faces;inputs.append(p)
 np.savez_compressed(O/'context-data.npz',**data);(O/'context-inputs.json').write_text(json.dumps({str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest()for p in inputs},indent=2));sys.exit(0)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import to_rgb
D=np.load(O/'context-data.npz');fig=plt.figure(figsize=(15,8))
for i,(elev,azim)in enumerate([(20,20),(8,100)],1):
 ax=fig.add_subplot(1,2,i,projection='3d')
 for n,color in [('cylinder-head','#909090'),('exhaust-front','#8c6043'),('fuel-supply-rail','#497450'),('front-manifold-lifting-eye','#6e6577'),('housing','#4b88b6'),('tube','#e1c148')]:
  tri=D[n+'_v'][D[n+'_f']];normal=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);normal/=np.maximum(np.linalg.norm(normal,axis=1,keepdims=True),1e-12);light=.3+.7*np.abs(normal@np.array([.8,-.3,.52]));ax.add_collection3d(Poly3DCollection(tri,facecolors=np.array(to_rgb(color))*light[:,None],edgecolor='none',alpha=1 if n in ['housing','tube']else .38))
 ax.set(xlim=(190,525),ylim=(-230,65),zlim=(30,440));ax.set_box_aspect((335,295,410));ax.view_init(elev=elev,azim=azim);ax.set_xlabel('X');ax.set_ylabel('Y');ax.set_zlabel('Z');ax.set_title('Actual tube and conflicting saved neighbors')
fig.suptitle('Source-estimated heater route FAIL — neighboring parts remain unchanged');fig.tight_layout();p=O/'context.png';fig.savefig(p,dpi=150);inputs=json.loads((O/'context-inputs.json').read_text());inputs.update({str(q.relative_to(R)):hashlib.sha256(q.read_bytes()).hexdigest()for q in [Path(__file__),O/'context-data.npz']});(R/'inventory/engine/waterpump-heater-source-context.json').write_text(json.dumps({'image':str(p.relative_to(R)),'image_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'inputs':inputs},indent=2)+'\n')
