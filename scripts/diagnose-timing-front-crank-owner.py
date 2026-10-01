#!/usr/bin/env python3
"""Actual owner diagnosis only; no part is changed or candidate manufactured."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
b.SkipClean.clean=False
import timing_cover_attachment_v2 as owner
import oil_pan_joint_v9_candidate as pan
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/timing-front-crank-owner-diagnosis';OUT.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return sum(abs(solid_volume(q,'adaptive')) for q in s.solids()) if s is not None and getattr(s,'wrapped',True) is not None else 0.
def bb(s):
 if s is None or not s.solids():return None
 q=s.bounding_box();return [list(q.min),list(q.max)]
paths={'block':ROOT/'cad/engine/generated/timing-pump-foot-faceted-candidate/block.step','gear':ROOT/'cad/engine/generated/timing-thrust-land-candidate/crank-timing-gear.step','cover':ROOT/'cad/engine/generated/timing-cover-attachment-v2/cover.step','removal':ROOT/'cad/engine/generated/timing-front-crank-clearance-research/proposed-removal.step','envelope':ROOT/'cad/engine/generated/timing-front-crank-clearance-research/analytic-envelope.step','main-gasket':ROOT/'cad/engine/generated/timing-cover-attachment-v2/main-gasket.step','pan-gasket':ROOT/'cad/engine/generated/timing-cover-attachment-v2/pan-gasket.step','terminal-sealant':ROOT/'cad/engine/generated/timing-cover-attachment-v2/front-terminal-sealant.step'}
inputs={str(p.relative_to(ROOT)):sha(p) for p in paths.values()}
for p in [Path(__file__),Path(owner.__file__),Path(pan.__file__),ROOT/'inventory/engine/timing-front-crank-clearance-research.json']:inputs[str(p.relative_to(ROOT))]=sha(p)
a={k:b.import_step(p) for k,p in paths.items()};frame=b.Pos(*owner.RELOCATIONS[23]);roi=frame*owner.cz(10,7.6,23.6);physical=a['cover'].intersect(roi)
wall=frame*(owner.cz(6.2,7.8,22.3)-owner.cz(4.18,7.7,22.4));floor=frame*owner.cz(3.95,22.6,23.6)
shared=a['block'].intersect(a['cover']);local_shared=shared.intersect(roi);removed_shared=a['removal'].intersect(a['cover'])
regions=[]
for name,mask in [('actual-center-socket',physical),('thread-wall',wall),('one-mm-tip-floor',floor),('main-gasket',a['main-gasket']),('pan-gasket',a['pan-gasket']),('terminal-sealant',a['terminal-sealant'])]:
 row={'name':name,'gear_overlap_mm3':vol(a['gear'].intersect(mask)),'gear_distance_mm':a['gear'].distance_to(mask),'proposed_block_removal_overlap_mm3':vol(a['removal'].intersect(mask)),'analytic_envelope_overlap_mm3':vol(a['envelope'].intersect(mask))}
 if name in ['thread-wall','one-mm-tip-floor']:row['missing_from_actual_cover_mm3']=vol(mask.cut(a['cover']))
 regions.append(row);print(row,flush=True)
mounts=[]
for n,p in enumerate(pan.STATIONS,1):mounts.append({'station':n,'canonical_xyz_mm':p,'classification':'retired canonical location; relocated in candidate' if n in owner.RELOCATIONS else 'unchanged active','candidate_xyz_mm':owner.RELOCATIONS.get(n,p),'candidate_owner':('future-block-land' if owner.RELOCATIONS[n][0]<373 else 'cover') if n in owner.RELOCATIONS else 'block'})
for name,s in [('actual-center-socket',physical),('local-shared-material',local_shared),('proposed-removal-shared-with-cover',removed_shared),('thread-wall-guard',wall),('tip-floor-guard',floor)]:
 if s is not None and s.solids():b.export_step(s,OUT/(name+'.step'))
r={'status':'RESEARCH ONLY; no cut','input_sha256':inputs,'actual_cover_valid':a['cover'].is_valid,'gear_cover_overlap_mm3':vol(a['gear'].intersect(a['cover'])),'gear_cover_distance_mm':a['gear'].distance_to(a['cover']),'block_cover_overlap_mm3':vol(shared),'local_center_block_cover_overlap_mm3':vol(local_shared),'local_shared_bounds_mm':bb(local_shared),'proposed_block_removal_already_shared_with_cover_mm3':vol(removed_shared),'shared_removal_bounds_mm':bb(removed_shared),'regions':regions,'mount_ownership':mounts,'unchanged_station_count':sum(n['classification']=='unchanged active' for n in mounts),'socket_contract':{'thread_wall_radii_mm':[4.18,6.2],'thread_wall_world_z_mm':[-59.2,-44.7],'floor_radius_mm':3.95,'floor_world_z_mm':[-44.4,-43.4],'owner':'cover','all_estimated':True},'limits':['No proposed cut applied to any part','Actual cover wall remains owned by cover; no neighbor-shaped subtraction','Old socket23 X371 is retired in proposed joint; future socket23 X390 is active cover owner','Estimated 1mm floor probe and2.02mm annular wall do not certify production strength','20unchanged block mounts require protection in any future transition contract'],'artifacts':{p.name:sha(p) for p in OUT.glob('*.step')}}
assert inputs=={p:sha(ROOT/p) for p in inputs};(ROOT/'inventory/engine/timing-front-crank-owner-diagnosis.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ['input_sha256','regions','mount_ownership','artifacts']},indent=2),flush=True)
