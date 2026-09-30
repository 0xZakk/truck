#!/usr/bin/env python3
"""Export exactly five validated CAD spring poses, isolated output only."""
from pathlib import Path
import argparse,json,hashlib,sys
import numpy as np,build123d as b,trimesh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import evr_mechanism_candidate as c
from cad_metrics import solid_volume,support_bounds
from OCP.BRepTools import BRepTools
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def prepare(out):
 out=Path(out).resolve();assert ROOT in out.parents and 'generated' in out.parts
 report=ROOT/'inventory/engine/evr-mechanism-candidate-validation.json';r=json.loads(report.read_text());assert r['status']=='PASS'
 for p,h in r['input_sha256'].items():assert sha(ROOT/p)==h,p
 out.mkdir(parents=True,exist_ok=True);poses=[]
 for index,t in enumerate([0,.2,.4,.6,.8]):
  s=c.spring(t);BRepTools.Clean_s(s.wrapped);v,f=s.tessellate(.025,.1);v=np.array([tuple(p) for p in v]);f=np.array(f)
  sp=out/f'spring-{index}.step';gp=out/f'spring-{index}.glb';b.export_step(s,sp)
  mesh=trimesh.Trimesh(v[:,[0,2,1]]*np.array([1,1,-1])/1000,f);mesh.merge_vertices(digits_vertex=8);mesh.update_faces(mesh.unique_faces());mesh.update_faces(mesh.nondegenerate_faces());mesh.export(gp)
  q=b.import_step(sp);box=support_bounds(s);bounds=np.array([tuple(box.min),tuple(box.max)]);err=float(np.max(abs(bounds-np.array([v.min(0),v.max(0)]))))
  assert s.is_valid and len(s.solids())==1 and q.is_valid and abs(solid_volume(q)-solid_volume(s))<.001 and mesh.is_watertight and err<.1
  poses.append(dict(index=index,travel_mm=t,spring_glb=f'/models/engine/evr-motion/spring-{index}.glb',spring_sha256=sha(gp),step_sha256=sha(sp),disc_offset_cad_mm=[0,0,.8-t],disc_offset_viewer_m=[0,(.8-t)/1000,0],cad_bounds_mm=bounds.tolist(),mesh_cad_bounds_error_mm=err,watertight=True))
 data=dict(schema_version=1,label='Illustrative vent opening',baseline_travel_mm=.8,frame='EVR geometry-local; preserve occurrence and ancestor transforms',axes='CAD millimeters[x,y,z] -> viewer meters[x,z,-y]',scope='Exactly five validated discrete kinematic fixtures, not PCM duty cycle, vacuum pressure or elastic simulation',candidate_report_sha256=sha(report),candidate_source_sha256=sha(Path(c.__file__)),poses=poses)
 (out/'poses.json').write_text(json.dumps(data,indent=2)+'\n');return data
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=ROOT/'cad/engine/generated/evr-motion');a=p.parse_args();print(json.dumps(prepare(a.out),indent=2))
