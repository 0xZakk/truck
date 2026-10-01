#!/usr/bin/env python3
import sys,json,math,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import oil_drive_layout as d
from assembly_math import transforms
from timing_block_axis_feature_candidate import DELTA
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text());f=transforms(m);defs={x['id']:x for x in m['definitions']};os={x['id']:x for x in m['occurrences']}
def sh(i):return f[i]*b.import_step(ROOT/defs[os[i]['definition']]['step'].lstrip('/'))
def volume(s):return sum(x.volume for x in s.solids())
tube=sh('oil-pickup-tube');pump=sh('oil-pump-housing');p=d.PUMP_FRAME;shift=b.Pos(*DELTA)
replay=d.pickup_tube(); rows=[]
for x in [-34,-33.9,-33,-32,-31,-30]:
 row={'pump_local_x_mm':x}
 for name,s in [('pump',pump),('old_tube',tube),('stale_tube_in_shifted_frame',shift.inverse()*tube)]:
  row[name]={}
  for r in [0,4.7,5.4,6.1,6.5]:
   n=72;pts=[(p*b.Vertex(x,r*math.cos(i*math.tau/n),5+r*math.sin(i*math.tau/n))).center() for i in range(n)]
   row[name][str(r)]={'inside_count':sum(s.is_inside(v,tolerance=1e-7) for v in pts),'sample_count':n}
 rows.append(row)
inputs=['scripts/probe-shifted-oil-drive-inlet.py','cad/engine/oil_drive_layout.py','cad/engine/timing_block_axis_feature_candidate.py','inventory/engine/full-assembly.json','cad/engine/generated/oil-pump-housing.step','cad/engine/generated/oil-pickup-tube.step']
out={'inputs':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in inputs},'status':'DIAGNOSTIC only; no geometry change','source_replay_difference_mm3':volume(tube.cut(replay))+volume(replay.cut(tube)),'actual_strict_point_sections':rows,'limits':['72 azimuth points per declared radius and Xstation, finite material probes','Current nominal tube starts at housing exterior tangent plane; full annular insertion/support is not established','Source replay Boolean accompanied by actual material probes; no new CAD acceptance']}
Path(ROOT/'inventory/engine/shifted-oil-drive-inlet-probes.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
