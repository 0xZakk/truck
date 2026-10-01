#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib,math
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import accessory_psac_carrier_trial1 as src
from assembly_clockwise_candidate import transforms
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();mp=R/'inventory/engine/corrected-engine-stage-v3.json';m=json.loads(mp.read_text());t=transforms(m,0,0);ds={d['id']:d for d in m['definitions']};oo={o['id']:o for o in m['occurrences']};inputs={str(p.relative_to(R)):sha(p)for p in [mp,Path(__file__),Path(src.__file__),R/'cad/engine/assembly_clockwise_candidate.py']};rows=[]
for g,n in [('PS','ps-pump-pulley'),('AC','ac-compressor-clutch-pulley'),('TENS','tensioner-pulley-wheel')]:
 p=R/ds[oo[n]['definition']]['step'].lstrip('/');inputs[str(p.relative_to(R))]=sha(p);original=t[n]*b.import_step(p);s=b.Pos(0,*src.SELECT['posedelta_yz_mm'][g])*original;cy,cz=src.C[g];faces=[]
 for f in s.faces():
  if f.geom_type!=b.GeomType.CYLINDER:continue
  c=f.geom_adaptor().Cylinder();a=c.Axis();pt=a.Location();direction=a.Direction()
  if abs(direction.X())<.9999999 or math.hypot(pt.Y()-cy,pt.Z()-cz)>1e-5:continue
  bb=f.bounding_box();faces.append({'radius_mm':c.Radius(),'x_span_mm':[bb.min.X,bb.max.X],'axis_yz_mm':[pt.Y(),pt.Z()]})
 assert faces,n
 radius=max(f['radius_mm']for f in faces);crest=[f for f in faces if abs(f['radius_mm']-radius)<1e-6];span=[min(f['x_span_mm'][0]for f in crest),max(f['x_span_mm'][1]for f in crest)];mid=sum(span)/2;bb=s.bounding_box();ob=original.bounding_box();error=max(abs(bb.min.X-ob.min.X),abs(bb.max.X-ob.max.X));assert error<1e-6
 rows.append({'occurrence':n,'group':g,'coaxial_cylinder_faces':len(faces),'maximum_coaxial_radius_mm':radius,'crest_x_span_mm':span,'crest_midplane_X_mm':mid,'offset_from_estimated_beltplane_mm':mid-473.56,'X_envelope_change_mm':error,'expected_axis_yz_mm':[cy,cz]})
r={'status':'COMPLETE actual cylindrical-axis and axial-envelope survey; effective belt pitch/production alignment remain unknown','rows':rows,'inputs':inputs};(R/'inventory/engine/accessory-psac-carrier-pulley-datums.json').write_text(json.dumps(r,indent=2)+'\n');print(rows)
