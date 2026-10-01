"""Five isolated female socket revisions; frozen sealing geometry elsewhere."""
from pathlib import Path
import build123d as b
ROOT=Path(__file__).resolve().parents[2]
FROZEN=ROOT/'cad/engine/generated/timing-cover-front-joint-candidate'
MALE=ROOT/'cad/engine/generated/pan-fastener-thread-candidate'
PARTS=('cover','main-gasket','future-block-land','front-terminal-sealant','pan-gasket','pan')
RELOCATIONS={20:(365.5,-132.,-32.1),10:(365.5,196.,-32.1),21:(390.,-110.,-32.1),23:(390.,0.,-67.),22:(390.,180.,-32.1)}
def norm(s):
 if s is None:return None
 shapes=s if isinstance(s,b.ShapeList) else [s]
 solids=[b.Solid(q.wrapped) for x in shapes if x.wrapped is not None for q in x.solids()]
 if not solids:return None
 return solids[0] if len(solids)==1 else b.Compound(solids)
def cz(r,a,z):return b.Pos(0,0,(a+z)/2)*b.Cylinder(r,z-a)
def load():return {k:norm(b.import_step(FROZEN/(k+'.step'))) for k in PARTS}
def build():
 parts=load();original=dict(parts)
 male=norm(b.import_step(MALE/'pan-screw.step'))
 female=norm(b.import_step(MALE/'female-test-coupon.step'))
 washer=norm(b.import_step(MALE/'existing-pan-washer.step'))
 occurrences={};owners={}
 for n,p in RELOCATIONS.items():
  owner='future-block-land' if p[0]<373 else 'cover';owners[n]=owner
  parts[owner]=norm(parts[owner].fuse(b.Pos(*p)*female))
  occurrences[f'oil-pan-mounting-screw-{n}']=b.Pos(*p)*male
  occurrences[f'oil-pan-mounting-washer-{n}']=b.Pos(*p)*washer
 return parts,original,occurrences,{'male':male,'female':female,'washer':washer},owners
