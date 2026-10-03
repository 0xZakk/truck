from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from cad_metrics import solid_volume
import pump_cover_candidate_20261003 as c
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return sum(abs(solid_volume(q,'adaptive'))for q in c.norm(s).solids())if s else 0.
ex=json.loads((R/'reference/engine/pump-cover-candidate-20261003-build.json').read_text());bp=R/ex['parts']['block']['path'];op=R/ex['block_features']['old_block']['path'];new=b.import_step(bp);old=b.import_step(op);r={'status':'RUNNING','changes':{},'host_conflicts':{},'inputs':{str(p.relative_to(R)):sha(p)for p in [Path(__file__),Path(c.__file__),bp,op]}};rp=R/'reference/engine/pump-cover-candidate-20261003-block-delta.json'
def save():rp.write_text(json.dumps(r,indent=2)+'\n')
for label,s in [('added',c.norm(new.cut(old))),('removed',c.norm(old.cut(new)))]:
 p=c.O/('block-delta-'+label+'.step');b.export_step(s,p);r['changes'][label]={'volume_mm3':vol(s),'bounds':[list(s.bounding_box().min),list(s.bounding_box().max)],'path':str(p.relative_to(R)),'sha256':sha(p)};save();print(label,r['changes'][label],flush=True)
for name in ['cylinder-head','head-gasket','thermostat-frame']:
 s=c.original(name);oldv=vol(old.intersect(s));newv=vol(new.intersect(s));r['host_conflicts'][name]={'original_v4_overlap_mm3':oldv,'candidate_overlap_mm3':newv,'delta_mm3':newv-oldv};save();print(name,r['host_conflicts'][name],flush=True)
r['status']='COMPLETE; actual interface failures retained';r['unchanged_x_below_350']=all(v['bounds'][0][0]>=350-1e-5 for v in r['changes'].values());r['cylinder_wall_limit']='Only X<350 is proven unchanged by difference bounds; deeper coolant passage and all wall thicknesses are not established';save()
