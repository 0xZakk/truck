"""Install a reviewed educational linkage with its coordinated support changes.

All new dimensions and retention construction remain inferred. This is not a
factory reconstruction or completion of the cable/spring/stop mechanism.
"""
from pathlib import Path
import hashlib
import build123d as b
import throttle_linkage_candidate as candidate

ROOT = Path(__file__).resolve().parents[2]
NEW_IDS = {'throttle-lever-estimated', 'throttle-cable-ball-stud-estimated',
           'throttle-lever-retaining-pin-estimated'}
CHANGED_IDS = NEW_IDS | {'throttle-shaft', 'accelerator-cable-bracket'}
SOURCE_ID = 'throttle-1994-linkage-study'


def install(define, add, definitions, occurrences, shapes):
    previous = {d['id']: d for d in definitions}
    shaft = shapes.get('throttle-shaft')
    if shaft is None:
        shaft = b.import_step(ROOT/previous['throttle-shaft']['step'].lstrip('/'))
    pieces = candidate.parts(shaft)
    pieces['throttle-shaft'] = pieces.pop('throttle-shaft-keyed-estimated')
    pieces['accelerator-cable-bracket'] = candidate.bracket_proposal()
    definitions[:] = [d for d in definitions if d['id'] not in CHANGED_IDS]
    occurrences[:] = [o for o in occurrences if o['id'] not in NEW_IDS]
    descriptions = {
        'throttle-lever-estimated': ('Throttle lever · estimated',
            'Converts cable pull at the ball stud into shaft rotation through a modeled D-shaped hub.'),
        'throttle-cable-ball-stud-estimated': ('Throttle cable ball stud · estimated',
            'Provides the spherical attachment for a cable socket; cable and socket are not yet reconstructed.'),
        'throttle-lever-retaining-pin-estimated': ('Throttle lever retaining pin · estimated',
            'Captures the hub axially against a shaft shoulder. This fitted-pin study does not establish Ford retention or pin locking.'),
        'throttle-shaft': ('Throttle shaft · estimated keyed end',
            'Turns both butterfly plates and the external lever. Its proposed D end, shoulder and transverse pin bore provide a teaching torque path.'),
        'accelerator-cable-bracket': ('Accelerator cable bracket · estimated',
            'Supports the cable housing on the throttle mounting studs. Its revised web and opening clear the modeled outward-facing lever and direct cable path.'),
    }
    for ident, shape in pieces.items():
        old = previous.get(ident, {})
        name, function = descriptions[ident]
        gaps = list(dict.fromkeys(old.get('unresolved', []) + candidate.GAPS + [
            'Pin locking, load capacity, spring return, shield, actual cable/socket, plate hardware and production stops remain unresolved.']))
        define(ident, shape, name, function, 'induction',
               old.get('color', '#9c8a62' if 'lever-estimated' in ident else '#879297'),
               list(dict.fromkeys(old.get('sources', []) + [SOURCE_ID])), gaps)
        if ident in NEW_IDS:
            add(ident, ident, 'throttle-moving', explode=(160, 100, 60))
    for occurrence in occurrences:
        if occurrence['id'] in CHANGED_IDS:
            occurrence['name'], occurrence['function'] = descriptions[occurrence['id']]


def sources():
    path = ROOT/'reference/engine/throttle-linkage-review.json'
    return {SOURCE_ID: {
        'title': '1994 throttle factory topology and explicitly inferred linkage interfaces',
        'url': 'https://charm.li/Ford/1994/F%20150%202WD%20Pickup%20L6-300%204.9L/Repair%20and%20Diagnosis/Powertrain%20Management/Fuel%20Delivery%20and%20Air%20Induction/Throttle%20Body/Service%20and%20Repair/',
        'path': '/reference/engine/throttle-linkage-review.json',
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}}
