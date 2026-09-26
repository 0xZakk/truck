"""Sample distributor movement and internal clearances; not an installation audit."""
from pathlib import Path
import sys,json,math,itertools
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())
d={d['id']:d for d in m['definitions']}
parts=[o for o in m['occurrences'] if o['parent'] in ['distributor-assembly','distributor-rotation']]
assert len(parts)>20
shapes={o['id']:b.import_step(ROOT/d[o['definition']]['step'].lstrip('/')) for o in parts}
collisions=[];count=0
for angle in range(0,721,60):
 loc=transforms(m,angle)
 # Check linkage ratio by following a point on the rotor away from its axis.
 p=b.Vertex(10,0,0).moved(loc['distributor-rotor']).center()
 t=math.radians(-angle/2)
 assert abs(p.X-(200+10*math.cos(t)))<1e-6
 assert abs(p.Y-(190+10*math.sin(t)))<1e-6
 placed={id:s.moved(loc[id]) for id,s in shapes.items()}
 boxes={id:s.bounding_box() for id,s in placed.items()}
 for a,c in itertools.combinations(placed,2):
  if not all(min(getattr(boxes[a].max,k),getattr(boxes[c].max,k))-max(getattr(boxes[a].min,k),getattr(boxes[c].min,k))>.01 for k in ['X','Y','Z']):continue
  count+=1;v=placed[a].intersect(placed[c]);volume=sum(s.volume for s in v.solids()) if v else 0
  if volume>.1:collisions.append({'crank_degrees':angle,'a':a,'b':c,'volume_mm3':round(volume,4)})
report={'sampled_crank_angles':list(range(0,721,60)),'candidate_pairs':count,'half_speed_rotation':'pass','clockwise_viewed_from_cap':'pass','collisions':collisions,'limits':'Sampled internal geometry only. Clockwise direction follows factory firing-order diagram. No cam gear engagement, cylinder indexing, spark timing or electrical simulation.'}
(ROOT/'inventory/engine/distributor-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
assert not collisions
