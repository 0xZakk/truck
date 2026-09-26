"""Offline controls for the issue-to-project update planner; no GitHub writes."""
from pathlib import Path
import importlib.util

path = Path(__file__).with_name('set-engine-project-status.py')
spec = importlib.util.spec_from_file_location('engine_status', path)
status = importlib.util.module_from_spec(spec)
spec.loader.exec_module(status)
item = {'id': 'engine-item', 'content': {'url': 'https://github.com/0xZakk/truck/issues/15'}, 'status': 'In review'}
assert status.plan_updates([item], [15], 'In progress', 'In review')[0]['change']
assert not status.plan_updates([item], [15], 'In review')[0]['change']
for items, expected in [([], None), ([item, item], None), ([item], 'Backlog'),
                        ([dict(item, content={'url': 'https://github.com/elsewhere/truck/issues/15'})], None)]:
    try:
        status.plan_updates(items, [15], 'In progress', expected)
    except ValueError:
        pass
    else:
        raise AssertionError('Unsafe update accepted')
print('PASS exact repository selection, idempotence, missing/duplicate items and stale-state controls')
