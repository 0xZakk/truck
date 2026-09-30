#!/usr/bin/env python3
"""Reject altered EVR promotion inputs in a disposable, repository-local stage."""
from pathlib import Path
import argparse
import copy
import hashlib
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / 'cad/engine/generated/evr-mechanism-integration-stage'
CONTROL = ROOT / 'cad/engine/generated/evr-mechanism-promotion-controls'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    global STAGE
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--stage-dir', type=Path, default=STAGE)
    STAGE = parser.parse_args().stage_dir.resolve()
    assert ROOT in STAGE.parents and 'generated' in STAGE.parts
    good = json.loads((STAGE / 'validation.json').read_text())
    assert good['status'] == 'PASS' and good['relevant_inputs_stable']
    record = json.loads((STAGE / 'installation.json').read_text())
    manifest = json.loads((STAGE / 'full-assembly.json').read_text())
    if CONTROL.exists():
        shutil.rmtree(CONTROL)
    shutil.copytree(STAGE, CONTROL)
    trials = []
    mutations = [
        ('candidate_evidence', 'installer.evidence()==rec', lambda r: r['candidate_evidence'].update(candidate_report_sha256='0'*64)),
        ('changed_checker', "scripts/check-evr-mechanism-installed.py", lambda r: r['input_sha256'].update({'scripts/check-evr-mechanism-installed.py': '0'*64})),
        ('changed_neighbor', 'neighbor_artifact_sha256', lambda r: r['neighbor_artifact_sha256'].update({next(iter(r['neighbor_artifact_sha256'])): '0'*64})),
        ('changed_export', 'models/evr-body.glb', lambda r: r['staged_artifact_sha256'].update({'models/evr-body.glb': '0'*64})),
    ]
    canonical = sha(ROOT / 'inventory/engine/full-assembly.json')
    for name, expected_error, mutate in mutations:
        bad = copy.deepcopy(record)
        mutate(bad)
        (CONTROL / 'installation.json').write_text(json.dumps(bad))
        result = subprocess.run([sys.executable, str(ROOT / 'scripts/check-evr-mechanism-installed.py'), '--stage-dir', str(CONTROL)], capture_output=True, text=True)
        assert result.returncode != 0 and 'AssertionError' in result.stderr and expected_error in result.stderr, (name, result.stderr)
        trials.append(dict(control=name, rejected=True, final_error=result.stderr.strip().splitlines()[-1]))
    (CONTROL / 'installation.json').write_text(json.dumps(record))
    shifted = copy.deepcopy(manifest)
    next(o for o in shifted['occurrences'] if o['id']=='evr-cap')['position_cad_mm'][0] += .5
    (CONTROL / 'full-assembly.json').write_text(json.dumps(shifted))
    result = subprocess.run([sys.executable, str(ROOT / 'scripts/check-evr-mechanism-installed.py'), '--stage-dir', str(CONTROL)], capture_output=True, text=True)
    assert result.returncode != 0 and 'AssertionError' in result.stderr and 'installer.scoped(m' in result.stderr, result.stderr
    trials.append(dict(control='changed_cap_frame', rejected=True, final_error=result.stderr.strip().splitlines()[-1]))
    assert canonical == sha(ROOT / 'inventory/engine/full-assembly.json')
    report = dict(status='PASS', scope='Promotion input guards only; scoped CAD check supplies geometry and replay proof', checker_sha256=sha(Path(__file__)), stage_validation_sha256=sha(STAGE/'validation.json'), stage_record_sha256=sha(STAGE/'installation.json'), canonical_manifest_sha256=canonical, controls=trials, canonical_unchanged=True)
    (CONTROL/'controls-validation.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))

if __name__ == '__main__':
    main()
