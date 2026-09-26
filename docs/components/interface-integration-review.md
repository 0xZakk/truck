# Independent component interface integration review

Reviewer: pump-seal worker; integration owner: root. Scope: component_interface_integration.py, install-engine-component-interfaces.py, full_engine.py hook, shared exporter convention and learning/source wiring. Dimensions are illustrative; this review establishes software behavior, not actual truck dimensions.

## Findings

1. **Fixed by root:** stud learning was keyed by definition `throttle-bracket-stud-estimated`, while browser lookup uses occurrence IDs. It would never display on `throttle-stud-3` / `throttle-stud-4`. Root changed to occurrence keys.
2. **Fixed by root:** navigation check omitted new component-interface and existing water-pump-joint learning modules, leaving broken lesson links undetected. Root consolidated module loading in viewer/engine-learning-modules.js and updated changed part counts.
3. **Fixed by reviewer:** installed seal checker previously verified source/neighbor file hashes but not changed manifest transforms. It now requires a candidate report for the exact installed manifest hash. After installation run the candidate checker on the installed manifest, then installed checker. The candidate checker already excludes all six replacement seal IDs and uses installed carrier pose, so this is exact current-neighbor revalidation, not a hash bypass. Harness uses its own candidate report.

## Structural review

An in-memory callback harness invoked `install` twice without disk exports or manifest writes. Both results were identical; all eight emitted definitions are valid single solids; IDs remain unique; all new definition source IDs resolve. Predicted counts: 705 definitions / 1,310 occurrences. Eight emitted definitions replace one old seal definition, yielding net +7 definitions; six seal occurrences replace one envelope and one bracket occurrence is added, yielding net +6 occurrences. Existing stud occurrences reuse the new single stud definition.

Reviewed source hashes:

- component_interface_integration.py: 729fdbd64d699220017cd932f0618422d74371d6c65b9acc9a2e58d97777dbd8
- install-engine-component-interfaces.py: e8247befa6ed4e1654fd15e16d5362e6cb3dd2d6b744d972d99f4c429b2e7471
- full_engine.py: a5817004ef62a93e56bb76654aa28c418b8d8465f466dcaf763555925b310d19
- Frozen manifest during review: 821f7d3bb47d49a00ffb2975fa5faffcd306fe90bea48ce7c0d6308cd636653f

The adapter removes only its own definitions/occurrences and old seal, recreates the seal child group, preserves parent transforms, sets absolute stud/nut X positions rather than accumulating offsets, and delegates actual exports to existing define/add/group. New IDs do not match legacy geometry adapters. Source metadata preserves generic water-pump construction versus application uncertainty; bracket metadata distinguishes photo evidence from inferred 34 mm stud envelopes. Source hash resolves the local reviewed ledger. The full-builder hook runs after affected parent groups and before final manifest/export. Unrelated refreshes reinstall these same candidate definitions without duplicate IDs or cumulative transform drift.

## Remaining integration checks

The in-memory test deliberately did not execute exporter writes, change the authoritative manifest, or claim browser acceptance. Root must export the eight definitions, run refreshed candidate and installed checks, verify all component learning links, and visually inspect actual GLBs. Full-assembly STEP remains explicitly historical unless regenerated. Fresh harness audit PASS under the stricter gate: candidate report matches the harness manifest exactly, 30 static checks and 52 sampled explosion checks pass, and all six installed STEP shapes/poses pass. A mismatched pre-install report is rejected by the new manifest guard (negative-control log preserved).

Reproduce the adapter idempotence check without exports using `.venv-cad/bin/python` from repository root:

```python
import copy, json, sys
sys.path.insert(0, 'cad/engine')
import component_interface_integration as adapter
m = json.load(open('inventory/engine/full-assembly.json'))
def define(key, shape, name, function, system, color, sources, gaps):
    assert shape.is_valid and len(shape.solids()) == 1
    m['definitions'].append(dict(id=key, name=name, function=function, system=system,
                                color=color, sources=sources, unresolved=gaps))
def add(key, definition, parent, pos=(0,0,0), explode=(0,0,0)):
    m['occurrences'].append(dict(id=key, definition=definition, parent=parent,
                                position_cad_mm=list(pos), explode_cad_mm=list(explode)))
def group(key, name, parent):
    m['assemblies'].append(dict(id=key, name=name, parent=parent))
args = (define, add, group, m['definitions'], m['occurrences'], m['assemblies'])
adapter.install(*args)
first = copy.deepcopy(m)
adapter.install(*args)
assert m == first
for collection in ['definitions', 'occurrences', 'assemblies']:
    assert len({x['id'] for x in m[collection]}) == len(m[collection])
sources = m['sources'] | adapter.sources()
assert all(s in sources for d in m['definitions'] if d['id'] in adapter.NEW_IDS for s in d['sources'])
print('PASS structural idempotence and source resolution')
```
