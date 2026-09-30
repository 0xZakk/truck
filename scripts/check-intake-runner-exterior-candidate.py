#!/usr/bin/env python3
"""Cheap isolated runner exterior feasibility before whole-neighbor audit."""
from pathlib import Path
import hashlib,json,sys
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import intake_runner_exterior_candidate as c
from assembly_math import transforms
from cad_metrics import solid_volume
OUT=ROOT/'cad/engine/generated/intake-runner-exterior-study';OUT.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return sum(abs(solid_volume(q,'adaptive')) for q in s.solids()) if s else 0.
def diff(a,z):
 aa=list(a.solids()) if a else [];zz=list(z.solids()) if z else []
 if not aa:return vol(z)
 if not zz:return vol(a)
 aa=b.Compound(children=aa);zz=b.Compound(children=zz)
 return vol(aa-zz)+vol(zz-aa)
def main():
 mp=ROOT/'inventory/engine/full-assembly.json';m=json.loads(mp.read_text());d=next(d for d in m['definitions'] if d['id']=='efi-upper-intake');sp=ROOT/d['step'].lstrip('/')
 inputs=[sp,Path(__file__),ROOT/'cad/engine/intake_runner_exterior_candidate.py',ROOT/'cad/engine/upper_intake_clearance_candidate.py',ROOT/'cad/engine/cad_metrics.py',ROOT/'reference/engine/intake-runner-exterior-review.json']
 before={str(p.relative_to(ROOT)):sha(p) for p in inputs};pose=transforms(m)['efi-upper-intake'];old=pose*b.import_step(sp)
 shape,exterior,air,curves=c.parts(old);print('Built lofts/union',shape.is_valid,len(shape.solids()),flush=True)
 if not shape.is_valid or len(shape.solids())!=1:
  failure=dict(status='FAIL invalid fused candidate',valid=shape.is_valid,solid_count=len(shape.solids()),input_sha256_before=before)
  (ROOT/'inventory/engine/intake-runner-exterior-candidate-validation.json').write_text(json.dumps(failure,indent=2)+'\n')
  raise AssertionError('Invalid geometry; further gates not run')
 b.export_step(shape,OUT/'runner-exterior.step');shape=b.import_step(OUT/'runner-exterior.step');b.export_step(old,OUT/'baseline.step')
 added=b.Compound(children=list((shape-old).solids()))
 regions={
 'lower_flange_seven_studs':b.Pos(0,-228,366.5)*b.Box(800,60,15),
 'throttle_flange_ports':b.Pos(200,25,490)*b.Box(16,124,68),
 'EGR_flange_port':b.Pos(-197,25,514)*b.Box(16,62,28),
 'regulator_vacuum_seat_R10':b.Pos(0,-47,460)*b.Rot(90,0,0)*b.Cylinder(10,20),
 'existing_plenum_wall':b.Pos(0,125,490)*b.Box(500,345,120)}
 protected={name:diff(shape&r,old&r) for name,r in regions.items()};air_hit=vol(added&air)
 enclosure=b.Pos(300,-12,414.75)*b.Cylinder(15.9,41.5)+b.Pos(300,-12,435)*b.Cylinder(37,44);cap_hit=vol(shape&enclosure)
 print('Protected',protected,'air',air_hit,'cap',cap_hit,flush=True)
 after={str(p.relative_to(ROOT)):sha(p) for p in inputs};assert before==after
 report=dict(status='PASS cheap feasibility; full-neighbor/motion/export/render gates NOT RUN' if shape.is_valid and len(shape.solids())==1 and max(protected.values())<.1 and air_hit<.1 and cap_hit<.1 else 'FAIL cheap feasibility',input_sha256_before=before,input_sha256_after=after,source_manifest_snapshot_sha256=sha(mp),intake_pose_mm=[list(pose.position),list(pose.orientation)],valid=shape.is_valid,solid_count=len(shape.solids()),exterior_lofts=[dict(valid=s.is_valid,solids=len(s.solids())) for s in exterior],added_material_mm3=vol(added),protected_difference_mm3=protected,new_air_blockage_mm3=air_hit,cap_withdrawal_overlap_mm3=cap_hit,step_sha256=sha(OUT/'runner-exterior.step'),limits=['Cheap feasibility only; no source-to-render comparison, GLB, full neighbors or new motion audit yet.','No PCV receiver datum is accepted; protected original plenum wall, no arbitrary port.','All cross-section and wall assumptions inferred.'])
 (ROOT/'inventory/engine/intake-runner-exterior-candidate-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(report['status']);assert report['status'].startswith('PASS')
if __name__=='__main__':main()
