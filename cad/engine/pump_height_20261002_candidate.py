"""Replacement-height local stack; core stage intentionally has no external ports."""
from pathlib import Path
import json,math
import build123d as b
from assembly_clockwise_candidate import transforms
R=Path(__file__).resolve().parents[2];O=R/'cad/engine/generated/pump-height-20261002-candidate'
MP=R/'inventory/engine/corrected-engine-stage-v4.json'
REAR=R/'cad/engine/generated/waterpump-heater-source-candidate/housing.step'
def cx(r,start,end):return b.Solid.make_cylinder(r,end-start,b.Plane(origin=(start,-32,170),z_dir=(1,0,0)))
def section(x,r):return b.Plane(origin=(x,-32,170),z_dir=(1,0,0))*b.Circle(r)
def norm(s):return b.Compound(s)if isinstance(s,b.ShapeList)else s

def parts(height=98.43):
 m=json.loads(MP.read_text());d={x['id']:x for x in m['definitions']};t=transforms(m,0,0);occ={x['id']:x for x in m['occurrences']};inputs={}
 def world(n):
  p=R/d[occ[n]['definition']]['step'].lstrip('/');inputs[n]=p;return t[n]*b.import_step(p)
 delta=height-147.;shift=b.Pos(delta,0,0);out={}
 names=['water-pump-drive-hub','water-pump-bearing','water-pump-slinger']+[n for n in occ if n.startswith(('water-pump-seal-','water-pump-pulley-bolt-','fan-clutch-','cooling-fan-'))]
 for n in names:out[n]=shift*world(n)
 out['water-pump-shaft']=cx(8,365,519+delta)
 rear=b.import_step(REAR).intersect(b.Pos(189,-32,170)*b.Box(400,600,600)) # rear own-region X<=389
 front=world('water-pump-housing').intersect(b.Pos(708,-32,170)*b.Box(500,600,600)) # X>=458
 loft=b.loft([section(x,r)for x,r in[(383,66),(389,55),(458+delta,29)]],ruled=True)
 inner=b.loft([section(x,r)for x,r in[(374,59),(383,59),(389,51),(458+delta,24),(467+delta,24)]],ruled=True)
 out['water-pump-housing']=norm((rear+shift*front+loft)-inner)
 face=375+height
 # Flat annular web reaches original rim; estimated2.5mm thickness retained.
 pulley=(cx(75,459.56,487.56)-cx(72.5,459,489))+(cx(73,face,face+2.5)-cx(15.05,face-1,face+3.5))
 for a in range(0,360,90):pulley-=b.Pos(0,25*math.cos(math.radians(a)),25*math.sin(math.radians(a)))*cx(3.5,face-1,face+3.5)
 out['water-pump-pulley']=norm(pulley)
 return out,inputs
