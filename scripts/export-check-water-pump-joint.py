"""Frozen STEP and actual-mesh review artifacts for uninstalled pump candidate."""
from pathlib import Path
import sys,json,hashlib
import numpy as np
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import water_pump_joint_candidate as p
import water_pump_thermactor_foot_candidate as t
from cad_metrics import solid_volume
paths=[Path(__file__),Path(p.__file__),Path(t.__file__),ROOT/'cad/engine/water_pump_gasket_topology_candidate.py',ROOT/'reference/engine/water-pump-mounting-topology-reviewed.json']
hashes={str(q.relative_to(ROOT)):hashlib.sha256(q.read_bytes()).hexdigest() for q in paths};step_hashes={}
def load(key):
 path=ROOT/f'cad/engine/generated/{key}.step';step_hashes[str(path.relative_to(ROOT))]=hashlib.sha256(path.read_bytes()).hexdigest();return b.import_step(path)
def vol(s):return sum(solid_volume(q,'adaptive') for q in s.solids()) if s else 0
parts={'block':p.block_interface(t.block_interface(load('block'))),'water-pump-housing':p.housing_interface(load('water-pump-housing')),'water-pump-gasket':p.gasket_shape(),'water-pump-shaft':p.shaft_shape(),'water-pump-impeller':p.impeller_interface(load('water-pump-impeller')),'water-pump-mounting-screw':p.screw_shape(),'thermactor-support-bracket':t.support(),'thermactor-engine-bolt-2':t.upper_bolt()}
out=Path('/private/tmp/water-pump-joint-candidate-step');out.mkdir(exist_ok=True)
roundtrips={}
for key,s in parts.items():
 assert s.is_valid and len(s.solids())==1,key
 path=out/(key+'.step');b.export_step(s,path);a=b.import_step(path)
 assert a.is_valid and len(a.solids())==1,key
 delta=vol(a)-vol(s);assert abs(delta)<.02,(key,delta);roundtrips[key]=delta
 print('STEP',key,delta,flush=True)
frame=b.Pos(*p.PUMP_POSITION)
visual={k:(s if k=='block' or k.startswith('thermactor') else frame*s) for k,s in parts.items() if k!='water-pump-mounting-screw' and not k.startswith('thermactor')}
for key in ('water-pump-seal','water-pump-slinger','water-pump-bearing','water-pump-drive-hub'):visual[key]=frame*load(key)
for n,(y,z) in enumerate(p.MOUNTING,1):visual[f'water-pump-mounting-screw-{n}']=frame*b.Pos(-51,y,z)*parts['water-pump-mounting-screw']
# Crop only the block length to expose the front cylinder; actual pump untouched.
visual['block']=visual['block'] & b.Pos(340,0,170)*b.Box(200,350,300)
arrays={};keys=[];colors=[]
for i,(key,s) in enumerate(visual.items()):
 v,f=s.tessellate(.2,.2);arrays[f'vertices_{i}']=np.asarray([tuple(q) for q in v]);arrays[f'faces_{i}']=np.asarray(f);keys.append(key)
 colors.append('#477176' if key=='block' else '#3babb5' if 'gasket' in key else '#949da3' if 'housing' in key or 'support' in key else '#b8bbc0')
arrays['metadata']=np.array(json.dumps({'parts':keys,'colors':colors,'pump_center':p.PUMP_POSITION,'module_sha256':hashes[str(Path(p.__file__).relative_to(ROOT))]}));np.savez_compressed('/private/tmp/water-pump-joint-actual.npz',**arrays)
section={};names=[];cs=[]
for key,shape in visual.items():
 cut=shape & b.Pos(400,218,170)*b.Box(600,500,600)
 if not cut or not cut.solids():continue
 i=len(names);v,f=cut.tessellate(.2,.2);section[f'vertices_{i}']=np.asarray([tuple(q) for q in v]);section[f'faces_{i}']=np.asarray(f);names.append(key);cs.append(colors[list(visual).index(key)])
section['metadata']=np.array(json.dumps({'parts':names,'colors':cs,'module_sha256':hashes[str(Path(p.__file__).relative_to(ROOT))]}));np.savez_compressed('/private/tmp/water-pump-joint-cutaway.npz',**section)
assert all(hashlib.sha256((ROOT/q).read_bytes()).hexdigest()==h for q,h in dict(hashes,**step_hashes).items())
(ROOT/'inventory/engine/water-pump-joint-step-validation.json').write_text(json.dumps({'input_hashes':hashes,'step_hashes':step_hashes,'inputs_unchanged':True,'step_volume_delta_mm3':roundtrips,'scope':'Eight valid single-solid STEP roundtrips and actual mesh export; no production fit or complete coolant network claim.'},indent=2)+'\n');print('PASS pump STEP roundtrips and mesh export')
