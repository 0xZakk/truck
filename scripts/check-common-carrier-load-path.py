"""Connectivity control only, not structural strength analysis."""
import sys,json,hashlib
from pathlib import Path
import build123d as cad
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import alt_thermactor_common_carrier_candidate as c
s=c.carrier();assert s.is_valid and len(s.solids())==1
cut=cad.Pos(425,-225,180)*cad.Box(200,500,.5)
broken=s-cut
assert len(broken.solids())==2,'Severing common spine must separate upper and lower load paths'
r={'passed':True,'candidate_sha256':hashlib.sha256(Path(c.__file__).read_bytes()).hexdigest(),'continuous_solid_count':len(s.solids()),'severed_spine_solid_count':len(broken.solids()),'cut_center_z_mm':180,'cut_thickness_mm':.5,'scope':'Topological connection and negative control only; no FEA, belt-load capacity, stress or fatigue claim.'}
(ROOT/'inventory/engine/alt-thermactor-common-carrier-path-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
