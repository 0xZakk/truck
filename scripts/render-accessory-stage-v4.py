"""Matched orthographic views of actual exported v3/v4 meshes at recorded q0 poses."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'cad/engine/generated/accessory-stage-v4-visual';O.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
EXPECTED='9da33ca507e31cf6d906d4ee2c92b87a64ba01db7abea8f14b72f244631f9fe9'
def selected(n):
 return n in ['block','cylinder-head','timing-cover','alternator-thermactor-common-carrier','ps-ac-support-bracket'] or n.startswith(('alternator-','thermactor-','power-steering-','ps-','ac-compressor-','ac-bracket-','alt-bracket-','alt-engine-','carrier-','tensioner-','water-pump-','damper-','timing-cover-main-'))
def color(n):
 if n in ['alternator-thermactor-common-carrier','ps-ac-support-bracket']:return [.85,.46,.17]
 if n=='block':return [.46,.50,.53]
 if n=='cylinder-head':return [.61,.65,.67]
 if n=='timing-cover':return [.72,.65,.45]
 if n.startswith('water-pump-'):return [.24,.56,.71]
 if n.startswith(('ps-','power-steering-')):return [.41,.61,.42]
 if n.startswith('ac-compressor-'):return [.63,.49,.69]
 if n.startswith('thermactor-'):return [.49,.66,.65]
 if n.startswith('alternator-'):return [.69,.73,.77]
 return [.39,.42,.45]
if '--extract' in sys.argv:
 sys.path.insert(0,str(R/'cad/engine'));import trimesh
 from assembly_clockwise_candidate import transforms
 data={};inputs={};rows=[];cache={}
 for stage in ['v3','v4']:
  p=R/f'inventory/engine/corrected-engine-stage-{stage}.json';inputs[str(p.relative_to(R))]=sha(p)
  if stage=='v4':assert sha(p)==EXPECTED,'Changed v4'
  m=json.loads(p.read_text());poses=transforms(m,0,0);defs={x['id']:x for x in m['definitions']}
  for o in m['occurrences']:
   n=o['id']
   if not selected(n):continue
   assert not o.get('valvetrain')
   q=R/defs[o['definition']]['glb'].lstrip('/');inputs[str(q.relative_to(R))]=sha(q)
   if q not in cache:cache[q]=trimesh.load(q,force='mesh')
   mesh=cache[q];v=mesh.vertices[:,[0,2,1]]*[1,-1,1]*1000
   t=poses[n].wrapped.Transformation();mat=np.array([[t.Value(i,j)for j in range(1,5)]for i in range(1,4)]);v=v@mat[:,:3].T+mat[:,3]
   key=f'{stage}__{n}';data[key+'_v']=v;data[key+'_f']=mesh.faces;data[key+'_c']=np.array(color(n));rows.append({'stage':stage,'occurrence':n,'definition':o['definition'],'glb':str(q.relative_to(R)),'world_matrix_3x4':mat.tolist(),'world_bounds_mm':[v.min(0).tolist(),v.max(0).tolist()],'triangles':len(mesh.faces)})
 for f in ['cad/engine/assembly_clockwise_candidate.py','cad/engine/assembly_math.py']:inputs[f]=sha(R/f)
 np.savez_compressed(O/'mesh-data.npz',**data);(O/'mesh-inputs.json').write_text(json.dumps({'inputs':inputs,'occurrences':rows},indent=2)+'\n');print(len(rows),'occurrence meshes extracted');sys.exit()
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
from matplotlib.patches import Patch
D=np.load(O/'mesh-data.npz');meta=json.loads((O/'mesh-inputs.json').read_text());fig,axes=plt.subplots(2,2,figsize=(16,13));cameras=[('Front',np.array([1.,0,0])),('Front oblique',np.array([1.,-.65,.42]))];views=[]
for col,(label,direction)in enumerate(cameras):
 direction/=np.linalg.norm(direction);right=np.cross([0,0,1],direction);right/=np.linalg.norm(right);up=np.cross(direction,right);basis=np.array([right,up,direction]);allpoints=np.concatenate([D[k]for k in D.files if k.endswith('_v')]);pr=allpoints@basis.T;bounds=np.array([pr[:,:2].min(0),pr[:,:2].max(0)]);pad=(bounds[1]-bounds[0])*.05;views.append({'name':label,'view_basis':basis.tolist(),'projected_bounds_mm':bounds.tolist()})
 for row,stage in enumerate(['v3','v4']):
  ax=axes[row,col];triangles=[];colors=[];depth=[]
  for record in meta['occurrences']:
   if record['stage']!=stage:continue
   key=stage+'__'+record['occurrence'];v=D[key+'_v'];f=D[key+'_f'];tri=v[f];norm=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1,keepdims=True),1e-12)
   light=.35+.65*np.abs(norm@np.array([.67,-.40,.62]));p=tri@basis.T;triangles.append(p[:,:,:2]);depth.append(p[:,:,2].mean(1));colors.append(D[key+'_c'][None,:]*light[:,None])
  tri=np.concatenate(triangles);dep=np.concatenate(depth);c=np.concatenate(colors);order=np.argsort(dep);ax.add_collection(PolyCollection(tri[order],facecolors=c[order],edgecolors='none',rasterized=True));ax.set_xlim(bounds[0,0]-pad[0],bounds[1,0]+pad[0]);ax.set_ylim(bounds[0,1]-pad[1],bounds[1,1]+pad[1]);ax.set_aspect('equal');ax.set_facecolor('#f3f4f5');ax.set_title(stage.upper()+' · '+label+(' · inferred layout/support prototypes'if stage=='v4'else ' · prior private stage'));ax.set_xlabel('Projected horizontal mm');ax.set_ylabel('Projected vertical mm');ax.grid(False)
fig.legend(handles=[Patch(color=color(n),label=l)for n,l in [('alternator-thermactor-common-carrier','Both support carriers'),('water-pump-housing','Water pump'),('ps-pump-housing','Power steering'),('ac-compressor-front-head','A/C compressor'),('thermactor-housing','Thermactor')]],loc='lower center',ncol=5)
fig.suptitle('Actual exported meshes and serialized q0 transforms — matched cameras\nOpaque surfaces; no collision removal, source-image overlays or installation claim',fontsize=15);fig.subplots_adjust(left=.055,right=.985,bottom=.08,top=.88,hspace=.24,wspace=.14);image=O/'comparison.png';fig.savefig(image,dpi=170);plt.close(fig)
inputs=meta['inputs'];inputs.update({str(p.relative_to(R)):sha(p)for p in [Path(__file__),O/'mesh-data.npz',O/'mesh-inputs.json']});report={'status':'rendered; worker inspected matched views; root review pending','image':str(image.relative_to(R)),'image_sha256':sha(image),'inputs':inputs,'views':views,'occurrence_count':{stage:sum(x['stage']==stage for x in meta['occurrences'])for stage in ['v3','v4']},'geometry_source':'Actual GLB triangles; glTF meters Y-up decoded to CAD millimeters Z-up, then actual occurrence transform. No CAD retessellation.','pose':'q0, axial0, compressor0; no valvetrain deformation included','limits':['Estimated support/layout comparison only; no factory silhouette or strength acceptance.','Opaque projection may hide internal overlaps; rendering is not collision verification.','No new pump hypotheses substituted: each stage uses exactly its manifest meshes.','No browser review or source photographs.']};(R/'inventory/engine/accessory-stage-v4-render.json').write_text(json.dumps(report,indent=2)+'\n');print(image)
