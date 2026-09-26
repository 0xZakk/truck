"""Explicit, verified Project status updates; dry-run unless --apply.

Uses gh's authentication, never resets the board from an old import snapshot.
Issue closure and checklist acceptance remain separate reviewed operations.
"""
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = '0xZakk/truck'
OWNER = '0xZakk'
PROJECT = '2'


def gh(*args):
    result = subprocess.run(['gh', *args], text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    return json.loads(result.stdout) if result.stdout.strip() else None


def plan_updates(items, issue_numbers, desired, expected=None):
    """Resolve exact repository URLs, rejecting missing/ambiguous/stale items."""
    planned = []
    for number in issue_numbers:
        url = f'https://github.com/{REPO}/issues/{number}'
        matches = [i for i in items if i.get('content', {}).get('url') == url]
        if len(matches) != 1:
            raise ValueError(f'Issue #{number}: expected one project item, got {len(matches)}')
        item = matches[0]
        current = item.get('status')
        if expected is not None and current not in (expected, desired):
            raise ValueError(f'Issue #{number}: expected {expected}, found {current}')
        planned.append({'issue': number, 'item_id': item['id'], 'before': current,
                        'after': desired, 'change': current != desired})
    return planned


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('issues', type=int, nargs='+')
    parser.add_argument('--status', required=True,
                        choices=['Backlog', 'Ready', 'In progress', 'In review', 'Done'])
    parser.add_argument('--expect', help='Refuse to overwrite an unexpected current status')
    parser.add_argument('--reason', required=True)
    parser.add_argument('--acceptance-record', type=Path,
                        help='Required for Done: reviewed repository handoff, not export success')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    mapping = json.loads((ROOT / 'inventory/engine/work-breakdown-issues.json').read_text())
    allowed = {1} | {v['number'] for v in mapping.values()}
    if not set(args.issues) <= allowed:
        parser.error('Only Engine #1 and mapped engine component issues are supported')
    if args.status == 'Done':
        record = args.acceptance_record
        if not record or not record.is_file() or not record.resolve().is_relative_to(ROOT):
            parser.error('Done requires an existing acceptance record inside this repository')
        # This is a traceability requirement, not an automated quality verdict.
    project = gh('project', 'view', PROJECT, '--owner', OWNER, '--format', 'json')
    fields = gh('project', 'field-list', PROJECT, '--owner', OWNER, '--format', 'json')['fields']
    status = next(f for f in fields if f['name'] == 'Status')
    option = next(o for o in status['options'] if o['name'] == args.status)
    def read_items():
        result = gh('project', 'item-list', PROJECT, '--owner', OWNER,
                    '--limit', '10000', '--format', 'json')
        if result.get('totalCount', len(result['items'])) > len(result['items']):
            raise RuntimeError('Project listing truncated; refusing incomplete reconciliation')
        return result['items']
    plan = plan_updates(read_items(), list(dict.fromkeys(args.issues)), args.status, args.expect)
    print(json.dumps({'apply': args.apply, 'reason': args.reason, 'updates': plan}, indent=2))
    if not args.apply:
        return
    for item in plan:
        if not item['change']:
            continue
        # Recheck immediately before this mutation, so an earlier read is not a blanket reset.
        plan_updates(read_items(), [item['issue']], args.status, item['before'])
        gh('project', 'item-edit', '--id', item['item_id'], '--project-id', project['id'],
           '--field-id', status['id'], '--single-select-option-id', option['id'])
    verified = plan_updates(read_items(), args.issues, args.status)
    if any(item['change'] for item in verified):
        raise RuntimeError('Post-write verification failed; inspect current board before retrying')
    print('Verified requested statuses. Issue bodies, checklists and open/closed states preserved.')


if __name__ == '__main__':
    main()
