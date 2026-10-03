from pathlib import Path
import sys,json,hashlib,numpy as np
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import pump_cover_candidate_20261003 as c
out={};inputs={};sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
names=['water-pump-housing','heater-pump-return-elbow','water-pump-drive-hub','water-pump-pulley','water-pump-impeller','water-pump-gasket']+[f'water-pump-mounting-screw-{i}'for i in range(1,5)]
for n in names:
 p=c.O/(n+'.step');s=b.import_step(p);inputs[str(p.relative_to(R))]=sha(p);vs,fs=s.tessellate(.05,.14);out[n+'__vertices']=np.array([tuple(v)for v in vs]);out[n+'__faces']=np.array(fs);print(n,len(fs),flush=True)
for n in ['timing-cover','timing-cover-mounting-screw-3','thermactor-engine-bolt-1','alternator-thermactor-common-carrier','coolant-outlet-housing','coolant-outlet-gasket','cylinder-head','head-gasket']:
 s=c.original(n)
 if n in ['cylinder-head','head-gasket']:s=c.norm(s.intersect(b.Pos(400,-20,270)*b.Box(140,240,120)))
 vs,fs=s.tessellate(.05,.14);out[n+'__vertices']=np.array([tuple(v)for v in vs]);out[n+'__faces']=np.array(fs);print(n,len(fs),flush=True)
np.savez_compressed(R/'reference/engine/pump-cover-candidate-20261003-display-data.npz',**out)
(R/'reference/engine/pump-cover-candidate-20261003-display-data.json').write_text(json.dumps({'scope':'Actual STEPs, display-only. Head/headgasket clipped toX330..470,Y-140..100,Z210..330 for local context, no geometry modification.','linear_mm':.05,'angular_rad':.14,'inputs':inputs},indent=2)+'\n')
