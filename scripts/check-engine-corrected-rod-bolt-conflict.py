#!/usr/bin/env python3
"""Preserve inherited interference and audit actual placeholder bolt datum."""
from pathlib import Path
import sys,json,math,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
from assembly_math import transforms
from engine_clockwise_pose_candidate import corrected_slider_frames
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());o=next(o for o in m['occurrences'] if o['id']=='c1-rod-bolt-1')
claimlist=json.loads((ROOT/'inventory/engine/dimensions.json').read_text())['claims'];claims={x['id']:x for x in claimlist};P={k:x['value'] for k,x in claims.items()}
paths={'bolt':ROOT/'cad/engine/generated/rod-bolt.step','oldblock':ROOT/'cad/engine/generated/block.step','newblock':ROOT/'cad/engine/generated/timing-front-block-expanded-seat-v3-candidate/block.step'}
shape={k:b.import_step(p) for k,p in paths.items()};bolt=shape['bolt'];oldblock=shape['oldblock'];newblock=shape['newblock']
replay=b.Pos(0,0,-4)*b.Cylinder(P['bolt_diameter']/2,54)+b.Pos(0,0,22)*b.extrude(b.RegularPolygon(7,6),amount=5)
replay_error=vol(bolt.cut(replay))+vol(replay.cut(bolt));assert replay_error<1e-5
R=m['mechanism']['stroke_mm']/2;L=m['mechanism']['rod_length_mm'];x=284.48
oldframe=transforms(m,55)['c1-rod-bolt-1'];newframe=corrected_slider_frames(305,0,R,L,x,measured_cad_rest_phase_degrees=0)['rod']*b.Pos(*o['position_cad_mm'])
frame_error=max(abs(oldframe.wrapped.Transformation().Value(i,j)-newframe.wrapped.Transformation().Value(i,j)) for i in range(1,4) for j in range(1,5));assert frame_error<1e-9
oldvolume=vol((oldframe*bolt).intersect(oldblock));newvolume=vol((newframe*bolt).intersect(newblock));assert min(oldvolume,newvolume)>.1 and abs(oldvolume-newvolume)<1e-5
point=[284.48000000000144,-73.36260011256176,65.2474860468778]
assert (oldframe*bolt).is_inside(point,tolerance=1e-7) and oldblock.is_inside(point,tolerance=1e-7) and newblock.is_inside(point,tolerance=1e-7)
local=b.Vector(point).transform(b.Matrix(newframe.inverse().wrapped.Transformation()));assert 22<local.Z<27
mask=b.Pos(x,-65,55)*b.Box(20,100,130);oldregion=oldblock.intersect(mask);newregion=newblock.intersect(mask)
region_error=vol(oldregion.cut(newregion))+vol(newregion.cut(oldregion));assert region_error<1e-5
scan=[]
for t in range(45,66):
 q=(360-t)%360;frame=corrected_slider_frames(q,0,R,L,x,measured_cad_rest_phase_degrees=0)['rod']*b.Pos(*o['position_cad_mm']);v=vol((frame*bolt).intersect(newregion));scan.append(dict(local_crank_deg=t,event_deg=q,overlap_mm3=v))
peak=max(scan,key=lambda row:row['overlap_mm3'])
files=[Path(__file__),ROOT/'cad/engine/first_assembly.py',ROOT/'inventory/engine/dimensions.json',ROOT/'inventory/engine/full-assembly.json',ROOT/'cad/engine/assembly_math.py',ROOT/'cad/engine/engine_clockwise_pose_candidate.py',ROOT/'inventory/engine/engine-corrected-combined-motion-validation.json']+list(paths.values())
r=dict(status='CONFIRMED inherited placeholder bolt-head/block interference; no geometry change',inputs={str(p.relative_to(ROOT)):sha(p) for p in files},bolt_source_replay_difference_mm3=replay_error,old_new_pose_matrix_difference=frame_error,canonical_block_overlap_mm3=oldvolume,candidate_block_overlap_mm3=newvolume,local_block_region_difference_mm3=region_error,strict_witness_world_mm=point,strict_witness_bolt_local_mm=list(local),witness_radius_from_crank_axis_mm=math.hypot(point[1],point[2]),declared_crankcase_clearance_radius_mm=98.,phase_scan=scan,largest_sample=peak,dimensions=dict(shank_diameter_mm=P['bolt_diameter'],shank_axial_mm=[-31,23],head_axial_mm=[22,27],hex_circumradius_mm=7,hex_across_flats_mm=14*math.cos(math.pi/6),bolt_spacing_half_mm=P['bolt_spacing_half']),evidence_claims={k:claims[k] for k in ['bolt_diameter','bolt_spacing_half','rod_width','rod_outer_radius','rod_length']},limits=['Head size/height and shank length are literal illustrative source-code values, not primary sourced dimensions','No factory rod bolt identity, thread or pressed shoulder dimensions established','R98 crankcase cutter is also an estimate; current evidence cannot choose a physical correction','Phase scan is21 samples, not global maximum proof','No clearance-only block cut or bolt resizing performed'])
(ROOT/'inventory/engine/engine-corrected-rod-bolt-conflict-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],oldvolume,newvolume,peak,flush=True)
