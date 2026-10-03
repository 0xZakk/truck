#!/usr/bin/env python3
"""Bounded protected-neighbor static diagnostic; no installed acceptance."""
from pathlib import Path
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
from assembly_math import transforms
out=ROOT/'cad/engine/generated/intake-joint-candidate-20261003';mp=ROOT/'inventory/engine/full-assembly.json';manifest=json.loads(mp.read_text());poses=transforms(manifest);defs={d['id']:d for d in manifest['definitions']};occ={o['id']:o for o in manifest['occurrences']}
def load(i):return poses[i]*b.import_step(ROOT/defs[occ[i]['definition']]['step'].lstrip('/'))
def vol(s):return sum(x.volume for x in s.solids()) if s else 0
ids=['valve-cover','oil-filler-cap','fuel-supply-rail','regulator-vacuum-fitting','throttle-housing','egr-body','intake-head-locating-dowel']+[f'injector-{i}-metal-body' for i in range(1,7)]
report={'manifest_sha256':hashlib.sha256(mp.read_bytes()).hexdigest(),'scope':'13 named protected neighbors, static only; not whole assembly or withdrawal/motion','rows':[]}
for part in ['efi-lower-intake','efi-upper-intake']:
 new=b.import_step(out/(part+'.step'));old=load(part)
 for key in ids:
  if key not in occ:report['rows'].append({'part':part,'neighbor':key,'status':'MISSING'});continue
  neighbor=load(key)
  try:
   before=vol(old&neighbor);after=vol(new&neighbor);row={'part':part,'neighbor':key,'baseline_overlap_mm3':before,'candidate_overlap_mm3':after,'delta_mm3':after-before,'status':'NEW OVERLAP' if after>before+.1 else 'NO INCREASE ABOVE0.1mm3'}
  except Exception as e:row={'part':part,'neighbor':key,'status':'ERROR','error':str(e)}
  report['rows'].append(row);print(row,flush=True)
 (out/'context.json').write_text(json.dumps(report,indent=2)+'\n')
