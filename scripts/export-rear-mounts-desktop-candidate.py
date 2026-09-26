"""Save the isolated rear bolt candidate for visual review; no installed writes."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
import build123d as cad
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
import rear_manifold_mounts_desktop_candidate as candidate

directory=ROOT/'cad/engine/candidates/rear-mounts-desktop'
directory.mkdir(parents=True,exist_ok=True)
source=ROOT/'cad/engine/generated/exhaust-rear.step'
source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
shapes={'exhaust-rear':candidate.rear_interface(cad.import_step(source)),**candidate.parts()}
arrays={}
for index,(identifier,shape) in enumerate(shapes.items()):
    assert shape.is_valid and len(shape.solids())==1,identifier
    cad.export_step(shape,directory/(identifier+'.step'))
    vertices,faces=shape.tessellate(.08,.15)
    arrays[f'vertices_{index}']=np.array([tuple(v) for v in vertices])
    arrays[f'faces_{index}']=np.array(faces)
    arrays[f'explode_{index}']=np.array((0,-100*index,0))
assert hashlib.sha256(source.read_bytes()).hexdigest()==source_hash
metadata={'assembly':'Rear mounting candidate — provisional geometry, not installed',
          'parts':len(shapes),'identifiers':list(shapes),'colors':['#87766b','#a4acb3','#a4acb3'],
          'source_step_sha256':source_hash,'module_sha256':hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest(),
          'limits':candidate.GAPS}
arrays['metadata']=np.array(json.dumps(metadata))
(directory/'provenance.json').write_text(json.dumps(metadata,indent=2)+'\n')
np.savez_compressed('/private/tmp/rear-mounts-desktop.npz',**arrays)
print('Exported isolated rear mounting candidate',flush=True)
