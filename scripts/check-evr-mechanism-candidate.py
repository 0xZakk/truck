#!/usr/bin/env python3
"""Scoped geometry witnesses, not calibrated vacuum/electrical simulation."""
from pathlib import Path
import sys,json,hashlib,itertools
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'cad/engine/generated/evr-mechanism-candidate'
if '--render' in sys.argv:
 import matplotlib;matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 from matplotlib.colors import to_rgb
 from mpl_toolkits.mplot3d.art3d import Poly3DCollection
 a=np.load(OUT/'preview.npz');names=json.loads(str(a['names']));fig=plt.figure(figsize=(15,9))
 for panel in range(2):
  ax=fig.add_subplot(1,2,panel+1,projection='3d');tri=[];col=[]
  for i,k in enumerate(names):
   if not len(a[f'f{i}']):continue
   vkey,fkey=(f'zv{i}',f'zf{i}') if panel==1 else (f'v{i}',f'f{i}')
   if not len(a[fkey]):continue
   t=a[vkey][a[fkey]];color=['#b4a16a','#b4a16a','#71838d','#a7b4b9','#d6b857','#627c94','#ceb989','#b77643','#8c969d','#b6bcc2','#9c9ca1'][i]
   if panel==1 and k not in ['evr-body','evr-core-illustrative','evr-disc-illustrative','evr-disc-spring-illustrative']:continue
   n=np.cross(t[:,1]-t[:,0],t[:,2]-t[:,0]);n/=np.maximum(np.linalg.norm(n,axis=1)[:,None],1e-12);shade=.4+.6*np.abs(n@np.array([.3,-.8,.5]));tri.extend(t);col.extend(shade[:,None]*np.array(to_rgb(color)))
  ax.add_collection3d(Poly3DCollection(tri,facecolors=col,edgecolor='none'))
  ax.set(xlim=(-20,34) if panel==0 else (-9,15),ylim=(-1,35) if panel==0 else (-1,9),zlim=(-9,60) if panel==0 else (-4,21),xlabel='X mm',ylabel='Y',zlabel='Z');ax.set_box_aspect((54,36,69) if panel==0 else (24,10,25));ax.view_init(18,-65)
  ax.set_title('Open vent: illustrative winding/core/disc arrangement' if panel==0 else 'Seated disc closes vent; source/outlet stay connected')
 fig.suptitle('EVR comparative mechanism — estimated dimensions; not a factory internal replica or calibration');fig.tight_layout();fig.savefig(OUT/'candidate-review.png',dpi=150);raise SystemExit
sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,trimesh
from OCP.BRepTools import BRepTools
import evr,evr_mechanism_candidate as c
from cad_metrics import solid_volume
vol=lambda s:sum(abs(solid_volume(q)) for q in s.solids()) if s else 0
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common
def ov(a,d):
 aa=a.bounding_box();dd=d.bounding_box()
 if any(tuple(aa.max)[i]<tuple(dd.min)[i]-1e-7 or tuple(dd.max)[i]<tuple(aa.min)[i]-1e-7 for i in range(3)):return 0.
 op=BRepAlgoAPI_Common(a.wrapped,d.wrapped);op.Build()
 if not op.IsDone():raise RuntimeError("CAD common failed")
 q=op.Shape()
 return 0. if q.IsNull() else vol(b.Compound(q))
def contact(a,d):
 return sum((q.area if q else 0) for f in a.faces() for g in d.faces() if f.geom_type==g.geom_type==b.GeomType.PLANE and f.distance_to(g)<1e-7 for q in [f.intersect(g)])
ledger=json.loads((ROOT/'reference/engine/evr-detail-mechanism-review.json').read_text())
for row in ledger['sources']:assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256'],row['path']
paths=[Path(__file__),Path(c.__file__),ROOT/'cad/engine/evr.py',ROOT/'cad/engine/evr_detail_candidate.py',ROOT/'cad/engine/cad_metrics.py',ROOT/'reference/engine/evr-detail-mechanism-review.json']
initial_hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
parts=c.build(c.TRAVEL);body=parts['evr-body'];cap=parts['evr-cap'];filt=parts['evr-vent-filter-illustrative'];core=parts['evr-core-illustrative'];coil=parts['evr-winding-illustrative'];shell=parts['evr-magnetic-shell-illustrative'];terms=[parts['evr-terminal-'+k] for k in ['supply','control']]
# Early render/export stage also used for silhouette before costly travel checks.
OUT.mkdir(parents=True,exist_ok=True);preview={'names':np.array(json.dumps(list(parts)))};exports={};scene=trimesh.Scene()
for i,(k,s) in enumerate(parts.items()):
 BRepTools.Clean_s(s.wrapped);v,f=s.tessellate(.02 if k=='evr-body' else .025,.06 if k=='evr-body' else .1);v=np.array([tuple(p) for p in v]);f=np.array(f)
 sp=OUT/(k+'.step');b.export_step(s,sp);q=b.import_step(sp);mesh=trimesh.Trimesh(v[:,[0,2,1]]*np.array([1,1,-1])/1000,f);mesh.merge_vertices(digits_vertex=8);mesh.update_faces(mesh.unique_faces());mesh.update_faces(mesh.nondegenerate_faces());gp=OUT/(k+'.glb');mesh.export(gp);scene.add_geometry(mesh,node_name=k)
 cut=s.intersect(b.Pos(0,50,25)*b.Box(100,100,100));cv,cf=cut.tessellate(.04,.12);preview[f'v{i}']=np.array([tuple(p) for p in cv]);preview[f'f{i}']=np.array(cf,dtype=int)
 zoomshape=c.moving(0)[k] if k.startswith('evr-disc') else s
 zoom=zoomshape.intersect(b.Pos(3,5,8.5)*b.Box(24,10,25));zv,zf=zoom.tessellate(.04,.12);preview[f'zv{i}']=np.array([tuple(p) for p in zv]);preview[f'zf{i}']=np.array(zf,dtype=int)
 vv=np.array(trimesh.load(gp,force='mesh').vertices)[:,[0,2,1]]*np.array([1,-1,1])*1000;uniterr=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([v.min(0),v.max(0)]))))
 exports[k]={'step_sha256':hashlib.sha256(sp.read_bytes()).hexdigest(),'glb_sha256':hashlib.sha256(gp.read_bytes()).hexdigest(),'mesh_roundtrip_axis_error_mm':uniterr,'valid':s.is_valid,'solids':len(s.solids()),'watertight':mesh.is_watertight,'step_volume_delta':abs(vol(q)-vol(s))}
np.savez_compressed(OUT/'preview.npz',**preview);scene.export(OUT/'candidate.glb')
if '--preview' in sys.argv:print(json.dumps(exports,indent=2));raise SystemExit
protected={'ears':b.Pos(0,0,27)*b.Box(8,70,14)-b.Pos(0,0,27)*b.Box(10,31,16),'connector':b.Pos(26,0,31)*b.Box(24,22,20),'nipple_ends':b.Pos(23,0,8)*b.Box(18,12,28)}
diff=b.Compound(children=list((body-evr.body()).solids())+list((evr.body()-body).solids()));preserved={k:ov(diff,s) for k,s in protected.items()}
print('Exports complete; checking material intersections',flush=True)
collisions={a+' / '+d:ov(parts[a],parts[d]) for a,d in itertools.combinations(parts,2)}
# Contiguous finite-radius witnesses, avoiding solid spring and disc in open pose.
source=c.cx(.15,6,25,1)+b.Pos(6,0,0)*c.cz(.15,14,1)+c.cx(.15,6,25,15)
vent=c.cx(.15,-19,38,54)+c.cz(.15,37.4,16.6)+c.cx(.15,0,6,16.6)+b.Pos(6,0,0)*c.cz(.15,1.6,15)+c.cx(.15,6,25,15)
fixed={k:s for k,s in parts.items() if 'disc' not in k}
states={}
for travel in [0,.2,.4,.6,.8]:
 print('Checking travel',travel,flush=True)
 move=c.moving(travel);allparts={**fixed,**move};disc=move['evr-disc-illustrative'];spring=move['evr-disc-spring-illustrative']
 states[str(travel)]={'source_output_obstruction_mm3':sum(ov(source,s) for s in allparts.values()),'vent_obstruction_mm3':sum(ov(vent,s) for s in allparts.values()),'disc_core_contact_mm2':contact(disc,core),'spring_base_contact_mm2':contact(spring,body),'spring_disc_contact_mm2':contact(spring,disc),'motion_collision_mm3':sum(ov(m,t) for m in move.values() for t in fixed.values())+ov(disc,spring)}
# Filter cross-section fully spans bore when illustrative pores are blocked.
plugged=filt
for x,y in c.pores():plugged+=b.Pos(x,y,0)*c.cz(.45,2,48)
bypass=vol(c.cz(13,.1,48.95)-b.Compound(children=[plugged,cap]))
retention=ov(b.Pos(0,0,.6)*cap,body);unlatched=ov(b.Pos(0,0,.6)*(cap-c.ring(13.05,12.6,1,44)),body);filter_seats={'body':contact(filt,body),'cap':contact(filt,cap)}
# Continuous helical material path joins the terminals. No resistance inferred.
electrical={'terminal_separation_mm':terms[0].distance_to(terms[1]),'terminal_core_gap_mm':min(t.distance_to(core) for t in terms),'terminal_shell_gap_mm':min(t.distance_to(shell) for t in terms),'coil_core_gap_mm':coil.distance_to(core),'coil_shell_gap_mm':coil.distance_to(shell),'lead_coil_contact_distance_mm':[t.distance_to(coil) for t in terms],'lead_terminal_contact_mm2':[contact(t,coil) for t in terms],'joined_conductor_solids':len((coil+terms[0]+terms[1]).solids())}
bridge=b.Pos(18,0,31)*b.Box(1,7,1);cut=b.Pos(10,-3,30)*b.Box(.5,2,10);opened=coil-cut
faults={'blocked_source_overlap_mm3':ov(source,c.cx(.5,8,1,1)),'closed_disc_vent_block_mm3':states['0']['vent_obstruction_mm3'],'oversize_disc_collision_mm3':ov(c.cz(8.5,.7,15.5),body),'filter_missing_free_bore_mm3':vol(c.cz(13,.1,48.95)-cap),'short_bridge_overlap_mm3':[ov(bridge,t) for t in terms],'cut_lead_solids':len(opened.solids()),'undersize_filter_bypass_mm3':vol(c.cz(13,.1,48.95)-b.Compound(children=[c.cz(12.5,2,48),cap])),'cap_pull_off_overlap_mm3':retention,'latch_removed_pull_off_overlap_mm3':unlatched}
hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
stable=hashes==initial_hashes
passed=stable and max(preserved.values())<1e-5 and max(collisions.values())<1e-5 and min(filter_seats.values())>100 and bypass<1e-5 and retention>1 and unlatched<1e-5 and all(e['valid'] and e['solids']==1 and e['watertight'] and e['step_volume_delta']<.001 and e['mesh_roundtrip_axis_error_mm']<.0001 for e in exports.values()) and all(s['source_output_obstruction_mm3']<1e-5 and s['motion_collision_mm3']<1e-5 and min(s['spring_base_contact_mm2'],s['spring_disc_contact_mm2'])>1 for s in states.values()) and states['0']['vent_obstruction_mm3']>.01 and states['0']['disc_core_contact_mm2']>10 and states['0.8']['vent_obstruction_mm3']<1e-5 and electrical['terminal_separation_mm']>1 and electrical['terminal_core_gap_mm']>1 and electrical['terminal_shell_gap_mm']>.1 and electrical['coil_shell_gap_mm']>.1 and electrical['coil_core_gap_mm']>.5 and max(electrical['lead_coil_contact_distance_mm'])<1e-5 and min(electrical['lead_terminal_contact_mm2'])>.1 and electrical['joined_conductor_solids']==1 and faults['undersize_filter_bypass_mm3']>1 and min(faults['short_bridge_overlap_mm3'])>.1 and faults['cut_lead_solids']==2 and faults['blocked_source_overlap_mm3']>.01 and faults['oversize_disc_collision_mm3']>1
r={'status':'PASS' if passed else 'FAIL','scope':'Illustrative comparative positive-gain topology; no calibrated production behavior or installed identity','input_sha256':hashes,'inputs_stable':stable,'protected_region_change_mm3':preserved,'collisions_mm3':{k:v for k,v in collisions.items() if v>1e-5},'states':states,'filter_seats_mm2':filter_seats,'blank_filter_bypass_mm3':bypass,'electrical':electrical,'faults':faults,'exports':exports,'installed_neighbors':'NOT RUN: isolated candidate, no promotion'}
(ROOT/'inventory/engine/evr-mechanism-candidate-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));raise SystemExit(0 if passed else 1)
