"""Package the reviewed checkpoint and fixtures, excluding reference originals.

Run after combined STEP/checks are refreshed. Requires the prior private CAD
archive; download instructions are in docs/CAD-ARTIFACTS.md. No network writes.
"""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import tarfile

ROOT = Path(__file__).resolve().parents[1]
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
FOLDERS = (
    'intake-runner-exterior-study', 'intake-runner-exterior-integration-stage',
    'evr-detail-candidate', 'evr-mechanism-candidate',
    'evr-mechanism-integration-stage', 'evr-mechanism-stage-before-runner',
    'evr-before-stop-hooks-20260930', 'evr-mechanism-promotion-controls',
    'evr-promotion-control-stage',
    'evr-motion', 'throttle-stop-baseline', 'throttle-stop-candidate',
    'throttle-stop-integration-stage', 'air-cleaner-candidate',
)
# Only known project-generated image views may enter this archive. In
# particular candidate-source-comparison.png contains reference imagery.
OWN_RENDER_NAMES = {
    'actual-stage-comparison.png', 'candidate-review.png',
    'candidate-section-review.png', 'candidate-endpoints.png', 'mesh-comparison.png',
}

def permitted(path):
    name = path.name.lower()
    if path.is_symlink() or name.endswith(('.pending', '.pyc')) or '__pycache__' in path.parts:
        return False
    if any('reference' in part.lower() for part in path.parts):
        return False
    if 'source-comparison' in name:
        return False
    if path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.heic', '.pdf'}:
        return path.name in OWN_RENDER_NAMES
    return True

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--previous', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    prior = json.loads((ROOT/'docs/cad-cable-distributor-checkpoint.json').read_text())
    assert sha(args.previous) == prior['sha256'], 'Wrong prior archive'
    manifest_path = ROOT/'inventory/engine/full-assembly.json'
    raw = manifest_path.read_bytes()
    manifest = json.loads(raw)
    digest = hashlib.sha256(raw).hexdigest()
    assert (len(manifest['definitions']), len(manifest['occurrences'])) == (741, 1349)
    combined = json.loads((ROOT/'inventory/engine/combined-step-export.json').read_text())
    assert combined['manifest_sha256'] == digest
    assert sha(ROOT/'cad/engine/generated/full-assembly.step') == combined['assembly_step_sha256']
    files = set()
    with tarfile.open(args.previous) as archive:
        for item in archive.getmembers():
            p = PurePosixPath(item.name)
            assert not p.is_absolute() and '..' not in p.parts
            if item.isfile():
                local = ROOT/item.name
                assert local.is_file(), f'Missing prior fixture: {item.name}'
                if permitted(local):
                    files.add(item.name)
    for d in manifest['definitions']:
        files.add(d['step'].lstrip('/'))
    files.add('cad/engine/generated/full-assembly.step')
    for folder in FOLDERS:
        source = ROOT/'cad/engine/generated'/folder
        assert source.is_dir(), source
        for p in source.rglob('*'):
            if p.is_file() and permitted(p):
                files.add(str(p.relative_to(ROOT)))
    assert all(p.startswith('cad/engine/generated/') for p in files)
    hashes = {p: sha(ROOT/p) for p in sorted(files)}
    with tarfile.open(args.output, 'w:gz') as archive:
        for p in sorted(files):
            archive.add(ROOT/p, arcname=p, recursive=False)
    assert manifest_path.read_bytes() == raw
    assert all(sha(ROOT/p) == h for p, h in hashes.items()), 'Input changed while packaging'
    report = dict(
        release_tag='checkpoint-2026-09-30-runner-evr-stops',
        asset=args.output.name, sha256=sha(args.output), size_bytes=args.output.stat().st_size,
        manifest_sha256=digest, definitions=741, occurrences=1349, files=len(files),
        scope='Active STEP definitions and combined assembly; prior fixtures plus runner, EVR, stops and isolated air-cleaner candidate. Browser acceptance remains NOT RUN. Excludes reference originals/composites, purchased manuals, owner photographs and next-batch exhaust/timing studies. Provisional; engine unfinished.',
    )
    (ROOT/'docs/cad-runner-evr-stops-checkpoint.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
