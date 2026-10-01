#!/usr/bin/env python3
"""Independent positive-material witnesses for nominal seal load/contact paths."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import front_seal_2692_candidate as c
OUT=ROOT/'cad/engine/generated/front-seal-2692-candidate';names=['damper-hub','seal-case-installed','seal-elastomer','seal-garter-spring'];paths={n:OUT/(n+'.step') for n in names};q={n:b.import_step(p) for n,p in paths.items()};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return sum(abs(solid_volume(x,'adaptive')) for x in s.solids()) if s else 0.
r={'status':'RUNNING','inputs':{str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),Path(c.__file__),ROOT/'cad/engine/cad_metrics.py']+list(paths.values())},'positive_bands':{},'garter_contact_witnesses':[]}
for name,owner,ri,ro,a,z in [('bond-metal','seal-case-installed',27.601,27.61,427.4,428.9),('bond-rubber','seal-elastomer',27.59,27.599,427.4,428.9),('lip-rubber','seal-elastomer',c.TRACK_R+.001,c.TRACK_R+.01,427.95,428.15),('lip-hub','damper-hub',c.TRACK_R-.01,c.TRACK_R-.001,427.95,428.15)]:
 probe=c.ring(ro,ri,a,z);v=vol(probe);missing=vol(probe.cut(q[owner]));assert v>.1 and missing<1e-5,(name,missing);r['positive_bands'][name]={'probe_mm3':v,'missing_mm3':missing}
# 96 winding-specific pairs of strict interior witnesses, either side of the
# shared groove at quarter phase; this is sampled support, not force/preload.
for j in range(c.TURNS):
 t=2*math.pi*(j+.25)/c.TURNS;x=c.SPRING_X+c.COIL_R+c.WIRE_R
 p=(x-.003,c.SPRING_R*math.cos(t),c.SPRING_R*math.sin(t));z=(x+.003,p[1],p[2]);a=any(s.is_inside(p,1e-6) for s in q['seal-garter-spring'].solids());b_=any(s.is_inside(z,1e-6) for s in q['seal-elastomer'].solids());assert a and b_,(j,a,b_);r['garter_contact_witnesses'].append({'turn':j,'wire_inside':a,'rubber_inside':b_})
r['negative_control_shifted_rubber_accepts_old_witness']=any(s.is_inside(z,1e-6) for s in (b.Pos(4,0,0)*q['seal-elastomer']).solids());assert not r['negative_control_shifted_rubber_accepts_old_witness']
r['coverage']='Complete annular bond/lip positive bands; 96 sampled winding groove witnesses. Nominal axisymmetric track supports arbitrary crank angle; endplay/preload unknown.';r['status']='PASS positive exported material bands and sampled spring seating'
(ROOT/'inventory/engine/front-seal-2692-contact-bands-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
