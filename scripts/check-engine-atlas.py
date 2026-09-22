"""Verify saved artifacts, hierarchy and selected mechanical interfaces.

This is a development report, not a certificate of OEM accuracy or completion.
"""
import json
import sys
import itertools
import hashlib
from pathlib import Path
import build123d as b
import numpy as np
import trimesh

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'cad/engine'))
from assembly_math import transforms

m=json.loads((ROOT/'inventory/engine/full-assembly.json').read_text())
defs={d['id']:d for d in m['definitions']}
assert len(defs)==len(m['definitions'])
ids={o['id'] for o in m['occurrences']}
assert len(ids)==len(m['occurrences'])
groups={a['id'] for a in m['assemblies']}
assert len(groups)==len(m['assemblies'])
assert not groups.intersection(ids), 'Occurrence and assembly ids must be distinct'
parts={}
for d in defs.values():
    s=b.import_step(ROOT/d['step'].lstrip('/'))
    assert s.is_valid and len(s.solids())==1 and s.volume>0,d['id']
    assert abs(s.volume/d['volume_mm3']-1)<1e-6,d['id']
    glb=trimesh.load(ROOT/d['glb'].lstrip('/'),force='scene')
    bb=s.bounding_box().size
    assert np.max(np.abs(glb.extents*1000-np.array([bb.X,bb.Z,bb.Y])))<.5,d['id']
    parts[d['id']]=s
for o in m['occurrences']:
    assert o['definition'] in defs and o['parent'] in groups,o['id']
    assert all(np.isfinite(o['position_cad_mm'])),o['id']
assembly=b.import_step(ROOT/'cad/engine/generated/full-assembly.step')
assert len(assembly.solids())==len(m['occurrences'])
print('Artifact, scale and hierarchy checks passed',flush=True)
collisions=[]
poses=[0] if '--all-static' in sys.argv else [0,90,180,270]
for angle in poses:
    loc=transforms(m,angle)
    targets=['block','crankshaft']+[f'c{i}-{p}' for i in range(1,7) for p in ['piston-1','connecting-rod-1','rod-cap-1']]
    placed={o['id']:parts[o['definition']].moved(loc[o['id']]) for o in m['occurrences'] if '--all-static' in sys.argv or o['id'] in targets}
    pairs=[('crankshaft','block')]+[(f'c{i}-{p}',target) for i in range(1,7) for p in ['piston-1','connecting-rod-1','rod-cap-1'] for target in ['block','crankshaft']]
    if '--all-static' in sys.argv:
        bounds={id:s.bounding_box() for id,s in placed.items()}
        pairs=[(a,c) for a,c in itertools.combinations(placed,2) if all(min(getattr(bounds[a].max,k),getattr(bounds[c].max,k))-max(getattr(bounds[a].min,k),getattr(bounds[c].min,k))>.01 for k in ['X','Y','Z'])]
        print('Testing',len(pairs),'broad-phase overlapping pairs',flush=True)
    for aid,bid in pairs:
        overlap=placed[aid].intersect(placed[bid])
        volume=sum(s.volume for s in overlap.solids()) if overlap else 0
        if volume>.1:collisions.append(dict(angle_deg=angle,a=aid,b=bid,volume_mm3=round(volume,3)))
    print('Checked rotating/core interfaces at',angle,flush=True)
report=dict(definitions=len(defs),occurrences=len(ids),artifact_integrity='pass',gltf_scale_axis_bounds='pass within 0.5 mm',
    assembled_step_solids=len(assembly.solids()),manifest_sha256=hashlib.sha256((ROOT/'inventory/engine/full-assembly.json').read_bytes()).hexdigest(),
    checked_poses_deg=poses,collision_scope='Crank, pistons, rods and caps against block and crank; does not cover all part pairs or continuous motion.',
    collisions=collisions,verified_complete=False)
if '--all-static' in sys.argv:report['collision_scope']='All part pairs with overlapping bounding boxes at a single static pose; intentional fit interfaces may be included.'
filename='atlas-static-validation.json' if '--all-static' in sys.argv else 'atlas-validation.json'
(ROOT/'inventory/engine'/filename).write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({**report,'collisions':f'{len(collisions)} overlaps; see {filename} for individual pairs'},indent=2))
if collisions:sys.exit(1)
