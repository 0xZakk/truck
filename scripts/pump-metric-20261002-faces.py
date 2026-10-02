from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from assembly_clockwise_candidate import transforms
mfile=R/'inventory/engine/corrected-engine-stage-v4.json';m=json.loads(mfile.read_text());ts=transforms(m,0,0);defs={d['id']:d for d in m['definitions']};rows={};inputs={}
for n in ['water-pump-drive-hub','water-pump-pulley','water-pump-bearing','water-pump-shaft','water-pump-slinger','water-pump-impeller']+[o['id']for o in m['occurrences']if o['id'].startswith('water-pump-seal-')]:
 o=next(q for q in m['occurrences']if q['id']==n);p=R/defs[o['definition']]['step'].lstrip('/');s=ts[n]*b.import_step(p);planes=[]
 for f in s.faces():
  bb=f.bounding_box()
  if f.geom_type==b.GeomType.PLANE and bb.size.X<1e-4:planes.append({'x_mm':f.center().X,'area_mm2':f.area,'bounds':[list(bb.min),list(bb.max)]})
 rows[n]={'bounds':[list(s.bounding_box().min),list(s.bounding_box().max)],'axial_planes':planes,'source':str(p.relative_to(R))};inputs[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
p=R/'cad/engine/generated/waterpump-heater-source-candidate/housing.step';s=b.import_step(p);rows['conditional-heater-housing']={'axial_planes':[{'x_mm':f.center().X,'area_mm2':f.area}for f in s.faces()if f.geom_type==b.GeomType.PLANE and f.bounding_box().size.X<1e-4]};inputs[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
for p in[mfile,Path(__file__),R/'cad/engine/assembly_clockwise_candidate.py']:inputs[str(p.relative_to(R))]=hashlib.sha256(p.read_bytes()).hexdigest()
(R/'reference/engine/pump-metric-20261002-faces.json').write_text(json.dumps({'parts':rows,'input_sha256':inputs,'scope':'Actual STEP axial plane extraction; housing is explicitly conditional heater study, others actual v4 q0'},indent=2)+'\n')
print('Extracted',len(rows),'parts')
