"""Rebuild the engine tracking inventory; no GitHub mutations. Run from repo root."""
import collections
import hashlib
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'inventory/engine'
manifest_path = BASE / 'full-assembly.json'
manifest = json.loads(manifest_path.read_text())
scope = json.loads((BASE / 'work-breakdown-scope.json').read_text())
issue_map_path = BASE / 'work-breakdown-issues.json'
issue_map = json.loads(issue_map_path.read_text()) if issue_map_path.exists() else {}
occurrences = collections.defaultdict(list)
for o in manifest['occurrences']:
    occurrences[o['definition']].append(o)
groups = {g['id']: {**g, 'parts': []} for g in scope['groups']}
for d in manifest['definitions']:
    matches = [g for g in scope['groups'] if any(re.fullmatch(p, d['id']) for p in g['patterns'])]
    if not matches:
        raise ValueError(f'Unmapped definition: {d["id"]}')
    # Ordered specific patterns precede broad family patterns, as documented in scope.
    g = groups[matches[0]['id']]
    g['parts'].append({
        'id': d['id'], 'name': d.get('name', d['id']),
        'modeled_quantity': len(occurrences[d['id']]),
        'geometry_status': d.get('geometry_status', 'unknown'),
        'function': d.get('function', ''), 'sources': d.get('sources', []),
        'unresolved': d.get('unresolved', []), 'glb': d.get('glb'), 'step': d.get('step'),
        'occurrences': [{'id': o['id'], 'parent': o['parent'], 'name': o.get('name')} for o in occurrences[d['id']]],
    })
sha = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
count = sum(len(g['parts']) for g in groups.values())
quantity = sum(p['modeled_quantity'] for g in groups.values() for p in g['parts'])
assert count == len(manifest['definitions']) and quantity == len(manifest['occurrences'])
assert set(occurrences) <= {d['id'] for d in manifest['definitions']}
DOC = ROOT / 'docs/engine-parts'
DOC.mkdir(exist_ok=True)
index = ['# Engine parts and work breakdown', '', '[Engine ticket](https://github.com/0xZakk/truck/issues/1) · [Engine parts project view](https://github.com/users/0xZakk/projects/2/views/6)', '',
         'Authoritative tracking snapshot of every current modeled definition and occurrence, plus known missing work. This is not a verified Ford production BOM: unknown variants, quantities and undiscovered internals remain an explicit reconciliation task.', '',
         f'Manifest SHA-256: `{sha}`. **{count} definitions / {quantity} modeled occurrences / {len(groups)} work packages.** Repeated physical instances share a checklist entry with their modeled quantity; occurrence IDs remain in the JSON inventory.', '',
         'Existing geometry is credited separately from acceptance. Integrated/candidate packages enter In review for acceptance triage; identified unbuilt work enters Backlog. In review does not assert that known fit/evidence failures have passed. Rejected parts remain open. No worker is implied to be running. Done requires a recorded acceptance decision, not geometry presence.', '',
         'Engine owns these current engine-mounted models; linked truck-system issues own their vehicle-side continuations. Do not duplicate the same physical part in another system backlog. Boundaries and unknown applicability are called out in each package.', '',
         'Each package lists every modeled part and its unresolved claims, then the additional known scope. Checklist boxes mean **accepted completion**, not mere geometry existence. The explicit geometry-delivered checkbox credits the existing model without closing unfinished parts.', '',
         '| Package | Modeled definitions | Modeled quantity | Board status | Ticket |',
         '|---|---:|---:|---|---|']
for g in groups.values():
    g['issue'] = issue_map.get(g['id'], {}).get('number', g['existing_issue'])
    has_candidate = g['id'] in ('oil-cap', 'throttle-bracket', 'dipstick', 'accessory-belt')
    g['status'] = g.get('tracking_status') or ('In review' if g['parts'] or has_candidate else 'Backlog')
    assert g['status'] in ('Backlog', 'Ready', 'In progress', 'In review', 'Done')
    if g['status'] == 'Done':
        assert g.get('acceptance_record') and (ROOT / g['acceptance_record']).is_file(), f"Done requires a recorded acceptance review: {g['id']}"
    g['status_reason'] = g.get('tracking_reason') or ('Existing provisional geometry/candidate and evidence await acceptance triage; listed failures and omissions remain open.' if g['status'] == 'In review' else 'Known scope not delivered as a complete modeled/installed package; applicability and quantity may need research.')
    g['accepted_complete'] = g['status'] == 'Done'
    g['modeled_quantity'] = sum(p['modeled_quantity'] for p in g['parts'])
    ticket = f'[#{g["issue"]}](https://github.com/0xZakk/truck/issues/{g["issue"]})' if g['issue'] else 'Pending creation'
    index.append(f'| [{g["title"]}]({g["id"]}.md) | {len(g["parts"])} | {g["modeled_quantity"]} | {g["status"]} | {ticket} |')
    lines = [f'# {g["title"]}', '', f'Engine parent: [#1](https://github.com/0xZakk/truck/issues/1). Component ticket: {ticket}.', '',
             f'**{g["status"]}** — {g["status_reason"]}', '',
             f'Baseline manifest: `{sha}`. Quantities below count current modeled instances, not verified production quantities.', '',
             '## Existing modeled parts', '',
             ('- [x] Provisional geometry is present in the integrated engine manifest.' if g['parts'] else '- No accepted installed definitions are mapped to this package; candidate artifacts may exist as noted below.'), '',
             'Acceptance checkboxes remain unchecked until the common quality gates pass for the agreed scope.', '']
    if g['id'] == 'water-pump':
        lines += ['Current-state correction: the cast inlet neck is present in this manifest. Older unresolved strings below saying it is missing are superseded; its production geometry and flow fidelity remain unverified.', '']
    for p in g['parts']:
        ids = ', '.join('`'+o['id']+'`' for o in p['occurrences'])
        lines += [f'- [{"x" if g["accepted_complete"] else " "}] **{p["name"]}** — `{p["id"]}`; modeled quantity **{p["modeled_quantity"]}**; {p["geometry_status"]}.',
                  f'  - Instances: {ids or "none (unused definition; reconcile)"}',
                  f'  - Source IDs: {", ".join(p["sources"]) or "not recorded"}. Resolve in `inventory/engine/full-assembly.json` / evidence records.']
        for gap in p['unresolved']:
            lines.append('  - Open: '+gap.replace('\n', ' '))
    if g.get('candidate_parts'):
        lines += ['', '## Separate candidate parts (not installed)', '']
        for candidate in g['candidate_parts']:
            lines.append(f"- [ ] **{candidate['name']}** — `{candidate['id']}`; {candidate['status']}. Source: `{candidate['artifact']}`.")
    if g.get('legacy_artifacts'):
        lines += ['', '## Historical artifacts (not current installed inventory)', '']
        for artifact in g['legacy_artifacts']:
            lines.append(f"- `{artifact['id']}` — {artifact['status']}.")
    lines += ['', '## Additional known scope and reconciliation', '']
    lines += ['- [ ] '+r for r in g['remaining']]
    if g['related_system_issues']:
        lines += ['', '## Cross-system boundaries', '', 'Coordinate with '+', '.join(f'[#{n}](https://github.com/0xZakk/truck/issues/{n})' for n in g['related_system_issues'])+'. Keep the current engine-mounted component here; agree ownership before adding its vehicle-side continuation.']
    lines += ['', '## Acceptance and handoff', '',
              'Use [the shared rubric](../onboarding/QUALITY-STANDARD.md) and [component handoff](../templates/COMPONENT-HANDOFF.md). Reconcile sources, critical dimensions, interfaces, motion/flow, actual render comparison, individual-part learning and browser behavior. A saved audit is evidence only for its recorded hashes and scope. Current global static/navigation passes do not complete every component.', '',
              'Evidence starting points: `inventory/engine/full-assembly.json`, component-specific evidence/learning/validation JSON, `docs/CURRENT-STATE.md`, and `inventory/engine/completion-plan.json`. Older completion prose contains superseded missing/pending statements; this package maps the current manifest. Future source/BOM reconciliation may add parts.', '']
    (DOC / (g['id']+'.md')).write_text('\n'.join(lines))
index += ['', '## Rebuild and audit', '', '`python3 scripts/build-engine-work-breakdown.py` regenerates this index and all package pages from the manifest, curated scope and persisted GitHub issue mapping. It fails on an unmapped definition and checks occurrence coverage. Update the curated scope when new part families appear. Do not infer Done from file existence or close an issue solely because a worker stopped.', '', 'To record a later status change in this snapshot, update tracking_status and tracking_reason in the curated scope. Done also requires acceptance_record pointing to the reviewed handoff in the repository. Regenerate and review the change; do not infer acceptance from file existence. The board is the operational status authority after import; this generated snapshot records the import assessment. Review status decisions against current handoffs before future updates; the generator does not overwrite GitHub statuses.', '']
(DOC / 'README.md').write_text('\n'.join(index))
output = {'schema_version': 1, 'manifest_sha256': sha, 'definition_count': count, 'occurrence_count': quantity, 'group_count': len(groups), 'verified_production_bom': False, 'groups': list(groups.values())}
(BASE / 'work-breakdown.json').write_text(json.dumps(output, indent=2)+'\n')
print(json.dumps({'groups': len(groups), 'definitions': count, 'occurrences': quantity, 'statuses': dict(collections.Counter(g['status'] for g in groups.values())), 'done': sum(g['accepted_complete'] for g in groups.values())}))
