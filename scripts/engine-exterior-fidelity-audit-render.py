"""Render actual canonical and v3 meshes; never copy reference photographs."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'cad/engine'),str(ROOT/'scripts')]
import numpy as np
sys.path.append(str(ROOT/'.venv-cad/lib/python3.13/site-packages'))
import trimesh
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb
from engine_qc_raster import render_mesh
sys.path.append(str(ROOT/'.venv-cad/lib/python3.13/site-packages'))
from assembly_math import transforms
from assembly_clockwise_candidate import transforms as corrected
OUT=ROOT/'cad/engine/generated/engine-exterior-fidelity-audit';OUT.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
files={};results=[]
fig,axes=plt.subplots(2,2,figsize=(14,13))
for col,(label,mp) in enumerate([('Canonical','inventory/engine/full-assembly.json'),('Private v3','inventory/engine/corrected-engine-stage-v3.json')]):
 p=ROOT/mp;raw=p.read_bytes();m=json.loads(raw);files[mp]=sha(p);defs={d['id']:d for d in m['definitions']};poses=(corrected if m.get('motion_revision') else transforms)(m,0);cache={};tris=[];cols=[]
 for o in m['occurrences']:
  d=defs[o['definition']];path=ROOT/d['glb'].lstrip('/')
  if str(path) not in cache:
   mesh=trimesh.load(path,force='scene').to_geometry();cache[str(path)]=(np.asarray(mesh.vertices)[:,[0,2,1]]*[1000,-1000,1000],np.asarray(mesh.faces));files[str(path.relative_to(ROOT))]=sha(path)
  v,f=cache[str(path)];t=poses[o['id']].wrapped.Transformation();mat=np.array([[t.Value(r,c)for c in range(1,5)]for r in range(1,4)]);tri=(v@mat[:,:3].T+mat[:,3])[f];n=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-12);shade=.42+.58*np.abs(n@np.array([.3,-.4,.866]));tris.append(tri);cols.append(shade[:,None]*to_rgb(d['color']))
 tri=np.concatenate(tris);colors=np.concatenate(cols)
 for row,(az,el,title)in enumerate([(0,72,'High front view'),(40,38,'Front-side view')]):
  axes[row,col].imshow(render_mesh(tri,colors,size=1000,elevation=el,azimuth=az));axes[row,col].axis('off');axes[row,col].set_title(label+' · '+title)
 results.append(dict(manifest=mp,occurrences=len(m['occurrences']),triangles=len(tri)))
 assert p.read_bytes()==raw
 del tri,colors,tris,cols,cache
fig.suptitle('Actual full-engine meshes · static event 0°\nQualitative owner-view comparison; orthographic cameras are not calibrated photo matches',fontsize=14)
fig.tight_layout();out=OUT/'whole-engine-review.png';fig.savefig(out,dpi=125);plt.close(fig)
files['scripts/engine-exterior-fidelity-audit-render.py']=sha(Path(__file__))
report=dict(status='Actual mesh render complete; source-view review pending',renders=[dict(path=str(out.relative_to(ROOT)),sha256=sha(out))],scenes=results,inputs=files,camera_views=[dict(azimuth=0,elevation=72),dict(azimuth=40,elevation=38)],limits=['No source photographs embedded','Orthographic projection; no dimensional photo registration','No browser or new collision acceptance'])
(ROOT/'inventory/engine/engine-exterior-fidelity-audit-render.json').write_text(json.dumps(report,indent=2)+'\n')
print('rendered',results)
