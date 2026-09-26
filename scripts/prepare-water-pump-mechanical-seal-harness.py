from pathlib import Path
import sys,json,shutil,copy
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'cad/engine'))
import water_pump_mechanical_seal_candidate as s
base=Path('/private/tmp/truck-seal-inlet-baseline-2032a3da');stage=Path('/private/tmp/truck-seal-inlet-install-harness');(stage/'scripts').mkdir(parents=True,exist_ok=True);(stage/'inventory/engine').mkdir(parents=True,exist_ok=True);(stage/'candidate-step').mkdir(exist_ok=True);(stage/'cad').mkdir(exist_ok=True)
if not (stage/'cad/engine').exists():(stage/'cad/engine').symlink_to(root/'cad/engine')
m=json.loads((base/'full-assembly.json').read_text());m['definitions']=[d for d in m['definitions'] if d['id']!='water-pump-seal'];m['occurrences']=[o for o in m['occurrences'] if o['id']!='water-pump-seal']
def define(key,shape,name,function,system,color,sources,gaps):
 shutil.copy2(Path('/private/tmp/water-pump-mechanical-seal-step')/(key+'.step'),stage/'candidate-step'/(key+'.step'));m['definitions'].append(dict(id=key,step='/candidate-step/'+key+'.step',name=name,function=function,system=system,color=color,sources=sources,unresolved=gaps))
def add(key,definition,parent,position=(0,0,0),explode=(0,0,0)):
 m['occurrences'].append(dict(id=key,definition=definition,parent=parent,position_cad_mm=list(position),rotation_cad_deg=[0,0,0],explode_cad_mm=list(explode)))
def group(key,name,parent):m['assemblies'].append(dict(id=key,name=name,parent=parent,position_cad_mm=[0,0,0]))
s.build((define,add,group));(stage/'inventory/engine/full-assembly.json').write_text(json.dumps(m,indent=2)+'\n');shutil.copy2(root/'scripts/check-water-pump-mechanical-seal-installed.py',stage/'scripts/check-water-pump-mechanical-seal-installed.py');print(len(m['definitions']),len(m['occurrences']),stage)
