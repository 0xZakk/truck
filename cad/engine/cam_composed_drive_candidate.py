"""Compose frozen corrected drive gear into frozen corrected-lobe cam locally."""
from pathlib import Path
import hashlib,math
import build123d as b
ROOT=Path(__file__).resolve().parents[2]
CAM=ROOT/'cad/engine/generated/cam-clockwise-candidate/camshaft-local.step'
GEAR=ROOT/'cad/engine/generated/crossed-oil-drive-corrected-pair/cam-drive-gear-local.step'
CAM_SHA='81933607c28c521f8f077239e16174a5d718c9aec0f1e4450ac041b1931fbc68'
GEAR_SHA='a8c0288344579f739983e3b7a29858c4806f364351917be11b3cf82bf5b23b29'
X=227.584
WIDTH=12.
CORE=15.
TIP=18+36*math.cos(math.radians(45))/16

def cylinder(radius,length=WIDTH):
 return b.Pos(X,0,0)*b.Rot(0,90,0)*b.Cylinder(radius,length)

def mask():return cylinder(TIP).cut(cylinder(CORE))

def build():
 for p,h in [(CAM,CAM_SHA),(GEAR,GEAR_SHA)]:
  assert hashlib.sha256(p.read_bytes()).hexdigest()==h,p
 cam=b.import_step(CAM);gear=b.Pos(X,0,0)*b.import_step(GEAR)
 remainder=cam.cut(mask());out=remainder.fuse(gear)
 assert out.is_valid and len(out.solids())==1
 return out.solids()[0]
