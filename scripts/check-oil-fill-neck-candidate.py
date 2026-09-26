"""Exact CAD feasibility first; full motion only after assembly gates pass."""
from pathlib import Path
import sys,json,hashlib,platform,importlib.metadata,math
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
from oil_fill_neck_candidate import candidate,cap_at,PITCH

def volume(s): return sum(x.volume for x in s.solids()) if s else 0.
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
m_path=ROOT/'inventory/engine/full-assembly.json'
m=json.loads(m_path.read_text()); defs={d['id']:d for d in m['definitions']}
snapshot_paths={m_path,Path(__file__),ROOT/'cad/engine/oil_fill_neck_candidate.py',ROOT/'cad/engine/pilot/oil-cap/oil_cap.py'}
snapshot_paths.update(ROOT/d[k].lstrip('/') for d in m['definitions'] for k in ('step','glb'))
snapshot_paths.update((ROOT/'cad/engine').glob('*.py'))
before={str(p.relative_to(ROOT)):sha(p) for p in snapshot_paths}
cover_path=ROOT/defs['valve-cover']['step'].lstrip('/')
cover=transforms(m)['valve-cover']*b.import_step(cover_path)
body,neck=candidate(cover); cap,seal=cap_at()
checks={
 'cover_solids':len(cover.solids()),'candidate_solids':len(body.solids()),
 'neck_attachment_volume_mm3':volume(neck&cover),
 'seated_cap_overlap_mm3':volume(body&cap),
 'seated_seal_overlap_mm3':volume(body&seal),
 'seated_seal_distance_mm':body.distance_to(seal),
 'fill_probe_overlap_mm3':volume(body&(b.Pos(240,-12,411)*b.Cylinder(10,30))),
}
print(json.dumps(checks),flush=True)
checks['axial_pull_overlap_mm3']=volume(body&cap_at(lift=PITCH/4)[0])
# Remove female flanks without changing the attachment geometry.
bad=body-b.Pos(240,-12,410)*b.Cylinder(16.1,40)
checks['oversized_bore_pull_overlap_mm3']=volume(bad&cap_at(lift=PITCH/4)[0])
screw=[]
for angle in range(0,1801,45):
 c,s=cap_at(angle); row={'angle_deg':angle,'lift_mm':PITCH*angle/360,'cap_overlap_mm3':volume(body&c),'seal_overlap_mm3':volume(body&s)}
 screw.append(row);print(json.dumps(row),flush=True)
checks['screw_removal']=screw
paths=[m_path,cover_path,Path(__file__),ROOT/'cad/engine/oil_fill_neck_candidate.py',ROOT/'cad/engine/pilot/oil-cap/oil_cap.py']
checks['feasible']=bool(checks['candidate_solids']==1 and checks['neck_attachment_volume_mm3']>1 and checks['seated_cap_overlap_mm3']<.1 and checks['seated_seal_overlap_mm3']<.1 and checks['seated_seal_distance_mm']<.002 and checks['fill_probe_overlap_mm3']<.1 and checks['axial_pull_overlap_mm3']>1 and checks['oversized_bore_pull_overlap_mm3']<.1 and all(x['cap_overlap_mm3']<.1 and x['seal_overlap_mm3']<.1 for x in screw))
report={'status':'FEASIBILITY_PASS' if checks['feasible'] else 'FEASIBILITY_FAIL','scope':'Isolated assumed 4.5 mm pitch illustrative mate, not OEM or installed','environment':{'python':platform.python_version(),'build123d':importlib.metadata.version('build123d')},'checks':checks,'rocker_motion':'NOT RUN: feasibility required first','input_hashes':{str(p.relative_to(ROOT)):sha(p) for p in paths}}
if checks['feasible']:
 rockers=[o for o in m['occurrences'] if o.get('valvetrain',{}).get('role')=='rocker']
 assert len(rockers)==12
 shapes={}
 for o in rockers:
  p=ROOT/defs[o['definition']]['step'].lstrip('/'); paths.append(p)
  if o['definition'] not in shapes: shapes[o['definition']]=b.import_step(p)
 paths.extend(ROOT/'cad/engine'/n for n in ('assembly_math.py','valvetrain_dispatch.py','valve_source_integration.py','valve_source_layout.py','valve_layout_integration.py','valve_layout_candidate.py','valve_motion_candidate.py','valve_dimensions_candidate.py','valve_spring_seating_candidate.py'))
 hashes={str(p.relative_to(ROOT)):sha(p) for p in paths}
 angles=set(range(0,721,5))
 for phase in range(0,720,120):
  for peak in (246,468):
   for delta in (-135,0,135): angles.add((phase+peak+delta)%720)
 focused=dict(m,occurrences=rockers)
 for angle in (0,246,468,720):
  whole,small=transforms(m,angle),transforms(focused,angle)
  assert all(whole[o['id']].to_tuple()==small[o['id']].to_tuple() for o in rockers)
 results=[]; broad=0
 for angle in sorted(angles):
  poses=transforms(focused,angle)
  for o in rockers:
   r=poses[o['id']]*shapes[o['definition']]
   aa,cc=neck.bounding_box(),r.bounding_box()
   bound=math.sqrt(sum(max(0.,tuple(aa.min)[i]-tuple(cc.max)[i],tuple(cc.min)[i]-tuple(aa.max)[i])**2 for i in range(3)))
   if bound>15: broad+=1;continue
   distance=neck.distance_to(r)
   results.append({'crank_deg':angle,'rocker':o['id'],'distance_mm':distance,'overlap_mm3':volume(neck&r) if distance<.002 else 0.})
  print('Neck rocker phase',angle,flush=True)
 closest=min(results,key=lambda x:x['distance_mm'])
 o=next(o for o in rockers if o['id']==closest['rocker'])
 r=transforms(focused,closest['crank_deg'])[o['id']]*shapes[o['definition']]
 bad_overlap=volume((b.Pos(0,0,-10)*neck)&r)
 assert bad_overlap>.1,'Neck collision negative control failed'
 assert hashes=={str(p.relative_to(ROOT)):sha(p) for p in paths},'Input changed during motion check'
 report['input_hashes']=hashes
 report['rocker_motion']={'status':'PASS' if all(x['distance_mm']>=.002 and x['overlap_mm3']<=.1 for x in results) else 'FAIL','scope':'Added neck only; existing cap motion audit separate; 12 installed rockers','phase_count':len(angles),'exact_pairs':len(results),'aabb_separated_pairs':broad,'closest':closest,'negative_control':{'neck_z_offset_mm':-10,'overlap_mm3':bad_overlap},'samples':results}
 report['status']='CANDIDATE_CHECKS_PASS' if report['rocker_motion']['status']=='PASS' else 'ROCKER_FAIL'
# Round trip verifies topology/volume, not visual fidelity.
out=ROOT/'inventory/engine/oil-fill-neck-candidate-validation.json';out.write_text(json.dumps(report,indent=2)+'\n')
art=ROOT/'cad/engine/generated/oil-fill-neck-study';art.mkdir(exist_ok=True)
b.export_step(body,art/'cover-with-neck.step');b.export_step(neck,art/'neck.step')
roundtrip=b.import_step(art/'cover-with-neck.step')
report['export']={'solids':len(roundtrip.solids()),'volume_delta_mm3':abs(volume(roundtrip)-volume(body)),'sha256':sha(art/'cover-with-neck.step'),'path':str((art/'cover-with-neck.step').relative_to(ROOT))}
assert report['export']['solids']==1 and report['export']['volume_delta_mm3']<.1
out.write_text(json.dumps(report,indent=2)+'\n')
print('Feasibility and rocker stages complete:',report['status'],flush=True)

# Sample the entire service removal against all nearby manifest geometry.
# GLB broad phase is conservative by 2 mm; exact CAD determines the verdict.
import numpy as np
import trimesh
poses=transforms(m); neighbors=[]; broad_ids=[]
for o in m['occurrences']:
 if o['id'] in ('valve-cover','oil-filler-cap','oil-filler-cap-seal'): continue
 d=defs[o['definition']]; gp=ROOT/d['glb'].lstrip('/')
 gm=trimesh.load(gp,force='mesh'); xyz=np.asarray(gm.vertices)
 cad=np.column_stack((xyz[:,0],-xyz[:,2],xyz[:,1]))*1000
 corners=np.array([[x,y,z] for x in (cad[:,0].min(),cad[:,0].max()) for y in (cad[:,1].min(),cad[:,1].max()) for z in (cad[:,2].min(),cad[:,2].max())])
 corners=np.array([tuple(b.Vertex(*q).moved(poses[o['id']]).center()) for q in corners])
 paths.append(gp)
 if np.all(corners.max(0)>np.array([203,-49,392])) and np.all(corners.min(0)<np.array([277,25,457])):
  sp=ROOT/d['step'].lstrip('/');paths.append(sp)
  neighbors.append((o['id'],poses[o['id']]*b.import_step(sp)))
 else: broad_ids.append(o['id'])
removal=[]
for angle in range(0,1801,45):
 print('Service removal angle',angle,flush=True)
 c,s=cap_at(angle)
 for ident,neighbor in neighbors:
  dist=c.distance_to(neighbor);ov=volume(c&neighbor) if dist<.002 else 0.
  sd=s.distance_to(neighbor);sv=volume(s&neighbor) if sd<.002 else 0.
  removal.append({'angle_deg':angle,'neighbor':ident,'distance_mm':min(dist,sd),'overlap_mm3':ov+sv})
report['service_removal_neighbors']={'status':'PASS' if all(x['overlap_mm3']<=.1 and x['distance_mm']>=.002 for x in removal) else 'FAIL','angles_deg':list(range(0,1801,45)),'exact_neighbor_ids':[x[0] for x in neighbors],'broadphase_excluded_ids':broad_ids,'minimum':min(removal,key=lambda x:x['distance_mm']) if removal else None,'failures':[x for x in removal if x['overlap_mm3']>.1 or x['distance_mm']<.002],'scope':'Engine off at crank zero, helical lift 0–22.5 mm; no hand/tool envelope or further carrying path'}

# Export actual tessellated candidate geometry, reload it and compare CAD bounds.
meshchecks=[];scene=trimesh.Scene()
for name,shape,color in [('cover',body,[170,180,185,255]),('cap',cap,[55,68,83,255]),('seal',seal,[162,122,63,255])]:
 vertices,faces=shape.tessellate(.12,.15);xyz=np.array([tuple(v) for v in vertices]);faces=np.array(faces)
 mesh=trimesh.Trimesh(vertices=xyz[:,[0,2,1]]*np.array([1,1,-1])/1000,faces=faces)
 mesh.visual.vertex_colors=color;scene.add_geometry(mesh,node_name=name)
 target=art/(name+'.glb');target.write_bytes(trimesh.Scene(mesh).export(file_type='glb'))
 rt=trimesh.load(target,force='mesh');a=np.asarray(rt.vertices);back=np.column_stack((a[:,0],-a[:,2],a[:,1]))*1000
 bb=shape.bounding_box();delta=float(np.max(np.abs(np.array([back.min(0),back.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))))
 meshchecks.append({'id':name,'bounds_error_mm':delta,'watertight':rt.is_watertight,'sha256':sha(target)})
 assert delta<.15 and rt.is_watertight
(art/'assembly.glb').write_bytes(scene.export(file_type='glb'))
report['mesh_exports']=meshchecks

# Portable orthographic CAD triangle rendering: full neck context and section.
# SVG is generated from actual Boolean cutaway geometry, never an invented image.
items=[]
for panel in (0,1):
 view=np.array([.48,-.72,.50]) if panel==0 else np.array([0.,-1.,0.]);view/=np.linalg.norm(view)
 right=np.array([1.,0.,0.]) if panel else np.array([.832,.555,0.]);up=np.cross(view,right)
 cut=b.Pos(240,18,415)*b.Box(100,60,80)
 crop=b.Pos(240,-12,415)*b.Box(90,90,65)
 for name,shape,col in [('cover',body&crop,np.array([164,182,188])),('cap',cap,np.array([70,87,108])),('seal',seal,np.array([190,140,63]))]:
  if panel:shape=shape&cut
  vs,fs=shape.tessellate(.12,.15);tri=np.array([tuple(v) for v in vs])[np.array(fs)]-np.array([240,-12,415])
  norm=np.cross(tri[:,1]-tri[:,0],tri[:,2]-tri[:,0]);norm/=np.maximum(np.linalg.norm(norm,axis=1)[:,None],1e-9)
  shade=.4+.6*np.abs(norm@np.array([.3,-.4,.866]));uv=np.stack([tri@right,-tri@up],axis=-1)*6+np.array([350+panel*700,350]);dep=(tri@view).mean(1)
  for points,z,sh in zip(uv,dep,shade):items.append((panel,z,points,tuple((col*sh).astype(int))))
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="650" viewBox="0 0 1400 650"><rect width="1400" height="650" fill="#f7f9fb"/>']
for panel,z,points,color in sorted(items,key=lambda x:(x[0],x[1])):
 svg.append('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in points)+'" fill="rgb'+str(tuple(int(c) for c in color))+'"/>')
svg.extend(['<text x="25" y="35" font-family="sans-serif" font-size="22">Illustrative 4.5 mm mate — actual CAD; factory neck construction unknown</text>','<text x="60" y="80" font-family="sans-serif" font-size="20">Assembled context</text>','<text x="760" y="80" font-family="sans-serif" font-size="20">Axial cutaway: cap, seal and attached neck</text>','</svg>'])
(art/'review.svg').write_text('\n'.join(svg))
report['render']={'path':str((art/'review.svg').relative_to(ROOT)),'sha256':sha(art/'review.svg')}
report['input_hashes']={str(p.relative_to(ROOT)):sha(p) for p in set(paths)}
report['input_hashes_before']={p:before[p] for p in report['input_hashes']}
report['input_guard_pass']=report['input_hashes_before']==report['input_hashes']
assert report['input_guard_pass'],'Inputs changed during study' 
report['status']='CANDIDATE_CHECKS_PASS' if checks['feasible'] and report['rocker_motion']['status']=='PASS' and report['service_removal_neighbors']['status']=='PASS' else 'CANDIDATE_CHECKS_FAIL'
# Localize a real failure, without modifying any neighbor to force a pass.
failures=report['service_removal_neighbors']['failures']
if failures:
 first=failures[0]; obstruct=next(shape for ident,shape in neighbors if ident==first['neighbor'])
 failed_cap,failed_seal=cap_at(first['angle_deg']);collision=(failed_cap&obstruct)+(failed_seal&obstruct)
 bb=collision.bounding_box()
 report['service_failure']={'first_sample':first,'lift_mm':PITCH*first['angle_deg']/360,'collision_bounds_cad_mm':[list(bb.min),list(bb.max)],'cap_stem_tip_z_mm':394+PITCH*first['angle_deg']/360,'neck_exit_z_mm':413,'required_pure_axial_exit_lift_mm':19,'interpretation':'Collision occurs before stem exit; full-length provisional plenum lies above filler cap. Do not shorten source-consistent stem merely to clear inferred plenum.'}
 # Views of actual complete plenum and localized contact. Transparent plenum is
 # deliberate to reveal the seated and withdrawing cap beneath its envelope.
 panels=[]
 for panel in (0,1):
  view=np.array([.3,-.7,.65]) if panel==0 else np.array([0.,-1.,0.]);view/=np.linalg.norm(view)
  right=np.array([.919,.394,0.]) if panel==0 else np.array([1.,0.,0.]);up=np.cross(view,right)
  center=np.array([0.,-70.,445.]) if panel==0 else np.array([240.,-12.,430.]);scale=.8 if panel==0 else 5.
  crop=b.Pos(240,-12,432)*b.Box(130,130,100)
  shapes_to_draw=[(body if panel==0 else body&crop,[140,160,165],1.),(cap,[60,85,130],1.),(failed_cap,[218,137,42],.9),(obstruct if panel==0 else obstruct&crop,[90,145,175],.35),(collision,[220,25,30],1.)]
  for shape,col,opacity in shapes_to_draw:
   vs,fs=shape.tessellate(.25,.25);tri=np.array([tuple(v) for v in vs])[np.array(fs)]-center
   uv=np.stack([tri@right,-tri@up],axis=-1)*scale+np.array([350+panel*700,355]);dep=(tri@view).mean(1)
   for points,z in zip(uv,dep):panels.append((panel,z,points,col,opacity))
 svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="650"><rect width="1400" height="650" fill="#f7f9fb"/>']
 for panel,z,points,col,opacity in sorted(panels,key=lambda x:(x[0],x[1])):
  svg.append('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in points)+'" fill="rgb'+str(tuple(col))+'" opacity="'+str(opacity)+'"/>')
 svg+=['<text x="25" y="32" font-family="sans-serif" font-size="22">Actual CAD failure: upper intake translucent, seated cap blue, withdrawing cap orange, overlap red</text>','<text x="60" y="78" font-family="sans-serif" font-size="19">Full provisional intake envelope above cap</text>','<text x="760" y="78" font-family="sans-serif" font-size="19">1035 degrees /12.9375 mm lift — stem remains in neck</text>','</svg>']
 (art/'removal-failure.svg').write_text('\n'.join(svg))
 report['service_failure']['render']={'path':str((art/'removal-failure.svg').relative_to(ROOT)),'sha256':sha(art/'removal-failure.svg')}
out.write_text(json.dumps(report,indent=2)+'\n')
print(report['status'],report['service_removal_neighbors']['minimum'],flush=True)
sys.exit(0 if report['status']=='CANDIDATE_CHECKS_PASS' else 1)
