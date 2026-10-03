from pathlib import Path
import sys,importlib.util,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from OCP.BRepGProp import BRepGProp
from OCP.GProp import GProp_GProps
p=ROOT/'cad/engine/fuel-rail-candidate-20261003.py';sp=importlib.util.spec_from_file_location('m',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
def mass(s):
 prop=GProp_GProps();err=BRepGProp.VolumeProperties_s(s.wrapped,prop,1e-9,True,False);return {'adaptive_volume':prop.Mass(),'integration_error':err,'default_volume':s.volume,'valid':s.is_valid}
defs,_,_,_=m.parts(1);a=defs['fuel-return-tube'];c=b.import_step(ROOT/'cad/engine/generated/fuel-rail-candidate-20261003/plus/local-fuel-return-tube.step')
r={'source':mass(a),'reimport':mass(c)}
for key,x,y in [('source_minus_reload',a,c),('reload_minus_source',c,a)]:
 try:r[key]=mass(m.solid(x-y))
 except Exception as e:r[key]={'error':str(e)}
(ROOT/'cad/engine/generated/fuel-rail-candidate-20261003/export-diagnostic.json').write_text(json.dumps(r,indent=2)+'\n');print(r)
