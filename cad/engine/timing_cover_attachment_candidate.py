"""Isolated pan attachment revision; source-supported male threads, ideal female form.

Main cover hardware is deliberately not invented: seven hole axes are recorded,
but applicable screw lengths/thread/head/washer mapping are not established.
"""
from pathlib import Path
import json
import build123d as b
ROOT=Path(__file__).resolve().parents[2]
FROZEN=ROOT/'cad/engine/generated/timing-cover-front-joint-candidate'
PARTS=('cover','main-gasket','future-block-land','front-terminal-sealant','pan-gasket','pan')
# Keep physical identities: negative/positive rails 20/10; front left/center/right21/23/22.
RELOCATIONS={20:(365.5,-132.,-32.1),10:(365.5,196.,-32.1),21:(390.,-110.,-32.1),23:(390.,0.,-67.),22:(390.,180.,-32.1)}

def norm(s):
 if s is None:return b.Compound([])
 if isinstance(s,b.ShapeList):solids=[q for x in s for q in x.solids()]
 else:solids=list(s.solids())
 # Imported assembly children can retain local transforms after Location moves.
 # Use plain solids, not an assembly Compound carrying child metadata.
 if len(solids)==1:return b.Solid(solids[0].wrapped)
 return b.Compound([b.Solid(q.wrapped) for q in solids])

def cz(r,z0,z1):return b.Pos(0,0,(z0+z1)/2)*b.Cylinder(r,z1-z0)
def load():return {k:norm(b.import_step(FROZEN/(k+'.step'))) for k in PARTS}
def build():
 parts=load();original=dict(parts)
 screw=norm(b.import_step(ROOT/'cad/engine/generated/oil-pan-mounting-screw.step'))
 washer=norm(b.import_step(ROOT/'cad/engine/generated/oil-pan-mounting-washer.step'))
 # Ideal conjugate, zero-clearance teaching thread. This is casting material,
 # not a threaded insert or a claim of factory thread class/manufacturability.
 female=norm(cz(4.17,7.8,22.3)-norm(screw+cz(4.0,22.0,23.0)))
 occ={};changes={}
 for n,pos in RELOCATIONS.items():
  frame=b.Pos(*pos);owner='future-block-land' if pos[0]<373 else 'cover'
  parts[owner]=norm(parts[owner]+frame*female)
  for role,shape in [('screw',screw),('washer',washer)]:occ[f'oil-pan-mounting-{role}-{n}']=frame*shape
  changes[str(n)]={'position_cad_mm':pos,'rotation_cad_deg':[0,0,0],'parent':'oil-pan-fastener-assembly','socket_owner':owner,'nominal_thread':'5/16-18','female_form':'Ideal zero-clearance conjugate of current modeled male; estimated form, no thread class or preload claim.'}
 return parts,occ,{'screw':screw,'washer':washer,'female_teaching_form':female},changes,original
