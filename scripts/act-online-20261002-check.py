"""Local comparison checks; never installs the sensor."""
from pathlib import Path
import sys,json,hashlib,itertools
import numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b,trimesh
import act_online_20261002_specimen as c
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
c.O.mkdir(exist_ok=True);parts=c.build();rows={};pairs=[]
for name,s in parts.items():
 print('export',name,flush=True);assert s.is_valid and len(s.solids())==1,(name,len(s.solids()))
 p=c.O/(name+'.step');b.export_step(s,p);s=b.import_step(p);parts[name]=s
 v,f=s.tessellate(.018,.08);m=trimesh.Trimesh(np.array([tuple(q) for q in v]),np.array(f));m.merge_vertices(digits_vertex=6);m.update_faces(m.nondegenerate_faces());m.update_faces(m.unique_faces());m.remove_unreferenced_vertices()
 assert m.is_watertight and m.is_winding_consistent and m.volume>0,name
 gp=p.with_suffix('.glb');trimesh.Trimesh(m.vertices[:,[0,2,1]]*[1,1,-1]/1000,m.faces).export(gp)
 g=trimesh.load(gp,force='mesh');vv=g.vertices[:,[0,2,1]]*[1,-1,1]*1000
 bounds=np.array([tuple(s.bounding_box().min),tuple(s.bounding_box().max)]);err=float(np.max(abs(np.array([vv.min(0),vv.max(0)])-bounds)));assert err<.05,(name,err)
 rows[name]={'step':str(p.relative_to(R)),'step_sha256':sha(p),'glb':str(gp.relative_to(R)),'glb_sha256':sha(gp),'valid':s.is_valid,'solid_count':len(s.solids()),'volume_mm3':s.volume,'watertight':True,'winding_consistent':True,'bounds_mm':bounds.tolist(),'bounds_error_mm':err}
for (an,a),(bn,z) in itertools.combinations(parts.items(),2):
 intersection=a&z;vol=0 if intersection is None else (sum(x.volume for x in intersection) if isinstance(intersection,b.ShapeList) else intersection.volume)
 pairs.append({'a':an,'b':bn,'overlap_mm3':vol,'distance_mm':a.distance_to(z)});assert vol<.1,(an,bn,vol)
shell=parts['act-online-metal-shell'];ins=parts['act-online-insulator'];bead=parts['act-online-visible-sensing-encapsulation'];a=parts['act-online-contact-1'];z=parts['act-online-contact-2']
# Same predicate must reject deliberate conductor bridge and filled guard.
def separated(x,y):return x.distance_to(y)>1
assert separated(a,z)
bridge=b.Pos(0,0,32)*b.Box(7,1,1)
assert not separated(a+bridge,z)
window=[(0,0,-7),(0,0,-6.8)]
assert all(not shell.is_inside(p) for p in window)
filled=shell+b.Pos(0,0,-6)*b.Box(4,3,6)
assert any(filled.is_inside(p) for p in window)
assert shell.distance_to(ins)<1e-6 and ins.distance_to(bead)<1e-6
for pin in (a,z):assert pin.distance_to(ins)<1e-6
# Actual material removal and crest/root predicates reject the frozen smooth-shell defect.
blank=b.Cone(8.55-15/32,8.55,15,align=(b.Align.CENTER,b.Align.CENTER,b.Align.MIN))-c.cyl(4,-.1,15.2)
region=b.Pos(0,0,7.5)*b.Cylinder(10,15)
actual=shell & region
removed=blank.volume-actual.volume
assert removed>50,removed
samples=[]
for phi in np.linspace(0,2*np.pi,8,endpoint=False):
 for zz in np.linspace(2,13,67):
  rr=8.55-(15-zz)/32-.2;pt=(rr*np.cos(phi),rr*np.sin(phi),zz);samples.append(shell.is_inside(pt))
assert 20<sum(samples)<len(samples)-20
smooth=[blank.is_inside(((8.55-(15-zz)/32-.2)*np.cos(phi),(8.55-(15-zz)/32-.2)*np.sin(phi),zz)) for phi in np.linspace(0,2*np.pi,8,endpoint=False) for zz in np.linspace(2,13,67)]
assert all(smooth)
thread={'actual_removed_mm3':removed,'crest_samples_inside':sum(samples),'root_samples_outside':len(samples)-sum(samples),'sample_count':len(samples),'smooth_negative_control_detected':True,'scope':'Actual helical surface with18TPI; gauge,truncations,1.5mmrunouts unverified'}
report={'status':'PASS local specimen geometry only; source dimensions/installed interface NOT VERIFIED','parameters':c.PARAMETERS,'actual_thread_check':thread,'parts':rows,'exact_local_pairs':pairs,'guards':{'contacts_separate':True,'guard_window_open':True,'insulator_shell_support':True,'encapsulation_insulator_contact':True,'pin_insulator_support':True},'negative_controls':{'bridged_contacts_detected':True,'filled_guard_detected':True},'missing':['hidden leads and electrical continuity','potting and calibrated thermistor internal','thread gauge/truncations and actual host fit','installed pose and harness mating fit','dynamic/tool/browser checks'],'inputs':{str(p.relative_to(R)):sha(p) for p in [Path(__file__),Path(c.__file__),R/'docs/components/act-online-20261002-specimen.md']}}
(R/'reference/engine/act-online-20261002-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS',flush=True)
