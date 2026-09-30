#!/usr/bin/env python3
"""Actual baseline/candidate GLB comparison, separate from interface acceptance."""
from pathlib import Path
import hashlib,json,importlib.util,argparse
import build123d as b,numpy as np,trimesh
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'cad/engine/generated/intake-runner-exterior-study'
HELPER=ROOT/'scripts/check-intake-exterior-candidate.py'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--allow-failed',action='store_true');args=parser.parse_args()
 proof=ROOT/'inventory/engine/intake-runner-exterior-candidate-validation.json';report=json.loads(proof.read_text());assert report['status'].startswith('PASS') or args.allow_failed
 paths=[proof,OUT/'baseline.step',OUT/'runner-exterior.step',HELPER,Path(__file__)];before={str(p.relative_to(ROOT)):sha(p) for p in paths};assert sha(OUT/'runner-exterior.step')==report['step_sha256']
 meshes=[];checks=[]
 for name in ('baseline','runner-exterior'):
  shape=b.import_step(OUT/(name+'.step'));vertices,faces=shape.tessellate(.07,.08);v=np.array([tuple(p) for p in vertices]);xyz=v[:,[0,2,1]]*np.array([1,1,-1])/1000
  mesh=trimesh.Trimesh(vertices=xyz.astype(np.float32),faces=faces);mask=mesh.area_faces>0;removed=int((~mask).sum());mesh.update_faces(mask);mesh.remove_unreferenced_vertices();mesh.visual.vertex_colors=[178,186,190,255]
  path=OUT/(name+'.glb');path.write_bytes(trimesh.Scene(mesh).export(file_type='glb'));check=trimesh.load(path,force='mesh');check.merge_vertices(digits_vertex=8)
  vv=np.array(check.vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000;box=shape.bounding_box();err=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([tuple(box.min),tuple(box.max)]))))
  assert check.is_watertight and err<.15
  meshes.append(check);checks.append(dict(id=name,glb_sha256=sha(path),watertight=True,bounds_error_mm=err,zero_area_faces_removed=removed,triangles=len(check.faces)))
 spec=importlib.util.spec_from_file_location('reviewed_intake_renderer',HELPER);helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
 target=OUT/'mesh-comparison.svg';helper.render(meshes,target)
 svg=target.read_text().replace('Actual exported meshes — source-compared casting exterior candidate','Actual exported meshes — runner exterior feasibility').replace('Checked compact casting baseline','Current installed round-runner exterior').replace('Rounded shoulder, ribs and observed raised wording','Broad runner faces and rounded edges — inferred trial').replace('Feature existence follows owner/specimen photos; dimensions and font shapes are estimates. No interface relocation.','Broad exterior form follows Ford/owner/specimen comparisons. Section sizes inferred; air and interfaces unchanged.')
 target.write_text(svg)
 after={str(p.relative_to(ROOT)):sha(p) for p in paths};assert before==after
 result=dict(status='PASS actual GLB export comparison only; see feasibility status',feasibility_status=report['status'],exports=checks,tessellation=dict(linear_deflection_mm=.07,angular_deflection_rad=.08),input_sha256_before=before,input_sha256_after=after,render_png_sha256=sha(OUT/'mesh-comparison.png'),render_svg_sha256=sha(target),limits='Render/export only. Full neighbor/motion/interface acceptance remains separate; later specimen is not exact1994 identity.')
 (ROOT/'inventory/engine/intake-runner-exterior-render-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
