from pathlib import Path
import sys,json,hashlib,shutil,numpy as np,trimesh
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report={}
for label,sign in [('plus',1),('minus',-1)]:
 folder=OUT/'r3'/label;folder.mkdir(parents=True,exist_ok=True)
 # Copy immutable neighboring STEP only; every r3 context is recomputed.
 for p in (OUT/label).glob('*.step'):shutil.copy2(p,folder/p.name)
 gx=174.136;gy=-163+24*sign
 controls=[(gx,gy,420),(gx,gy,444),(145,(-120 if sign==1 else -170),460),(80,-90,460),(0,-95,460),(0,-75,460)]
 curve=b.Bezier(*controls);lead=b.Edge.make_line((0,-75,460),(0,-55,460));route=b.Wire([curve,lead]);plane=b.Plane(origin=route@0,z_dir=route%0)
 hose=b.sweep(plane*b.Circle(6),path=route,is_frenet=True)-b.sweep(plane*b.Circle(4.1),path=route,is_frenet=True)
 hose-=b.Pos(gx,gy,424.5)*b.Cylinder(4.15,11)
 for prefix in ['', 'local-']:b.export_step(hose,folder/(prefix+'regulator-vacuum-hose.step'))
 loaded=b.import_step(folder/'regulator-vacuum-hose.step');v,f=loaded.tessellate(.07,.08);vv=np.array([tuple(x) for x in v]);xyz=vv[:,[0,2,1]]*np.array([1,1,-1])/1000
 mesh=trimesh.Trimesh(vertices=xyz.astype(np.float32),faces=f);mesh.update_faces(mesh.area_faces>0);mesh.remove_unreferenced_vertices();mesh.visual.vertex_colors=[50,50,50,255];glb=folder/'local-regulator-vacuum-hose.glb';glb.write_bytes(trimesh.Scene(mesh).export(file_type='glb'));ml=trimesh.load(glb,force='mesh');ml.merge_vertices(digits_vertex=8)
 report[label]={'valid':hose.is_valid,'roundtrip_valid':loaded.is_valid,'solids':len(loaded.solids()),'volume_delta_mm3':abs(hose.volume-loaded.volume),'watertight_glb':bool(ml.is_watertight),'curve_endpoint':list(curve@1),'curve_end_tangent':list(curve%1),'straight_lead_mm':lead.length,'protected_start':list(curve@0),'step_sha256':sha(folder/'regulator-vacuum-hose.step'),'glb_sha256':sha(glb)}
 build=json.loads((OUT/label/'build.json').read_text());build['revision']='r3 vacuum straight lead only; rail r2 preserved'
 for kind in ['definitions','occurrences']:
  for ident,r in build[kind].items():
   path=folder/(('local-' if kind=='definitions' else '')+ident+'.step');r['path']=str(path.relative_to(ROOT));r['sha256']=sha(path)
   if ident=='regulator-vacuum-hose':r.update(valid=hose.is_valid,roundtrip_valid=loaded.is_valid,solids=len(hose.solids()),roundtrip_solids=len(loaded.solids()),volume_mm3=hose.volume,volume_delta_mm3=abs(hose.volume-loaded.volume))
 (folder/'build.json').write_text(json.dumps(build,indent=2)+'\n')
(OUT/'vacuum-r3.json').write_text(json.dumps(report,indent=2)+'\n');print(report)
