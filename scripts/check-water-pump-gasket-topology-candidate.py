"""Isolated topology test, with render input; not an installed joint audit."""
from pathlib import Path
import sys,json,hashlib
import build123d as b
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import water_pump_gasket_topology_candidate as p
paths=[Path(__file__),Path(p.__file__),ROOT/'reference/engine/water-pump-mounting-topology-reviewed.json']
hashes={str(q.relative_to(ROOT)):hashlib.sha256(q.read_bytes()).hexdigest() for q in paths}
s=p.gasket_shape();assert s.is_valid and len(s.solids())==1
b.export_step(s,'/private/tmp/water-pump-gasket-topology.step')
a=b.import_step('/private/tmp/water-pump-gasket-topology.step');assert a.is_valid and len(a.solids())==1
holes=[]
for y,z in (*p.MOUNTING,p.EXTRA):
 q=b.Pos(0,y,z)*b.Rot(0,90,0)*b.Cylinder(2,4)
 v=sum(i.volume for i in (s&q).solids());assert v<1e-8;holes.append(v)
faces=[f for f in s.faces() if abs(f.normal_at().X)>.99]
assert len(faces)==2 and all(len(f.wires())==7 for f in faces)
verts,tri=s.tessellate(.15,.15)
np.savez_compressed('/private/tmp/water-pump-gasket-topology.npz',vertices_0=np.asarray([tuple(v) for v in verts]),faces_0=np.asarray(tri),explode_0=np.zeros(3),metadata=np.array(json.dumps({'assembly':'Uninstalled water-pump gasket topology','parts':1,'colors':['#37a1ad']})))
assert all(hashlib.sha256((ROOT/q).read_bytes()).hexdigest()==h for q,h in hashes.items())
report={'status':'PASS isolated topology only; NOT installed','input_hashes':hashes,'inputs_unchanged':True,'valid_single_solid':True,'step_roundtrip_valid':True,'mounting_apertures':4,'larger_unidentified_apertures':1,'planar_face_wire_counts':[len(f.wires()) for f in faces],'five_open_aperture_probe_mm3':holes,'gaps':p.GAPS}
(ROOT/'inventory/engine/water-pump-gasket-topology-candidate-validation.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS isolated gasket topology')
