"""Cross-language source-v2 linkage and installed transform fixtures."""
from pathlib import Path
import json,sys,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
from valve_source_integration import state,annotate_manifest,apply_valve_transforms
import valve_source_layout as v
import build123d as b
OUT=ROOT/'cad/engine/candidates/valve-source-all12'
angles=[0,111,150,180,210,246,282,333,342,360,372,420,468,516,540,564,603,720]
rows=[]
for a in angles:
 for c in range(1,7):
  for k in ['intake','exhaust']:
   s=state(a,c,k)
   poses=[]
   rest=v.solve(0,k)
   for role in ['lifter','valve','rocker','pushrod','spring']:
    angle=rest['angle'] if role=='rocker' else (-math.atan2(rest['top'][0]-rest['bottom'][0],rest['top'][1]-rest['bottom'][1]) if role=='pushrod' else 0)
    meta={'model':'source-sized-v2','role':role,'cylinder':c,'kind':k}
    loc=b.Pos(10,20,30)*b.Rot(math.degrees(angle),0,0)
    changed=apply_valve_transforms({'occurrences':[{'id':'probe','valvetrain':meta}]},{'probe':loc},a)['probe']
    points=[list((changed*b.Vertex(*q)).to_tuple()) for q in [(0,0,0),(1,0,0),(0,1,0),(0,0,1)]]
    poses.append({'metadata':meta,'rest_angle':angle,'points':points})
   rows.append({'crank_deg':a,'cylinder':c,'kind':k,'state':s,'poses':poses})
(OUT/'motion-api-fixtures.json').write_text(json.dumps(rows,indent=2)+'\n')
m=json.loads((OUT/'baseline/manifest.json').read_text());n=annotate_manifest(m)
assert annotate_manifest(n)==n
assert [o['id'] for o in m['occurrences']]==[o['id'] for o in n['occurrences']]
print(len(rows),'fixtures; idempotent annotation; occurrence identities preserved')
