"""Reuse unchanged contact evidence and independently qualify only movedhole21."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b,numpy as np
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
import timing_pan21_lateral_candidate as c
base=ROOT/'cad/engine/generated/timing-pan21-lateral-candidate';paths=[base/(n+'.step')for n in ['cover','pan','pan-gasket']];cover,pan,gasket=[b.import_step(p)for p in paths];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
summarypaths=[ROOT/'inventory/engine'/n for n in ['timing-pan-perimeter-contact-summary.json','timing-pan-upper-contact-summary.json']];summaries=[json.loads(p.read_text())for p in summarypaths];paths+=summarypaths
for r in summaries:
 for p,h in r['sha256'].items():assert sha(ROOT/p)==h,p
assert summaries[0]['geometry_changes']is False and summaries[1]['geometry_changed']is False
routepath=ROOT/'cad/engine/generated/timing-pan-perimeter-contact/inboard-route.npz';paths.append(routepath);pts=np.load(routepath)['points'];a=pts[:,:2];d=np.roll(a,-1,axis=0)-a;center=np.array(c.NEW[:2]);t=np.clip(np.sum((center-a)*d,axis=1)/np.maximum(np.sum(d*d,axis=1),1e-30),0,1);distance=float(np.linalg.norm(a+d*t[:,None]-center,axis=1).min());ang=np.arctan2(a[:,1]-center[1],a[:,0]-center[0]);winding=float((((np.diff(np.r_[ang,ang[0]])+np.pi)%(2*np.pi))-np.pi).sum()/(2*np.pi))
def vol(s):
 if s is None:return 0.
 if isinstance(s,b.ShapeList):return sum(vol(q)for q in s)
 total=0.
 for q in s.solids():
  prop=GProp_GProps();e=BRepGProp.VolumeProperties_s(q.wrapped,prop,1e-9,True,False);assert e<=1e-7,e;total+=abs(prop.Mass())
 return total
# Continuous swept R6.2 band betweenold/newaxes, excluding thetwoactualR4.3openings.
def bridge(z0,z1):
 ends=[b.Pos(390,y)*c.owner.cz(6.2,z0,z1)for y in [-110,-95]];mid=b.Pos(390,-102.5,(z0+z1)/2)*b.Box(12.4,15,z1-z0);s=c.norm(ends[0].fuse(ends[1],mid))
 for y in[-110,-95]:s=c.norm(s.cut(b.Pos(390,y)*c.owner.cz(4.3,z0-1,z1+1)))
 return s
r={'contact_studies_modify_geometry':False,'lower_route_reuse':{'old_width_mm':summaries[0]['width_mm'],'new_hole_center_minimum_xy_segment_distance_mm':distance,'new_hole_edge_clearance_lower_mm':distance-4.3,'new_hole_winding':winding,'required_halfwidth_plus_original_allowance_mm':summaries[0]['width_mm']/2+.2,'proof':'Exact XYpoint-to-segment lowerbound; oldroute retained onunchangedcontact outside onlynewR4.3hole. Fillingretiredhole cannotremovecontact.'},'changed_contact_bridge':{'upper_owner_missing_mm3':vol(bridge(-24.5,-24.48).cut(cover)),'lower_owner_missing_mm3':vol(bridge(-26.52,-26.5).cut(pan)),'gasket_missing_mm3':vol(bridge(-26.5,-24.5).cut(gasket))},'old_overhangs_and_rear_ownership':'Preserved; studiesareanalysis-only, norepairassetexists','inputs_sha256':{str(p.relative_to(ROOT)):sha(p)for p in paths+[Path(__file__)]}}
r['status']='PASS changedcontact/reuse scope'if distance-4.3>summaries[0]['width_mm']/2+.2 and abs(winding)<1e-5 and all(v<1e-5 for v in r['changed_contact_bridge'].values())else'FAIL';(ROOT/'inventory/engine/timing-front-stage-contact-delta.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
