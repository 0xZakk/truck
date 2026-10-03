#!/usr/bin/env python3
from pathlib import Path
import sys,importlib.util,json,hashlib,time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
path=ROOT/'cad/engine/fuel-rail-candidate-20261003.py';spec=importlib.util.spec_from_file_location('fuel_candidate',path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
OUT=ROOT/'cad/engine/generated/fuel-rail-candidate-20261003';OUT.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for sign in [1,-1]:
 start=time.time();folder=OUT/('plus' if sign==1 else 'minus');folder.mkdir(exist_ok=True)
 print('Build variant',sign,flush=True);defs,worlds,poses,info=m.parts(sign)
 report={'sign':sign,'parameters_sha256':sha(m.PARAM),'builder_sha256':sha(path),'definitions':{},'occurrences':{},'readiness':'isolated candidate; not installed'}
 for kind,rows in [('definitions',defs),('occurrences',worlds)]:
  for ident,shape in rows.items():
   dest=folder/(('local-' if kind=='definitions' else '')+ident+'.step');print('Export',sign,kind,ident,flush=True);b.export_step(shape,dest);loaded=b.import_step(dest);bb=shape.bounding_box();br=loaded.bounding_box()
   report[kind][ident]={'path':str(dest.relative_to(ROOT)),'sha256':sha(dest),'valid':shape.is_valid,'roundtrip_valid':loaded.is_valid,'solids':len(shape.solids()),'roundtrip_solids':len(loaded.solids()),'volume_mm3':shape.volume,'volume_delta_mm3':abs(shape.volume-loaded.volume),'bounds_max_error_mm':max(abs(a-c) for a,c in zip((*bb.min,*bb.max),(*br.min,*br.max)))}
 report['elapsed_seconds']=time.time()-start;(folder/'build.json').write_text(json.dumps(report,indent=2)+'\n');print('Done',sign,time.time()-start,flush=True)
