"""Localize frozen seal assets for later coordinated integration; no installation."""
from pathlib import Path
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import build123d as b
import numpy as np
import trimesh
from assembly_math import transforms

OUT = ROOT / 'cad/engine/generated/front-seal-2692-integration-stage'
SOURCE = ROOT / 'cad/engine/generated/front-seal-2692-candidate'

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def bindings(obj):
    if isinstance(obj, dict):
        for p, value in obj.items():
            if '/' in p and isinstance(value, str) and len(value) == 64:
                yield p, value
            else:
                yield from bindings(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from bindings(value)

def bounds(shape):
    bb = shape.bounding_box()
    return np.array([tuple(bb.min), tuple(bb.max)])

def main():
    manifest = ROOT / 'inventory/engine/full-assembly.json'
    delivery = ROOT / 'inventory/engine/front-seal-2692-delivery-validation.json'
    watched = {manifest: sha(manifest), delivery: sha(delivery)}
    proof = json.loads(delivery.read_text())
    # Every directly named hash in the frozen delivery must still match.
    for path, expected in bindings(proof):
        p = ROOT / path
        assert p.exists() and sha(p) == expected, path
        watched[p] = expected
    m = json.loads(manifest.read_text())
    poses = transforms(m)
    occurrences = {o['id']: o for o in m['occurrences']}
    specifications = [
        ('timing-cover', 'cover', 'timing-cover'),
        ('damper-hub', 'damper-hub', 'damper-hub'),
        ('front-seal-case', 'seal-case-installed', 'front-seal'),
        ('front-seal-elastomer', 'seal-elastomer', 'front-seal'),
        ('front-seal-garter-spring', 'seal-garter-spring', 'front-seal'),
    ]
    OUT.mkdir(parents=True, exist_ok=True)
    rows = []
    for identity, stem, datum in specifications:
        pose = poses[datum]
        # These existing frames are pure translations. Reject any future
        # rotational change rather than translating meshes incorrectly.
        t = pose.wrapped.Transformation()
        rotation = np.array([[t.Value(i,j) for j in range(1,4)] for i in range(1,4)])
        assert np.max(np.abs(rotation - np.eye(3))) < 1e-10
        translation = np.array([t.Value(i,4) for i in range(1,4)])
        sp, gp = SOURCE / (stem + '.step'), SOURCE / (stem + '.glb')
        watched[sp], watched[gp] = sha(sp), sha(gp)
        source = b.import_step(sp)
        local = pose.inverse() * source
        staged_step = OUT / (identity + '.step')
        b.export_step(local, staged_step)
        reread = b.import_step(staged_step)
        assert reread.is_valid and len(reread.solids()) == len(source.solids())
        assert len(reread.faces()) == len(source.faces())
        volume_error = abs(reread.volume - source.volume)
        assert volume_error < .1
        restored = pose * reread
        step_error = float(np.max(np.abs(bounds(restored) - bounds(source))))
        assert step_error < .01
        original = trimesh.load(gp, force='mesh')
        mesh = original.copy()
        offset = translation[[0,2,1]] * np.array([1,1,-1]) / 1000
        mesh.vertices -= offset
        staged_glb = OUT / (identity + '.glb')
        trimesh.Scene(mesh).export(staged_glb)
        read_mesh = trimesh.load(staged_glb, force='mesh')
        assert read_mesh.vertices.shape == original.vertices.shape
        assert np.array_equal(read_mesh.faces, original.faces)
        vertex_error = float(np.max(np.abs(read_mesh.vertices + offset - original.vertices))) * 1000
        assert vertex_error < .01 and read_mesh.is_watertight and read_mesh.is_winding_consistent
        double_error = float(np.max(np.abs(read_mesh.vertices + 2*offset - original.vertices))) * 1000
        assert double_error > 100, 'Double-placement negative control failed'
        row = {'id': identity, 'source_world_asset': stem,
               'world_frame_translation_mm': translation.tolist(),
               'step_world_bounds_error_mm': step_error,
               'mesh_world_vertex_error_mm': vertex_error,
               'double_placement_fault_mm': double_error,
               'solid_count': len(reread.solids()), 'volume_roundtrip_error_mm3': volume_error,
               'face_count':len(reread.faces()), 'triangles': len(read_mesh.faces),
               'step': str(staged_step.relative_to(ROOT)), 'step_sha256': sha(staged_step),
               'glb': str(staged_glb.relative_to(ROOT)), 'glb_sha256': sha(staged_glb)}
        if datum != 'front-seal':
            row['preserved_occurrence'] = occurrences[datum]
        else:
            row['proposed_occurrence'] = {'id':identity, 'definition':identity,
                'parent':'front-seal-assembly', 'position_cad_mm':[0,0,0], 'rotation_cad_deg':[0,0,0]}
        rows.append(row)
        print(identity, 'localized STEP/GLB verified', flush=True)
    assert all(sha(p) == expected for p, expected in watched.items())
    report = {'status':'PASS asset coordinate stage only; not installed',
        'inputs':{str(p.relative_to(ROOT)):value for p,value in watched.items()},
        'checker_sha256':sha(Path(__file__)), 'parts':rows,
        'proposed_seal_assembly':{'id':'front-seal-assembly','parent':occurrences['front-seal']['parent'],
            'position_cad_mm':occurrences['front-seal']['position_cad_mm'], 'motion':None},
        'required_navigation_alias':{'front-seal':'front-seal-assembly'},
        'canonical_modified':False,
        'limits':['No full manifest or geometry promotion.','Free case is a comparison state, not a fourth seal part.',
                  'Coordinated timing integration and old-link handling remain required.','Browser NOT RUN.']}
    (ROOT / 'inventory/engine/front-seal-2692-stage-validation.json').write_text(json.dumps(report,indent=2)+'\n')

if __name__ == '__main__':
    main()
