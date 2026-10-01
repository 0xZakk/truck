#!/usr/bin/env python3
"""Exact spherical-interface neighborhood comparison for new common rocker."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import timing_valvetrain_inclined_candidate as c
oldp=ROOT/'cad/engine/generated/rocker-arm.step';newp=ROOT/'cad/engine/generated/timing-valvetrain-inclined-candidate/rocker-arm.step'
a=b.import_step(oldp);z=b.import_step(newp)
def vol(q):return sum(abs(solid_volume(s,'adaptive')) for s in q.solids()) if q else 0.
def diff(a,z):return vol(a.cut(z))+vol(z.cut(a))
mask=b.Sphere(15.05);fulcrum=diff(a.intersect(mask),z.intersect(mask))
oldcup=(0,c.v.PUSHROD_Y-c.v.PIVOT_Y,c.v.CUP_Z);newcup=(0,c.P['PUSHROD_Y']-c.P['PIVOT_Y'],c.P['CUP_Z'])
ac=b.Pos(*[-v for v in oldcup])*a;zc=b.Pos(*[-v for v in newcup])*z
cup=diff(ac.intersect(b.Sphere(c.v.BALL_R+.05)),zc.intersect(b.Sphere(c.v.BALL_R+.05)))
# Pad patch compared after translating each modeled pad center to origin.
ap=b.Pos(0,-(c.v.VALVE_Y-c.v.PIVOT_Y),-c.v.PAD_CENTER_Z)*a
zp=b.Pos(0,-(c.v.VALVE_Y-c.P['PIVOT_Y']),-c.v.PAD_CENTER_Z)*z
pad=diff(ap.intersect(b.Pos(0,0,-11)*b.Box(16,16,3)),zp.intersect(b.Pos(0,0,-11)*b.Box(16,16,3)))
assert max(fulcrum,cup,pad)<1e-5,(fulcrum,cup,pad)
r={'status':'PASS exact protected contact neighborhoods','input_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(c.__file__),oldp,newp]},'symmetric_difference_mm3':{'fulcrum_R15p05':fulcrum,'aligned_ball_socket_Rplus0p05':cup,'aligned_pad_bottom_patch':pad},'limits':['Only declared contact neighborhoods; entire estimated rocker contour intentionally differs.']}
(ROOT/'inventory/engine/timing-valvetrain-inclined-rocker-interfaces-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
