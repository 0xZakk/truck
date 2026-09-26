"""Export a reproducible seal-only replacement manifest without editing assembly."""
from pathlib import Path
import sys,json,argparse
import build123d as b
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import water_pump_mechanical_seal_candidate as s
ap=argparse.ArgumentParser()
ap.add_argument('--manifest',type=Path,default=ROOT/'inventory/engine/full-assembly.json')
ap.add_argument('--output-dir',type=Path,default=ROOT/'cad/engine/candidates/mechanical-seal/harness')
a=ap.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True)
m=json.loads(a.manifest.read_text());keys=set(s.LABELS)|{'water-pump-seal'}
m['definitions']=[d for d in m['definitions'] if d['id'] not in keys]
m['occurrences']=[o for o in m['occurrences'] if o['id'] not in keys]
m['assemblies']=[g for g in m['assemblies'] if g['id']!='water-pump-mechanical-seal-assembly']
def define(key,shape,name,function,system,color,sources,gaps):
 path=a.output_dir/(key+'.step');b.export_step(shape,path)
 m['definitions'].append(dict(id=key,step='/'+str(path.resolve().relative_to(ROOT)),name=name,function=function,system=system,color=color,sources=sources,unresolved=gaps))
def add(key,definition,parent,position=(0,0,0),explode=(0,0,0)):
 m['occurrences'].append(dict(id=key,definition=definition,parent=parent,position_cad_mm=list(position),rotation_cad_deg=[0,0,0],explode_cad_mm=list(explode)))
def group(key,name,parent):m['assemblies'].append(dict(id=key,name=name,parent=parent,position_cad_mm=[0,0,0]))
s.build((define,add,group));out=a.output_dir/'full-assembly.json';out.write_text(json.dumps(m,indent=2)+'\n');print(out.relative_to(ROOT))
