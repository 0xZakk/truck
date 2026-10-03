"""Replay a local neck-wall witness and bind the scoped static context report."""
from pathlib import Path
import hashlib
import json
import build123d as cad

ROOT = Path(__file__).resolve().parents[1]
PREFIX = ROOT / 'reference/engine/ho2s-host-candidate-20261003-front-neck-seam'
ARTIFACTS = ROOT / 'cad/engine/generated/ho2s-host-candidate-20261003'
report = Path(str(PREFIX) + '-context.json')
data = json.loads(report.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
changed = [p for p, h in data['inputs'].items() if sha(ROOT / p) != h]
assert not changed, changed
old_path = ARTIFACTS / 'front-repair/candidate.step'
new_path = ARTIFACTS / 'front-neck-seam/candidate.step'
old, new = cad.import_step(old_path), cad.import_step(new_path)
point = (195.688, -205, 211)
cube = cad.Pos(*point) * cad.Box(1, 1, 1)
def volume(shape):
    return 0 if shape is None else sum(s.volume for s in shape.solids())
old_volume, new_volume = volume(old & cube), volume(new & cube)
assert old_volume < 1e-6 and abs(new_volume - 1) < 1e-6
assert new.is_valid and len(new.solids()) == 1
out = {
    'scope': 'Independent local saved STEP wall witness and context input audit, not full acceptance',
    'old_step_sha256': sha(old_path), 'new_step_sha256': sha(new_path),
    'context_input_hashes_verified': len(data['inputs']), 'changed_inputs': changed,
    'context_conflicts': data['conflicts'], 'context_errors': data['errors'],
    'cube_center_mm': point, 'old_wall_witness_volume_mm3': old_volume,
    'new_wall_witness_volume_mm3': new_volume, 'new_valid_single_solid': True,
    'context_report_sha256': sha(report), 'checker_sha256': sha(Path(__file__)),
}
Path(str(PREFIX) + '-root-witness.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
