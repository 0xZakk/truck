#!/usr/bin/env python3
"""Internal non-contact pairs using exported solids and conservative spring envelope."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import front_seal_2692_candidate as c
OUT=ROOT/'cad/engine/generated/front-seal-2692-candidate';names=['cover','damper-hub','seal-case-installed','seal-elastomer','seal-garter-spring'];paths={n:OUT/(n+'.step') for n in names};q={n:b.import_step(p) for n,p in paths.items()};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return sum(abs(solid_volume(x,'adaptive')) for x in s.solids()) if s else 0.
r={'inputs':{str(p.relative_to(ROOT)):sha(p) for p in [Path(__file__),Path(c.__file__),ROOT/'cad/engine/cad_metrics.py']+list(paths.values())},'pairs':[]}
for a,z in [('cover','damper-hub'),('cover','seal-elastomer'),('seal-case-installed','damper-hub')]:
 gap=q[a].distance_to(q[z]);overlap=vol(q[a].intersect(q[z]));assert gap>.01 and overlap<1e-5,(a,z,gap,overlap);r['pairs'].append({'pair':[a,z],'gap_mm':gap,'overlap_mm3':overlap,'method':'exported solid pair'})
# Each ruled circular section is contained in the convex hull of its endpoint
# disks. Relative to a rotating major-circle frame, maximum additional error
# is bounded by outer support radius times major arc sagitta. Inflate by .001.
minor=c.COIL_R+c.WIRE_R+.001;sagitta=(c.SPRING_R+c.COIL_R+c.WIRE_R)*(1-math.cos(math.pi/(c.TURNS*48)));assert sagitta<.001
envelope=b.Pos(c.SPRING_X,0,0)*b.Rot(0,90,0)*b.Torus(c.SPRING_R,minor)
r['spring_bound']={'minor_radius_mm':minor,'major_arc_sagitta_bound_mm':sagitta,'basis':'ruled endpoint-disk convex hull plus major-frame sagitta; nominal section radii from bound source code','continuous':True}
for z in ['cover','damper-hub','seal-case-installed']:
 gap=envelope.distance_to(q[z]);v=vol(envelope.intersect(q[z]));assert gap>.01 and v<1e-5,(z,gap,v);r['pairs'].append({'pair':['seal-garter-spring',z],'conservative_gap_mm':gap,'envelope_overlap_mm3':v,'method':'conservative continuous winding envelope against exported neighbor'})
fault=b.Pos(0,0,4)*envelope;r['negative_control_displaced_spring_case_overlap_mm3']=vol(fault.intersect(q['seal-case-installed']));assert r['negative_control_displaced_spring_case_overlap_mm3']>.1
r['status']='PASS all six non-contact internal pairs; four intended contact pairs checked separately';(ROOT/'inventory/engine/front-seal-2692-internal-clearance-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'])
