"""Probe actual casting openings and hardware clearance, not just bounding boxes."""
from pathlib import Path
import json,sys
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from first_assembly import cx
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())
d={d['id']:d for d in m['definitions']}
s={k:b.import_step(ROOT/d[k]['step'].lstrip('/')) for k in ['coolant-outlet-housing','coolant-outlet-gasket','coolant-outlet-bolt']}
results=[]
for name,probe in [
 ('thermostat throat',b.Pos(14.5,0,0)*cx(26.9,27.5)),
 ('taper center',b.Pos(37,0,0)*b.Sphere(3)),
 ('neck elbow center',b.Pos(70.556349,0,6.443651)*b.Sphere(3)),
 ('hose neck bore',b.Pos(77,0,60)*b.Cylinder(15.9,48)),
 ('secondary passage',b.Pos(19,28,-30)*cx(10.9,40)),
 ('left mounting hole',b.Pos(3.7,-40,0)*cx(.313*25.4/2-.02,5.9)),
 ('right mounting hole',b.Pos(3.7,40,0)*cx(.313*25.4/2-.02,5.9))]:
 hit=s['coolant-outlet-housing'].intersect(probe)
 vol=sum(x.volume for x in hit.solids()) if hit else 0
 assert vol<.1,(name,vol)
 results.append(name)
# A connected six-mm-diameter probe verifies an unbroken route through the
# throat, transition, elbow and hose neck, beyond isolated point samples.
quadrant=b.Pos(90,0,-13)*b.Box(70,100,70)
bend=(b.Pos(55,0,22)*b.Rot(90,0,0)*b.Torus(22,3)) & quadrant
channel=b.Pos(27.5,0,0)*cx(3,55)+bend+b.Pos(77,0,54)*b.Cylinder(3,64)
assert len(channel.solids())==1
hit=s['coolant-outlet-housing'].intersect(channel)
assert not hit or sum(x.volume for x in hit.solids())<.1
results.append('continuous six-mm-diameter main flow route')
for y in [-40,40]:
 bolt=b.Pos(0,y,0)*s['coolant-outlet-bolt']
 hit=s['coolant-outlet-housing'].intersect(bolt)
 assert not hit or sum(x.volume for x in hit.solids())<.1
report={'open_passages':results,'bolt_clearance':'pass','source':'dorman-902-1002','limits':'Probes validate modeled openings only. Head-side connection, production flow area, hose fit, thread form and production dimensions remain unverified.'}
(ROOT/'inventory/engine/coolant-outlet-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
