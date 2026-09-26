"""Focused rear journal/bearing and twelve gasket passage candidate checks."""
from pathlib import Path
import argparse,hashlib,json,sys,tempfile
import build123d as b
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--assembly-root',type=Path,required=True);args=p.parse_args();MODEL=args.assembly_root
sys.path.insert(0,str(MODEL/'cad/engine'));sys.path.insert(1,str(ROOT/'cad/engine'))
import rear_cam_clearance_desktop as fix
from assembly_math import transforms
from valve_layout_integration import occurrence_shape
from cad_metrics import solid_volume
from first_assembly import P
raw=(MODEL/'inventory/engine/full-assembly.json').read_bytes();m=json.loads(raw);ds={d['id']:d for d in m['definitions']};os={o['id']:o for o in m['occurrences']};cache={};hashes={}
def load(name):
 if name not in cache:
  path=MODEL/ds[name]['step'].lstrip('/');hashes[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest();cache[name]=b.import_step(path)
 return cache[name]
def volume(s):return sum(solid_volume(q,'adaptive') for q in s.solids()) if s else 0
def common(a,c):return volume(a.intersect(c))
rad=sum(P['camshaft_journal_diameter_range'])/4
cam=fix.cam_interface(load('camshaft'),rad)
stations=[o['position_cad_mm'][0] for o in m['occurrences'] if o['id'].endswith(('-intake-valve','-exhaust-valve'))]
gasket=fix.gasket_interface(load('head-gasket'),stations)
checks=[];fail=[]
for name,shape in [('camshaft',cam),('head-gasket',gasket)]:
 assert shape.is_valid and len(shape.solids())==1,name
 with tempfile.TemporaryDirectory() as td:
  f=Path(td)/'s.step';b.export_step(shape,f);s=b.import_step(f)
  delta=abs(volume(s)-volume(shape));assert s.is_valid and len(s.solids())==1 and delta<.02,(name,delta)
  checks.append({'roundtrip':name,'delta_mm3':delta})
poses=transforms(m,0);bearing=b.Pos(fix.NEW_STATION,90,72)*load('cam-bearing');placedcam=poses['camshaft']*cam
neighbors=['block','crankshaft','rear-cam-plug']+[f'c{i}-{kind}-lifter-body' for i in range(1,7) for kind in ['intake','exhaust']]
for name in neighbors:
 other=poses[name]*load(os[name]['definition'])
 for changed,s in [('camshaft',placedcam),('cam-bearing-1',bearing)]:
  v=common(s,other);checks.append({'a':changed,'b':name,'volume_mm3':v})
  if v>.01:fail.append(checks[-1])
# Positive radial-envelope checks prevent a clearance pass from deleting the journal.
core=fix.axial(rad-.01,fix.WIDTH-.02,fix.NEW_STATION)
missing=volume(core)-common(cam,core);assert missing<.001,missing
# Lifter and port motion checks across a full engine cycle.
rodids=[o['id'] for o in m['occurrences'] if o.get('valvetrain',{}).get('role')=='pushrod']
for angle in range(0,721,15):
 pose=transforms(m,angle);g=pose['head-gasket']*gasket
 for name in rodids:
  v=common(g,pose[name]*load(os[name]['definition']))
  if v>.001:fail.append({'a':'head-gasket','b':name,'angle':angle,'volume_mm3':v})
 print('Gasket passages',angle,flush=True)
assert raw==(MODEL/'inventory/engine/full-assembly.json').read_bytes()
assert all(hashlib.sha256(Path(path).read_bytes()).hexdigest()==h for path,h in hashes.items())
report={'passed':not fail,'manifest_sha256':hashlib.sha256(raw).hexdigest(),'checks':checks,'gasket_motion_checks':49*len(rodids),'positive_journal_missing_mm3':missing,'failures':fail,'inputs':hashes,'limits':fix.GAPS}
(ROOT/'inventory/engine/rear-cam-clearance-desktop-validation.json').write_text(json.dumps(report,indent=2)+'\n')
print('RESULT',report['passed'],'failures',fail,flush=True)
assert not fail
