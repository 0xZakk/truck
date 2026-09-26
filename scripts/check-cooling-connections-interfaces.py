"""Verify the generated cooling API placements against the candidate geometry."""
import hashlib
import json
from pathlib import Path
import sys
import build123d as b

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'cad/engine'))
import cooling_connections as candidate
from assembly_math import transforms

manifest_path = ROOT / 'inventory/engine/full-assembly.json'
raw = manifest_path.read_bytes()
manifest = json.loads(raw)
definitions = {}
occurrences = []


def define(identifier, shape, *metadata):
    definitions[identifier] = shape


def group(identifier, name, parent='engine', motion=None, position=(0, 0, 0)):
    manifest['assemblies'].append({'id': identifier, 'name': name, 'parent': parent,
                                   'position_cad_mm': position, 'motion': motion})


def add(identifier, definition, parent, pos=(0, 0, 0), explode=(0, 0, 0), rotation=(0, 0, 0)):
    occurrences.append({'id': identifier, 'definition': definition, 'parent': parent,
                        'position_cad_mm': pos, 'rotation_cad_deg': rotation})


candidate.build((define, add, group))
manifest['occurrences'] = occurrences
poses = transforms(manifest)
expected = {identifier: b.Pos(*position) * definitions[definition]
            for identifier, definition, position in candidate.placements()}
for occurrence in occurrences:
    actual = definitions[occurrence['definition']].moved(poses[occurrence['id']])
    target = expected[occurrence['id']]
    common = actual.intersect(target)
    volume = sum(solid.volume for solid in common.solids()) if common else 0
    assert abs(volume - target.volume) < .02, occurrence['id']

assert raw == manifest_path.read_bytes()
report = {'manifest_sha256': hashlib.sha256(raw).hexdigest(),
          'source_sha256': hashlib.sha256(Path(candidate.__file__).read_bytes()).hexdigest(),
          'api_transform_checks': len(occurrences), 'verified_production_fit': False}
(ROOT / 'inventory/engine/cooling-connections-interface-validation.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2), flush=True)
