from pathlib import Path
import sys,json,hashlib,math,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut,BRepAlgoAPI_Common
from cad_metrics import solid_volume
import pump_cover_candidate_20261003 as c
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return sum(abs(solid_volume(q,'adaptive'))for q in c.norm(s).solids())if s else 0.
r={'status':'RUNNING','checks':{},'controls':{},'inputs':{},'limits':['Finite nominal geometry only, no pressure/strength or factory dimensions','Smooth pump sockets and inherited bearing gaps are not verified threads/press fits']};rp=R/'reference/engine/pump-cover-candidate-20261003-check.json';ex=json.loads((R/'reference/engine/pump-cover-candidate-20261003-build.json').read_text())
def save():rp.write_text(json.dumps(r,indent=2)+'\n')
def load(n,key='parts'):
 v=ex[key][n];p=R/v['path'];assert sha(p)==v['sha256'];r['inputs'][str(p.relative_to(R))]=sha(p);return b.import_step(p)
def face_missing(f,s):
 q=BRepAlgoAPI_Cut(f.wrapped,b.Compound(list(s.faces())).wrapped);q.Build();assert q.IsDone();return b.Compound(q.Shape()).area
h=load('water-pump-housing');g=load('water-pump-gasket');block=load('block');tube=load('heater-pump-return-elbow');regions={n:load(n,'regions')for n in ex['regions']}
for n,s in regions.items():
 if n=='seal_land_face'or n.startswith('bolt_seat'):r['checks'][n]={'missing_mm2':face_missing(s,h)}
 elif n.startswith('dry_bore')or n=='fifth_aperture':r['checks'][n]={'obstruction_mm3':vol(s.intersect(h))}
 else:r['checks'][n]={'missing_mm3':vol(s.cut(h))}
 print('REGION',n,r['checks'][n],flush=True);save()
back=b.Compound([f for f in g.faces()if abs(f.center().X-373)<1e-5 and f.bounding_box().size.X<1e-5])
r['checks']['gasket_block_backing']={'required_area_mm2':back.area,'missing_mm2':face_missing(back,block)}
for i,(y,z)in enumerate(c.MOUNTING,1):
 screw=load(f'water-pump-mounting-screw-{i}');underside=b.Compound([f for f in screw.faces()if abs(f.center().X-389)<1e-5 and f.bounding_box().size.X<1e-5]);q=BRepAlgoAPI_Common(underside.wrapped,regions[f'bolt_seat_{i}'].wrapped);q.Build();seat=b.Compound(q.Shape())
 floor=c.T*c.cylinder(4.3,355,356,y*c.G,z*c.G);socket=load(f'new_void_socket_{i}','block_features')
 r['checks'][f'actual_screw_{i}']={'seat_area_mm2':seat.area,'missing_seat_mm2':face_missing(seat,h),'block_overlap_mm3':vol(screw.intersect(block)),'housing_overlap_mm3':vol(screw.intersect(h)),'socket_obstruction_mm3':vol(socket.intersect(block)),'one_mm_blind_floor_missing_mm3':vol(floor.cut(block)),'nominal_tip_x':357.25,'nominal_engagement_mm':15.75,'clearance_socket_radius_mm':4.3,'smooth_shank_radius_mm':4.,'thread_engagement_status':'NOT MODELED / unverified'};print('SCREW',i,flush=True);save()
rotor=c.T*(c.cx(51,369,373).fuse(c.cx(math.hypot(48.5,1.5),372,384)).cut(c.cx(8.05,368,385)))
guard=c.T*(c.cx(51.5,369,373.5).fuse(c.cx(math.hypot(48.5,1.5)+.5,372,384.5)))
print('ROTOR HOUSING/BLOCK INTERSECTIONS START',flush=True)
r['checks']['rotor']={'containment_proof':'Inherited functional exact containment under common rigid transform; no new Boolean containment claimed'}
for name,a,z in [('housing_overlap_mm3',h,rotor),('block_overlap_mm3',block,rotor),('housing_guard_overlap_mm3',h,guard),('block_guard_overlap_mm3',block,guard)]:
 print('START',name,flush=True);r['checks']['rotor'][name]=vol(a.intersect(z));save();print('DONE',name,r['checks']['rotor'][name],flush=True)
r['inputs']['reference/engine/pump-functional-20261003-check.json']=sha(R/'reference/engine/pump-functional-20261003-check.json')

save();print('ROTOR DONE, PATHS START',flush=True)
root,end,crest,ed=c.old.datums(c.HEIGHT);probes={'inlet':c.T*c.inlet(probe=True),'heater':c.T*(c.old.sweep(.7,c.HEIGHT).fuse(c.old.segment(.7,root-46*c.old.DIR,root-12*c.old.DIR)))}
y,z=np.array(c.EXTRA)*c.G;start=np.array([386,y-32,z+170]);end5=np.array([386,.75*y-32,.75*z+170]);probes['fifth']=c.T*c.old.segment(.5,start,end5)
for n,s in probes.items():r['checks'][n+'_path']={'obstruction_mm3':vol(s.intersect(h.fuse(tube)))}
r['checks']['housing_tube']={'overlap_mm3':vol(h.intersect(tube))};r['checks']['dry_axial_bore']={'obstruction_mm3':vol((c.T*c.cx(23.99,409.43,464.43)).intersect(h))}
for n in ['chamber','fifth']:
 v=load('new_void_'+n,'block_features');r['checks']['block_'+n]={'obstruction_mm3':vol(v.intersect(block))}
save();print('PATHS DONE, HUB START',flush=True)
# Exact shared hub/pulley witness unchanged in its physical dimensions.
face=473.43;thin=c.cx(35,face,face+.001).cut(c.cx(15.05,face-1,face+1))
for a in range(0,360,90):thin=thin.cut(b.Pos(0,25*math.cos(math.radians(a)),25*math.sin(math.radians(a)))*c.cx(3.5,face-1,face+1))
seat=c.T*b.Compound([f for f in thin.faces()if f.geom_type==b.GeomType.PLANE and abs(f.center().X-face)<1e-5])
for n in ['water-pump-drive-hub','water-pump-pulley']:r['checks']['hub_seat_'+n]={'area_mm2':seat.area,'missing_mm2':face_missing(seat,load(n))}
r['checks']['height']={'mounting_x':375,'hub_seat_x':473.43,'difference_mm':98.43,'source':'Carterreplacement comparison, not factory measurement'}
notch=c.T*(b.Pos(376,c.MOUNTING[0][0]*c.G-32,c.MOUNTING[0][1]*c.G+170)*b.Box(4,16,16))
r['controls']['missing_boss_mm3']=vol(regions['dry_boss_1'].cut(h.cut(notch)));r['controls']['shifted_face_mm2']=face_missing(regions['seal_land_face'],b.Pos(1,0,0)*h);r['controls']['plugged_bore_mm3']=vol(regions['dry_bore_1']);r['controls']['blocked_fifth_mm3']=vol(probes['fifth'].intersect(c.T*(b.Pos(*((start+end5)/2))*b.Sphere(1))))
r['inputs'].update({str(p.relative_to(R)):sha(p)for p in[Path(__file__),Path(c.__file__),R/'reference/engine/pump-cover-candidate-20261003-build.json']});r['status']='FINISHED; inspect every named metric';save();print(json.dumps({'checks':r['checks'],'controls':r['controls']},indent=2),flush=True)
