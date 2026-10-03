from pathlib import Path
import sys,json,hashlib,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from OCP.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Common
from cad_metrics import solid_volume
import pump_functional_20261003 as c
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def vol(s):return sum(abs(solid_volume(q,'adaptive'))for q in c.norm(s).solids())if s else 0.
ex=json.loads((R/'reference/engine/pump-functional-20261003-build.json').read_text());r={'status':'RUNNING','scope':'independent functional regions; finite paths/walls not pressure proof','checks':{},'controls':{},'inputs':{}}
def load(n):
 p=R/ex['parts'][n]['path'];assert sha(p)==ex['parts'][n]['sha256'];r['inputs'][str(p.relative_to(R))]=sha(p);return b.import_step(p)
h=load('water-pump-housing');tube=load('heater-pump-return-elbow');regions={}
for n,v in ex['regions'].items():
 p=R/v['path'];assert sha(p)==v['sha256'];regions[n]=b.import_step(p);r['inputs'][str(p.relative_to(R))]=sha(p)
def face_missing(face,s):
 op=BRepAlgoAPI_Cut(face.wrapped,b.Compound(list(s.faces())).wrapped);op.Build()
 return b.Compound(op.Shape()).area
for n,s in regions.items():
 if n=='seal_land_face'or n.startswith('bolt_seat'):r['checks'][n]={'missing_mm2':face_missing(s,h)}
 elif n.startswith('dry_bore')or n=='fifth_aperture':r['checks'][n]={'obstruction_mm3':vol(s.intersect(h))}
 else:r['checks'][n]={'missing_mm3':vol(s.cut(h))}
# Actual existing screw underside, limited only by its declared clearance bore.
for i in range(1,5):
 screw=c.world(f'water-pump-mounting-screw-{i}')
 underside=b.Compound([f for f in screw.faces()if abs(f.center().X-389)<1e-5 and f.bounding_box().size.X<1e-5])
 common=BRepAlgoAPI_Common(underside.wrapped,regions[f'bolt_seat_{i}'].wrapped);common.Build();seat=b.Compound(common.Shape())
 r['checks'][f'actual_head_seat_{i}']={'area_mm2':seat.area,'missing_mm2':face_missing(seat,h)}
 p=c.O/(f'region-actual-head-seat-{i}.step');b.export_step(seat,p);r['inputs'][str(p.relative_to(R))]=sha(p)
# Analytic exact swept envelope from actual original disk and six rectangular vanes.
# Actual source disk R51 X369..373; vanes radial11.5..48.5 halfwidth1.5 X372..384.
rotor=c.cx(51,369,373).fuse(c.cx(math.hypot(48.5,1.5),372,384)).cut(c.cx(8.05,368,385))
guard=c.cx(51.5,369,373.5).fuse(c.cx(math.hypot(48.5,1.5)+.5,372,384.5))
impeller=c.world('water-pump-impeller')
r['checks']['rotor']={'actual_impeller_outside_swept_envelope_mm3':vol(impeller.cut(rotor)),'housing_swept_overlap_mm3':vol(h.intersect(rotor)),'housing_clearance_guard_overlap_mm3':vol(h.intersect(guard)),'radial_clearance_guard_mm':.5,'analytic_source':'cad/engine/water_pump.py build impeller disk/six boxes'}
for n,s in [('rotor-sweep',rotor),('rotor-clearance',guard)]:
 p=c.O/('region-'+n+'.step');b.export_step(s,p);r['inputs'][str(p.relative_to(R))]=sha(p)
root,end,crest,ed=c.datums(c.HEIGHT)
probes={'inlet':c.inlet(probe=True),'heater':c.sweep(.7,c.HEIGHT).fuse(c.segment(.7,root-46*c.DIR,root-12*c.DIR))}
for n,s in probes.items():r['checks'][n+'_path']={'obstruction_mm3':vol(s.intersect(h.fuse(tube)))}
r['checks']['housing_tube']={'overlap_mm3':vol(h.intersect(tube))}
r['checks']['dry_axial_bore']={'obstruction_mm3':vol(c.cx(23.99,375+c.HEIGHT-64,513+c.HEIGHT-147).intersect(h))}
# Finite full cross-section skin witnesses over transition. Exclude its intended open entry/terminal.
for label,y in [('join',45),('bend',60),('round',96),('mouth',135)]:
 slab=b.Pos(403,y,6)*b.Box(100,.1,100);slab=b.Pos(0,-32,170)*b.Rot(-130,0,0)*slab
 skin=c.inlet().cut(c.inlet(True)).intersect(slab)
 cavity=b.loft([c.core.section(x,rad)for x,rad in[(374,59),(383,59),(389,51),(375+c.HEIGHT-64,24),(375+c.HEIGHT-55,24)]],ruled=True)
 expected=skin.cut(cavity)
 r['checks']['wall_'+label]={'missing_mm3':vol(expected.cut(h)),'witness_volume_mm3':vol(expected),'intended_cavity_communication_mm3':vol(skin.intersect(cavity))}
# Missing-stock / blocked-flow / shifted-interface negative controls.
notch=b.Pos(376,-32,234)*b.Box(4,4,4)
r['controls']['backing_notch_missing_mm3']=vol(regions['seal_backing'].cut(h.cut(notch)))
r['controls']['shifted_face_missing_mm2']=face_missing(regions['seal_land_face'],b.Pos(1,0,0)*h)
r['controls']['blocked_inlet_mm3']=vol(probes['inlet'].intersect(b.Pos(0,-32,170)*b.Rot(-130,0,0)*(b.Pos(403,100,6)*b.Sphere(3))))
r['controls']['plugged_bore_mm3']=vol(regions['dry_bore_1'].intersect(regions['dry_bore_1']))
r['checks']['valid']={'housing':h.is_valid,'housing_solids':len(h.solids()),'tube':tube.is_valid}
r['inputs'].update({str(p.relative_to(R)):sha(p)for p in[Path(__file__),Path(c.__file__),R/'reference/engine/pump-functional-20261003-build.json',R/'cad/engine/water_pump.py']})
r['status']='CHECKS COMPLETE; inspect every metric'
(R/'reference/engine/pump-functional-20261003-check.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'checks':r['checks'],'controls':r['controls']},indent=2),flush=True)
