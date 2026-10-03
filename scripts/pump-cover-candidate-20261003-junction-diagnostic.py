from pathlib import Path
import sys,json,hashlib,collections
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from OCP.TopExp import TopExp
from OCP.TopAbs import TopAbs_EDGE,TopAbs_FACE
from OCP.TopTools import TopTools_IndexedDataMapOfShapeListOfShape
import pump_cover_candidate_20261003 as c
r={'status':'RUNNING','stages':[]};rp=R/'reference/engine/pump-cover-candidate-20261003-junction-diagnostic.json'
def inspect(name,s):
 mp=TopTools_IndexedDataMapOfShapeListOfShape();TopExp.MapShapesAndAncestors_s(s.wrapped,TopAbs_EDGE,TopAbs_FACE,mp);counts=collections.Counter(len({hash(f)for f in mp.FindFromIndex(i)})for i in range(1,mp.Extent()+1));v={'stage':name,'valid':s.is_valid,'solids':len(s.solids()),'edge_unique_faces_counts':dict(counts)};r['stages'].append(v);rp.write_text(json.dumps(r,indent=2)+'\n');print(v,flush=True)
g=c.gasket_oldframe();regions=c.regions_oldframe(g);front=c.norm(c.frozen('water-pump-housing').intersect(c.cx(29.01,409.43,464)));outer=b.loft([c.old.core.section(x,rr)for x,rr in [(375,66*c.G),(383,66*c.G),(389,55*c.G),(409.43,29)]],ruled=True);inner=b.loft([c.old.core.section(x,rr)for x,rr in [(374,59*c.G),(383,59*c.G),(389,51),(409.43,24),(418.43,24)]],ruled=True);root,end,crest,ed=c.old.datums(c.HEIGHT)
h=c.norm(outer.fuse(front));inspect('outer_front',h)
h=c.norm(h.cut(inner));inspect('cut_main_cavity_first',h)
port=c.norm(c.inlet().cut(c.inlet(True)));inspect('port_wall',port);port=c.norm(port.cut(inner));inspect('port_wall_minus_cavity',port);h=c.norm(h.fuse(port));inspect('fuse_port_wall',h)
h=c.norm(h.fuse(c.old.segment(12,root-42*c.old.DIR,root),regions['seal_backing']));inspect('heater_backing',h)
for n,tool in [('inlet_lumen',c.inlet(True)),('heater_small',c.old.segment(6.5,root-46*c.old.DIR,root+c.old.DIR)),('heater_socket',c.old.segment(8,root-12*c.old.DIR,root+c.old.DIR)),('dry_bore',c.cx(24,409.43,464.43))]:h=c.norm(h.cut(tool));inspect(n,h)
y,z=c.EXTRA[0]*c.G,c.EXTRA[1]*c.G;h=c.norm(h.fuse(c.cylinder(11.5*c.G,375,394,y,z)));h=c.norm(h.cut(b.Solid.make_cylinder(6.5,(.25*y)**2**.5 if False else __import__('math').hypot(.25*y,.25*z),b.Plane(origin=(386,y-32,z+170),z_dir=(0,-y,-z)))))
for i in range(1,5):h=c.norm(h.fuse(regions[f'dry_boss_{i}']))
for i in range(1,5):h=c.norm(h.cut(regions[f'dry_bore_{i}']))
h=c.norm(h.cut(regions['fifth_aperture']))
for y,z in c.MOUNTING:h=c.norm(h.cut(c.cylinder(11.5,389,430,y*c.G,z*c.G)))
inspect('final',h);p=c.O/'housing-sequential-diagnostic.step';b.export_step(c.T*h,p);r['status']='COMPLETE';r['output']={'path':str(p.relative_to(R)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()};r['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();rp.write_text(json.dumps(r,indent=2)+'\n')
