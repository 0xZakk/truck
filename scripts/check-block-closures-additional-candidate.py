#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,numpy as np,trimesh
import block_closures_additional_candidate as c
import block_closures_coverage_candidate as frozen
c.OD_MM=c.MPS59A["od_mm"];c.HEIGHT_MM=c.MPS59A["height_mm"];c.OD_RANGE_MM=(2.065*25.4,2.075*25.4)
a=c.cup(**c.MPS126,wall_mm=1);z=frozen.build();assert abs(a.volume-z.volume)<1e-8;assert sum(s.volume for s in a.cut(z).solids())<1e-8;assert sum(s.volume for s in z.cut(a).solids())<1e-8
OUT=ROOT/'cad/engine/generated/block-closures-additional-candidate';OUT.mkdir(exist_ok=True);q=c.build();assert q.is_valid and len(q.solids())==1
sp=OUT/'block-core-cup-mps59a.step';b.export_step(q,sp);rt=b.import_step(sp);bb=rt.bounding_box();assert max(abs(x-y) for x,y in zip(tuple(bb.size),(c.OD_MM,c.OD_MM,c.HEIGHT_MM)))<1e-6
assert rt.is_inside((0,0,.5)) and not rt.is_inside((0,0,2));assert not c.build(.25).is_inside((0,0,.5))
v,f=rt.tessellate(.05,.1);v=np.array([tuple(x) for x in v]);m=trimesh.Trimesh(v[:,[0,2,1]]*[1,1,-1]/1000,np.array(f),process=True);gp=OUT/'block-core-cup-mps59a.glb';m.export(gp);m=trimesh.load(gp,force='mesh');m.merge_vertices(digits_vertex=8);assert m.is_watertight and m.is_winding_consistent and m.volume>0
vv=m.vertices[:,[0,2,1]]*[1,-1,1]*1000;be=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-np.array([tuple(bb.min),tuple(bb.max)]))));assert be<.05
# Actual exported mesh section, no source art redistribution.
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
m.vertices=vv;s=trimesh.intersections.mesh_plane(m,[0,1,0],[0,0,0]);fig,ax=plt.subplots(figsize=(7,3));ax.add_collection(LineCollection(s[:,:,[0,2]],colors='#956b35',linewidths=2));ax.autoscale();ax.set_aspect('equal');ax.set_xlabel('Local X (mm)');ax.set_ylabel('Local Z (mm)');ax.set_title('MPS-59A free envelope • actual mesh section\n1 mm wall estimated; no host bore or installed pose');fig.tight_layout();ip=OUT/'cup-section.png';fig.savefig(ip,dpi=150)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();paths=['cad/engine/block_closures_coverage_candidate.py','scripts/check-block-closures-additional-candidate.py','cad/engine/block_closures_additional_candidate.py','reference/engine/research-2026-09-23/melling-expansion-plug-guide.pdf'];r={'status':'PASS uninstalled replacement envelope only','inputs':{p:sha(ROOT/p) for p in paths},'artifacts':{str(p.relative_to(ROOT)):sha(p) for p in [sp,gp,ip]},'free_od_mm':c.OD_MM,'free_od_range_mm':c.OD_RANGE_MM,'height_mm':c.HEIGHT_MM,'estimated_wall_mm':1,'step_roundtrip_volume_error_mm3':abs(q.volume-rt.volume),'mesh_bounds_error_mm':be,'valid_solids':1,'watertight':True,'winding_consistent':True,'positive_volume':True,'negative_control':'Floor point present at1mmwall, absent at.25mmwall','frozen_mps126_replay_difference_mm3':0.,'printed_metric_od_mm':52.48,'inch_metric_disagreement_mm':.098,'host_bore':None,'occurrence_transforms':None};(ROOT/'inventory/engine/block-closures-additional-candidate-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
