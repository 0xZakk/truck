"""Independent saved STEP replay, including near-tip ridge negative control."""
from pathlib import Path
import json,hashlib,math,sys
import build123d as b
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import airbox_screw_online_20261002 as c
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
f=R/'reference/engine/airbox-screw-online-20261002-validation.json';d=json.loads(f.read_text())
for p,h in (d['inputs']|d['asset_hashes']).items():assert sha(R/p)==h,p
s=b.import_step(R/d['step']);assert s.is_valid and len(s.solids())==1
for q in d['thread_probes']:assert s.is_inside((2.95*math.cos(q['theta']),2.95*math.sin(q['theta']),q['z']))==q['expected_inside']
p=c.PARAMETERS;rows=[]
def point_probes(shape):
 results=[]
 for angle in range(8):
  theta=angle*math.pi/4
  for k in [9,10]:
   for off,want in [(0,True),(.5,False)]:
    z=(k+angle/8+off)*p['pitch']
    if not 16<z<18.9:continue
    radius=.94*(p['major_diameter']/2+(z-15)*(p['estimated_tip_radius']-p['major_diameter']/2)/4)
    got=shape.is_inside((radius*math.cos(theta),radius*math.sin(theta),z));results.append(got==want)
    if shape is s:rows.append({'theta':theta,'z':z,'radius':radius,'expected_inside':want,'actual_inside':got})
 return all(results)
assert point_probes(s),rows
outside_count=0
for j in range(1,40):
 z=15+j*.1
 r=p['major_diameter']/2+(z-15)*(p['estimated_tip_radius']-p['major_diameter']/2)/4+.03
 for i in range(24):
  theta=i*math.pi/12
  assert not s.is_inside((r*math.cos(theta),r*math.sin(theta),z))
  outside_count+=1
smooth=c.envelope();assert not point_probes(smooth)
old=b.import_step(c.O/'attempt1-air-cleaner-body-bracket-screw.step');assert not point_probes(old)
out={'status':'PASS independent saved-STEP replay and tapered-profile control','inputs':{str(f.relative_to(R)):sha(f),d['step']:sha(R/d['step']),str(Path(__file__).relative_to(R)):sha(Path(__file__)),str((c.O/'attempt1-air-cleaner-body-bracket-screw.step').relative_to(R)):sha(c.O/'attempt1-air-cleaner-body-bracket-screw.step')},'valid':s.is_valid,'solids':len(s.solids()),'body_thread_probes_passed':80,'tip_thread_probes':rows,'outside_taper_envelope_probes':outside_count,'smooth_point_rejected':True,'original_smooth_tip_attempt_rejected':True,'scope':'Sampled material alternation in saved STEP, not manufacturing gauge or receiving-pilot acceptance.'}
(R/'reference/engine/airbox-screw-online-20261002-replay.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS',len(rows),'point probes')
