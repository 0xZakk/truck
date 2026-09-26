"""Validate the uninstalled cover candidate; this does not establish engine fit."""
from pathlib import Path
import sys,json,tempfile,itertools
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from pushrod_cover import cover_shape,gasket_shape,grommet_shape,bolt_shape,STATIONS
s=cover_shape()
assert s.is_valid and len(s.solids())==1
with tempfile.TemporaryDirectory(prefix='truck-cover-') as d:
 p=Path(d)/'cover.step';b.export_step(s,p);r=b.import_step(p)
 assert r.is_valid and len(r.solids())==1
 assert abs(r.volume/s.volume-1)<1e-5
for x in STATIONS:
 assert not s.intersect(b.Pos(x,0,5)*b.Cylinder(6.7,30)), 'Circular mounting hole obstructed'
 for dx,dy in [(9,0),(0,9),(6.4,6.4)]:
  material=s.intersect(b.Pos(x+dx,dy,8.4)*b.Cylinder(.5,.8))
  assert material and material.volume>.6, 'Stamped recess breaks through the grommet seating land'
gasket=gasket_shape();grommet=grommet_shape();bolt=bolt_shape()
parts={'cover':s,'gasket':gasket}
for i,x in enumerate(STATIONS,1):
 parts[f'grommet-{i}']=b.Pos(x,0,0)*grommet
 parts[f'bolt-{i}']=b.Pos(x,0,7.8+.48*25.4-25.4)*bolt
for name,shape in parts.items():
 assert shape.is_valid and len(shape.solids())==1,name
collisions=[]
for (a,sa),(c,sc) in itertools.combinations(parts.items(),2):
 overlap=sa.intersect(sc);volume=sum(v.volume for v in overlap.solids()) if overlap else 0
 if volume>.01:collisions.append({'a':a,'b':c,'mm3':volume})
assert not collisions,collisions
with tempfile.TemporaryDirectory(prefix='truck-cover-assembly-') as d:
 p=Path(d)/'assembly.step';b.export_step(b.Compound(children=list(parts.values())),p)
 r=b.import_step(p);assert len(r.solids())==14 and all(v.is_valid for v in r.solids())
report={'candidate_valid_single_solid':True,'candidate_definitions':4,'candidate_occurrences':14,'internal_collisions':collisions,'step_round_trip':'pass','circular_mounting_holes':6,'grommet_seat_probes':18,
 'installed_in_engine':False,'verified_production_fit':False,
 'limits':'Photo-based six-hole architecture only. Envelope, sheet thickness, ribs and hole stations remain assumed. Perimeter gasket and six grommet/bolt pairs form an isolated candidate assembly. Block window and mounting bosses are not integrated; no compression or installed fit is verified.'}
p=ROOT/'inventory/engine/pushrod-cover-candidate-validation.json';p.write_text(json.dumps(report,indent=2)+'\n');print(p.read_text())
