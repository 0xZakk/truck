#!/usr/bin/env python3
from pathlib import Path
import sys,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'cad/engine'))
import build123d as b
from accessory_brackets import axial
from cad_metrics import solid_volume
O=R/'cad/engine/generated/accessory-matched-carriers';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();tool=axial(11,40,(411,-100,90));b.export_step(tool,O/'lower-engine-bolt-tool.step');r={'contract':'EstimatedR11 +X tool from head frontX391 to431; fixed bolt unchanged','rows':[],'inputs':{str(Path(__file__).relative_to(R)):sha(Path(__file__))}}
for label in ['nominal','low-offset','high-offset']:
 p=R/f'cad/engine/generated/waterpump-source-offset-inlet-candidate/{label}-housing.step';r['inputs'][str(p.relative_to(R))]=sha(p);c=tool.intersect(b.import_step(p));w=O/f'lower-engine-bolt-{label}-tool-overlap.step';b.export_step(c,w);bb=c.bounding_box();r['rows'].append({'hypothesis':label,'overlap_mm3':solid_volume(c),'bounds':[tuple(bb.min),tuple(bb.max)],'witness':str(w.relative_to(R)),'sha256':sha(w)})
(R/'inventory/engine/accessory-matched-carriers-tool-witness.json').write_text(json.dumps(r,indent=2)+'\n')
