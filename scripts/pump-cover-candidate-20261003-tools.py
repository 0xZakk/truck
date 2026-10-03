from pathlib import Path
import sys,json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
from assembly_clockwise_candidate import transforms,occurrence_shape
import pump_cover_candidate_20261003 as c
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();mp=c.MP;m=json.loads(mp.read_text());pose=transforms(m,0,0);occ={x['id']:x for x in m['occurrences']};defs={x['id']:x for x in m['definitions']};ex=json.loads((R/'reference/engine/pump-cover-candidate-20261003-build.json').read_text());prior=json.loads((R/'inventory/engine/accessory-stage-v4-solids.json').read_text());bounds={n:np.array(q)for n,q in prior['bounds'].items()};loaded={};inputs={}
for n,v in ex['parts'].items():bounds[n]=np.array(v['bounds'])
def get(n):
 if n not in loaded:
  if n in ex['parts']:p=R/ex['parts'][n]['path'];assert sha(p)==ex['parts'][n]['sha256'];loaded[n]=b.import_step(p)
  else:
   p=R/defs[occ[n]['definition']]['step'].lstrip('/');assert sha(p)==prior['occurrence_geometry'][n]['sha256'];loaded[n]=pose[n]*occurrence_shape(occ[n],b.import_step(p),0,0)
  inputs[str(p.relative_to(R))]=sha(p)
 return loaded[n]
def vol(s):return sum(abs(solid_volume(q,'adaptive'))for q in c.norm(s).solids())if s else 0.
def cyl(r,lo,hi,y,z):return b.Solid.make_cylinder(r,hi-lo,b.Plane(origin=(lo,y,z),z_dir=(1,0,0)))
tools={};owners={}
for i,(y,z)in enumerate(c.MOUNTING,1):
 n=f'water-pump-mounting-screw-{i}';tools[f'pump{i}_socket_R10_5']=c.T*c.cylinder(10.5,389,435,y*c.G,z*c.G);owners[f'pump{i}_socket_R10_5']=n
 # Exact estimated hex-head cross-section swept31.75mm along extraction axis.
 head=b.Pos(389,y*c.G-32,z*c.G+170)*b.Rot(0,90,0)*b.extrude(b.RegularPolygon(13/np.sqrt(3),6),amount=5.3+31.75)
 tools[f'pump{i}_head_withdrawal']=c.T*head;owners[f'pump{i}_head_withdrawal']=n
for i in range(1,8):
 n=f'timing-cover-mounting-screw-{i}';x,y,z=occ[n]['position_cad_mm'];tools[f'cover{i}_socket_R10_5']=cyl(10.5,x,435,y,z);owners[f'cover{i}_socket_R10_5']=n
 flange=cyl(8.75,x,x+1.6+22.225,y,z);hexhead=b.Pos(x+1.6,y,z)*b.Rot(0,-90,0)*b.extrude(b.RegularPolygon(12.7/np.sqrt(3),6),amount=-(3.7+22.225));tools[f'cover{i}_head_withdrawal']=c.norm(flange.fuse(hexhead));owners[f'cover{i}_head_withdrawal']=n
r={'status':'RUNNING','scope':'Estimated socket cylinders and actual modeled head cross-section straight withdrawal sweeps. No wrench swing or helical thread-unwinding claim.','threshold_mm3':.1,'tools':{},'checks':[],'conflicts':[],'errors':[],'gear_checks':[]};rp=R/'reference/engine/pump-cover-candidate-20261003-tools.json'
def save():r['inputs']=inputs;rp.write_text(json.dumps(r,indent=2)+'\n')
for label,s in tools.items():
 box=np.array([list(s.bounding_box().min),list(s.bounding_box().max)]);r['tools'][label]={'bounds':box.tolist(),'owner_excluded':owners[label]};print('TOOL',label,flush=True)
 for n,boundsn in bounds.items():
  if n==owners[label]or np.any(np.minimum(box[1],boundsn[1])-np.maximum(box[0],boundsn[0])< -1e-5):continue
  row={'tool':label,'neighbor':n}
  try:
   v=vol(s.intersect(get(n)));row['overlap_mm3']=v
   if v>.1:r['conflicts'].append(row);print('CONFLICT',row,flush=True)
  except Exception as e:row['error']=repr(e);r['errors'].append(row)
  r['checks'].append(row)
 save()
for a in ['crank-timing-gear','cam-timing-gear']:
 for z in ['timing-cover','timing-cover-main-gasket','block','water-pump-housing','water-pump-gasket','water-pump-impeller']:
  r['gear_checks'].append({'a':a,'b':z,'overlap_mm3':vol(get(a).intersect(get(z))),'scope':'FreshactualXdependentq0 only; no fullmotion claim'});save()
inputs.update({str(p.relative_to(R)):sha(p)for p in [Path(__file__),Path(c.__file__),mp,R/'reference/engine/pump-cover-candidate-20261003-build.json',R/'inventory/engine/accessory-stage-v4-solids.json']});r['status']='FAIL'if r['conflicts']else'INCONCLUSIVE'if r['errors']else'PASS scoped envelopes';save();print(r['status'],len(r['checks']),len(r['conflicts']),len(r['errors']),flush=True)
