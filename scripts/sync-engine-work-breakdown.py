"""Publish engine work packages as sub-issues of #1; explicit --apply required.

Uses the caller's gh authentication. Writes a resumable issue map after each
creation. Does not close issues or override operational Project status.
"""
import argparse
import json
import subprocess
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'inventory/engine'
REPO = '0xZakk/truck'
parser = argparse.ArgumentParser()
parser.add_argument('--apply', action='store_true')
args = parser.parse_args()
data = json.loads((BASE / 'work-breakdown.json').read_text())
map_path = BASE / 'work-breakdown-issues.json'
issue_map = json.loads(map_path.read_text()) if map_path.exists() else {}

def api(endpoint, payload=None, method=None):
    cmd = ['gh', 'api', endpoint]
    if payload is not None:
        cmd += ['--method', method or 'POST', '--input', '-']
    result = subprocess.run(cmd, input=json.dumps(payload) if payload is not None else None,
                            text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f'{endpoint}: {result.stderr[:400]}')
    if payload is not None:
        time.sleep(1.5)  # Keep mutations comfortably below burst limits.
    return json.loads(result.stdout) if result.stdout.strip() else None

def paged(endpoint):
    all_items = []
    for page in range(1, 30):
        rows = api(endpoint + ('&' if '?' in endpoint else '?') + f'per_page=100&page={page}')
        all_items.extend(rows)
        if len(rows) < 100:
            return all_items
    raise RuntimeError('Unexpected pagination length')

def body(g):
    marker = f'<!-- engine-work-package:{g["id"]} -->'
    url = f'https://github.com/{REPO}/blob/main/docs/engine-parts/{g["id"]}.md'
    lines = [marker, f'Engine component work package under #1. **Import assessment: {g["status"]}.**', '',
             g['status_reason'], '',
             f'Existing inventory: **{len(g["parts"])} definitions / {g["modeled_quantity"]} modeled instances**. All are provisional. Quantities are modeled counts, not certified Ford quantities.', '',
             f'[Full parts/evidence/gaps list]({url}) · [Common quality standard](https://github.com/{REPO}/blob/main/docs/onboarding/QUALITY-STANDARD.md)', '',
             '## Modeled parts — acceptance checklist', '',
             'Boxes mean accepted completion. Existing modeled geometry is credited below; an unchecked box does not mean the model is absent.', '']
    if g['parts']:
        lines.append('- [x] Provisional integrated geometry already exists for the following inventory.')
    for p in g['parts']:
        lines.append(f'- [ ] {p["name"]} — `{p["id"]}`, modeled quantity {p["modeled_quantity"]}.')
    if not g['parts']:
        lines.append('No installed definitions mapped; see candidate/remaining scope below.')
    if g.get('candidate_parts'):
        lines += ['', '## Separate candidate parts (not installed)', '']
        for candidate in g['candidate_parts']:
            lines.append(f"- [ ] {candidate['name']} — `{candidate['id']}`; {candidate['status']}.")
    lines += ['', '## Additional known parts / work', '']
    lines += ['- [ ] '+x for x in g['remaining']]
    lines += ['', '## Acceptance gates', '',
              '- [ ] Resolve applicability, BOM and source-supported dimensions; record all remaining assumptions.',
              '- [ ] Validate CAD/export, source-image comparison, attachment contacts and neighboring clearances.',
              '- [ ] Validate relevant motion/flow and staged disassembly/reassembly.',
              '- [ ] Complete individual part explanations/diagnostics and verify browser navigation.',
              '- [ ] Integration owner records acceptance against input hashes and merges the checked result.', '',
              'Related truck-system boundaries: '+(', '.join('#'+str(n) for n in g['related_system_issues']) or 'Engine-owned')+'.', '',
              'Before starting, assign an owner and create a handoff from `docs/templates/COMPONENT-HANDOFF.md`. Do not close this package from geometry existence, a static check alone, or worker completion. Existing failures remain open. Missing internals/variant quantities require reconciliation; this is not a certified exhaustive production BOM.']
    if g['existing_issue']:
        lines += ['', f'Pilot history: `docs/pilot/{"throttle-bracket" if g["id"] == "throttle-bracket" else g["id"]}.md` and `docs/pilot/RESULTS.md`. Candidate remains unaccepted.']
    return '\n'.join(lines)+'\n'

if not args.apply:
    print(f'Dry run: {len(data["groups"])} packages; {sum(not g["existing_issue"] and g["id"] not in issue_map for g in data["groups"])} potential new issues. No mutations.')
    raise SystemExit()
labels = {x['name'] for x in paged(f'repos/{REPO}/labels')}
for name, color in [('engine:parts-inventory','1d76db'),('engine:acceptance-review','fbca04'),('engine:unmodeled-scope','c5def5')]:
    if name not in labels:
        api(f'repos/{REPO}/labels', {'name': name, 'color': color})
existing = paged(f'repos/{REPO}/issues?state=all')
by_number = {x['number']: x for x in existing}
by_marker = {}
for issue in existing:
    for g in data['groups']:
        if f'<!-- engine-work-package:{g["id"]} -->' in (issue.get('body') or ''):
            by_marker[g['id']] = issue
children = {x['id'] for x in paged(f'repos/{REPO}/issues/1/sub_issues')}
for index, g in enumerate(data['groups'], 1):
    saved_number = issue_map.get(g['id'], {}).get('number', g['existing_issue'])
    issue = by_number.get(saved_number) or by_marker.get(g['id'])
    planned = body(g)
    package_labels = ['system:engine', 'type:component', 'engine:parts-inventory',
                      'engine:acceptance-review' if g['status'] == 'In review' else 'engine:unmodeled-scope']
    if issue is None:
        issue = api(f'repos/{REPO}/issues', {'title': '[Engine] '+g['title'], 'body': planned, 'labels': package_labels})
    else:
        # Preserve the pilot history, append a bounded generated tracking section.
        marker = f'<!-- engine-work-package:{g["id"]} -->'
        original = issue.get('body') or ''
        prefix = original.split(marker)[0].rstrip() if g['existing_issue'] else ''
        updated = (prefix+'\n\n' if prefix else '') + planned
        combined = sorted(set(package_labels + [x['name'] for x in issue.get('labels', [])]))
        if marker not in original and (updated != original or combined != sorted(x['name'] for x in issue.get('labels', []))):
            issue = api(f'repos/{REPO}/issues/{issue["number"]}', {'body': updated, 'labels': combined}, 'PATCH')
    issue_map[g['id']] = {'number': issue['number'], 'id': issue['id'], 'url': issue['html_url'], 'import_status': g['status']}
    map_path.write_text(json.dumps(issue_map, indent=2)+'\n')
    if issue['id'] not in children:
        api(f'repos/{REPO}/issues/1/sub_issues', {'sub_issue_id': issue['id']})
        children.add(issue['id'])
    if index % 10 == 0 or index == len(data['groups']):
        print(f'Published/linked {index}/{len(data["groups"])} packages', flush=True)
print('Issue publication complete. Project statuses require verification; no issues were closed.')
