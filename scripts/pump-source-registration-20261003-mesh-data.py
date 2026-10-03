from pathlib import Path
import numpy as np,trimesh,json,hashlib
R=Path(__file__).resolve().parents[1];p=R/'cad/engine/generated/pump-functional-20261003/water-pump-housing.glb';g=trimesh.load(p,force='mesh');v=g.vertices[:,[0,2,1]]*[1,-1,1]*1000;o=R/'reference/engine/pump-source-registration-20261003-candidate-projection.npz';np.savez_compressed(o,vertices=v,faces=g.faces)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
(R/'reference/engine/pump-source-registration-20261003-mesh-data.json').write_text(json.dumps({'source_path':str(p.relative_to(R)),'source_sha256':sha(p),'npz_path':str(o.relative_to(R)),'npz_sha256':sha(o),'script_sha256':sha(Path(__file__))},indent=2)+'\n')
