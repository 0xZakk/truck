#!/usr/bin/env python3
"""Independent fault injection for runner air/interface/neighbor/cap checks."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'));sys.path.insert(0,str(ROOT/'scripts'))
import build123d as b
import intake_runner_exterior_candidate as c
from importlib import import_module
check=import_module('check-intake-runner-exterior-candidate');vol=check.vol;diff=check.diff
OUT=ROOT/'cad/engine/generated/intake-runner-exterior-study'
def main():
 inputs=[Path(__file__),OUT/'runner-exterior.step',OUT/'baseline.step',Path(c.__file__),Path(check.__file__)]
 before={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
 shape=b.import_step(OUT/'runner-exterior.step');old=b.import_step(OUT/'baseline.step');path=c.paths()[0]
 plane=b.Plane(origin=path@.55,z_dir=path%.55);air=plane*b.Cylinder(15,8);plugged=shape+air
 air_good=vol(shape&air);air_bad=vol(plugged&air);assert air_good<.1 and air_bad>1
 # A neighbor placed in the new broad face, outside the original round tube,
 # produces a positive newly-added overlap using the context audit predicate.
 tangent=path%.55;x=b.Vector(1,0,0)-tangent*tangent.dot(b.Vector(1,0,0));x=x.normalized()
 witness=b.Pos(*tuple((path@.55)+x*26))*b.Box(8,8,8)
 prior=vol(old&witness);now=vol(shape&witness);assert now-prior>1
 cap=b.Pos(300,-12,414.75)*b.Cylinder(15.9,41.5)+b.Pos(300,-12,435)*b.Cylinder(37,44)
 intruder=b.Pos(275,-12,450)*b.Box(65,10,10)
 cap_good=vol(shape&cap);cap_bad=vol(b.Compound(children=list((shape+intruder).solids()))&cap);assert cap_good<.1 and cap_bad>1
 region=b.Pos(200,25,490)*b.Box(16,124,68);cut=b.Pos(201,70,511)*b.Box(12,8,8)
 interface_good=diff(shape&region,old&region);interface_bad=diff((shape-cut)&region,old&region);assert interface_good<.1 and interface_bad>1
 after={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs};assert before==after
 result=dict(status='PASS fault controls',controls=dict(air=dict(unchanged_overlap_mm3=air_good,plugged_overlap_mm3=air_bad),neighbor=dict(prior_overlap_mm3=prior,new_overlap_mm3=now,added_overlap_mm3=now-prior),cap=dict(unchanged_overlap_mm3=cap_good,intrusion_overlap_mm3=cap_bad),interface=dict(unchanged_difference_mm3=interface_good,cut_seat_difference_mm3=interface_bad)),input_sha256_before=before,input_sha256_after=after)
 (ROOT/'inventory/engine/intake-runner-exterior-controls-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
