"""Export independent Python reference points for the browser numeric adapter."""
from pathlib import Path
import importlib.util,json,hashlib
R=Path(__file__).resolve().parents[1]
p=R/'scripts/valve-spring-reconciliation-20261003-c1-study.py'
spec=importlib.util.spec_from_file_location('numeric',p);n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
out={'inputs':{str(p.relative_to(R)):sha(p), 'reference/engine/valve-spring-reconciliation-20261003-audit.json':sha(n.P.with_name(n.P.name+'-audit.json'))},'parameters':{},'fixtures':[]}
for kind in ('intake','exhaust'):
 s=n.Spring(kind,'literal_angular_count')
 out['parameters'][kind]={'radius':s.r,'wire':s.d,'free':s.free,'solid':s.solid,'freeTurns':s.T0,'endPitch':s.pe,'grind':s.g,'wireLength':s.L}
 for i in range(21):
  h=s.solid+.01+(s.free-s.solid-.01)*i/20;t,pitch=s.state(h)
  us=[0,.375,.75,.875,1,t/2,t-1,t-.875,t-.75,t-.375,t]
  points=s.points(us,t,pitch);points[:,2]-=-s.d/2+s.g
  out['fixtures'].append({'kind':kind,'height':h,'turns':t,'pitch':pitch,'u':us,'points':points.tolist()})
(R/'reference/engine/valve-spring-reconciliation-20261003-browser-fixtures.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out['parameters'],indent=2))
