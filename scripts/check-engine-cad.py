#!/usr/bin/env python3
"""Validate saved STEP/GLB artifacts and assembled solid interference at TDC."""
import itertools
import json
import math
from pathlib import Path
import build123d as b
import numpy as np
import trimesh

root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'inventory/engine/first-assembly.json').read_text())
parts={}
for d in manifest['definitions']:
    s=b.import_step(root/d['step'].lstrip('/'))
    assert s.is_valid and len(s.solids())==1 and s.volume>0, d['id']
    assert abs(s.volume-d['volume_mm3'])/d['volume_mm3']<1e-6, d['id']
    mesh=trimesh.load(root/d['glb'].lstrip('/'),force='scene')
    native=s.bounding_box().size
    expected=np.array([native.X,native.Z,native.Y])
    assert np.max(np.abs(mesh.extents*1000-expected))<0.25, (d['id'],mesh.extents*1000,expected)
    parts[d['id']]=s
R=manifest['mechanism']['stroke_mm']/2
L=manifest['mechanism']['rod_length_mm']
collisions=[]
for degrees in [0,90,180,270]:
    angle=math.radians(degrees)
    journal_y=-R*math.sin(angle)
    journal_z=R*math.cos(angle)
    rise=math.sqrt(L*L-journal_y*journal_y)
    transforms={'crank-group':b.Rot(degrees,0,0),
                'rod-group':b.Pos(0,journal_y,journal_z)*b.Rot(-math.degrees(math.asin(-journal_y/L)),0,0),
                'piston-group':b.Pos(0,0,journal_z+rise)}
    placed=[]
    for o in manifest['occurrences']:
        loc=transforms[o['parent']]*b.Pos(*o['position_cad_mm'])
        placed.append((o['id'],parts[o['definition']].moved(loc)))
    for (aid,a),(bid,c) in itertools.combinations(placed,2):
        overlap=a.intersect(c)
        volume=sum(s.volume for s in overlap.solids()) if overlap is not None else 0
        if volume>0.1:collisions.append({'angle_deg':degrees,'a':aid,'b':bid,'volume_mm3':volume})
assembly=b.import_step(root/'cad/engine/generated/first-assembly.step')
assert len(assembly.solids())==len(placed)
report={'saved_definitions':len(parts),'assembled_occurrences':len(placed),'step_roundtrip':'pass',
        'gltf_scale_axis_bounds':'pass within 0.25 mm tessellation envelope',
        'interference_poses_deg':[0,90,180,270],
        'interference_scope':'Four sampled poses; continuous operating sweep not certified',
        'collisions_above_0_1_mm3':collisions}
(root/'inventory/engine/validation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
if collisions:raise SystemExit(1)
