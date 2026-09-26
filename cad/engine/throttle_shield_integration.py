"""Stationary educational splash hood and pushpin; factory dimensions unknown."""
import throttle_shield_candidate as candidate
from throttle_linkage_integration import SOURCE_ID, sources

NEW_IDS = {'throttle-linkage-shield-estimated', 'throttle-shield-pushpin-estimated'}
CHANGED_IDS = NEW_IDS | {'accelerator-cable-bracket'}


def install(define, add, definitions, occurrences, shapes):
    previous = {d['id']: d for d in definitions}
    pieces = candidate.parts()
    pieces['accelerator-cable-bracket'] = pieces.pop('accelerator-bracket-shield-hole-estimated')
    definitions[:] = [d for d in definitions if d['id'] not in CHANGED_IDS]
    occurrences[:] = [o for o in occurrences if o['id'] not in NEW_IDS]
    descriptions = {
        'throttle-linkage-shield-estimated': ('Throttle linkage splash shield · estimated',
            'Covers the external linkage while leaving its travel path open. Factory illustrations identify the shield; its current contour and dimensions are estimates.'),
        'throttle-shield-pushpin-estimated': ('Throttle shield pushpin · estimated',
            'The modeled head and split barb capture the shield ear against the bracket. Actual Ford pin shape, material and flexure remain unverified.'),
    }
    for ident, shape in pieces.items():
        old = previous.get(ident, {})
        name, function = descriptions.get(ident, (old.get('name'), old.get('function')))
        define(ident, shape, name, function, 'induction', old.get('color', '#36424c'),
               list(dict.fromkeys(old.get('sources', [])+[SOURCE_ID])),
               list(dict.fromkeys(old.get('unresolved', [])+candidate.GAPS)))
        if ident in NEW_IDS:
            add(ident, ident, 'throttle-assembly', explode=(0, 170, 100))
