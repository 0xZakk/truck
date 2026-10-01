#!/usr/bin/env python3
"""Verify practical linkage adapter against frozen geometry law with shifted event time."""
from pathlib import Path
import sys,json,hashlib,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'cad/engine'))
import cam_clockwise_candidate as c
import timing_valvetrain_inclined_candidate as old
m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())
rows=[]
for q in [0,372,468,720]:
 for axial in [0,-.1]:
  frames=c.linkage_frames(m,q,axial)
  assert not any(key in frames for key in ['crankshaft','camshaft','crank-timing-gear','cam-timing-gear'])
  assert not any(f'c{i}-{kind}-spring' in frames for i in range(1,7) for kind in ['intake','exhaust'])
  # Old law sees theta-2Kx; new law sees q+2Kx. Set theta=q+4Kx.
  equivalent=old.poses(m,q+4*math.degrees(c.K*axial),axial)
  error=max(abs(frame.wrapped.Transformation().Value(i,j)-equivalent[key].wrapped.Transformation().Value(i,j)) for key,frame in frames.items() for i in range(1,4) for j in range(1,5))
  assert error<1e-9,error
  rows.append(dict(event_deg=q,axial_mm=axial,frame_count=len(frames),maximum_matrix_difference=error))
paths=[Path(__file__),Path(c.__file__),Path(old.__file__),ROOT/'inventory/engine/full-assembly.json']
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
r=dict(status='PASS practical linkage API scoped frames and unchanged source law',inputs={str(p.relative_to(ROOT)):sha(p) for p in paths},samples=rows,identity='Old(theta=q+4deg(Kx),x) has same effective event as New(q,x), both q+2deg(Kx)',excluded=['crank/cam general transforms','valve-spring compressed geometry (internal lifter springs remain rigid lifter members)'],limits=['Matrix replay of unchanged source law, not whole-engine actual neighbor check'])
(ROOT/'inventory/engine/cam-clockwise-candidate-linkage-validation.json').write_text(json.dumps(r,indent=2)+'\n');print(r['status'],rows)
