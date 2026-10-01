#!/usr/bin/env python3
import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import ignition_leads as c
OUT=ROOT/'cad/engine/generated/shifted-ignition-lead-replay';OUT.mkdir(exist_ok=True)
p=ROOT/'cad/engine/generated/ignition-lead-1-jacket.step';old=b.import_step(p)
print('rebuild source',flush=True);q,_=c.cable(c.plug_path(1),c.cap_frame(1));b.export_step(q,OUT/'replayed-lead1-jacket.step')
vol=lambda s:sum(x.volume for x in s.solids()) if s else 0.
r={'status':'DIAGNOSTIC','old_volume_mm3':vol(old),'replay_volume_mm3':vol(q),'old_bounds':[list(old.bounding_box().min),list(old.bounding_box().max)],'replay_bounds':[list(q.bounding_box().min),list(q.bounding_box().max)]};print(r,flush=True)
a=old.cut(q);print('old-minus-new',vol(a),flush=True);z=q.cut(old);print('new-minus-old',vol(z),flush=True);r['old_minus_replay_mm3']=vol(a);r['replay_minus_old_mm3']=vol(z)
for n,s in [('old-minus-replay',a),('replay-minus-old',z)]:
 if s and s.solids():b.export_step(s,OUT/(n+'.step'))
paths=['scripts/probe-ignition-lead-source-replay.py','cad/engine/ignition_leads.py','cad/engine/oil_drive_layout.py','cad/engine/plug_mounts.py','cad/engine/generated/ignition-lead-1-jacket.step'];r['inputs']={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths};(ROOT/'inventory/engine/shifted-ignition-lead-source-replay-diagnostic.json').write_text(json.dumps(r,indent=2)+'\n')
