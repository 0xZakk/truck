"""Actual saved-STEP all12 train at phase0, external castings omitted for QC."""
from pathlib import Path
import json,sys,argparse,importlib.util
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/candidates/valve-source-all12'
p=argparse.ArgumentParser();p.add_argument('--export',type=Path);p.add_argument('--render',type=Path);p.add_argument('--output',type=Path);args=p.parse_args()
if args.export:
 import build123d as b
 sys.path.insert(0,str(ROOT/'cad/engine'))
 from valve_source_integration import candidate_transforms,occurrence_shape
 spec=importlib.util.spec_from_file_location('frozen_source_assembly_math',OUT/'baseline/assembly_math.py');authority=importlib.util.module_from_spec(spec);spec.loader.exec_module(authority)
 m=json.loads((OUT/'manifest.json').read_text());poses=candidate_transforms(m,0,base_transforms=authority.transforms);dmap={d['id']:d for d in m['definitions']};defs={};arrays={};meta=[]
 suffixes=['-valve','-spring','-retainer','-keeper-1','-keeper-2','-rocker','-fulcrum','-rocker-bolt','-guide','-pushrod','-lifter-body']
 for o in m['occurrences']:
  oid=o['id']
  if oid!='camshaft' and not (any(f'-{k}-' in oid for k in ['intake','exhaust']) and any(oid.endswith(s) for s in suffixes)):continue
  did=o['definition']
  if did not in defs:defs[did]=b.import_step(ROOT/dmap[did]['step'].lstrip('/'))
  shape=occurrence_shape(o,defs[did],0).moved(poses[oid]);verts,faces=shape.tessellate(.22);index=len(meta)
  arrays[f'v{index}']=np.asarray([tuple(v) for v in verts]);arrays[f'f{index}']=np.asarray(faces)
  color=[.63,.7,.74]
  if oid=='camshaft':color=[.72,.49,.24]
  elif 'spring' in oid:color=[.72,.59,.28]
  elif 'lifter' in oid:color=[.28,.57,.68]
  elif 'rocker' in oid:color=[.43,.5,.6]
  meta.append({'id':oid,'color':color})
 arrays['metadata']=np.array(json.dumps(meta));np.savez_compressed(args.export,**arrays);print(len(meta),'parts',flush=True)
else:
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from engine_qc_raster import render_mesh
 archive=np.load(args.render,allow_pickle=False);meta=json.loads(str(archive['metadata']));triangles=[];colors=[]
 for i,item in enumerate(meta):
  vertices=archive[f'v{i}'];faces=vertices[archive[f'f{i}']];normals=np.cross(faces[:,1]-faces[:,0],faces[:,2]-faces[:,0]);normals/=np.maximum(np.linalg.norm(normals,axis=1)[:,None],1e-12)
  shade=.4+.6*np.abs(normals@np.array([.768,-.4,.5]));triangles.append(faces);colors.append(shade[:,None]*np.array(item['color']))
 fig,ax=plt.subplots(figsize=(15,9));ax.imshow(render_mesh(np.concatenate(triangles),np.concatenate(colors),azimuth=62,elevation=15));ax.set_axis_off()
 ax.set_title('All twelve source-sized valve stations · actual saved STEP at crank0\nExternal castings omitted. Source-sized envelopes; assumed internal datums and teaching cam profile.');fig.tight_layout();fig.savefig(args.output,dpi=140)
