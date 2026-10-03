from pathlib import Path
import sys,json,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import pump_functional_20261003 as c
out={}
names=['water-pump-housing','heater-pump-return-elbow','water-pump-drive-hub','water-pump-pulley']
for n in names:
 s=b.import_step(c.O/(n+'.step'));vs,fs=s.tessellate(.05,.14);out[n+'__vertices']=np.array([tuple(v)for v in vs]);out[n+'__faces']=np.array(fs)
 print(n,len(fs),flush=True)
for n in ['water-pump-impeller','water-pump-gasket','timing-cover','timing-cover-mounting-screw-3','thermactor-engine-bolt-1','alternator-thermactor-common-carrier']+[f'water-pump-mounting-screw-{i}'for i in range(1,5)]:
 s=c.world(n);vs,fs=s.tessellate(.05,.14);out[n+'__vertices']=np.array([tuple(v)for v in vs]);out[n+'__faces']=np.array(fs)
np.savez_compressed(R/'reference/engine/pump-functional-20261003-display-data.npz',**out)
