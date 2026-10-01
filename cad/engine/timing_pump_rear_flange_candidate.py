"""Authorized estimated exterior contour only. Frozen source assets remain intact."""
from pathlib import Path
import json,hashlib
import build123d as b
from assembly_math import transforms
import timing_cover_seven_fastener_candidate as main
import water_pump_joint_candidate as pump
R=Path(__file__).resolve().parents[2];O=R/'cad/engine/generated/timing-pump-rear-flange-candidate'
AXIS=(-32.,170.);BOTTOM=(-24.3,103.5);BOSS_RADIUS=8.75;BOUNDARY_RADIUS=66.25
EXPECTED={'housing':'eb1210428b06759483a99fade22a1c1b613954c76aced701383aa0f08fb5498b','pump-gasket':'b0dc04a02df5928d546da6c23a94354c7fb93b0c2d3c296d23c6df6d016bfe88','cover':'c27ac0620982322ae414ed277518d87c5611d3c91b9a253dd8599b003cc69f40','main-gasket':'47a586fe0b00212529a41c492aefbf6e2225d62e4020107b925ae3534117a96b'}
cx=main.front.c.cx
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):
 if not s:return None
 ss=list(s.solids());return b.Compound(ss)if ss else None
def load():
 mp=R/'inventory/engine/full-assembly.json';m=json.loads(mp.read_text());poses=transforms(m);defs={q['id']:q for q in m['definitions']}
 paths={'housing':R/defs['water-pump-housing']['step'].lstrip('/'),'pump-gasket':R/defs['water-pump-gasket']['step'].lstrip('/'),'cover':R/'cad/engine/generated/timing-pan21-lateral-candidate/cover.step','main-gasket':R/'cad/engine/generated/timing-cover-attachment-v2/main-gasket.step'}
 assert all(sha(p)==EXPECTED[k]for k,p in paths.items())
 old={k:b.import_step(p)for k,p in paths.items()}
 for k,n in [('housing','water-pump-housing'),('pump-gasket','water-pump-gasket')]:old[k]=poses[n]*old[k]
 return old,paths,m,poses

def masks(radius=BOUNDARY_RADIUS):
 stock=cx(66,375,389,*AXIS)
 lug=cx(11.5,375,389,*BOTTOM).cut(cx(BOSS_RADIUS,374,390,*BOTTOM)).cut(stock)
 gasket=cx(9.5,373,375,*BOTTOM).cut(cx(BOSS_RADIUS,372,376,*BOTTOM)).cut(cx(65,372,376,*AXIS))
 window=b.Pos(379.5,5,120)*b.Box(13,60,60)
 boundary=cx(radius,372,387,*AXIS).intersect(window)
 return {'housing':lug,'pump-gasket':gasket,'cover':boundary,'main-gasket':boundary}

def build():
 old,paths,m,poses=load();cutters=masks();new={k:norm(s.cut(cutters[k]))for k,s in old.items()}
 return new,old,cutters,paths,m,poses
