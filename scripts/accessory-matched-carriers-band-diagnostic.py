#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
import accessory_matched_carriers_candidate as c
import accessory_brackets as base
from cad_metrics import solid_volume
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();inputs={str(p.relative_to(R)):sha(p)for p in [Path(__file__),Path(c.__file__),Path(base.__file__)]};rows=[]
for label in ['nominal','low-offset','high-offset']:
 f=R/f'cad/engine/generated/waterpump-source-offset-inlet-candidate/{label}-housing.step';inputs[str(f.relative_to(R))]=sha(f);p=b.import_step(f)
 parts={g+' band':c.band(g)for g in ['ALT','AP']}
 for i,(y,z)in enumerate(c.EARS['AP']):parts['AP mandatory boss'+str(i)]=base.boss(c.FACES['AP'],y,z,11,5.5)
 for name,s in parts.items():
  x=s.intersect(p);v=solid_volume(x)if x else 0;row={'pump':label,'component':name,'overlap_mm3':v,'distance_mm':s.distance_to(p)}
  if v>.1:
   w=R/'cad/engine/generated/accessory-matched-carriers'/f'trial0-{label}-{name.replace(" ","-")}-overlap.step';b.export_step(x,w);row['witness']=str(w.relative_to(R))
  rows.append(row)
(R/'inventory/engine/accessory-matched-carriers-band-diagnostic.json').write_text(json.dumps({'rows':rows,'inputs':inputs},indent=2)+'\n');print(rows)
