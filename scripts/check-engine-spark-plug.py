"""Audit catalog envelope and free firing gap of one reusable plug study."""
from pathlib import Path
import json,math,itertools
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())
defs={d['id']:d for d in m['definitions'] if d['id'].startswith('spark-plug-')}
s={k:b.import_step(ROOT/d['step'].lstrip('/')) for k,d in defs.items()}
assert len(s)==9
shell=s['spark-plug-shell'];assert abs(shell.bounding_box().min.Z+11.684)<1e-6
# Sample nominal threaded envelope, and directly bound the hex along its flats.
section=shell.intersect(b.Pos(0,0,-5)*b.Box(50,50,6));assert abs(section.bounding_box().size.X-18)<.01
# The external thread must alternate metal/void and repeat at its modeled pitch.
occupancy=[]
for i in range(30):
 z=-8+i*.045
 inside=shell.is_inside((8.65,0,z))
 assert inside==shell.is_inside((8.65,0,z+1.5))
 occupancy.append(inside)
assert any(occupancy) and not all(occupancy)
hexpart=shell.intersect(b.Pos(0,0,9)*b.Box(50,50,.01));assert abs(hexpart.bounding_box().size.Y-20.6375)<1e-6
center=s['spark-plug-center-electrode'];ground=s['spark-plug-ground-electrode']
gap=center.distance_to(ground);assert abs(gap-1.1176)<1e-6,gap
collisions=[]
for a,c in itertools.combinations(s,2):
 v=s[a].intersect(s[c]);vol=sum(z.volume for z in v.solids()) if v else 0
 if vol>.1:collisions.append({'a':a,'b':c,'volume_mm3':vol})
report={'nominal_thread_diameter_mm':18,'reach_mm':11.684,'hex_across_flats_mm':20.6375,'firing_gap_mm':gap,'modeled_thread_pitch_mm':1.5,'thread_periodicity':'pass','collisions':collisions,'limits':'Reusable study envelope only; family-derived thread pitch/tolerances, production internals and head fit remain unverified.'}
(ROOT/'inventory/engine/spark-plug-validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));assert not collisions
