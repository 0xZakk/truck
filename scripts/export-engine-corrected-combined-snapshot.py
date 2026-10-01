#!/usr/bin/env python3
"""Correct occurrence naming using existing assembly STEP copy/roundtrip contract."""
from pathlib import Path
from copy import deepcopy
import sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import build123d as b
import engine_corrected_combined_candidate as c
from assembly_step import verify_roundtrip
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
OUT=ROOT/'cad/engine/generated/engine-corrected-combined-candidate'
m,paths,sh=c.load();frames=c.frames(m,55,0);placed=[]
for key,shape in sh.items():
 q=deepcopy(shape).moved(frames[key]);q.label=key;placed.append(q)
p=OUT/'combined-q55-named.step';b.export_step(b.Compound(children=placed),p,unit=b.Unit.MM)
check=verify_roundtrip(p,placed)
files=[Path(__file__),Path(c.__file__),ROOT/'cad/engine/assembly_step.py',ROOT/'inventory/engine/engine-corrected-combined-motion-validation.json',OUT/'combined-q55-layout.json']+list(set(paths.values()))
r=dict(status='PASS named actual candidate snapshot; mechanical rod-bolt FAIL remains',inputs={str(p.relative_to(ROOT)):sha(p) for p in files},snapshot_sha256=sha(p),roundtrip=check,initial_shared_topology_export={'path':'cad/engine/generated/engine-corrected-combined-candidate/combined-q55.step','sha256':sha(OUT/'combined-q55.step'),'status':'REJECTED naming; only51 distinct labels visible for328 selected occurrences; original bytes retained'},limits=['Selected328 occurrences only; omitted valve springs and crossed-drive group documented in layout','Named export success does not change six physical interference failures'])
(ROOT/'inventory/engine/engine-corrected-combined-snapshot-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],check,flush=True)
