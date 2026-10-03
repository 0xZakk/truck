from pathlib import Path
import sys,json,numpy as np,trimesh
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import pump_functional_20261003 as c
rows=json.loads((R/'reference/engine/pump-functional-20261003-build.json').read_text())['parts'];out={}
for n,v in rows.items():
 if n.startswith(('fan-clutch-','cooling-fan-','water-pump-pulley-bolt-'))or n=='water-pump-seal-spring':continue
 gp=(R/v['path']).with_suffix('.glb')
 if not gp.exists():continue
 g=trimesh.load(gp,force='mesh');out[n+'__vertices']=g.vertices[:,[0,2,1]]*[1,-1,1]*1000;out[n+'__faces']=g.faces
for n in ['water-pump-impeller','water-pump-gasket','timing-cover','timing-cover-mounting-screw-3','thermactor-engine-bolt-1','alternator-thermactor-common-carrier']+[f'water-pump-mounting-screw-{i}'for i in range(1,5)]:
 s=c.world(n);vs,fs=s.tessellate(.025,.08);out[n+'__vertices']=np.array([tuple(v)for v in vs]);out[n+'__faces']=np.array(fs)
np.savez_compressed(R/'reference/engine/pump-functional-20261003-render-data.npz',**out)
print('complete',len(out)//2,flush=True)
